import sys
import argparse
import re
import urllib.parse
import urllib.request
import time
from collections import namedtuple
import os

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QFileDialog

class AudioExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google TTS Audiobook Maker")
        self.language_tags = {
            'english': 'en-us',
            'french': 'fr-fr',
            'mandarin chinese': 'zh-cn',
            'japanese': 'ja-jp'
        }
        self.init_ui()

    def init_ui(self):
        self.language_label = QLabel("Select language:")
        self.language_combo = QComboBox()
        self.language_combo.addItems(self.language_tags.keys())

        self.speed_label = QLabel("Select reading speed:")
        self.speed_input = QLineEdit()
        self.speed_input.setPlaceholderText("Speed (e.g., 0.4)")

        self.file_button = QPushButton("Select File")
        self.file_button.clicked.connect(self.select_file)

        self.convert_button = QPushButton("Convert to MP3")
        self.convert_button.clicked.connect(self.convert_to_mp3)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.language_label)
        main_layout.addWidget(self.language_combo)
        main_layout.addWidget(self.speed_label)
        main_layout.addWidget(self.speed_input)
        main_layout.addWidget(self.file_button)
        main_layout.addWidget(self.convert_button)

        self.setLayout(main_layout)

    def select_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Select File")
        self.file_input.setText(file_path)

    def convert_to_mp3(self):
        language_index = self.language_combo.currentIndex()
        selected_language = list(self.language_tags.keys())[language_index]
        language_tag = self.language_tags[selected_language]

        speed = float(self.speed_input.text())
        file_path = self.file_input.text()

        base_name = os.path.splitext(file_path)[0]
        output_filename = base_name + ".mp3"

        with open(file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()

        audio_extract(input_text=input_text, language=language_tag, speed=speed, output_filename=output_filename)

def split_text(input_text, max_length=100):
    def split_text_rec(input_text, regexps, max_length=max_length):
        if len(input_text) <= max_length:
            return [input_text]

        if isinstance(regexps, str):
            regexps = [regexps]
        regexp = regexps.pop(0) if regexps else '(.{%d})' % max_length

        text_list = re.split(regexp, input_text)
        combined_text = []
        combined_text.extend(split_text_rec(text_list.pop(0), regexps, max_length))
        for val in text_list:
            current = combined_text.pop()
            concat = current + val
            if len(concat) <= max_length:
                combined_text.append(concat)
            else:
                combined_text.append(current)
                combined_text.extend(split_text_rec(val, regexps, max_length))
        return combined_text

    return split_text_rec(input_text.replace('\n', ''), ['([\,|\.|;]+)', '( )'])

audio_args = namedtuple('audio_args', ['output'])

def get_language_tag(language):
    return language_tags.get(language.lower())

def download_chunk(mp3url, headers):
    try:
        response = urllib.request.urlopen(mp3url)
        return response.read()
    except urllib.error.URLError as e:
        print('%s' % e)
        return None

def audio_extract(input_text='', language='en-us', speed=0.4, output_filename='output.mp3'):
    args = audio_args(output=open(output_filename, 'wb'))
    combined_text = split_text(input_text)

    max_workers = 20
    downloaded_chunks = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for idx, val in enumerate(combined_text):
            mp3url = f"https://www.google.com/speech-api/v1/synthesize?text={urllib.parse.quote(val)}&enc=mpeg&lang={language}&speed={speed}&client=lr-language-tts&use_google_only_voices=1"
            headers = {
                "Host": "www.google.com",
                "Referer": "http://www.gstatic.com/translate/sound_player2.swf",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.163 Safari/535.19"
            }
            future = executor.submit(download_chunk, mp3url, headers)
            futures.append((future, idx))

        for future, idx in futures:
            data = future.result()
            downloaded_chunks[idx] = data

    for idx in range(len(combined_text)):
        if idx in downloaded_chunks and downloaded_chunks[idx]:
            args.output.write(downloaded_chunks[idx])

    args.output.close()
    print(f"Saved MP3 to {args.output.name}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    audio_extractor = AudioExtractor()
    audio_extractor.show()
    sys.exit(app.exec_())
