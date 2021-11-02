import requests
import base64
import hashlib
import pathlib
from datetime import datetime
import os


class XTTS:
    def __init__(self, token, text, language, path='./'):
        self.token = token
        self.text = text
        self.language = language
        self.errors = None
        self.success = False
        self.audio_bytes = None
        self.id_hash = self.__generate_id_hash()
        self.path = path

        self.cached_exists = self.__does_cached_exist()

    def __generate_id_hash(self):
        body = self.text + self.language
        hashed = hashlib.sha1()
        hashed.update(body.encode())
        return hashed.hexdigest()

    def __does_cached_exist(self):
        path = pathlib.Path(self.path + '/' + self.id_hash + '.ogg')
        if path.is_file():
            created = datetime.fromtimestamp(os.path.getctime(path))
            now = datetime.now()
            diff = int((now - created).total_seconds())
            # if difference is greater than 2 weeks
            if diff >= 1210000:
                return False

            return True
        return False

    def work(self):
        if self.cached_exists:
            return True

        input_ = {
            "text": self.text
        }
        voice = {
            "languageCode": self.language,
            "name": "John",
            "ssmlGender": "FEMALE"
        }
        audio_config = {
            "audioEncoding": "OGG_OPUS",
            "speakingRate": 0.85
        }
        payload = {
            'input': input_,
            'voice': voice,
            'audioConfig': audio_config,
        }
        url = 'https://texttospeech.googleapis.com/v1/text:synthesize'
        url = f'{url}?key={self.token}'
        res = requests.post(
            url=url,
            json=payload
        )
        if res.status_code == 200:
            self.success = True
            self.audio_bytes = res.json().get('audioContent')
            return True
        else:
            self.errors = res.json()
            self.success = False
            return False

    def save_audio(self):
        if self.cached_exists:
            print('cache exists')
            return self.path + '/' + self.id_hash + '.ogg'

        if not self.audio_bytes:
            raise Exception('Please call work() before saving to audio file')
        if not self.success:
            raise Exception('Request either failed or work() was not called')
        if self.errors:
            raise Exception('Request returned errors. Please rectify.')
        path = self.path + '/' + self.id_hash + '.ogg'
        with open(path, 'wb') as f:
            audio_bytes = base64.b64decode(self.audio_bytes)
            f.write(audio_bytes)
        return path
