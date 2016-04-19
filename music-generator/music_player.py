import pyaudio
import wave


def play(filename):
    if (type(filename) is int):
        filename = "output-"+str(filename)+".wav"
    wave_sound = wave.open(filename)
    audio = pyaudio.PyAudio()

    chunk = 1024
    stream = audio.open(format=audio.get_format_from_width(wave_sound.getsampwidth()),
                    channels=wave_sound.getnchannels(),
                    rate=wave_sound.getframerate(),
                    output=True)

    data = wave_sound.readframes(chunk)

    while data != '':
        stream.write(data)
        data = wave_sound.readframes(chunk)

if __name__ == "__main__":
    filename = "output.wav"
    play(filename)