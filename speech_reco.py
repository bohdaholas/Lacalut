from __future__ import division

import re
import sys

from google.cloud import speech, texttospeech
from playsound import playsound

import pyaudio
from six.moves import queue

RATE = 16000
CHUNK = int(RATE / 10)

TEST_STR = 'Думи мої думи мої Лихо мені з вами Нащо стали на папері Сумними рядами Чом вас вітер не розвіяв В степу як пилину Чом вас лихо не приспало Як свою дитину За карії оченята За чорнії брови Серце рвалося сміялось Виливало мову Виливало як уміло За темнії ночі За вишневий сад зелений За ласки дівочі За степи та за могили Що на Україні'.lower()


TEST_LIST = [
    'Думи мої, думи мої,',
    'Лихо мені з вами!',
    'Нащо стали на папері',
    'Сумними рядами?..',
    'Чом вас вітер не розвіяв',
    'В степу, як пилину?',
    'Чом вас лихо не приспало,',
    'Як свою дитину?…',
    'За карії оченята,',
    'За чорнії брови',
    'Серце рвалося, сміялось,',
    'Виливало мову,',
    'Виливало, як уміло,',
    'За темнії ночі,',
    'За вишневий сад зелений,',
    'За ласки дівочі…',
    'За степи та за могили,',
    'Що на Україні']


def purify_str(strr: str) -> str:
    '''
    This function removes all comas, exclemation points and other punctuation stuff
    '''
    return re.sub('[,!?.…–-]', '', strr)



word_ind = 0

line_ind = 0


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b"".join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them."""
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        overwrite_chars = " " * (num_chars_printed - len(transcript))

        global word_ind
        global line_ind

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

            if len(transcript.split(' ')) == len(TEST_LIST[line_ind].split(' ')):
                pass

        else:
            print(transcript + overwrite_chars)
            is_right = True
            for word in transcript.strip().lower().split(' '):
                correct_word = purify_str(TEST_LIST[line_ind].split(' ')[word_ind]).lower()
                print('comparison:', word, correct_word)
                try:
                    if word == correct_word:
                        word_ind += 1
                    else:
                        is_right = False
                        synthesize_text(TEST_STR.split(' ')[word_ind])
                        break
                except IndexError as err:
                    print('1!!!: ', err)
                    break

            if is_right:
                print(TEST_LIST[line_ind])
                line_ind += 1
                word_ind = 0

            if re.search(r"\b(exit|quit)\b", transcript, re.I):
                print("Exiting..")
                break

            num_chars_printed = 0


def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="uk-UA",
        name="uk-UA-Standard-A",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    playsound("output.mp3")


def main():
    language_code = "uk-UA"

    client = speech.SpeechClient()

    interaction_type = speech.RecognitionMetadata.InteractionType.DICTATION

    metadata = speech.RecognitionMetadata(
        interaction_type=interaction_type
    )

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        metadata=metadata,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        listen_print_loop(responses)


if __name__ == "__main__":
    main()
