import json
import random


def load_data_from_json(dataset):
    with open(dataset, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_data_to_json(data, output_file_json):
    with open(output_file_json, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def process_json_true(input_file_json):
    data = {}
    n = 0
    k = 0
    for i in input_file_json:
        try:
            line = {
                "match": True,
                "human1": {
                    "games": i[f'User{n}']["Games"],
                    "music": i[f'User{n}']["Music"],
                    "occupation": i[f'User{n}']["Occupation"]["type"],
                    "personal": {
                        "alcohol": i[f'User{n}']["Personal"]["Alcohol"],
                        "smoking": i[f'User{n}']["Personal"]["Smoking"],
                        "inspired_by": i[f'User{n}']["Personal"]["Inspired by"],
                        "people_main": i[f'User{n}']["Personal"]["People Main"],
                        "life_main": i[f'User{n}']["Personal"]["Life Main"],
                    },
                    "groups": [group["Group Thematic"] for group in i[f'User{n}']["Groups"]]
                },
                "human2": {
                    "games": i[f'User{n}']["Relation Partner"]["Games"],
                    "music": i[f'User{n}']["Relation Partner"]["Music"],
                    "occupation": i[f'User{n}']["Relation Partner"]["Occupation"]["type"],
                    "personal": {
                        "alcohol": i[f'User{n}']["Relation Partner"]["Personal"]["Alcohol"],
                        "smoking": i[f'User{n}']["Relation Partner"]["Personal"]["Smoking"],
                        "inspired_by": i[f'User{n}']["Relation Partner"]["Personal"]["Inspired by"],
                        "people_main": i[f'User{n}']["Relation Partner"]["Personal"]["People Main"],
                        "life_main": i[f'User{n}']["Relation Partner"]["Personal"]["Life Main"],
                    },
                    "groups": [group["Group Thematic"] for group in i[f'User{n}']["Relation Partner"]["Groups"]]
                }
            }
            data[f"record{k}"] = line
            k += 1
        except Exception as ex:
            print(ex)
        n += 1
    return data


def process_json_false(input_file_json1, input_file_json2):
    data = {}
    n = 0
    k = 0

    for i in range(len(input_file_json1)):
        l1 = input_file_json1[i]
        l2 = input_file_json2[i]
        try:
            line = {
                "match": False,
                "human1": {
                    "games": l1[f'User{n}']["Games"],
                    "music": l1[f'User{n}']["Music"],
                    "occupation": l1[f'User{n}']["Occupation"]["type"],
                    "personal": {
                        "alcohol": l1[f'User{n}']["Personal"]["Alcohol"],
                        "smoking": l1[f'User{n}']["Personal"]["Smoking"],
                        "inspired_by": l1[f'User{n}']["Personal"]["Inspired by"],
                        "people_main": l1[f'User{n}']["Personal"]["People Main"],
                        "life_main": l1[f'User{n}']["Personal"]["Life Main"],
                    },
                    "groups": [group["Group Thematic"] for group in l1[f'User{n}']["Groups"]]
                },
                "human2": {
                    "games": l2[f'User{n}']["Games"],
                    "music": l2[f'User{n}']["Music"],
                    "occupation": l2[f'User{n}']["Occupation"]["type"],
                    "personal": {
                        "alcohol": l2[f'User{n}']["Personal"]["Alcohol"],
                        "smoking": l2[f'User{n}']["Personal"]["Smoking"],
                        "inspired_by": l2[f'User{n}']["Personal"]["Inspired by"],
                        "people_main": l2[f'User{n}']["Personal"]["People Main"],
                        "life_main": l2[f'User{n}']["Personal"]["Life Main"],
                    },
                    "groups": [group["Group Thematic"] for group in l2[f'User{n}']["Groups"]]
                }
            }
            data[f"record{k}"] = line
            k += 1
        except Exception as ex:
            print(ex)
        n += 1
    return data


file_path_true = 'user_info.json'
file_path_false1 = 'user_red21.json'
file_path_false2 = 'user_chastity.json'

input_file_true = load_data_from_json(file_path_true)
input_file_false1 = load_data_from_json(file_path_false1)
input_file_false2 = load_data_from_json(file_path_false2)


data_true = process_json_true(input_file_true)
data_false = process_json_false(input_file_false1, input_file_false2)


combined_data = {**data_true, **data_false}
combined_list = list(combined_data.items())
random.shuffle(combined_list)
shuffled_data = dict(combined_list)

output_file = "dataset.json"

# Запись обработанных данных в файл JSON
write_data_to_json(shuffled_data, output_file)
