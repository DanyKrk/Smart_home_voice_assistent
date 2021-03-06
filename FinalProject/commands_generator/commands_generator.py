import json

# Klasa obiektów, która zamienia (metodą get_commands) słownik polecenia, zwracany prze text_parser, na listę poleceń,
# oraz komunikat ewentualnego błędu (np. kiedy podane urządzenie nie istnieje).
# polecenia są postaci: cmd/piętro/pokój/szczegółowe_miejsce/urządzenie akcja
class CommandsGenerator:
    def __init__(self, home_cfg_path):
        with open(home_cfg_path, encoding='utf-8') as cfg:
            self.home_dict = json.load(cfg)
            self.rooms_list = self.create_rooms_list()
            self.storeys_dict = self.create_storeys_dict()

    # Tworzy listę pomieszczeń występujących w home_cfg
    def create_rooms_list(self):
        rooms_list = []
        for device_dict in self.home_dict["devices"]:
            room = device_dict["room"]
            if room not in rooms_list:
                rooms_list.append(room)
        return rooms_list

    # Tworzy słownik w którym kluczami są piętra, a wartościami są listy pomieszczeń znajdujących się na danym piętrze
    def create_storeys_dict(self):
        storeys_dict = {}
        for device_dict in self.home_dict["devices"]:
            room = device_dict["room"]
            storey = device_dict["storey"]
            if storey not in storeys_dict.keys():
                storeys_dict[storey] = []
            if room not in storeys_dict[storey]:
                storeys_dict[storey].append(room)
        return storeys_dict


    # Tworzenie komendy na podstawie słownika opisującego urządzenie i akcji
    def device_command(self, action, device_dict):
        tmp_command = "cmd/"
        if device_dict["storey"] is not None:
            tmp_command += device_dict["storey"]
        if device_dict["room"] is not None:
            tmp_command = tmp_command + "/" + device_dict["room"]
        if device_dict["detailed_place"] is not None:
            tmp_command = tmp_command + "/" + device_dict["detailed_place"]
        if device_dict["name"] is not None:
            tmp_command += "/" + device_dict["name"]
        split_action = action.split()[0]
        if split_action != "toggle":
            if split_action not in device_dict["possible_actions"]:
                print("Nie ma akcji: ", split_action, "dla urządzenia: ", device_dict["name"])
                # exit(1)
        tmp_command = tmp_command + " " + action
        return tmp_command

    # Sprawdzenie czy pokój istnieje
    def validate_room(self, room):
        if room not in self.rooms_list:
            print("Nie ma pomieszczenia: ", room)
            return False
        return True

    # Sprawdzenie czy urządzenie jest w pokoju
    def validate_device_in_room(self, room, device):
        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] == device and device_dict["room"] == room:
                return True
        print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room)
        return False

    # Sprawdzenie, czy istnieje urządzenie w danym miejscu
    def validate_detailed_place(self, room, device, detailed_place):
        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] == device and device_dict["room"] == room and \
                    device_dict["detailed_place"] == detailed_place:
                return True
        print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room, " w miejscu: ", detailed_place)
        return False

    # Sprawdzenie, czy na urządzeniu w danym miejscu można wykonać daną akcję
    def validate_action(self, room, device, detailed_place, action):
        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] == device and device_dict["room"] == room and device_dict[
                "detailed_place"] == detailed_place \
                    and action in device_dict["possible_actions"]:
                return True
        print("Nie ma urządzenia: ", device, " w pomieszczeniu: ", room, " w miejscu: ", detailed_place,
              "o możliwej akcji: ", action)
        return False

    # Lista urządzeń w danym pokoju
    def devices_in_room(self, room):
        devices = []
        for device_dict in self.home_dict["devices"]:
            if device_dict["room"] == room:
                devices.append(device_dict)
        return devices

    # lista urządzeń na danym piętrze
    def devices_in_storey(self, storey):
        devices = []
        for room in self.storeys_dict[storey]:
            devices += self.devices_in_room(room)
        return devices

    # Urządzenia w danym miejscu (np nad szafkami)
    def devices_with_detailed_place(self, detailed_place):
        devices = []
        for device_dict in self.home_dict["devices"]:
            if device_dict["detailed_place"] == detailed_place:
                devices.append(device_dict)
        return devices

    # zwraca listę zawierającą wszystkie słowniki opisujące urządzenia o danej nazwie
    def all_devices(self, name):
        devices = []
        for device_dict in self.home_dict["devices"]:
            if name is not None and device_dict["name"] == None:
                devices.append(device_dict)
        return devices

    # Sprawdza, czy dane piętro istnieje (jest w home_cfg)
    def validate_storey(self, storey):
        if storey in self.storeys_dict.keys():
            return True
        return False

    # Sprawdza, czy dane pomieszczenie znajduje się na którymś z pięter wyszególnionych w storeys
    def room_is_in_storeys(self, room, storeys):
        for storey in storeys:
            if room in self.storeys_dict[storey]:
                return True
        return False

    # Zwraca komunikat błędu, oraz listę słowników opisujących urządzenia. Urządzenia są wybierane na podstawie podanego
    # (lub nie) piętra, pomieszczena, szegółowego miejsca, nazwy urządzenia i akcji. Jeżeli nie podano piętra, to jest ono dowolne.
    # Jeżeli nie podano pomieszcenia, to jest ono dowolne (w ramach wyspecyfiowanych pięter). Jeżeli nie jest
    # podane szczegółowe miejsce urządzenia w pomieszczeniu, to brane są wszystkie urządzenia o danej nazwie znajdujące
    # się w danym pomieszceniu. Jeżeli znalezione zostanie conajmniej jedno urządzenie spełniające kryteria,
    # komunikat błędu jest pustym ciągiem znaków. W przeciwnym razie zwracany jest odpowiedni komunikat w zależności
    # od sytuacji.
    def get_device_dicts(self, storey, room, detailed_place, device, action):
        device_dicts = []
        error_message = ""

        storeys = []
        if storey is not None:
            if self.validate_storey(storey):
                storeys.append(storey)
            else:
                error_message = "Nie ma piętra: " + storey
                return error_message, device_dicts
        else:
            for home_storey in self.storeys_dict.keys():
                storeys.append(home_storey)

        rooms = []
        if room is not None:
            if self.room_is_in_storeys(room, storeys):
                rooms.append(room)
            else:
                error_message = "Nie ma pomieszczenia: " + room + " na piętrach: " + str(storeys)
                return error_message, device_dicts
        else:
            for storey, storey_rooms in self.storeys_dict.items():
                if storey in storeys:
                    rooms += storey_rooms

        for device_dict in self.home_dict["devices"]:
            if device_dict["name"] != device:
                continue
            if device_dict["room"] not in rooms:
                continue
            if detailed_place is not None and device_dict["detailed_place"] != detailed_place:
                continue
            split_action = action.split()[0]
            if split_action not in device_dict["possible_actions"]:
                continue
            device_dicts.append(device_dict)

        if len(device_dicts) == 0:
            if device is None:
                error_message = "Nie podano urządzenia"
            else:
                error_message = "Nie ma podanego urządzenia w podanych miejscach lub o podanej akcji"
        return error_message, device_dicts

    # Generowanie wyjściowych poleceń (zwracana jest lista). Domyślną akcją jest "toggle"
    def get_commands(self, command_dict):
        storey = command_dict["storey"]
        room = command_dict["room"]
        device = command_dict["device"]
        detailed_place = command_dict["detailed_place"]
        action = command_dict["action"]

        if action is None:
            action = "toggle"

        error_message, device_dicts = self.get_device_dicts(storey, room, detailed_place, device, action)

        commands = []
        for device_dict in device_dicts:
            commands.append(self.device_command(action, device_dict))

        return error_message, commands