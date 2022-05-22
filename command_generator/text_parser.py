import json
from device import Device
from thefuzz import process
from stempel import StempelStemmer

class TextParser:
    def __init__(self):
        self.stemmer = StempelStemmer.polimorf()
        with open('assistant_cfg.json', encoding='utf-8') as cfg:
            self.assistant_cfg = json.load(cfg)
            for subdict in self.assistant_cfg.values():
                for key, value in subdict.items():
                    subdict[key] = list(map(self.stemmer.stem, value))

        with open('home_cfg.json', encoding='utf-8') as cfg:
            device_cfg = json.load(cfg)
            self.device_list = []
            for device in device_cfg['devices']:
                self.device_list.append(Device(device['name'],
                                               device['storey'],
                                               device['room'],
                                               device['detailed_place'],
                                               device['possible_actions']))

    def get_best_match(self, match_result):
        if match_result[0][1] >= 85:
            return match_result[0][0]

        if match_result[0][1] >= 65 and (len(match_result) < 2 or match_result[0][1] / match_result[1][1] > 1.3):
            return match_result[0][0]

        return None

    def find_symbol_by_word(self, word, source):
        if word is None:
            return None

        for key, value in source.items():
            if word in value:
                return key

        return None

    def parse_text(self, text):
        rooms_list = [room for sublist in self.assistant_cfg['rooms'].values() for room in sublist]
        detailed_places_list = [place for sublist in self.assistant_cfg['detailed_places'].values() for place in sublist]
        devices_list = [device for sublist in self.assistant_cfg['devices'].values() for device in sublist]
        actions_list = [action for sublist in self.assistant_cfg['actions'].values() for action in sublist]

        text_list = text.split()
        text_list = list(filter(lambda word: len(word) > 2, text_list))
        text = ' '.join(list(map(self.stemmer.stem, text_list)))

        room = self.get_best_match(process.extract(text, rooms_list))
        detailed_place = self.get_best_match(process.extract(text, detailed_places_list))
        device = self.get_best_match(process.extract(text, devices_list))
        action = self.get_best_match(process.extract(text, actions_list))

        room_cmd = self.find_symbol_by_word(room, self.assistant_cfg['rooms'])
        detailed_place_cmd = self.find_symbol_by_word(detailed_place, self.assistant_cfg['detailed_places'])
        device_cmd = self.find_symbol_by_word(device, self.assistant_cfg['devices'])
        action_cmd = self.find_symbol_by_word(action, self.assistant_cfg['actions'])

        return {
            'room': room_cmd,
            'detailed_place': detailed_place_cmd,
            'device': device_cmd,
            'action': action_cmd
        }
