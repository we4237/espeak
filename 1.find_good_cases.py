from collections import defaultdict
import json
import os
from tqdm import tqdm
import numpy as np

def conditions(new_dict) -> bool:
    all_values_greater_than_two = all(value >= 4 for value in list(new_dict.values())[:40])

    all_values_greater_than_one = all(value >= 1 for value in list(new_dict.values())[:53])

    first_30_values_greater_than_three = all(value >= 10 for value in list(new_dict.values())[:30])

    if all_values_greater_than_one and all_values_greater_than_two and first_30_values_greater_than_three:
        return True
    else:
        return False

def sentence_test(new_dict,npy_path):
    bs = 300
    mark_idx,count = 0,0
    whole_words = 0
    lines = np.load(npy_path,allow_pickle=True)
    ans = []
    tmp = []
    for line in lines:
        whole_words += len(line) 
        for word in line:
            count += 1
            word = word.split('_')
            for ph in word:
                if ph in new_dict.keys():
                    new_dict[ph] += 1
                    
                    tmp.extend(ph)
                if count == bs:
                    # print(new_dict)                    
                    if conditions(new_dict):
                        ans.append(mark_idx)

                    # 清空计数
                    for key in new_dict.keys():
                        new_dict[key] = 0

                    tmp = []
                    count = 0
                    mark_idx += 1
                    
    if whole_words % bs > 0 and conditions(new_dict):
        ans.append(mark_idx)

    return ans
    
def find_type(ph_idx,file_chunks,result_files,output_chunks=True):
    
    number = int(ph_idx)
    # 是否输出符合条件语句在原文中的第几段
    if output_chunks:
        if number <= 510:

            result_files['business'].append([number,file_chunks])
        elif  number <= (510+386):
            number -= 510
            result_files['entertainment'].append([number,file_chunks])
        elif  number <= (510+386+417):
            number -= 510+386
            result_files['politics'].append([number,file_chunks])
        elif  number <= (510+386+417+511):
            number -= 510+386+417
            result_files['sport'].append([number,file_chunks])
        else:
            number -= 510+386+417+511
            result_files['tech'].append([number,file_chunks])
    else:
        if number <= 510:
            result_files['business'].append(number)
        elif  number <= (510+386):
            number -= 510
            result_files['entertainment'].append(number)
        elif  number <= (510+386+417):
            number -= 510+386
            result_files['politics'].append(number)
        elif  number <= (510+386+417+511):
            number -= 510+386+417
            result_files['sport'].append(number)
        else:
            number -= 510+386+417+511
            result_files['tech'].append([number,file_chunks])
    return result_files

if __name__ == '__main__':
    path_folder = '/mnt/users/chenmuyin/espeak/output/ph_files'
    dict_path = '/mnt/users/chenmuyin/espeak/output/file_en-us_0815_sorted.json'

    save_folder = '/mnt/users/chenmuyin/espeak/output/chosen'
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    # 读取.txt文件内容并保存为列表
    # input_paths = []
    # with open(path_files, 'r') as f:
    #     for line in f:
    #         input_paths.append(line.strip())  # 去除行尾的换行符等空白字符

    # input_paths = ['/mnt/users/chenmuyin/espeak/test_bbc/tech/354.txt']
    with open(dict_path, 'r') as file:
        data = file.read()
        en_dict = json.loads(data)

    result_files = {'business':[],
                'entertainment':[],
                'politics':[],
                'sport':[],
                'tech':[]}
    json_name = os.path.join(save_folder,'good_cases.json')    
    dict_out_path = os.path.join(save_folder,json_name)

    for idx,npy_name in tqdm(enumerate(os.listdir(path_folder))):
        npy_path = os.path.join(path_folder,npy_name)
        ph_idx = npy_name.split('_')[2].split('.')[0]

        new_dict = defaultdict(int)
        for key in en_dict.keys():
            new_dict[key]

        file_chunks = sentence_test(new_dict,npy_path)
        if file_chunks :
            # arr = np.array(choice_file)
            # save_path = os.path.join(save_folder,npy_name)
            # np.save(save_path,arr)

            result_files = find_type(ph_idx,file_chunks,result_files,output_chunks=True)
        
        
    with open(dict_out_path, 'w', encoding='utf-8') as f:
        json.dump(result_files, f, ensure_ascii=False, indent=4)
