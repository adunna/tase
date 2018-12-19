from pydub import AudioSegment
import numpy as np
from deepspeech import Model, printVersions
from helper import TASEHelper

BEAM_WIDTH = 500
LM_WEIGHT = 1.50
VALID_WORD_COUNT_WEIGHT = 2.25
N_FEATURES = 26
N_CONTEXT = 9

class STTConverter:

    def __init__(self, model, alphabet, lm, trie):
        
        # setup variables
        self.model_path = model
        self.alphabet_path = alphabet
        self.lm_path = lm
        self.trie_path = trie

        # setup model
        self.model = Model(model, N_FEATURES, N_CONTEXT, alphabet, BEAM_WIDTH)
        self.model.enableDecoderWithLM(alphabet, lm, trie, LM_WEIGHT, VALID_WORD_COUNT_WEIGHT)

        # setup helper
        self.helper = TASEHelper()

    '''
    Description: Convert given audio file into text.
    Input:
        audio: string or AudioSegment: Either input file path or input audio segment.
        fmt: string: If input file, then fmt is audio format. (ex: "mp3", "wav")
    Output:
        string: Converted string.
    '''
    def Convert(self, audio, fmt="wav"):
        
        # process input audio
        if isinstance(audio, str):
            audio = self.helper.ReadAudio(audio, fmt)
        audio = np.frombuffer(self.helper.Convert16WAV(audio).raw_data, np.int16)

        # run conversion
        prediction = self.model.stt(audio, 16000)

        return prediction

    '''
    Description: Convert given audio file slice into text.
    Input:
        audio: string or AudioSegment: Either input file path or input audio segment.
        start: int: Start timestamp (in ms).
        stop: int: Stop timestamp (in ms).
        fmt: string: If input file, then fmt is audio format. (ex: "mp3", "wav")
    Output:
        string: Converted string.
    '''
    def ConvertSlice(self, audio, start, end, fmt="wav"):

        # process input audio
        if isinstance(audio, str):
            audio = self.helper.ReadAudio(audio, fmt)
        audio = self.helper.SliceAudio(audio, start, end)
        audio = self.helper.Convert16WAV(audio)
        audio = np.frombuffer(audio.raw_data, np.int16)

        # run conversion
        prediction = self.model.stt(audio, 16000)

        return prediction
