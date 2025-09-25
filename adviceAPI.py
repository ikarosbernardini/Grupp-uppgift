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
from datetime import datetime
import requests



class AdviceApp:
    def __init__(self, db_path="advice.db"):
        self.db_path = db_path
        self.api_url = 'https://api.adviceslip.com/advice'
        self.init_db()

    # Initierar databas och tabell om de inte finns
    def init_db(self):
        """Creates the database and the advice table if they do not exist."""
        conn = sqlite3.connect("advice.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS advice (
            advice_id INTEGER PRIMARY KEY,
            advice_text TEXT NOT NULL,
            date_added TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    #Hämtar visdomsord från API och returnerar dem
    def get_advice(self):
        response = requests.get(self.api_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        advice_id = data['slip']['id']
        advice_text = data['slip']['advice']
        print(f"Advice: {advice_text}")
        return advice_id, advice_text
    
    # Sparar visdomsord i databasen om det inte redan finns
    def save_advice(self, advice_id, advice_text):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT OR IGNORE INTO advice (advice_id, advice_text, date_added)
        VALUES (?, ?, ?)
        ''', (advice_id, advice_text, date_added))
        conn.commit()
        conn.close()
        print("Advice has been saved to the database if it was not already present.")
    
    # ISABELLA testa att utveckla följande funktioner om du vill.
"""
    # Visar alla sparade visdomsord
    def list_saved_advice(self):
        pass

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
        """