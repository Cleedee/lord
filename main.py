from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from kivymd.app import MDApp

from lord.repository import encontra_decks

class MainWindow(Screen):
    pass

class ListaDecks(GridLayout):
    def __init__(self, **kwargs):
        # construtor
        # GridLayout(cols=1, spacing=10, size_hint_y=None)
        GridLayout.__init__(self, **kwargs)
        self.bind(minimum_height=self.setter('height'))
        decks = encontra_decks()
        for deck in decks:
            btn = Button(text=deck.name, size_hint_y=None, height=40)
            self.add_widget(btn)
        #self.add_widget(Button(text='Voltar', size_hint_y=None, height=40))


class DecksWindow(Screen):
    pass



class WindowManager(ScreenManager):
    pass

class LordApp(MDApp):

    def build(self):
        self.title = 'Lord'
        self.theme_cls.theme_style = "Dark"

    def mostra_mensagem(self):
        print(self.user_data_dir)


LordApp().run()
