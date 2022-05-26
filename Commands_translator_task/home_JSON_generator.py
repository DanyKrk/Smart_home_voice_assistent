import json

JSON_file_name = "home_JSON.json"


def generate_home_JSON(home_dict):
    JSON_file = open(JSON_file_name, "w")
    JSON_file.write(json.dumps(home_dict))
    JSON_file.close()

def generate_home_dict():
    home_dict = {}
    home_dict["devices"] = []
    home_dict["rooms"] = []
    home_dict["storeys"] = {}
    return home_dict

def add_room(home_dict, room_name, room_storey):
    home_dict["rooms"].append(room_name)

    if room_storey not in home_dict["storeys"]:
        home_dict["storeys"][room_storey] = []
    home_dict["storeys"][room_storey].append(room_name)

def add_device(home_dict, name, room, detailed_place, possible_actions):
    if room not in home_dict["rooms"]:
        print("Specified room not in dictionary!!!\n")
        return
    home_dict["devices"].append({"name": name,
                                 "room": room,
                                 "detailed_place": detailed_place,
                                 "possible_actions": possible_actions})

home_dict = generate_home_dict()

add_room(home_dict, "kitchen", 1)
add_room(home_dict, "bedroom", 2)
add_room(home_dict, "guest room", 2)
add_room(home_dict, "workshop", 2)
add_room(home_dict, "salon", 1)
add_room(home_dict, "anteroom", 1)
add_room(home_dict, "staircase", 1)

add_device(home_dict, "lamp", "anteroom", "ceiling", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "bedroom", "ceiling", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "kitchen", "above_the_cabinets", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "kitchen", "ceiling", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "workshop", "ceiling", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "salon", "right_wall", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "salon", "left_wall", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "salon", "ceiling", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "staircase", "right_wall", ["on", "off", "toggle", "brightness"])
add_device(home_dict, "lamp", "staircase", "left_wall", ["on", "off", "toggle", "brightness"])

generate_home_JSON(home_dict)



