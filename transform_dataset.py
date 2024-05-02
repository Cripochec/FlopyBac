import json


def load_data_from_json(dataset):
    with open(dataset, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def write_data_to_json(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


# Функция для преобразования записи в соответствии с заданным форматом
def process_json(input_file):
    data = {}
    n = 0
    k = 0
    for i in input_file:
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


file_path = 'user_info.json'
input_file = load_data_from_json(file_path)  # Укажите путь к вашему JSON файлу
output_file = "dataset.json"  # Укажите путь к файлу, в который будет записан результат

data = process_json(input_file)
write_data_to_json(data, output_file)
