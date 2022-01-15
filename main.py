# import requirements for the app
import logging 
logging.basicConfig(filename="logs.log", 
					format='%(asctime)s %(message)s',
					filemode='w') 
import kivy
from kivy.app import App
from kivy.config import ConfigParser
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.settings import SettingsWithTabbedPanel, SettingsWithSidebar
from kivy.logger import Logger
from kivy.lang import Builder

import pyttsx3
import random
import os

engine = pyttsx3.init()

builderString = """
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        Button:
            text: 'Menu'
            id: btn_menu
            size_hint: (0.4, 1)
            on_release: app.open_settings()
        Button:
            text: 'TTS'
            id: btn_tts
            size_hint: (0.3, 1)
        Button:
            text: 'EXIT'
            id: btn_exit
            size_hint: (0.3, 1)
            on_release: app.stop()
    TextInput:
        id: text_input
        size_hint: (1, 9.7)
        hint_text: "Type Here..."
"""

class settings:
    class MenuButton(Button):
        def __init__(self, parent_self, **kwargs):
            self.super_cls = parent_self
            super().__init__(**kwargs)
            self.text = "Settings"
            self.size_hint = (0.4, 1)
    
        def on_release(self):
            App.open_settings(self.super_cls)

    class DefaultSettingsPanel(SettingsWithTabbedPanel):
        """
        It is not usually necessary to create subclass of a settings panel. There
        are many built-in types that you can use out of the box
        (SettingsWithSidebar, SettingsWithSpinner etc.).
        You would only want to create a Settings subclass like this if you want to
        change the behavior or appearance of an existing Settings class.
        """
        def on_close(self):
            Logger.info("main.py: MySettingsWithTabbedPanel.on_close")

        def on_config_change(self, config, section, key, value):
            Logger.info(
                "main.py: MySettingsWithTabbedPanel.on_config_change: "
                "{0}, {1}, {2}, {3}".format(config, section, key, value))


class TTS(App):
    def build(self):
        """
        /////////////////////////////////////////////
        SETTING
        """
        self.settings_cls = settings.DefaultSettingsPanel

        # get the root from the builder string
        root = Builder.load_string(builderString)

        # adjust the bg and fg of the text area
        textArea = root.ids.text_input
        textArea.font_size = float(self.config.get('TTS Settings', 'font_size'))
        if self.config.get("TTS Settings", "dark_mode") == "1":
            textArea.background_color = (0,0,0)
            textArea.foreground_color = (255,255,255)
        else:
            textArea.background_color = (255,255,255)
            textArea.foreground_color = (0,0,0)

        # create a popup for the entry of the file name
        def tts(ins):
            # get the text from the text area which is at the root
            text = root.ids.text_input.text

            # get the paths in the current directory
            paths = [f for f in os.listdir(self.config.get('TTS Settings', 'path'))]
            # create a layout for the popup which says: saving the file, dont close the app
            # create a lable
            PopLayout = BoxLayout(orientation = 'vertical')
            lab1 = Label(text="Saving The Text As Audio! Please Dont Close The App If It Stops Responding.")
            PopLayout.add_widget(lab1)

            # create a layout for the popup that gets a file name
            main_layout = BoxLayout(orientation="vertical")
            sub_1 = BoxLayout()
            fname = TextInput(multiline = False, size_hint_x = 1, hint_text = "Type Here... the file will be saved as .mp3 file") # the input where the user inputs the file name
            sub_1.add_widget(fname)
            btn_ok = Button(text = "Please Enter The File Name To Save The Audio As!", disabled = True)
            btn_close = Button(text = "Cancel")

            # check the input with a live function
            def Entering(ins, val):
                if len(val) < 1: # if the user has entered nothing
                    btn_ok.text = "Please Enter The File Name To Save The Audio As!"
                    btn_ok.disabled = True
                    btn_ok.background_color = (255,0,0, 0)
                elif len(val) < 3: # if the file's name is shorter that 3 letters
                    btn_ok.disabled = True
                    btn_ok.text = "The Name Is Too Short!"
                    btn_ok.background_color = (255,0,0, 0)
                else:
                    if val+'.mp3' not in paths: # if the filename dose not exist
                        btn_ok.text = "Click Here To Save File As :'"+val+".mp3':"
                        btn_ok.background_color = (0,255,0, 0)
                        btn_ok.disabled = False
                    else: # if the file name exists
                        btn_ok.text = "File Named :'"+val+".mp3': Already Exists!"
                        btn_ok.disabled = True

            # bind the function for live filename check
            fname.bind(text = Entering)

            # the function called by the :save: button in the filename popup
            def get_fname(ins):
                # get the file's name, and the text in root
                filename = fname.text
                text = textArea.text if len(textArea.text.strip()) > 0 else "THIS APP IS A PRODUCT OF SPRINGREEN, hope you liked this app."

                # create a popup to display saving process
                pop = Popup(
                    title="TTS POPUP",
                    content=PopLayout,
                    auto_dismiss=False
                )
                pop1298349.dismiss()
                pop.open()

                # prepare the voice engine and save the file
                voices = engine.getProperty('voices')
                engine.setProperty('rate', self.config.get('TTS Settings', 'speech_rate'))
                engine.setProperty('voice', voices[int(self.config.get('TTS Settings', 'voice_gender'))].id)
                path = self.config.get('TTS Settings', 'path')
                path = path if os.path.isdir(path) else os.path.dirname(path)
                engine.save_to_file(str(text), f'{path}/{filename}.mp3')
                engine.runAndWait()
                pop.dismiss()

            # bind the :save: function with the button on the first popup
            btn_ok.bind(on_release = get_fname)

            # add all the widgets to the layout and put the layout in the 1st popup
            main_layout.add_widget(sub_1)
            main_layout.add_widget(btn_ok)
            main_layout.add_widget(btn_close)
            pop1298349 = Popup(title = "Save Audio As?", content = main_layout, auto_dismiss=False)
            pop1298349.open()
            btn_close.bind(on_release = pop1298349.dismiss)

        # bind the first popup's function with the :tts: button in the root
        root.ids.btn_tts.bind(on_release= tts)

        # return the root to display it in the main screen
        return root

    # set the settings from the tts.ini file
    def build_config(self, config: ConfigParser):
        # open the tts.ini file, read all the stuffs and close it
        config_file = open("tts.ini", "r")
        lines = [line for line in config_file.readlines()]
        config_file.close()
        speech_rate = int(lines[2].split("=")[1].strip())
        font_size = int(lines[3].split("=")[1].strip())
        dark_mode = int(lines[4].split("=")[1].strip())
        
        # set defaults for that
        config.setdefaults('TTS Settings',
            {
                "default_settings": 0,
                "speech_rate": speech_rate,
                "font_size": font_size,
                "dark_mode": 0,
                "voice_gender": 0,
                "path": "/"
            }
        )

    # create a settings panel for the one of tts
    def build_settings(self, setting: settings.DefaultSettingsPanel):
        setting.add_json_panel("TTS Settings", self.config, "settings.json")        
    
    # check the changes in the settings
    def on_config_change(self, config: ConfigParser, section, key, value):
        Logger.info(f"main.py: App.on_config_change: Config-{config}, Section-{section}, Key-{key}, Value-{value}")
        if section == "TTS Settings":
            if key == "default_settings":
                if value == "1":
                    config.setall('TTS Settings', 
                        {
                            "default_settings": 0,
                            "speech_rate": 120,
                            "font_size": 20,
                            "dark_mode": 0,
                            "voince_gender": 0
                        }
                    )
                    ids = self.root.ids
                    ids.text_input.font_size = 20
                    self.root.ids.text_input.background_color = (255,255,255)
                    self.root.ids.text_input.foreground_color = (0,0,0)
                    print(config.write())
                    config.update_config('tts.ini', True)

            elif key == "dark_mode":
                if value == "1":
                    self.root.ids.text_input.background_color = (0,0,0)
                    self.root.ids.text_input.foreground_color = (255,255,255)
                if value == "0":
                    self.root.ids.text_input.background_color = (255,255,255)
                    self.root.ids.text_input.foreground_color = (0,0,0)
        
            elif key == "font_size":
                self.root.ids.text_input.font_size = float(value)
            
            elif key == "path":
                ___path = value
                ___path = ___path if os.path.isdir(___path) else os.path.dirname(___path)
                self.config.set("TTS Settings", "path", ___path)
                print(config.write())
                config.update_config('tts.ini', True)
                
# run the main app
TTS().run()