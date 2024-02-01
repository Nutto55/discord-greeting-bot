import os
import discord
import asyncio
from discord.ext import commands
from speaker import Speaker
from datetime import datetime

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(intents=intents, command_prefix="!")

@bot.event
async def on_ready():
    try:
        print(f"{bot.user.name} has connected to Discord!")
        await bot.tree.sync()
        print("synced command")
    except Exception as e:
        print(e)

@bot.event
async def on_voice_state_update(
    member: discord.Member,
    before: discord.VoiceState,
    after: discord.VoiceState
):
    if member.bot:
        return

    if before.channel == after.channel:
        return

    def is_connected(member: discord.Member):
        client = discord.utils.get(bot.voice_clients, guild=member.guild)
        return client and client.is_connected()

    if is_connected(member):
        if after.channel is not None:
            if not any(
                after.channel.id == voice_client.channel.id for voice_client in bot.voice_clients
            ):
                return

            current_channel_id = int(after.channel.id)
            current_channel = bot.get_channel(current_channel_id)
            name = member.nick if member.nick else member.name
            print(f"{name} is entering")
            greeting_item = Speaker(name)
            greeting_obj = greeting_item.greeting_by_person()
            voice_client = member.guild.voice_client if member.guild.voice_client else await current_channel.connect()
            audio_source = discord.FFmpegPCMAudio(source=greeting_obj, pipe=True)
            await asyncio.sleep(2)
            voice_client.play(audio_source)
            await asyncio.sleep(1)

@bot.event
async def on_command():
    print("on command")

@bot.tree.command(name="greeting", description="I will help you greeting people")
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
            await interaction.response.send_message("I'm coming to you")
            return

        await user_voice.channel.connect()

        speaker = Speaker()
        greeting_obj = speaker.greeting_all()
        audio_source = discord.FFmpegPCMAudio(source=greeting_obj, pipe=True)
        interaction.guild.voice_client.play(audio_source)
        await interaction.response.send_message("I'm joining")
    except Exception as e:
        print(e)
        await interaction.response.send_message("Joining failed")

@bot.tree.command(name="goodbye", description="I'm going out from voice channel")
async def goodbye(interaction: discord.Interaction):
    try:
        user_voice = interaction.user.voice
        if not user_voice:
            await interaction.response.send_message("Sorry, you should be in voice channel.")
            return

        bot_voice = interaction.guild.voice_client
        if bot_voice is not None:
            if bot_voice.channel.id == user_voice.channel.id:
                speaker = Speaker()
                goodbye_obj = speaker.generate_mp3_file_object("ไว้พบกันใหม่นะคะ บะบาย")
                audio_source = discord.FFmpegPCMAudio(source=goodbye_obj, pipe=True)
                interaction.guild.voice_client.play(audio_source)
                await interaction.response.defer()
                await asyncio.sleep(2)
                await interaction.followup.send("See you later!")
                await bot_voice.disconnect()
                return

        await interaction.response.send_message("I'm not in any voice channel")

    except Exception as e:
        print(e)
        await interaction.response.send_message("Joining failed")

@bot.tree.command(name="daily",description="Alert people to daily channel")
async def daily(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("Let's daily")
        channels = interaction.guild.channels
        now = datetime.now()
        message = f"Happy {now.strftime("%A")} มาเดลี่กันเถอะค่ะ"
        speaker = Speaker()
        daily_message = speaker.generate_mp3_file_object(message)
        for channel in channels:
            print(channel.id, channel.type, channel.name)
            joinable = channel.permissions_for(channel.guild.me).connect
            if channel.type.name == "voice" and joinable:
                await channel.connect()
                audio_source = discord.FFmpegPCMAudio(source=daily_message, pipe=True)
                await asyncio.sleep(5)
                channel.guild.voice_client.play(audio_source)
                await asyncio.sleep(5)
                bot_voice = channel.guild.voice_client
                if bot_voice is not None:
                    await bot_voice.disconnect()
                    await asyncio.sleep(2)
    except Exception as e:
        print(e)
        await interaction.response.send_message("Daily Failed")

bot.run(TOKEN)
