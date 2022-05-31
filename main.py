from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from voice_assistant_module.voice_assistant import VoiceAssistant
from mqtt.publisher import Publisher
from command_generator.text_parser import TextParser
from command_generator.commands_generator import CommandsGenerator
import time

publisher = Publisher()
text_parser = TextParser('configs/assistant_cfg.json')
command_generator = CommandsGenerator('configs/home_cfg.json')
voice_assistant = VoiceAssistant()


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.popup = Popup(title='Słucham',
                           content=Label(text='Słucham...', font_size='20sp'),
                           size_hint=(None, None), size=(200, 200))
        self.title_label = Label(text='Asystent domowy',
                                 color=(0, 0, 0),
                                 font_size='40sp',
                                 size_hint=(1, 0.3))
        self.listen_button = Button(text='Naciśnij i mów',
                                    size_hint=(0.4, 0.1),
                                    font_size='20sp',
                                    pos_hint={'center_x': 0.5},
                                    on_press=lambda instance: self.popup.open(),
                                    on_release=lambda instance: self.listen_action())
        self.command_input_box = BoxLayout(orientation='horizontal',
                                           size_hint=(0.7, 0.1),
                                           spacing=10,
                                           pos_hint={'center_x': 0.5})
        self.command_input = TextInput(multiline=False,
                                       hint_text='Wpisz polecenie i naciśnij przycisk',
                                       font_size='17sp')
        self.command_submit = Button(text='Wyślij polecenie',
                                     font_size='20sp',
                                     on_press=lambda instance: self.handle_command(self.command_input.text))
        self.command_input_box.add_widget(self.command_input)
        self.command_input_box.add_widget(self.command_submit)

        self.add_widget(self.title_label)
        self.add_widget(self.listen_button)
        self.add_widget(self.command_input_box)

    def listen_action(self):
        command = voice_assistant.listen()
        self.handle_command(command)
        self.popup.dismiss()

    def handle_command(self, text):
        parsed = text_parser.parse_text(text)
        error_msg, command_list = command_generator.get_commands(parsed)
        print(command_list)
        if len(error_msg) == 0:
            for cmd in command_list:
                topic, payload = cmd.split(maxsplit=1)
                publisher.publish(topic, payload)
            voice_assistant.speak('Wysłano komendy')
        else:
            voice_assistant.speak(error_msg)


class HomeAssistant(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)
        return MainLayout(orientation='vertical',
                          spacing=20,
                          padding=80)


HomeAssistant().run()
