#TO-DO: Dubbelkolla att dessa funktioner är korrekta, funkar och om fler behövs.
#Funktioner
#   Hämta visdomsord
#   Radera
#   Spara i databas?
#       J/N?
#   Söka
#   Läs upp alla sparade
#   Slumpa fram visdomsord från databas

import sqlite3
import random



class Visdom:

    def init(self, db_path: str='advice.db') -> None:
        self.db_path=db_path
        self._skapa_tabell()


    def show_visdom(self):
        conn=sqlite3.connect(self.db_path)
        c=conn.cursor()
        c.execute('Select advice_text from advice')
    for row in c.fetchall():
        print(row[0]) #va bara in siffran 0 som exempel, ni kan ändra
        conn.close()


    def random(self):
        conn=sqlite3.connect(self.db_path)
        c.conn.cursor()
        c.execute('select advice_text from advice')
        rader= [rad[0] for rad in c.fetchall()]
        conn.close()
        if rader:
            print(random.choice(rader))
        else:
            print('No result')

    def delete(self, text):
        conn=sqlite3.connect(self.db_path)
        c=conn.cursor()
        c.execute('Delete from advice ' , (text,))
        conn.commit()
        conn.close()
        print(f'We have now deleted: {text}')

    def add(self, text):
        conn=sqlite3.connect(self.db_path)
        c=conn.cursor()
        c.execute('insert into advice', (text))
        conn.commit()
        conn.close()
        print(f'We have now added: {text}')