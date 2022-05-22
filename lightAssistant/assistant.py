# Stworzyłem plik json z konfiguracją asystenta, który trzyma słowniki z informacją, jakie słowa w języku
# naturalnym odpowiadają jakim komendą domu, np. kitchen to kuchnia, mirror to lustro. Używam go do dopasowywania
# słów. Wykonując dopasowywanie nie używam bezpośrednio słów otrzymanych z modułu STT. Najpierw eliminuje słowa
# krótsze niż 3 litery, aby nie zaciemniały dopasowywania. Następnie zamieniam słowa na rdzenie słowotwórcze,
# wykorzystując stemmer języka polskiego z biblioteki stempel. Dopiero tak przygotowane słowa dopasowuje
# biblioteką thefuzz. Dzięki temu dopasowanie, które uzyskuje jest stosunkowo dokładne.

import json
from thefuzz import process
from stempel import StempelStemmer
import speech_recognition as sr

stemmer = StempelStemmer.polimorf()

# klasa trzymająca dane urządzenia
class Device:
    def __init__(self, id, name, place, detailed_place):
        self.id = id
        self.place = place
        self.name = name
        self.detailed_place = detailed_place


with open('../configs/assistant_cfg.json', encoding='utf-8') as cfg:
    assistant_cfg = json.load(cfg)
    for subdict in assistant_cfg.values():
        for key, value in subdict.items():
            subdict[key] = list(map(stemmer.stem, value))

with open('../configs/home_cfg.json') as cfg:
    light_cfg = json.load(cfg)
    light_list = []
    for light in light_cfg['devices']:
        light_list.append(Device(light['id'], light['name'], light['place'], light['detailed_place']))

last_place = None
last_detailed_place = None


# funkcja sprawdzająca czy dopasowanie znalezione przez bibliotekę thefuzz jest wystarczająco dobre
# sprawdza na podstawie ratio dopasowania i stosunku do kolejnego dopasowania
def get_best_match(match_result):
    if match_result[0][1] >= 85:
        return match_result[0][0]

    if match_result[0][1] >= 65 and (len(match_result) < 2 or match_result[0][1] / match_result[1][1] > 1.3):
        return match_result[0][0]

    return None


# wyszukiwanie części komendy na podstawie dopasowanego słowa języka naturalnego
def find_symbol_by_word(word, source):
    if word is None:
        return None

    for key, value in source.items():
        if word in value:
            return key

    return None


# funkcja tworząca komendę na podstawie identyfikatorów miejsca i urządzenia
def create_command(place, detailed_place, device, action):
    global last_place
    global last_detailed_place
    if action is None:
        action = 'toggle'

    if place is None:
        if last_place is None:
            return 'Nieznane miejsce'
        place = last_place
        detailed_place = last_detailed_place

    last_place = place
    last_detailed_place = detailed_place

    if device is None:
        return 'Nieznana komenda'

    result_list = []
    if detailed_place is not None:
        found = False
        for light in light_list:
            if light.place == place and light.detailed_place == detailed_place and light.name == device:
                found = True
                break

        if not found:
            return 'Nie ma takiego urządzenia w podanym miejscu'
        result_list.append('/'.join(['cmd', place, detailed_place, device]) + ' ' + action)
    else:
        for light in light_list:
            if light.name == device and light.place == place:
                command = '/'.join(['cmd', place, light.detailed_place, device]) + ' ' + action
                result_list.append(command)

    if len(result_list) == 0:
        return 'Nieznana komenda'

    return result_list


# funkcja wykonująca dopasowanie i zwracająca komendę
def parse_text(text):
    places_list = [place for sublist in assistant_cfg['places'].values() for place in sublist]
    detailed_places_list = [place for sublist in assistant_cfg['detailed_places'].values() for place in sublist]
    devices_list = [device for sublist in assistant_cfg['devices'].values() for device in sublist]
    actions_list = [action for sublist in assistant_cfg['actions'].values() for action in sublist]
    storey_list = [storey for sublist in assistant_cfg['storeys'].values() for storey in sublist]

    text_list = text.split()
    text_list = list(filter(lambda word: len(word) > 2 or word.isnumeric(), text_list))
    text = ' '.join(list(map(stemmer.stem, text_list)))

    place = get_best_match(process.extract(text, places_list))
    detailed_place = get_best_match(process.extract(text, detailed_places_list))
    device = get_best_match(process.extract(text, devices_list))
    action = get_best_match(process.extract(text, actions_list))
    storey = get_best_match(process.extract(text, storey_list))
    print(storey);

    place_cmd = find_symbol_by_word(place, assistant_cfg['places'])
    detailed_place_cmd = find_symbol_by_word(detailed_place, assistant_cfg['detailed_places'])
    device_cmd = find_symbol_by_word(device, assistant_cfg['devices'])
    action_cmd = find_symbol_by_word(action, assistant_cfg['actions'])
    storey_cmd = find_symbol_by_word(storey, assistant_cfg['storeys'])

    return create_command(place_cmd, detailed_place_cmd, device_cmd, action_cmd)


stt = sr.Recognizer()
print('Napisz polecenie lub wciśnij enter i powiedz')
with open('polecenia.txt', 'w', encoding='utf-8') as command_file:
    while True:
        text = input('>> ')
        if len(text) > 0:
            print(text, file=command_file)
            print(parse_text(text))
        else:
            with sr.Microphone() as source:
                print('Powiedz polecenie')
                audio = stt.listen(source)
                try:
                    text = stt.recognize_google(audio, language='pl_PL')
                    print(text)
                    print(text, file=command_file)
                    print(parse_text(text))
                except sr.UnknownValueError:
                    print('Nie udało się rozpoznać')
                except sr.RequestError as e:
                    print('Error: ' + e)
