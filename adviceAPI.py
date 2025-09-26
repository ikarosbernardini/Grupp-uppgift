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
        self.api_url = "https://api.adviceslip.com/advice"
        self.init_db()

     
    def init_db(self):
        """Initierar databas och tabell om de inte finns.

        Funktion:
            Använder sqlite3 för att skapa en databas och tabell."""
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
    
    def get_advice(self):
        """Hämtar visdomsord från API och returnerar dem.
        
        Funktion:
            Använder requests för att göra ett GET-anrop till API:et."""
        response = requests.get(self.api_url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        advice_id = data['slip']['id']
        advice_text = data['slip']['advice']
        print(f"Advice: {advice_text}")
        print("Do you want to save this advice? (y/n)")
        user_input = input().strip().lower()
        if user_input == 'y': 
            self.save_advice(advice_id, advice_text)
            print("Advice has been saved.")
        return #advice_id, advice_text
    
    def save_advice(self, advice_id, advice_text):
        """Sparar visdomsord i databasen om det inte redan finns.

        Funktion:
            Använder INSERT OR IGNORE för att undvika dubbletter baserat på advice_id."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT OR IGNORE INTO advice (advice_id, advice_text, date_added)
        VALUES (?, ?, ?)
        ''', (advice_id, advice_text, date_added))
        conn.commit()
        conn.close()
        print("Advice has been saved to the database if it was not already present.")
    
    
    def add_manually(self, advice_text: str):
        """
        Lägger till ett visdomsord manuellt i databasen.

        Funktion:
            Kontrollerar att texten inte är tom, sparar den med aktuell tid.
        """
        if not advice_text or not advice_text.strip():
            print("You must write something to add advice.")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        date_added = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO advice (advice_text, date_added) VALUES (?, ?)",
            (advice_text.strip(), date_added)
        )
        conn.commit()
        conn.close()
        print(f'You have now added: {advice_text}')

    def show_all(self):
        """
        Visar alla sparade visdomsord från databasen.

        Funktion:
             Hämtar och skriver ut alla visdomsord med tillhörande ID.
                Meddelar om databasen är tom.
        """

        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute("SELECT advice_id, advice_text FROM advice")
        rows= cursor.fetchall()
        conn.close()

        if rows:
            print("All the saved wise advice:")
            for row in rows:
                print(f"\t{row[1]}")

        else:
            print("You have nothing saved yet")

    def delete_advice(self):
        """
        Frågar användaren efter text och raderar motsvarande visdomsord.
        Funktion:
        Tar bort raden från databasen om den finns, annars meddelar användaren.
        """
        print("Type the advice you want to delete:")
        advice_text = input().strip()

        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute("SELECT advice_id FROM advice WHERE advice_text = ?", (advice_text,))
        row=cursor.fetchone()

        if row:
            advice_id=row[0]
            self.delete(advice_id)
        else:
            print(f'Could not find "{advice_text}" in the database.')

# def delete(self, advice_id: int):
#     """
#     Raderar ett visdomsord från databasen baserat på dess ID.
#     Funktion:
#     Tar bort raden från databasen och bekräftar borttagningen.
#     """
#     conn=sqlite3.connect(self.db_path)
#     cursor=conn.cursor()
#     cursor.execute("DELETE FROM advice WHERE advice_id= ?", (advice_id,))
#     conn.commit()
#     conn.close()
#     print(f'Advice id: {advice_id} is now deleted')

    def random_from_db(self):
        """
        Visar ett slumpmässigt visdomsord från databasen.
        Funktion:
        Hämtar alla visdomsord och väljer ett slumpmässigt.
        Meddelar om databasen är tom.
        """

        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute("SELECT advice_id, advice_text FROM advice")
        rows=cursor.fetchall()
        conn.close()

        if rows:
            random_row=random.choice(rows)
            print(f'Random choice: {random_row[1]}')
        else:
            print("There are nothing saved in db")

    def search_for_advice(self, keyword: str):
        """
        Söker efter visdomsord som innehåller ett specifikt nyckelord.
        Funktion:
         Visar alla visdomsord som innehåller sökordet.
        Meddelar om inget resultat hittas.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT advice_id, advice_text FROM advice WHERE advice_text LIKE ?",
            ('%' + keyword + '%',)
        )
        rows = cursor.fetchall()
        conn.close()

        if rows:
            print(f'Found the following advice containing "{keyword}":')
            for row in rows:
                print(f'\t {row[1]}')
        else:
            print(f'Advices containing "{keyword}" could not be found.')
