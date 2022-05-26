import json

translations_JSON_file_name = "translations_JSON.txt"
home_JSON_file_name = "home_JSON.txt"

def get_dict_from_file(file_name):
    file = open(file_name, "r")
    JSON_string = file.read()
    file.close()
    return json.loads(JSON_string)

#Wyszukiwanie słowa z danej kategorii (np. pokoju w tekście)
def category_representative_in_command(translations_dict, category, command):
    for representative in translations_dict[category]:
        for polish_name in translations_dict[category][representative]:
            if command.find(polish_name) != -1:
                return representative
    return None


# Zamiana comendy na słownik z przypisanymi znaczeniami do słów
def TextParser(translations_dict, command):
    command_dict = {}
    command_dict["storey"] = category_representative_in_command(translations_dict, "storeys", command)
    command_dict["room"] = category_representative_in_command(translations_dict, "rooms", command)
    command_dict["detailed_place"] = category_representative_in_command(translations_dict, "detailed_places", command)
    command_dict["action"] = category_representative_in_command(translations_dict, "actions", command)
    command_dict["device"] = category_representative_in_command(translations_dict, "devices", command)
    return command_dict

# Generowanie wyjściowych poleceń (zwracana jest lista)
def CommandsGenerator(home_dict, command_dict, previous_room):
    commands = []

    storey = command_dict["storey"]
    room = command_dict["room"]
    device = command_dict ["device"]
    detailed_place = command_dict["detailed_place"]
    action = command_dict["action"]

    if action == None:
        action = "toggle"

    command = "cmd/"
    if(room != None):
        validate_room(home_dict, room)
        command = command + "/" + room
        if(device != None):
            validate_device_in_room(home_dict, room, device)
            command = command + "/" + device
            if(detailed_place != None):
                validate_detailed_place(home_dict, room, device, detailed_place)
                command = command + "/" + detailed_place
                if (action != "toggle"):
                    validate_action(home_dict, room, device, detailed_place, action)
                command = command + " " + action
                commands.append(command)
            else:
                for device_dict in devices_in_room(home_dict, room):
                    if device_dict["name"] == device:
                        detailed_place = device_dict["detailed_place"]
                        if (action != "toggle"):
                            validate_action(home_dict, room, device, detailed_place, action)
                        tmp_command = device_command(action, device_dict)
                        commands.append(tmp_command)
        else:
            for device_dict in devices_in_room(home_dict, room):
                tmp_command = device_command(action, device_dict)
                commands.append(tmp_command)
    else:
        if storey != None:
            for device_dict in devices_in_storey(home_dict, storey):
                tmp_command = device_command(action, device_dict)
                commands.append(tmp_command)
        elif detailed_place != None:
            for device_dict in devices_with_detailed_place(home_dict, detailed_place):
                tmp_command = device_command(action, device_dict)
                commands.append(tmp_command)
        else:
            room = previous_room
            validate_room(home_dict, room)
            command = command + "/" + room
            if (device != None):
                validate_device_in_room(home_dict, room, device)
                command = command + "/" + device
                if (detailed_place != None):
                    validate_detailed_place(home_dict, room, device, detailed_place)
                    command = command + "/" + detailed_place
                    if (action != "toggle"):
                        validate_action(home_dict, room, device, detailed_place, action)
                    command = command + " " + action
                    commands.append(command)
                else:
                    for device_dict in devices_in_room(home_dict, room):
                        if device_dict["name"] == device:
                            detailed_place = device_dict["detailed_place"]
                            if (action != "toggle"):
                                validate_action(home_dict, room, device, detailed_place, action)
                            tmp_command = device_command(action, device_dict)
                            commands.append(tmp_command)

    if len(commands) == 0:
        print("Nie rozumiem polecenia")
        exit(1)
    print(commands)
    return commands


#Tworzenie komendy na podstawie słownika urządzenia i akcji
def device_command(action, device_dict):
    tmp_command = "cmd/" + device_dict["name"]
    if (device_dict["room"] != None):
        tmp_command = tmp_command + "/" + device_dict["room"]
    if (device_dict["detailed_place"] != None):
        tmp_command = tmp_command + "/" + device_dict["detailed_place"]
    if (action != "toggle"):
        if action not in device_dict["possible_actions"]:
            print("Nie ma akcji: ", action, "dla urządzenia: ", device_dict["name"])
            exit(1)
    tmp_command = tmp_command + " " + action
    return tmp_command

#Sprawdzenie czy pokój istnieje
def validate_room(home_dict, room):
    if room not in home_dict["rooms"]:
        print("Nie ma pomieszczenia: ", room)
        exit(1)

#Sprawdzenie czy urządzenie jest w pokoju
def validate_device_in_room(home_dict, room, device):
    for device_dict in home_dict["devices"]:
        if device_dict["name"] == device and device_dict["room"] == room:
            return
    print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room)
    exit(1)

#Sprawdzenie, czy istnieje urządzenie w danym miejscu
def validate_detailed_place(home_dict, room, device, detailed_place):
    for device_dict in home_dict["devices"]:
        if device_dict["name"] == device and device_dict["room"] == room and device_dict["detailed_place"] == detailed_place:
            return
    print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room, " w miejscu: ", detailed_place)
    exit(1)

#Sprawdzenie, czy na urządzeniu w danym miejscu można wykonać daną akcję
def validate_action(home_dict, room, device, detailed_place, action):
    for device_dict in home_dict["devices"]:
        if device_dict["name"] == device and device_dict["room"] == room and device_dict["detailed_place"] == detailed_place\
                and action in device_dict["possible_actions"]:
            return
    print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room, " w miejscu: ", detailed_place,
          "o możliwej akcji: ", action)
    exit(1)

#Lista urządzeń w danym pokoju
def devices_in_room(home_dict, room):
    devices = []
    for device_dict in home_dict["devices"]:
        if device_dict["room"] == room:
            devices.append(device_dict)
    return devices

#lista urządzeń na danym piętrze
def devices_in_storey(home_dict, storey):
    devices = []
    for room in home_dict["storeys"][storey]:
        devices = devices + devices_in_room(home_dict, room)
    return devices

#Urządzenia w danym miejscu (np nad szafkami)
def devices_with_detailed_place(home_dict, detailed_place):
    devices = []
    for device_dict in home_dict["devices"]:
        if device_dict["detailed_place"] == detailed_place:
            devices.append(device_dict)
    return devices

#funkcja do testowania
def test_commands(commands):
    for command in commands:
        CommandsGenerator(home_dict, TextParser(translations_dict, command), "kitchen")

home_dict = get_dict_from_file(home_JSON_file_name)
translations_dict = get_dict_from_file(translations_JSON_file_name)

commands = ["włącz lampę w kuchni",
            "włącz światło na parterze",
            "załącz wszystkie lampy w salonie",
            "włącz światło nad szafkami",
            "lampa w kuchni",
            "która jest godzina"]

test_commands(commands)