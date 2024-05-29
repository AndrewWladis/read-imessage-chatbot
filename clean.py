import csv
import json
import sys

# Increase the CSV field size limit
csv.field_size_limit(sys.maxsize)

# Read the CSV file
with open('chats.csv', mode='r') as file:
    csv_reader = csv.DictReader(file)
    messages = list(csv_reader)

# Initialize an empty list to store JSON objects
json_objects = []

# Iterate over the messages
for i in range(len(messages) - 1):
    if messages[i]['is_from_me'] == '0' and messages[i - 1]['is_from_me'] == '1' and messages[i]['text'] != '�' and messages[i - 1]['text'] != '�' and messages[i]['handle_id'] == messages[i - 1]['handle_id'] and messages[i]['text'] != '' and messages[i - 1]['text'] != '' and messages[i - 1]['text'] != 'Sea Battle' and messages[i - 1]['text'] != 'Cup Pong' and messages[i - 1]['text'] != '8 Ball':
        prompt = messages[i]['text']
        completion = messages[i - 1]['text']
        json_object = {
            "prompt": prompt,
            "completion": completion
        }
        json_objects.append(json_object)

# Write the JSON objects to a file as a single array
with open('output.json', mode='w', encoding='utf-8') as json_file:
    json.dump(json_objects, json_file, ensure_ascii=False, indent=4)

print("JSON objects have been written to output.json")
