input_files = ['positive_plain.jsonl', 'negative_plain.jsonl']
output_file = open('dataset_plain.jsonl', 'w+', encoding='utf-8')

for file in input_files:
    with open(file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        output_file.write(line)

output_file.close()
