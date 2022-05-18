import json

JSON_file_name = "translations_JSON.txt"


def generate_translations_JSON(home_dict):
    JSON_file = open(JSON_file_name, "w")
    JSON_file.write(json.dumps(home_dict))
    JSON_file.close()

def generate_translations_dict():
    t_dict = {}
    t_dict["devices"] = {}
    t_dict["rooms"] = {}
    t_dict["detailed_places"] = {}
    t_dict["storeys"] = {}
    t_dict["actions"] = {}
    return t_dict

def add_object(t_dict, category, name, polish_names):
    if category not in t_dict:
        print("specified category not in dict!!!")
        return
    t_dict[category][name] = polish_names

t_dict = generate_translations_dict()
add_object(t_dict, "rooms", "kitchen", ["kuchnia", "kuchni"])
add_object(t_dict, "rooms", "bedroom", ["sypialnia", "sypialni"])
add_object(t_dict, "rooms", "guest room", ["pokój gościnny", "gościnny", "gościnnym", "pokoju gościnnym"])
add_object(t_dict, "rooms", "workshop", ["pracownia", "pracowni"])
add_object(t_dict, "rooms", "salon", ["salon", "salonie"])
add_object(t_dict, "rooms", "anteroom", ["przedpokój", "przedpokoju"])
add_object(t_dict, "rooms", "staircase", ["schody", "klatka schodowa", "klatce schodowej", "schodach"])

add_object(t_dict, "storeys", 1, ["parter", "parterze"])
add_object(t_dict, "storeys", 2, ["pierwsze", "pierwsze piętro", "pierwszym", "pierwszym piętrze"])
add_object(t_dict, "storeys", 3, ["drugie", "drugie piętro", "drugim", "drugim piętrze"])
add_object(t_dict, "storeys", 0, ["piwnica", "piwnicy"])

add_object(t_dict, "devices", "light", ["lampa", "lampę", "światło", "oświetlenie", "żarówka", "żarówkę"])

add_object(t_dict, "actions", "on", ["włączyć", "włącz", "załączyć", "załącz", "zapalić", "zapal", "zaświecić", "zaświeć"])
add_object(t_dict, "actions", "off", ["wyłączyć", "wyłącz", "zgasić", "zgaś"])
add_object(t_dict, "actions", "toggle", ["przełączyć", "przełącz", "zmienić", "zmień"])


generate_translations_JSON(t_dict)