import glob
import sqlite3

from Score import Score


class Model:
    def __init__(self):
        self.__database = 'databases/hangman_words_ee.db'
        self.__image_files = glob.glob('images/*.png')

        # TODO juhuslik sõna,
        # TODO kõik sisestatud tähed
        # TODO vigade lugeja (s.h. pildi id)
        # TODO kasutaja leitud tähed (visuaal muidu on seal allkriips _)

    @property
    def database(self):
        return self.__database

    @property
    def image_files(self):
        return self.__image_files

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

    # TODO Meetod mis seadistab uue mängu
    # TODO Seadistab uue sõna äraarvamiseks
    # TODO Seadistab mõningate muutujate algväärtused (vaata ___init__ kolme viimast TODO. Neljas muutuja on eelmine rida)
    # TODO Seadistab ühe muutuja nii et iga tähe asemel paneb allkiriipsu mida näidata aknas äraarvatavas sõnas (LIST)

    # TODO Meetod mis seadistab juhusliku sõna muutujasse
    # TODO Teeb andmebaasi ühenduse ja pärib sealt ühe juhusliku sõna ning kirjutab selle muutujasse

    # TODO kasutaja siestuse kontroll (Vaata COntrolleris btn_send_click esimest TODO)
    # TODO Kui on midagi sisestatud võta sisestusest esimene märk (me saame sisestada pika teksti aga esimene täht on oluline!)
    # TODO Kui täht on otsitavas sõnas, siis asneda tulemuses allkriips õige tähega.
    # TODO kui tähte polnud, siis vigade arv kasvab +1 ning lisa vigane täht eraldi listi

    # TODO Meetod mis tagastab vigaste tähtede listi asemel tulemuse stringina. ['A', 'B', 'C'] => A, B, C

    # TODO Meetod mis lisab mängija ja tema aja andmebaasi (Vaata Controlleris viimast TODO rida)
    # TODO Võtab hetke/jooksva aja kujul AAAA-KK-PP TT:MM:SS (Y-m-d H:M:S)
    # TODO Kui kasutaja sisestas nime, siis eemalda algusest ja lõpust tühikud
    # TODO Tee andmebaasi ühendus ja lisa kirje tabelisse scores. Salvesta andmed tabelis ja sulge ühendus.
