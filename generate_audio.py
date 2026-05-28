from gtts import gTTS

# Tricking the TTS engine with phonetic spelling to force a humming sound
text_to_read = "manok... mangga... mata"

# Generate the audio
tts = gTTS(text=text_to_read, lang='tl')
tts.save("m_pronunce.mp3")
print("Audio generated! Go listen to m_intro.mp3")