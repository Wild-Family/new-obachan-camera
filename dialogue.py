import pandas as pd
import requests
import settings
import pygame.mixer
import os
import time


aitalk_url = "https://webapi.aitalk.jp/webapi/v2/ttsget.php"
csv_path = "./audio/dialogue.csv"
audio_folder = "./audio/"
df = pd.read_csv(csv_path, index_col=0)
pygame.mixer.init()

def get_dialogue(status):
    print(df['dialogue'][status])
    return df['dialogue'][status]

def get_filename(status):
    print(df['filename'][status])
    return df['filename'][status]

def play_audio(status):
    file_path = audio_folder + df['filename'][status]
    print(file_path)
    audio = pygame.mixer.Sound(file_path)
    channel = audio.play()
    # wait to finish
    while channel.get_busy():
        pygame.time.delay(100)
    pygame.time.delay(500)

def call_my_name(display_name):
    text = display_name
    filename = display_name + '.wav'
    request_aitalk(text, filename)
    file_path = audio_folder + filename
    audio = pygame.mixer.Sound(file_path)
    channel = audio.play()
    # wait to finish
    while channel.get_busy():
        pygame.time.delay(100)
    pygame.time.delay(300)
    play_audio("start")
    # remove audio file
    os.remove(file_path)

def count_down():
    play_audio("count3")
    pygame.time.delay(500)
    play_audio("count2")
    pygame.time.delay(500)
    play_audio("count1")
    pygame.time.delay(500)
    audio = pygame.mixer.Sound(audio_folder + "shut.wav")
    channel = audio.play()
    # wait to finish
    while channel.get_busy():
        pygame.time.delay(100)

def request_aitalk(dialogue, filename):
    params = {
        'username': settings.AITALK_USERNAME,
        'password': settings.AITALK_PASSWORD,
        'text': dialogue,
        'speaker_name': 'miyabi_west',
        'input_type': 'text',
        'volume': 1.00, # 音量
        'speed': 1.10, # 話速
        'pitch': 1.30, # 声の高さ
        'range': 1.20, # 抑揚(声の高さの範囲)
        'ext': 'wav'
    }
    # get an audio file from AITALK
    response = requests.get(aitalk_url, params=params)
    if response.status_code == 200:
        with open(audio_folder + filename, 'wb') as saveFile:
            saveFile.write(response.content)
    else:
        print(response)

def get_audio(status):
    dialogue = get_dialogue(status)
    filename = get_filename(status)
    # request an audio file and save it
    request_aitalk(dialogue, filename)

def main():
    get_dialogue("smile again")
    get_filename("smile again")
    get_audio("start")
    call_my_name("ドナルド・フォントルロイ・ダック")
    count_down()
    #request_aitalk("オバチャンが撮ったるで！", 'test.mp3')

if __name__ == '__main__':
    main()
        