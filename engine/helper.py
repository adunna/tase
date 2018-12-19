from pydub import AudioSegment
import re

class TASEHelper:

    '''
    Description: Read audio from path into AudioSegment.
    Input:
        audio_path: string: Input audio path.
        fmt: string: Audio format. (ex: "mp3", "wav")
    Output:
        AudioSegment: Read audio segment.
    '''
    def ReadAudio(self, audio_path, fmt):
        audio = AudioSegment.from_file(audio_path, fmt)
        return audio

    '''
    Description: Read text from path into string.
    Input:
        text_path: string: Input text path.
        preprocess: boolean: Whether to preprocess using Prepare function or not, default=False.
    Output:
        string or list(string): Read text, string if preprocess=False, list if preprocess=True.
    '''
    def ReadText(self, text_path, preprocess=False):
        text = None
        with open(text_path, "r") as f:
            text = f.read()
        if preprocess:
            text = self.PrepareText(text)
        return text

    '''
    Description: Convert audio into 16000 Hz WAV.
    Input:
        audio: AudioSegment: Input audio segment.
    Output:
        AudioSegment: Converted audio segment.
    '''
    def Convert16WAV(self, audio):
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        return audio

    '''
    Description: Slice audio segment at specific timestamps.
    Input:
        audio: AudioSegment: Input audio segment.
        start: int: Start timestamp (in ms).
        end: int: Stop timestamp (in ms).
    Output:
        AudioSegment: Sliced audio segment.
    '''
    def SliceAudio(self, audio, start, end):
        audio = audio[start : end]
        return audio

    '''
    Description: Trim all whitespace from input text.
    Input:
        text: string: Input string.
    Output:
        string: Trimmed string.
    '''
    def RemoveWhitespace(self, text):
        return re.sub('[\s+]', '', text)

    '''
    Description: Prepare text for synchronization process.
    Input:
        text: string: Input text.
    Output:
        string: Output text.
    '''
    def PrepareText(self, text):
        return re.sub("[^a-z']", " ", text.lower()).split()
