from collections import defaultdict
import json
import os
import subprocess
from tqdm import tqdm
import numpy as np

def calculate_times(txt_path,DICT):
    count = 0
    bs = 300
    raw_dict = DICT
    dicts = []
    split_words = []
    bs_words = []
    with open(txt_path, 'r') as f:
        for line in f:
            file_contents = line.strip()
            if not file_contents:
                continue
            sentence = file_contents#[0:len(file_contents)]
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
                    count += 1
                    bs_words.append(word)
                    phs = word.split("_")
                    for ph in phs:
                            if ph != '':
                                raw_dict[ph] += 1

                            # if ph == 'oː':
                            #     print(phs)
                           
                    if count == bs:
                        tmp = raw_dict.copy()
                        dicts.append(tmp)
                        # 清空字典
                        for key in raw_dict.keys():
                            raw_dict[key] = 0
                        
                        # 清空记录
                        split_words.append(bs_words)
                        count = 0
                        bs_words = []
    return dicts,split_words


def test_top(new_dict):

    # Check if all values in the new_defaultdict are greater than 1
    all_values_greater_than_one = all(value >= 1 for value in list(new_dict.values())[:50])

    # Check if the first 30 values in the new_defaultdict are greater than 3
    first_30_values_greater_than_three = all(value >= 9 for value in list(new_dict.values())[:30])

    if all_values_greater_than_one and first_30_values_greater_than_three:
        return True
    else:
        return False

if __name__ == '__main__':
    txt_folder = '/mnt/users/chenmuyin/espeak/test_bbc/test_cases_xb/300'
    dict_path = '/mnt/users/chenmuyin/espeak/output/file_en-us_0815_sorted.json'

    save_folder = '/mnt/users/chenmuyin/espeak/output/chosen_dict_xb_sports'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    # 读取dict的降序排列
    with open(dict_path, 'r') as file:
        data = file.read()
        en_dict = json.loads(data)


    for idx,txt_name in tqdm(enumerate(os.listdir(txt_folder))):
        
        # 创建对应计数词典
        new_dict = defaultdict(int)
        for key in en_dict.keys():
            new_dict[key]

        # 确定输入txt的path
        txt_path = os.path.join(txt_folder,txt_name)
        dicts,split_words = calculate_times(txt_path, new_dict)

        
        for i,dict in enumerate(dicts):
            json_name = txt_name.split('.')[0]+f'_{i:02d}'

            if test_top(dict):
                print(f'输入文件{json_name}符合条件')
                words_name = json_name+'_good'+'.txt'
                json_name = json_name+'_good'+'.json'
                words_path = os.path.join(save_folder,words_name)
                # 保存字典为 txt 文件
                with open(words_path, 'w', encoding='utf-8') as file:
                    for item in split_words[i]:
                        file.write(str(item) + '\n')
            else:
                print(f'输入文件{json_name}不符合条件')
                json_name = json_name+'_bad'+'.json'          

            # 确定输出path       
            dict_out_path = os.path.join(save_folder,json_name)
            # 保存字典为 JSON 文件
            with open(dict_out_path, 'w', encoding='utf-8') as f:
                json.dump(dict, f, ensure_ascii=False, indent=4)

