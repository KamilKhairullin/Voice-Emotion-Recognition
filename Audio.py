from abc import ABC
from enum import Enum
from typing import Union, Generator


class SoundClassifier(Enum):
    UNCLASSIFIED = 1
    SPEECH = 2
    NOISE = 3
    OTHER = 4


class Audio:
    class Sample:

        def __init__(self, starts: int, ends: int, classified_as: Union[SoundClassifier, None]):
            self.starts = starts
            self.ends = ends
            self.type = classified_as if classified_as is not None else SoundClassifier.UNCLASSIFIED

    def __init__(self, path: str, duration: int, sample_rate: int = 44100):
        self.file_path = path
        self.duration = duration
        self.samples = []
        self.sample_rate = sample_rate


class AudioClassifier(ABC):

    @staticmethod
    def process_audio(audio: Audio) -> Audio:
        raise NotImplemented


class AudioController(ABC):

    @staticmethod
    def next_audio() -> Generator[Audio, None, None]:
        raise NotImplemented

    @staticmethod
    def process(audio: Audio, impl: AudioClassifier) -> Audio:
        raise NotImplemented

    @staticmethod
    def create_audio(*args, **kwargs):
        raise NotImplemented
