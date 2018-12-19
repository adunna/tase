from helper import TASEHelper
from sync import SyncEngine
import random

def runBenchmark():

    clip_sizes = list(range(5, 51, 5))
    match_percents = [x / 100 for x in range(50, 91, 5)]
    clip_movements = list(range(1, 11, 1))

    helper = TASEHelper()

    engine = SyncEngine("../model/output_graph.pbmm", "../model/alphabet.txt", "../model/lm.binary", "../model/trie")

    testText = "Text-Audio Synchronization Engine (TASE) Benchmark"
    padText = "-" * (len(testText))
    print("\n\n\n" + padText + "\n" + testText  +"\n" + padText + "\n\n\n")
    
    audioFile = "../benchmarks/samples/timemachinewells_01_ae_64kb.mp3"
    textFile = "../benchmarks/samples/35-0.txt"
    audioTimestamp = 312 * 1000 # in ms
    textTimestamp = 735 # word position

    text = helper.ReadText(textFile, preprocess=True)
    aud = helper.ReadAudio(audioFile, fmt="mp3")
    
    print("Benchmarking:\n\nAudio: {0}\nText: {1}\n\n".format(audioFile, textFile))
    
    if (False): # Audio to Text Benchmark
        print("Audio to Text Benchmark (negative distance means prediction before actual):\n\n")
        print("clip_size,match_percent,clip_movement,audio_timestamp,returned_word_position,actual_word_position,distance,confidence,sync_time,text_sample")
        for clipSize in clip_sizes:
            for matchPercent in match_percents:
                for clipMovement in clip_movements:
                    engine.changeParameters(clip_size = clipSize, match_percent = matchPercent, clip_movement = clipMovement)
                    audioResults = engine.AudioWithText(audioFile, textFile, audioTimestamp, fmt="mp3")
                    textSample = " ".join(text[audioResults[0] : audioResults[0] + clipSize])
                    print('{0},{1},{2},{3},{4},{5},{6},{7},{8},"{9}"'.format(clipSize, matchPercent, clipMovement, audioTimestamp, audioResults[0], textTimestamp, audioResults[0] - textTimestamp, audioResults[1], audioResults[2], textSample))

    if (False): # Text to Audio Benchmark
        print("\n\nText to Audio Benchmark (negative distance means prediction before actual):\n\n")
        print("clip_size,match_percent,clip_movement,word_position,returned_audio_timestamp,actual_audio_timestamp,distance,confidence,sync_time,text_sample")
        for clipSize in clip_sizes:
            for matchPercent in match_percents:
                for clipMovement in clip_movements:
                    engine.changeParameters(clip_size = clipSize, match_percent = matchPercent, clip_movement = clipMovement)
                    textResults = engine.TextWithAudio(audioFile, textFile, textTimestamp, fmt="mp3")
                    textSample = " ".join(text[textTimestamp : textTimestamp + clipSize])
                    print('{0},{1},{2},{3},{4},{5},{6},{7},{8},"{9}"'.format(clipSize, matchPercent, clipMovement, textTimestamp, textResults[0], audioTimestamp, textResults[0] - audioTimestamp, textResults[1], textResults[2], textSample))
    
    if (False): # Audio to Text Benchmark, Optimal
        print("Audio to Text Benchmark (negative distance means prediction before actual):")
        print("Using Optimal Values of: clip_size = 25, match_percent = 0.8, clip_movement = 3\n")
        print("audio_timestamp,returned_word_position,confidence,sync_time")
        ATrand = random.sample(range(5000, int(aud.duration_seconds * 1000)-10000), 1000)
        engine.changeParameters(clip_size = 25, match_percent = 0.8, clip_movement = 3)
        for ts in ATrand:
            audioResults = engine.AudioWithText(audioFile, textFile, ts, fmt="mp3")
            print('{0},{1},{2},{3}'.format(ts, audioResults[0], audioResults[1], audioResults[2]))

    if (True): # Text to Audio Benchmark, Optimal
        print("Text to Audio Benchmark (negative distance means prediction before actual):")
        print("Using Optimal Values of: clip_size = 40, match_percent = 0.8, clip_movement = 3\n")
        print("word_position,returned_audio_timestamp,confidence,sync_time")
        ATrand = random.sample(range(100, len(text)-100), 1000)
        engine.changeParameters(clip_size = 40, match_percent = 0.8, clip_movement = 3)
        for ts in ATrand:
            textResults = engine.TextWithAudio(audioFile, textFile, ts, fmt="mp3")
            print('{0},{1},{2},{3}'.format(ts, textResults[0], textResults[1], textResults[2]))

runBenchmark()
