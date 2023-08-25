import json
import os
import fnmatch
import shutil

# 指定要搜索的路径
chosen_path = '/mnt/users/chenmuyin/espeak/output/chosen'

# 搜索路径下所有的.txt文件
txt_files = []
for root, dirs, files in os.walk(chosen_path):
    for file in files:
        if fnmatch.fnmatch(file, '*.npy'):
            txt_files.append(os.path.join(root, file))

# 计算它原本的名字
result_files = {'business':[],
                'entertainment':[],
                'politics':[],
                'sport':[],
                'tech':[]}

for txt_file in txt_files:
    number = os.path.basename(txt_file).split('_')[2].split('.')[0]
    number = int(number)
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
        result_files['tech'].append(number)

# 移动文件
bbc_path = '/mnt/users/chenmuyin/espeak/bbc'
test_path = '/mnt/users/chenmuyin/espeak/test_bbc/test_cases_xb'
for key,list in zip(result_files.keys(),result_files.values()):
    for number in list:
                
        new_name = str(key) + '-' + str(number).zfill(3) + '.txt'
        source_path = os.path.join(bbc_path,str(key),str(number).zfill(3)+'.txt')
        destination_path = os.path.join(test_path,new_name)
        shutil.copy(source_path,destination_path)

# 输出字典      
dict_out_path = os.path.join(chosen_path,'chosen.json')
# 保存字典为 JSON 文件
with open(dict_out_path, 'w', encoding='utf-8') as f:
    json.dump(result_files, f, ensure_ascii=False, indent=4)

