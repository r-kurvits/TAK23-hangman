from GameTime import GameTime
from Model import Model
from View import View


class Controller:
    def __init__(self, db_name=None):
        self.__model = Model()
        self.__view = View(self, self.__model)
        if db_name is not None:
            self.__model.database = db_name
        self.__game_time = GameTime(self.__view.lbl_time)

    def main(self):
        self.__view.main()

    def btn_scoreboard_click(self):
        window = self.__view.create_scoreboard_window()
        data = self.__model.read_scores_data()
        self.__view.draw_scoreboard(window, data)

    def buttons_no_game(self):
        self.__view.btn_new['state'] = 'normal'
        self.__view.btn_cancel['state'] = 'disabled'
        self.__view.btn_send['state'] = 'disabled'
        self.__view.char_input.delete(0, 'end')
        self.__view.char_input['state'] = 'disabled'

    def buttons_game(self):
        self.__view.btn_new['state'] = 'disabled'
        self.__view.btn_cancel['state'] = 'normal'
        self.__view.btn_send['state'] = 'normal'
        self.__view.char_input['state'] = 'normal'
        self.__view.char_input.focus()

    def btn_new_click(self):
        self.buttons_game()
        self.__view.change_image(0)
        # TODO Mängu pilt muuda esimeseks (ISESESIVALT TUNNIS KOHE)
        # TODO Seadista mudelis uus mäng. Juhuslik sõna andmebaasist vaja kätte saada
        # TODO Näita äraarvatavat sõna aga iga tähe asemel on allkriips. Kirjastiil on big_font
        # TODO Veateadete label muuda tekst "Vigased tähed:"
        self.__game_time.reset()
        self.__game_time.start()

    def btn_cancel_click(self):
        self.__game_time.stop()
        self.__view.change_image(-1)
        self.buttons_no_game()

    def btn_send_click(self):
        print(self.__view.char_input.get())
        # TODO Loe sisestus kastist saadud info ja suuna mudelisse infot töötlema
        # TODO Muuda teksti tulemus aknas (äraarvatav sõna)
        # TODO Muuda teksti Vigased tähed
        # TODO Tühjanda sisestus kast (ISESESIVALT TUNNIS KOHE)
        # TODO KUI on vigu tekkinud, muuda alati vigade tekst punaseks ning näita vastavalt vea numbrile õiget pilti
        # TODO on mäng läbi. MEETOD siin samas klassis.

    # TODO Kontrollida kas mäng on läbi.
    # TODO JAH puhul peata mänguaeg
    # TODO Seadista nupud õigeks (meetod juba siin klassis olemas)
    # TODO Küsi mängija nime (simpledialog.askstring)
    # TODO Saada sisestatud mängija nimi ja mängu aeg sekundites mudelisse kus toimub kogu muu tegevus kasutajanimega mänguaeg on muutujas self.__game_time.counter
