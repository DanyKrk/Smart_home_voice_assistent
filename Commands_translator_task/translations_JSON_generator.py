import json

JSON_file_name = "translations_JSON.txt"


def generate_translations_JSON(home_dict):
    JSON_file = open(JSON_file_name, "w")
    JSON_file.write(json.dumps(home_dict))
    JSON_file.close()

def generate_translations_dict():
    t_dict = {}
    t_dict["devices"] = {}
    t_dict["places"] = {}
    t_dict["detailed_places"] = {}
    t_dict["storeys"] = {}
    return t_dict

def add_object(t_dict, category, name, polish_names):
    if category not in t_dict:
        print("specified category not in dict!!!")
        return
    t_dict[category][name] = polish_names

t_dict = generate_translations_dict()
add_object(t_dict, "places", "kitchen", ["kuchnia", "kuchni"])
add_object(t_dict, "places", "bedroom", ["sypialnia", "sypialni"])
add_object(t_dict, "places", "guest room", ["pokój gościnny", "gościnny", "gościnnym", "pokoju gościnnym"])
add_object(t_dict, "places", "workshop", ["pracownia", "pracowni"])
add_object(t_dict, "places", "salon", ["salon", "salonie"])
add_object(t_dict, "places", "anteroom", ["przedpokój", "przedpokoju"])
add_object(t_dict, "places", "staircase", ["schody", "klatka schodowa", "klatce schodowej", "schodach"])

add_object(t_dict, "storeys", 1, ["parter", "parterze"])
add_object(t_dict, "storeys", 2, ["pierwsze", "pierwsze piętro", "pierwszym", "pierwszym piętrze"])
add_object(t_dict, "storeys", 3, ["drugie", "drugie piętro", "drugim", "drugim piętrze"])
add_object(t_dict, "storeys", 0, ["piwnica", "piwnicy"])


