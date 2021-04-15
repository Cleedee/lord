from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from kivymd.app import MDApp

KV = '''
WindowManager:
    MainWindow:
    DecksWindow:

<MainWindow>:
    name: "main"
    BoxLayout:
        orientation: "vertical"

        MDFillRoundFlatButton:
            text: "Decks"
            theme_text_color: "Custom"
            text_color: 0, 0, 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.5}
            on_release:
                app.root.current = 'decks_window'
                root.manager.transition.direction = "left"
        MDFillRoundFlatButton:
            text: "Scenarios"
            theme_text_color: "Custom"
            text_color: 0, 0, 1, 1
            pos_hint: {"center_x": 0.5, "center_y": 0.5}


<DecksWindow>:
    name: "decks_window"

    Button:
        text: "Go Back"
        on_release:
            app.root.current = "main"
            root.manager.transition.direction = "right"
'''

class MainWindow(Screen):
    pass


class DecksWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass

class Example(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)

    def mostra_mensagem(self):
        print(self.user_data_dir)


Example().run()
