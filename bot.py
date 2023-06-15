import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()

bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event
async def on_ready():
    try:
        print(f'{bot.user.name} has connected to Discord!')
        await bot.tree.sync()
        print('synced command')
    except Exception as e:
        print(e)

@bot.event
async def on_command():
    print("on command")

@bot.tree.command(name='greeting', description='I will help you greeting people')
async def greeting(interaction: discord.Interaction):
    try:
        user_voice = interaction.user.voice

        if not user_voice:
            await interaction.response.send_message("Sorry, you should be in voice channel.")
            return

        bot_voice = interaction.guild.voice_client

        if bot_voice is not None:
            if bot_voice.channel.id == user_voice.channel.id:
                await interaction.response.send_message("I'm in your voice channel!")
                return

            await bot_voice.move_to(user_voice.channel)
            await interaction.response.send_message("Hello!", tts=True)
            return

        await user_voice.channel.connect()
        await interaction.response.send_message("Hello!", tts=True)
    except Exception as e:
        print(e)
        await interaction.response.send_message('Joining failed')

bot.run(TOKEN)
