import json
import os
import re

def split_text_into_chunks(text, chunk_size,chunk_num):
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
    
    ans = []
    for idx,chunk in enumerate(chunks):
        if idx in chunk_num:
            ans.append(chunk)
    return ans

if __name__ == '__main__':
    # 输入txt文件路径
    txt_file_folder = '/mnt/users/chenmuyin/espeak/bbc'
    # 读取json
    file_folder = '/mnt/users/chenmuyin/espeak/output/chosen'
    if not os.path.exists(os.path.join(file_folder,'text')):
        os.mkdir(os.path.join(file_folder,'text'))
    dict_path = os.path.join(file_folder,'good_cases.json')
    with open(dict_path, 'r') as file:
        data = file.read()
        cases_dict = json.loads(data)

    for type in cases_dict.keys():
        for idx,chunks in cases_dict[type]:
            for chunk in chunks:
                # 指定英文文本文件路径
                txt_file_path = os.path.join(txt_file_folder,type,f'{idx:03d}.txt')
                # txt_file_path = '/mnt/users/chenmuyin/espeak/test_bbc/test_cases_xb/sport-058.txt'
                chunk_size = 300

                # 读取英文文本文件内容
                with open(txt_file_path, 'r', encoding='utf-8') as f:
                    file_content = f.read()

                # 将文本按照每300个词切分，保证首尾语句完整
                ans_chunks = split_text_into_chunks(file_content, chunk_size,chunks)

                for chunk_idx,chosen_chunk in zip(chunks,ans_chunks):
                    chosen_txt_name = f'{type}-{idx:03d}-{chunk_idx:02d}.txt'
                    chosen_txt_path = os.path.join(file_folder,'text',chosen_txt_name)
                    # 打印切分后的文本块
                    with open(chosen_txt_path, 'w', encoding='utf-8') as f:
                        f.write(chosen_chunk)
