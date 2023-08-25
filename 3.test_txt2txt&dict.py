import argparse
from collections import defaultdict
import json
import os
import re
import subprocess
from tqdm import tqdm
import numpy as np

def split_text_into_chunks(text, chunk_size=300):
    sentences = re.split(r'(?<=[.!?])\s+', text)  # 使用正则表达式分割句子
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        sentence = sentence.replace("\n",' ')
        if len(current_chunk.split()) + len(sentence.split()) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

def calculate_times(txt_path,DICT,is_split=False):

    bs = 300
    raw_dict = DICT
    dicts = []

    with open(txt_path, 'r') as f:
        file_content = f.read()
    if is_split:
        # 将文本分割成每300个单词的列表，并忽略空行和换行符
        result_lists = split_text_into_chunks(file_content, chunk_size=bs)
    else:
        result_lists = split_text_into_chunks(file_content, chunk_size=len(file_content))
   
    
    for sentence in result_lists:
        sentence = sentence.replace("\"",' ')
        sentence = sentence.replace("\"",' ')
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
            if word != '':
                phs = word.split("_")
                for ph in phs:
                    if ph != '':
                        raw_dict[ph] += 1

        tmp = raw_dict.copy()
        dicts.append(tmp)
        # 清空字典
        for key in raw_dict.keys():
            raw_dict[key] = 0


    return dicts,result_lists


def test_top(new_dict):

    all_values_greater_than_two = all(value >= 4 for value in list(new_dict.values())[:40])

    all_values_greater_than_one = all(value >= 1 for value in list(new_dict.values())[:53])

    first_30_values_greater_than_three = all(value >= 10 for value in list(new_dict.values())[:30])

    if all_values_greater_than_one and all_values_greater_than_two and first_30_values_greater_than_three:
        return True
    else:
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--txt_folder", type=str, default='/mnt/users/chenmuyin/espeak/test_bbc/test_again')
    # 默认固定
    parser.add_argument("--dict_path", type=str, default='/mnt/users/chenmuyin/espeak/output/file_en-us_0815_sorted.json')
    parser.add_argument("--save_folder", type=str, default='/mnt/users/chenmuyin/espeak/output/chosen_txt2txt')
    # parser.add_argument("--bs", type=int, default=300)

    # 对输入文本是否需要按给定字数切割
    parser.add_argument("--is_split", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.save_folder):
        os.mkdir(args.save_folder)

    # 读取dict的降序排列
    with open(args.dict_path, 'r') as file:
        data = file.read()
        en_dict = json.loads(data)


    for idx,txt_name in tqdm(enumerate(os.listdir(args.txt_folder))):
        
        # 创建对应计数词典
        new_dict = defaultdict(int)
        for key in en_dict.keys():
            new_dict[key]

        # 确定输入txt的path
        txt_path = os.path.join(args.txt_folder,txt_name)
        dicts,word_list = calculate_times(txt_path, new_dict,is_split=args.is_split)

        for i,dict in enumerate(dicts):
            json_name = txt_name.split('.')[0]+f'_{i:02d}'

            if test_top(dict):
                print(f'输入文件{json_name}符合条件')
                words_name = json_name+'_good'+'.txt'
                json_name = json_name+'_good'+'.json'
                words_path = os.path.join(args.save_folder,words_name)
                # 保存字典为 txt 文件
                with open(words_path, 'w', encoding='utf-8') as file:
                    file.write(' '.join(word_list))
            else:
                print(f'输入文件{json_name}不符合条件')
                json_name = json_name+'_bad'+'.json'          

            # 确定输出path       
            dict_out_path = os.path.join(args.save_folder,json_name)
            # 保存字典为 JSON 文件
            with open(dict_out_path, 'w', encoding='utf-8') as f:
                json.dump(dict, f, ensure_ascii=False, indent=4)

