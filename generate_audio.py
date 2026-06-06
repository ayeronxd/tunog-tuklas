from gtts import gTTS

# Tricking the TTS engine with phonetic spelling to force a humming sound
text_to_read = "elepante... eroplano... eskwela"

# Generate the audio
tts = gTTS(text=text_to_read, lang='tl')
tts.save("e_pronounce.mp3")
print("Audio generated! Go listen to generated audio")