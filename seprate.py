from collections import defaultdict
import subprocess
from phonemizer import phonemize
from phonemizer.separator import Separator
import json
import os
import numpy as np
from tqdm import tqdm

DICT = defaultdict(int)


def get_txt_files_recursive(folder_path):
    txt_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files

def calculate_times(sentence,DICT):
    cmd = f"espeak-ng -x -v en-us \"{sentence}\" --ipa=1"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # a = phonemize(f'{output.stdout}', language="en-us", backend="espeak", strip=True, separator=Separator(phone=' ', syllable='', word=''))
    # print(sentence)
    tmp = output.stdout.replace("ˈ",'')
    tmp = tmp.replace("'",'')
    tmp = tmp.replace(",",'')
    tmp = tmp.replace("ˌ",'')
    tmp = tmp.replace("\n",' ')
    words = tmp.split(" ")
    for word in words:
        # print(word)
        phs = word.split("_")
        for ph in phs:
            if ph != '':
                if len(ph)> 4:
                    print('==='+ph+'===')
                DICT[ph] += 1
    # print('+++')

def save_path_files(folder_path,path_files):
    txt_files = get_txt_files_recursive(folder_path)
    # 将txt_files保存为一个txt文件
    with open(path_files, 'w') as f:
        for txt_file in txt_files:
            f.write(txt_file + '\n')

if __name__ == '__main__':
    path_files = '/mnt/users/chenmuyin/espeak/output/path_files.txt'
    dict_path = '/mnt/users/chenmuyin/espeak/output/file_en-us_0814.json'

    # path_files = '/mnt/users/chenmuyin/espeak/output/path_files_tech.txt'
    # folder_path = '/mnt/users/chenmuyin/espeak/test_bbc'
    # save_path_files(folder_path,path_files)

    # 读取.txt文件内容并保存为列表
    input_paths = []
    with open(path_files, 'r') as f:
        for line in f:
            input_paths.append(line.strip())  # 去除行尾的换行符等空白字符

    # input_paths = ['/mnt/users/chenmuyin/espeak/test_bbc/tech/354.txt']

    for idx,path in tqdm(enumerate(input_paths)):
        # dict_path = f'/mnt/users/chenmuyin/espeak/output/jsons/file_en-us_{(idx+1):04d}.json'
        # dict_path = f'/mnt/users/chenmuyin/espeak/output/jsons/file_en-us_354_copy.json'

        with open(path, 'r') as f:
            for line in f:
                file_contents = line.strip()
                if not file_contents:
                    continue
                sentence = file_contents#[0:len(file_contents)]
                sentence = sentence.replace("\"",' ')
                sentence = sentence.replace("\"",' ')
                # print(sentence)
                calculate_times(sentence, DICT)
        print(f'{idx+1}')
        # 保存字典为 JSON 文件
        with open(dict_path, 'w', encoding='utf-8') as f:
            json.dump(DICT, f, ensure_ascii=False, indent=4)


