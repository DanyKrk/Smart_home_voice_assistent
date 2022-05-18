import json

translations_JSON_file_name = "translations_JSON.txt"
home_JSON_file_name = "home_JSON.txt"

def get_dict_from_file(file_name):
    file = open(file_name, "r")
    JSON_string = file.read()
    file.close()
    return json.loads(JSON_string)

def category_representative_in_command(translations_dict, category, command):
    for representative in translations_dict[category]:
        for polish_name in translations_dict[category][representative]:
            if command.find(polish_name) != -1:
                return representative
    return None



def TextParser(translations_dict, command):
    command_dict = {}
    command_dict["storey"] = category_representative_in_command(translations_dict, "storeys", command)
    command_dict["room"] = category_representative_in_command(translations_dict, "rooms", command)
    command_dict["detailed_place"] = category_representative_in_command(translations_dict, "detailed_places", command)
    command_dict["action"] = category_representative_in_command(translations_dict, "actions", command)
    command_dict["device"] = category_representative_in_command(translations_dict, "devices", command)
    return command_dict


home_dict = get_dict_from_file(home_JSON_file_name)
translations_dict = get_dict_from_file(translations_JSON_file_name)

command = "włącz lampę w kuchni"
print(TextParser(translations_dict, command))
