from collections import OrderedDict
import json

# 指定要读取的 JSON 文件路径
input_json_path = '/mnt/users/chenmuyin/espeak/output/file_en-us_0814.json'
save_json_path = '/mnt/users/chenmuyin/espeak/output/file_en-us_0815_sorted.json'
# 读取 JSON 文件内容
with open(input_json_path, 'r', encoding='utf-8') as f:
    data = json.load(f, object_pairs_hook=OrderedDict)

#对字典进行排序
sorted_data = OrderedDict(sorted(data.items(), key=lambda item: item[1], reverse=True))
# print(sorted_data)
with open(save_json_path, 'w', encoding='utf-8') as f:
    json.dump(sorted_data, f, ensure_ascii=False, indent=4)