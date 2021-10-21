from . import XTTS

text = 'Namaskaram'
api_token = 'your-token-here'
language_code = 'ml-IN'
tts = XTTS(api_token, text, language_code)
tts.work()
file = tts.save_audio('./')
print(file)
