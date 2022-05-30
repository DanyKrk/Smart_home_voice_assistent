from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from voice_assistant_module.voice_assistant import VoiceAssistant
from mqtt.publisher import Publisher
from command_generator.text_parser import TextParser
from command_generator.commands_generator import CommandsGenerator


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.info_label = Label(text='Asystent domowy',
                                color=(0, 0, 0,),
                                font_size='40sp',
                                size_hint=(1, 0.3))
        self.listen_button = Button(text='Naciśnij i mów',
                                    size_hint=(0.4, 0.1),
                                    font_size='20sp',
                                    pos_hint={'center_x': 0.5})
        self.command_input_box = BoxLayout(orientation='horizontal',
                                           size_hint=(0.7, 0.1),
                                           spacing=10,
                                           pos_hint={'center_x': 0.5})
        self.command_input = TextInput(multiline=False,
                                       hint_text='Wpisz polecenie i naciśnij przycisk',
                                       font_size='17sp')
        self.command_submit = Button(text='Wyślij polecenie',
                                     font_size='20sp')
        self.command_input_box.add_widget(self.command_input)
        self.command_input_box.add_widget(self.command_submit)

        self.add_widget(self.info_label)
        self.add_widget(self.listen_button)
        self.add_widget(self.command_input_box)


class HomeAssistant(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainLayout(orientation='vertical',
                          spacing=20,
                          padding=80)


# print('Podaj polecenie lub wciśnij enter, aby powiedzieć')
# while True:
#     text = input('>> ')
#     if len(text) == 0:
#         text = voice_assistant.listen()
#
#     command_list = command_generator.get_commands(text_parser.parse_text(text))
#     for cmd in command_list:
#         topic, payload = cmd.split()
#         publisher.publish(topic, payload)

# publisher = Publisher()
# text_parser = TextParser('configs/assistant_cfg.json')
# command_generator = CommandsGenerator('configs/home_cfg.json')
# voice_assistant = VoiceAssistant()

HomeAssistant().run()
