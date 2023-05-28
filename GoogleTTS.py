import sys
import argparse
import re
import urllib.parse
import urllib.request
import time
from collections import namedtuple
import os
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

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

LANGUAGE_TAGS = {
    'English': 'en-us',
    'French': 'fr-fr',
    'Mandarin chinese': 'zh-cn',
    'Japanese': 'ja-jp'
}

def get_language_tag(language):
    return LANGUAGE_TAGS.get(language.lower())

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

    progress_bar = tqdm(total=len(combined_text), ncols=80, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')

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
            progress_bar.update(1)

    for idx in range(len(combined_text)):
        if idx in downloaded_chunks and downloaded_chunks[idx]:
            args.output.write(downloaded_chunks[idx])

    args.output.close()
    print(f"Saved MP3 to {args.output.name}")

def text_to_speech_mp3_argparse():
    print("Welcome to Google TTS audiobook maker")
    print("Please select your document's language:")
    for idx, language in enumerate(LANGUAGE_TAGS.keys(), 1):
        print(f"{idx}. {language}")
    language_selection = int(input("Select language: "))
    language_list = list(LANGUAGE_TAGS.keys())
    selected_language = language_list[language_selection - 1]
    language_tag = get_language_tag(selected_language)

    speed = float(input("Please select the speed at which you want your file to be read: "))
    file_path = input("Input file name: ")

    base_name = os.path.splitext(file_path)[0]
    output_filename = base_name + ".mp3"

    with open(file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()

    audio_extract(input_text=input_text, language=language_tag, speed=speed, output_filename=output_filename)

if __name__ == "__main__":
    text_to_speech_mp3_argparse()
