from tkinter import simpledialog

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
        self.__model.new_game()
        self.__view.lbl_result['text'] = self.__model.correct_letters
        self.__view.lbl_error['text'] = 'Vigased tähed'
        self.__view.lbl_error['fg'] = 'black'
        self.__game_time.reset()
        self.__game_time.start()

    def btn_cancel_click(self):
        self.__game_time.stop()
        self.__view.change_image(-1)
        self.buttons_no_game()
        self.__view.lbl_result['text'] = "Mängime!".upper()

    def btn_send_click(self):
        self.__model.check_user_input(self.__view.char_input.get())
        self.__view.char_input.delete(0, 'end')
        self.__view.lbl_result['text'] = " ".join(self.__model.correct_letters).upper()
        self.__view.lbl_error['text'] = f'Vigased tähed {self.__model.list_to_string(self.__model.wrong_letters)}'
        if self.__model.wrong_count > 0:
            self.__view.lbl_error['fg'] = 'red'
        self.__view.change_image(self.__model.wrong_count)
        self.game_over()

    def game_over(self):
        game_over = False
        game_guessed = False
        if self.__model.wrong_count == 11:
            game_over = True

        if self.__model.word.lower() == self.__model.list_to_string(self.__model.correct_letters):
            game_guessed = True
            game_over = True
        if game_over:
            self.__game_time.stop()
            self.buttons_no_game()
            if game_guessed:
                name = simpledialog.askstring('Mäng läbi', 'Mäng läbi! \nSisesta mängija nimi:')
                if name:
                    self.__model.save_score(name, self.__game_time.counter)
