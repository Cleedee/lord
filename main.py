from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from kivymd.app import MDApp

from lord.repository import encontra_decks, encontra_deck_por_nome

class MainWindow(Screen):
    pass

class DecksWindow(Screen):
    pass

class DeckWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass

class ListaDecks(GridLayout):
    def __init__(self, **kwargs):
        GridLayout.__init__(self, **kwargs)
        self.bind(minimum_height=self.setter('height'))
        decks = encontra_decks()
        for deck in decks:
            btn = Button(text=deck.name, size_hint_y=None, height=40, on_release = self.para_os_decks)
            self.add_widget(btn)

    def para_os_decks(self, instance):
        app = MDApp.get_running_app()
        app.root.transition = SlideTransition(direction='left')
        app.root.current = 'deck_window'
        deck = encontra_deck_por_nome(instance.text)
        app.deck_atual = deck
        print(deck.starting_threat)

class LordApp(MDApp):

    def __init__(self, **kwargs):
        MDApp.__init__(self, **kwargs)
        self.deck_atual = None

    def build(self):
        self.title = 'Lord'
        self.theme_cls.theme_style = "Dark"

    def mostra_mensagem(self):
        print(self.user_data_dir)


LordApp().run()
