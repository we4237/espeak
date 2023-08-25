import subprocess
import numpy as np


npy_path = f'output/chosen/file_en-us_0342.npy'
a = np.load(npy_path,allow_pickle=True)
# print(a)
txt_path = '/mnt/users/chenmuyin/espeak/bbc/business/342.txt'
count = 0
res = []
tmp = []
with open(txt_path, 'r') as f:
    for line in f:
        file_contents = line.strip()
        if not file_contents:
            continue
        sentence = file_contents#[0:len(file_contents)]
        sentence = sentence.replace("\"",' ')
        sentence = sentence.replace("\"",' ')  
        
        for word in sentence.split(' '):
            count += 1
            if count <= 300:
                tmp.append(word)
            else:
                count = 1
                res.append(tmp)
                tmp = []
                tmp.append(word)

for x in res:
    sentence = ' '.join(x)
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