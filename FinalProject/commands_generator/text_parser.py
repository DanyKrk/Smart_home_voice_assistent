import json
from thefuzz import process
from stempel import StempelStemmer

class TextParser:
    def __init__(self, config_path):
        self.stemmer = StempelStemmer.polimorf()
        with open(config_path, encoding='utf-8') as cfg:
            self.assistant_cfg = json.load(cfg)
            for subdict in self.assistant_cfg.values():
                for key, value in subdict.items():
                    subdict[key] = list(map(self.stemmer.stem, value))

    def get_best_match(self, word_list, ref_list):
        for word in word_list:
            result = process.extract(word, ref_list)
            if result[0][1] >= 80:
                return result[0][0]

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
        storey_list = [storey for sublist in self.assistant_cfg['storeys'].values() for storey in sublist]
        storey_number_list = [number for sublist in self.assistant_cfg['storey_numbers'].values() for number in sublist]

        text = ''.join(filter(lambda sign: sign != '%', text))
        text_list = text.split()
        text_list = list(filter(lambda word: len(word) > 2 or word.isnumeric(), text_list))
        text_list = list(map(self.stemmer.stem, text_list))

        room = self.get_best_match(text_list, rooms_list)
        detailed_place = self.get_best_match(text_list, detailed_places_list)
        device = self.get_best_match(text_list, devices_list)
        action = self.get_best_match(text_list, actions_list)
        storey = self.get_best_match(text_list, storey_list)
        storey_number = self.get_best_match(text_list, storey_number_list)

        room_cmd = self.find_symbol_by_word(room, self.assistant_cfg['rooms'])
        detailed_place_cmd = self.find_symbol_by_word(detailed_place, self.assistant_cfg['detailed_places'])
        device_cmd = self.find_symbol_by_word(device, self.assistant_cfg['devices'])
        action_cmd = self.find_symbol_by_word(action, self.assistant_cfg['actions'])
        storey_cmd = self.find_symbol_by_word(storey, self.assistant_cfg['storeys'])
        storey_number_cmd = self.find_symbol_by_word(storey_number, self.assistant_cfg['storey_numbers'])

        if storey_cmd != 'floor_0' and storey_cmd is not None and storey_number_cmd is not None:
            storey_cmd = storey_cmd + storey_number_cmd
        elif storey_cmd != 'floor_0':
            storey_cmd = None

        if action_cmd == 'set':
            numbers = list(map(str, range(0, 101)))
            number = None
            for word in text.split():
                if word in numbers:
                    number = word
                    action_cmd += ' ' + number
                    break
            if number is None:
                action_cmd = None

        return {
            'room': room_cmd,
            'detailed_place': detailed_place_cmd,
            'device': device_cmd,
            'action': action_cmd,
            'storey': storey_cmd
        }
