from voice_assistant_module.voice_assistant import VoiceAssistant
from mqtt.publisher import Publisher
from command_generator.text_parser import TextParser
from command_generator.commands_generator import CommandsGenerator

# publisher = Publisher()
text_parser = TextParser('configs/assistant_cfg.json')
command_generator = CommandsGenerator('Commands_translator_task/home_JSON.txt')
voice_assistant = VoiceAssistant()

print('Podaj polecenie lub wciśnij enter, aby powiedzieć')
while True:
    text = input('>> ')
    if len(text) == 0:
        print('Słucham...')
        text = voice_assistant.listen()

    print(command_generator.get_commands(text_parser.parse_text(text)))
