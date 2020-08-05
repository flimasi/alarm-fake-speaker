#!/usr/bin/env python3
# Import playsound module
from playsound import playsound
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import struct

def main():
    chunk = 1024
    formato = pyaudio.paInt16
    canais = 1
    taxaDeAmostragem = 44100
    tempoDeGravacao = 2
    nomeArquivoSaida = "outputMic.wav"

    deltaX = 1.0 / taxaDeAmostragem

    objetoPyAudio = pyaudio.PyAudio()

    print("Recording ", tempoDeGravacao, "  seconds...")

    streamMic = objetoPyAudio.open(format=formato, channels=canais, rate=taxaDeAmostragem, input=True,
                                   frames_per_buffer=chunk)

    framesWav = []

    # captura dados do microfone
    for nLoop in range(0, int(taxaDeAmostragem / chunk * tempoDeGravacao)):
        dadosLidosMic = streamMic.read(chunk)
        framesWav.append(dadosLidosMic)
    # framesWav é uma lista com 215 "chunks" de 1024 amostras

    streamMic.stop_stream()
    streamMic.close()
    objetoPyAudio.terminate()

    # criamos uma única lista com todos os bytes encadeados
    framesWavJuntos = b''.join(framesWav)

    # salvamos o arquivo wave
    arquivoWav = wave.open(nomeArquivoSaida, 'wb')
    arquivoWav.setnchannels(canais)
    arquivoWav.setsampwidth(objetoPyAudio.get_sample_size(formato))
    arquivoWav.setframerate(taxaDeAmostragem)
    arquivoWav.writeframes(framesWavJuntos)
    arquivoWav.close()

    sinalAudio = np.frombuffer(framesWavJuntos, np.int16)
    # print(sinalAudio)
    signal = "0"
    changeNoise = False
    for i in sinalAudio:
        print(i)
        if signal != "0":
            if (i) < 500:
                changeNoise = True
                print('Detect Change Noise')
            if changeNoise:
                playsound("sounds/optimusprime.mp3")
                break
        signal = i
    tempo = np.linspace(0, len(sinalAudio) / taxaDeAmostragem, num=len(sinalAudio))
    print(tempo)
    plt.figure(1)
    plt.title('Audio recorded')
    plt.plot(tempo, sinalAudio)
    plt.show()

    print("End recording")

    return 0

main()
