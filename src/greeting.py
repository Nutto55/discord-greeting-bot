from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
import random

class Greeting:
    """
        A class for sending greeting message
    """

    def __init__(self, name: str = ""):
        self.name = name

    def speak(self, text: str):
        """Play speech
        Args:
            text: word or sentence to speak
        Returns:
            None.
        """
        mp3_file_object = self.generate_mp3_file_object(text)
        sound = AudioSegment.from_mp3(mp3_file_object)
        play(sound)

    def greeting_all(self):
        """Greeting all people in mp3 file object
        Args:
            None.
        Returns:
            BytesIO
        """
        return self.generate_mp3_file_object("สวัสดีทุกคนค่ะ")

    def greeting_by_person(self):
        """Random greeting by person in mp3 file object
        Args:
            text: word or sentence
        Returns:
            BytesIO
        """
        greeting_list = [
            'สวัสดี',
            'ว่าไง',
            'ขอบคุณที่แวะมานะ',
            'หนีห่าว',
            'มาทวงงานใครคะ',
            'บองชู้ว'
        ]
        return self.generate_mp3_file_object(f'{random.choice(greeting_list)} {self.name}')

    def generate_mp3_file_object(self, text: str, lang: str = "th"):
        """Convert text to mp3 file object
        Args:
            text: word or sentence
            lang(optional): language
        Returns:
            BytesIO
        """
        tts = gTTS(text=text, lang=lang)
        mp3_file_object = BytesIO()
        tts.write_to_fp(mp3_file_object)
        mp3_file_object.seek(0)
        return mp3_file_object
