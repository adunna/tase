from helper import TASEHelper
from converters import STTConverter
from pydub import AudioSegment
import numpy as np
import time

class SyncEngine:

    '''
    Description: Engine initialization.
    Input:
        model: string: Model file path.
        alphabet: string: Alphabet file path.
        lm: string: LM file path.
        trie: string: Trie file path.
        clip_size: int: Average size of word clips to search with. Default is 40.
        match_percent: float: Percentage of characters to match (spaces are ignored). Range is 0 to 1. Default is 0.85.
        clip_movement: int: How many words over to move clip, on average, before matching next clip. Default is int(clip_size / 4).
    '''
    def __init__(self, model, alphabet, lm, trie, clip_size=40, match_percent=0.85, clip_movement=-1):

        # setup converter
        self.converter = STTConverter(model, alphabet, lm, trie)

        # setup variables
        self.clip_size = clip_size
        self.match_percent = match_percent
        self.timeout = 600
        self.clip_movement = clip_movement
        if clip_movement <= 0:
            self.clip_movement = int(clip_size / 4)

        # setup helper
        self.helper = TASEHelper()

    '''
    Description: Change parameters for engine; you can choose any of parameters clip_size, match_percent, or clip_movement. You can specify one, two, or all three. ex: changeParameters(match_percent = 0.8), or changeParameters(clip_size = 10, clip_movement = 1)
    Input:
        clip_size: int: Average size of word clips to search with.
        match_percent: float: Percentage of characters to match (spaces are ignored).
        clip_movement: int: How many words over to move clip, on average, before matching next clip.
    '''
    def changeParameters(self, clip_size=None, match_percent=None, clip_movement=None):
        if clip_size is not None:
            self.clip_size = clip_size
        if match_percent is not None:
            self.match_percent = match_percent
        if clip_movement is not None:
            self.clip_movement = clip_movement

    '''
    Description: Convert position in audio to position in text.
    Input:
        audio: string or AudioSegment: Either input file path or input audio segment.
        text: string: Either input text file path or input text; specify with 'text_type', default is file path.
        position: int: Audio position timestamp (in ms).
        wpm: int: Average WPM of audio speaker. Default is 150.
        direction: string: "forward" or "backward" or "both", which defines the direction to search in. Default is "both".
        text_type: string: "file" or "text", which defines the type of text input for 2nd argument. Default is "file".
        fmt: string: If input audio is file path, then fmt is audio format. (ex: "mp3", "wav")
    Output:
        (int, float, float): Start of corresponding audio timestamp, confidence percentage, and synchronization time. Returns (-1, 1, time) if no position was found. The position SHOULD BE padded by the clip movement length in implementation (so will be a few words prior to the position expected, to account for confidences sub 100%.)
    '''
    def AudioWithText(self, audio, text, position, wpm=150, direction="both", text_type="file", fmt="wav"):
        
        startTime = time.time()
        timeout = startTime + self.timeout

        # read files
        if text_type == "file":
            text = self.helper.ReadText(text, preprocess=True)
        else:
            text = self.helper.PrepareText(text)
        if isinstance(audio, str):
            audio = self.helper.ReadAudio(audio, fmt)
        
        # calculate expected position
        current_position_forward = [int((position / 1000 / 60) * wpm), position]
        current_position_backward = [current_position_forward[0], position]

        # loop search
        confidence = 0
        max_length = [len(text), audio.duration_seconds * 1000]
        audio_movement = int((self.clip_movement / wpm) * 60 * 1000)
        audio_clip_size = int((self.clip_size / wpm) * 60 * 1000)

        clip = self.converter.ConvertSlice(audio, current_position_forward[1], current_position_forward[1] + audio_clip_size)
        clip = clip.split()
        text_clip_forward, text_clip_backward, confidence_forward, confidence_backward = (None, None, None, None)

        while True:

            #if (direction == "forward" or direction == "both") and current_position_forward[0] + self.clip_size < max_length[0] and current_position_forward[1] + audio_clip_size < max_length[1]:
            if (direction == "forward" or direction == "both") and current_position_forward[0] + self.clip_size < max_length[0]:

                #clip = self.converter.ConvertSlice(audio, current_position_forward[1], current_position_forward[1] + audio_clip_size) # For TextToAudio
                #clip = clip.split() # For TextToAudio
                text_clip_forward = text[current_position_forward[0] : current_position_forward[0] + len(clip)]
                match = [word for word in clip if word in text_clip_forward] # Reverse for TextToAudio
                confidence_forward = (len(match) / len(clip))
                if confidence_forward >= self.match_percent:
                    return (current_position_forward[0], confidence_forward, (time.time() - startTime))

                current_position_forward[0] += self.clip_movement # For AudioToText
                #current_position_forward[1] += audio_movement # For TextToAudio

            #if (direction == "backward" or direction == "both") and current_position_backward[0] - self.clip_size > 0 and current_position_backward[1] - audio_clip_size > 0:
            if (direction == "backward" or direction == "both") and current_position_backward[0] - self.clip_size > 0:

                #clip = self.converter.ConvertSlice(audio, current_position_backward[1] - audio_clip_size, current_position_backward[1]) # For TextToAudio
                #clip = clip.split() # For TextToAudio
                text_clip_backward = text[current_position_backward[0] - len(clip) : current_position_backward[0]]
                match = [word for word in clip if word in text_clip_backward] # Reverse for TextToAudio
                confidence_backward = (len(match) / len(clip))
                if confidence_backward >= self.match_percent:
                    return (current_position_backward[0] - len(clip), confidence_backward, (time.time() - startTime))
                current_position_backward[0] -= self.clip_movement # For AudioToText
                #current_position_backward[1] -= audio_movement # For TextToAudio

            if time.time() - startTime > 10:
                print(current_position_forward)
                print(current_position_backward)

            # timeout or out of bounds of audio/text clips
            if time.time() >= timeout or (current_position_backward[1] - audio_clip_size <= 0 and current_position_forward[1] + audio_clip_size >= max_length[1]) or (current_position_backward[0] - self.clip_size <= 0 and current_position_forward[0] + self.clip_size >= max_length[0]):
                break

        return (-1, 1, time.time() - startTime)

    '''
    Description: Convert position in text to position in audio.
    Input:
        audio: string or AudioSegment: Either input file path or input audio segment.
        text: string: Either input text file path or input text; specify with 'text_type', default is file path.
        position: int: Text word position (ex: 227 = 227th word).
        wpm: int: Average WPM of audio speaker. Default is 150.
        direction: string: "forward" or "backward" or "both", which defines the direction to search in. Default is "both".
        text_type: string: "file" or "text", which defines the type of text input for 2nd argument. Default is "file".
        fmt: string: If input audio is file path, then fmt is audio format. (ex: "mp3", "wav")
    Output:
        (int, float, float): Start of corresponding audio timestamp, confidence percentage, and synchronization time. Returns (-1, 1, time) if no position was found. The position SHOULD BE padded by the clip movement length in implementation (so will be a few words prior to the position expected, to account for confidences sub 100%.)
    '''
    def TextWithAudio(self, audio, text, position, wpm=150, direction="both", text_type="file", fmt="wav"):

        startTime = time.time()
        timeout = startTime + self.timeout

        # read files
        if text_type == "file":
            text = self.helper.ReadText(text, preprocess=True)
        else:
            text = self.helper.PrepareText(text)
        if isinstance(audio, str):
            audio = self.helper.ReadAudio(audio, fmt)

        # calculate expected position
        current_position_forward = [position, int((position / wpm) * 1000 * 60)]
        current_position_backward = [position, current_position_forward[0]]

        # loop search
        confidence = 0
        max_length = [len(text), audio.duration_seconds * 1000]
        audio_movement = int((self.clip_movement / wpm) * 60 * 1000)
        audio_clip_size = int((self.clip_size / wpm) * 60 * 1000)

        clip = text[position : position + self.clip_size]
        audio_clip_forward, audio_clip_backward, confidence_forward, confidence_backward = (None, None, None, None)

        while True:

            if (direction == "forward" or direction == "both") and current_position_forward[1] + audio_clip_size < max_length[1]:

                audio_clip_forward = self.converter.ConvertSlice(audio, current_position_forward[1], current_position_forward[1] + audio_clip_size)
                audio_clip_forward = audio_clip_forward.split()
                match = [word for word in clip if word in audio_clip_forward]
                confidence_forward = (len(match) / len(clip))
                if confidence_forward >= self.match_percent:
                    return (current_position_forward[1], confidence_forward, (time.time() - startTime))

                current_position_forward[1] += audio_movement

            if (direction == "backward" or direction == "both") and current_position_backward[1] - audio_clip_size > 0:

                audio_clip_backward = self.converter.ConvertSlice(audio, current_position_backward[1] - audio_clip_size, current_position_backward[1])
                audio_clip_backward = audio_clip_backward.split()
                match = [word for word in clip if word in audio_clip_backward]
                confidence_backward = (len(match) / len(clip))
                if confidence_backward >= self.match_percent:
                    return (current_position_backward[1] - audio_clip_size, confidence_backward, (time.time() - startTime))
                current_position_backward[1] -= audio_movement

            # timeout or out of bounds of audio/text clips
            if time.time() >= timeout or (current_position_backward[1] - audio_clip_size <= 0 and current_position_forward[1] + audio_clip_size >= max_length[1]) or (current_position_backward[0] - self.clip_size <= 0 and current_position_forward[0] + self.clip_size >= max_length[0]):
                break

        return (-1, 1, time.time() - startTime)

