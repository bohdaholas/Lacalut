from __future__ import division
import time
from tkinter import *
from tkinter import scrolledtext  
from functools import partial
from tkinter.ttk import Combobox
from tkinter.ttk import Radiobutton

import random
import json
import re

ERROR_MESSAGES = ['Ви помилилися!', 'Помилка', 'Неправильно', 'Чьо це таке']


import sys

from google.cloud import speech, texttospeech
from playsound import playsound

import pyaudio
from six.moves import queue


RATE = 16000
CHUNK = int(RATE / 10)


TEST_STR = 'Думи мої думи мої Лихо мені з вами Нащо стали на папері Сумними рядами Чом вас вітер не розвіяв В степу як пилину Чом вас лихо не приспало Як свою дитину За карії оченята За чорнії брови Серце рвалося сміялось Виливало мову Виливало як уміло За темнії ночі За вишневий сад зелений За ласки дівочі За степи та за могили Що на Україні'.lower()

prev_ind = word_ind = 0

class Lacalut:
    def __init__(self):
        self.custom_verse_available = True
        self.verse = None
        self.proceed_db()

    def proceed_db(self):
        with open("poetry_db.json", mode="r", encoding="utf-8") as f:
                data = json.load(f)
        self.newdata = {}
        for key in data:
            newkey = re.sub('[“”(</a>)(</A>)]', '', key)
            self.newdata[newkey] = [data[key][0], data[key][1]]

    def initialise_starting_window(self):
        self.starting_window = Tk()
        # self.starting_window.configure(bg = "#63C77C")
        text = Label(self.starting_window, text= "знайдіть вірш за назвою, або введіть власний")
        text.pack()

        self.input = Entry(self.starting_window)
        self.input.pack()

        self.starting_window.title("Lacalut")
        self.starting_window.geometry('350x600')

        self.lbl = Label(self.starting_window, text="")
        self.lbl.pack()
        
        self.enter_custom_btn = Button(self.starting_window, text="ввести власний вірш", bg = "#315EBB", command = self.initialise_custom_verse_window)
        self.enter_custom_btn.pack()

        self.submit_verse_btn = Button(self.starting_window, text="підтвердити вірш", bg = "#315EBB", command = self.submit_verse)
        self.submit_verse_btn.pack()

        self.user_verse_preview = Label(self.starting_window, text= "*тут буде відображатися прев'ю вашого вірша*", fg="#616264", height= 25)
        self.user_verse_preview.pack()


        self.selected = IntVar()

        self.rad1 = Radiobutton(self.starting_window, text='режим перевірки в прямому часі', value=1, variable=self.selected)
        self.rad1.pack()  
        self.rad2 = Radiobutton(self.starting_window, text='режим пост аналізу', value=2, variable=self.selected)
        self.rad2.pack()

        self.move_to_analisys_btn = Button(self.starting_window, text="proceed to studying", command= self.proceed_with_settings, bg= "#315EBB")
        self.move_to_analisys_btn.pack()
        # self.btn1 = Button(self.starting_window, text="print verse", bg = "#315EBB", command = self.print_custom_verse)
        # self.btn1.pack()

        self.starting_window.mainloop()
    
    def proceed_with_settings(self):
        print(self.selected.get())
        if self.selected.get() == 1:
            self.initialise_last_page_streaming()
        elif self.selected.get() == 2:
            self.initialise_last_page_post_processing()

    def initialise_last_page_streaming(self):
        self.learning_window = Tk()
        self.learning_window.geometry('400x300')
        self.learning_window.title("потокове навчання")

        self.start_listening_btn = Button(self.learning_window, text= "почати роботу", command= self.start_listening)
        self.start_listening_btn.pack()


        self.stop_listening_btn = Button(self.learning_window, text= "зупинити роботу", command= self.stop_listening)
        self.stop_listening_btn.pack()


        self.indicator = Label(self.learning_window, text= "почніть говорити коли готові\nробіть паузи в 2-3 секунди між рядками", bg="#64F341", height= 5, width= 35, font=("Arial", 15))
        self.indicator.pack()

        self.test_wrong_btn = Button(self.learning_window, text= "TEST_BTN_WRONG", command = self.indicate_streaming_mistake)
        self.test_wrong_btn.pack()

        self.test_ok_btn = Button(self.learning_window, text= "TEST_BTN_OK", command = self.indicate_streaming_ok)
        self.test_ok_btn.pack()

        self.learning_window.mainloop()
    
    def initialise_last_page_post_processing(self):
        self.learning_window = Tk()
        self.learning_window.geometry('300x300')
        self.learning_window.title("пост аналіз")

        self.start_listening_btn = Button(self.learning_window, text= "start listening", command= self.start_listening)
        self.start_listening_btn.pack()

        self.stop_listening_btn = Button(self.learning_window, text= "stop listening", command= self.stop_listening)
        self.stop_listening_btn.pack()

        self.learning_window_msg = Label(self.learning_window, text= "grats")
        self.learning_window_msg.pack()

        self.report = Label(self.learning_window, text="your report will be here")
        self.report.pack()

        self.learning_window.mainloop()

    def indicate_streaming_mistake(self, line= "!!LINE!!"):
        self.indicator.configure(text= "помилка в стрічці\n{}".format(line), bg="#FA9D0E")

    def indicate_streaming_ok(self):
        self.indicator.configure(text= "все чудово!", bg="#64F341")

    def indicate_streaming_stop(self):
        self.indicator.configure(text= "розпізнавання призупинено", bg="#D3FE92")

    def print_custom_verse(self):
        print(self.verse)

    def submit_verse(self):
        if self.verse == None or self.input.get():
            if self.input.get() in self.newdata:
                self.verse = self.newdata[self.input.get()]
        if len(self.verse) > 600:
            self.verse = self.verse[:600] + "..."
        self.user_verse_preview.config(text=self.verse, fg="#000000")

    
    def initialise_custom_verse_window(self):
        if self.custom_verse_available:
            self.custom_verse_available = False
            self.custom_verse_window = Tk()
            self.custom_verse_window.title("ввід свого вірша")

            self.enter_your_verse = Label(self.custom_verse_window, text= "введіть текст вірша")
            self.enter_your_verse.pack()

            self.txt = scrolledtext.ScrolledText(self.custom_verse_window, width=40, height=10, bg="#85ABFC")
            self.txt.pack(anchor='center')
            
            self.submit_btn = Button(self.custom_verse_window, text="підтвердити вірш", bg = "#315EBB", command = self.submit_custom_verse)
            self.submit_btn.pack()

            self.custom_verse_window.mainloop()

    
    def submit_custom_verse(self):
        self.verse = self.txt.get(1.0, END)
        self.custom_verse_window.destroy()
        self.custom_verse_available = True


    def start_listening(self):
        self.indicate_streaming_ok()
        main(self)

    def stop_listening(self):
        self.indicate_streaming_stop()


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


def listen_print_loop(responses, lacalut):
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
        global prev_ind


        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + "\r")
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            if transcript.strip() == 'кінець':
                print("Exiting..")
                return 0

            print(transcript + overwrite_chars)
            for word in transcript.strip().lower().split(' '):
                try:
                    if word == TEST_STR.split(' ')[word_ind]:
                        word_ind += 1
                    else:
                        synthesize_text('Стоп стоп стоп, харе' + random.choice(ERROR_MESSAGES))
                        if word_ind == 0:
                            synthesize_text(TEST_STR.split(' ')[word_ind])
                            # time.sleep(5)

                        else:
                            synthesize_text(' '.join(TEST_STR.split(' ')[word_ind-1:word_ind+1]))
                            # time.sleep(5)

                        lacalut.indicate_streaming_mistake(word)
                        break
                except IndexError:
                    break

            try:
                print(' '.join(TEST_STR.split(' ')[:word_ind]))
                prev_ind = word_ind
            except IndexError:
                word_ind = 0

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


def main(lacalut):
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

        listen_print_loop(responses, lacalut)


lacalut = Lacalut()
if __name__ == "__main__":
    lacalut.initialise_starting_window()


