import glob
import sqlite3
from datetime import datetime

from Score import Score


class Model:
    def __init__(self):
        self.__database = 'databases/hangman_words_ee.db'
        self.__image_files = glob.glob('images/*.png')
        self.__word = ''
        self.__letters = []
        self.__wrong_count = 0
        self.__correct_letters = []
        self.__wrong_letters = []

    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

    @property
    def word(self):
        return self.__word

    @property
    def correct_letters(self):
        return self.__correct_letters

    @property
    def wrong_letters(self):
        return self.__wrong_letters

    @property
    def wrong_count(self):
        return self.__wrong_count

    @database.setter
    def database(self, value):
        self.__database = value

    def read_scores_data(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT * FROM scores ORDER BY seconds;'
            cursor = connection.execute(sql)
            data = cursor.fetchall()
            result = []
            for row in data:
                result.append(Score(row[1], row[2], row[3], row[4], row[5]))

            return result
        except sqlite3.Error as error:
            print(f'Viga andmebaasiga {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()

    def new_game(self):
        self.__wrong_count = 0
        self.__letters = []
        self.__correct_letters = []
        self.__wrong_letters = []
        self.__word = self.random_word()
        self.__correct_letters = list("_" * len(self.__word))

    def random_word(self):
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            sql = 'SELECT word FROM words ORDER BY RANDOM() LIMIT 1;'
            cursor = connection.execute(sql)
            word = cursor.fetchone()[0]
            cursor.close()
            return word
        except sqlite3.Error as error:
            print(f'Viga andmebaasiga {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()

    def check_user_input(self, text):
        if text:
            guess = text[0].strip().lower()
            self.__letters.append(guess)
            word_letters = list(self.__word.lower())
            if guess in word_letters:
                for index, letter in enumerate(word_letters):
                    if guess == letter:
                        self.__correct_letters[index] = guess
            else:
                self.__wrong_count += 1
                if guess in self.__letters and guess not in self.__wrong_letters:
                    self.__wrong_letters.append(guess)

    def list_to_string(self, char_list):
        return ''.join(char_list)

    def save_score(self, name, game_time):
        name = name.strip()
        connection = None
        try:
            connection = sqlite3.connect(self.__database)
            today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sql = 'INSERT INTO scores (name, word, missing, seconds, date_time) VALUES (?, ?, ?, ?, ?)'
            connection.execute(sql, (
                name,
                self.__word,
                self.list_to_string(self.__wrong_letters),
                game_time,
                today
            ))
            connection.commit()
        except sqlite3.Error as error:
            print(f'Viga andmebaasiga {self.__database} ühendamisel: {error}')
        finally:
            if connection:
                connection.close()
