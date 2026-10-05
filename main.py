import sounddevice as sd
from googletrans import Translator
import scipy.io.wavfile as wav
import speech_recognition as sr
import time
import random
while True:

    words_by_level = {
        "facil": ["gato", "cachorro", "maçã", "leite", "sol"],
        "medio": ["casa", "escola", "amigo", "janela", "amarelo"],
        "dificil": ["tecnologia", "universidade", "informação", "pronúncia", "imaginação"]
    }

    pontuacao = 0
    erros = 0

    print("===================================")
    print("       🎤 JOGO DE PRONÚNCIA 🎤")
    print("===================================")
    print("Fale corretamente a palavra em inglês!")
    print("Você pode cometer até 3 erros.")
    print()

    nivel = input("Escolha um nível: facil, medio ou dificil: ").lower()

    while nivel not in words_by_level:
        print("❌ Nível inválido!")
        nivel = input("Escolha: facil, medio ou dificil: ").lower()

    print()
    print("Nível escolhido:", nivel)
    print("Prepare-se!")
    time.sleep(2)

    for i in range(10):

        if erros >= 3:
            break

        palavra = random.choice(words_by_level[nivel])
        
        print()
        print("-----------------------------------")
        print("🎯 Palavra em português:", palavra)
        print("🎤 Fale a palavra em inglês!")
        print("-----------------------------------")
        iniciar = input("caso queira mudar a dificuldade digite (1),para continuar aperte enter")
        if iniciar == "1":
                nivel = input("Escolha um nível: facil, medio ou dificil: ").lower()
                palavra = random.choice(words_by_level[nivel])
        time.sleep(2)

        duration = 5
        sample_rate = 44100

        print("🔴 Gravando...")
        
        recording = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="int16"
        )

        sd.wait()

        wav.write("output.wav", sample_rate, recording)

        print("✅ Gravação concluída!")
        print("🔎 Reconhecendo fala...")

        recognizer = sr.Recognizer()

        with sr.AudioFile("output.wav") as source:

            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(
                    audio_data,
                    language="en-US"
                )

                recognized = text.lower()

                print("🗣️ Você disse:", recognized)

            except sr.UnknownValueError:
                print("❌ Não foi possível reconhecer a fala.")
                erros += 1
                print("❌ Erros:", erros)
                continue

            except sr.RequestError as e:
                print("❌ Erro no serviço de reconhecimento:", e)
                continue

        print("🌍 Traduzindo...")

        try:
            translator = Translator()
            translated = translator.translate(
                recognized,
                dest="pt"
            )

            print("🌍 Tradução:", translated.text)

        except Exception as e:
            print("❌ Erro na tradução:", e)
            continue

        # Verifica se a tradução corresponde à palavra escolhida
        if translated.text.lower() == palavra.lower():

            print("🎉 CORRETO!")
            pontuacao += 1

        else:

            print("❌ ERRADO!")
            print("A palavra esperada era:", palavra)
            erros += 1

        print()
        print("⭐ Pontuação:", pontuacao)
        print("❌ Erros:", erros)

        time.sleep(2)


    print()
    print("===================================")
    print("           🏁 FIM DE JOGO")
    print("===================================")
    print("⭐ Pontuação final:", pontuacao)
    print("❌ Erros:", erros)

    if erros >= 3:
        print("💀 Você cometeu 3 erros!")

    else:
        print("🎉 Parabéns! Você terminou o jogo!")

    print("Obrigado por jogar! 👋")
