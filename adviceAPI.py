import sqlite3
import random
from datetime import datetime
import requests



class AdviceApp:
    def __init__(self, db_path: str = "advice.db"):
        """Initierar AdviceApp med databasväg och API URL.
        Funktion:
            Skapar en SQLite-databas och tabell om de inte finns."""

        self.db_path: str = db_path
        self.api_url: str = "https://api.adviceslip.com/advice"
        self.init_db()
     
    def init_db(self):
        """Initierar databas och tabell om de inte finns.

        Funktion:
            Använder sqlite3 för att skapa en databas och tabell."""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS advice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            advice_id INTEGER UNIQUE,
            advice_text TEXT NOT NULL,
            date_added TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()
    
    def get_advice(self) -> tuple[int, str] | None: 
        """Hämtar visdomsord från API och returnerar dem.
        
        Funktion:
            Använder requests för att göra ett GET-anrop till API:et.
            Returnerar i tuple, (ID=int och text=str) eller None om man inte sparar något."""

        response = requests.get(self.api_url)
        response.raise_for_status()  # Skickar ett errormeddelande i fall anropet misslyckas
        data = response.json()
        advice_id: int = data['slip']['id']
        advice_text: str = data['slip']['advice']
        print(f"Advice: {advice_text}")
        print("Do you want to save this advice? (y/n)")
        user_input = input().strip().lower()
        if user_input == 'y': 
            row_id = self.save_advice(advice_id, advice_text)
            print(f"Advice has been saved as entry #{row_id} in the database.")
        return 
    
    def save_advice(self, advice_id: int, advice_text: str) -> int:
        """Sparar visdomsord i databasen om det inte redan finns.

        Funktion:
            Använder INSERT OR IGNORE för att undvika dubbletter baserat på advice_id."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        date_added: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute('''
        INSERT OR IGNORE INTO advice (advice_id, advice_text, date_added)
        VALUES (?, ?, ?)
        ''', (advice_id, advice_text, date_added))
        conn.commit()

        cursor.execute('SELECT id FROM advice WHERE advice_id = ?', (advice_id,))
        row_id: int = cursor.fetchone()[0]  # Hämtar det interna ID:t för raden
        conn.close()
        return row_id

    def add_advice_manually(self, advice_text: str) -> None:
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
        date_added: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "INSERT INTO advice (advice_id, advice_text, date_added) VALUES (?, ?, ?)",
            (None, advice_text.strip(), date_added)
        )
        conn.commit()
        conn.close()
        print(f'You have now added: {advice_text.strip()}')

    def show_all_advice(self) -> None:
        """
        Visar alla sparade visdomsord från databasen.

        Funktion:
             Hämtar och skriver ut alla visdomsord med tillhörande ID.
                Meddelar om databasen är tom.
        """

        conn=sqlite3.connect(self.db_path)
        cursor=conn.cursor()
        cursor.execute("SELECT id, advice_text, date_added FROM advice ORDER BY id ASC")
        rows: list[tuple[int, str, str]] = cursor.fetchall()  #Vi hamtar lista med tuples: ID, advice_text, date_added
        conn.close()

        if rows:
            print("All the saved wise advice:")
            valid_ids = []
            for row in rows:
                print(f"\t{row[0]}. Added on {row[2]}: {row[1]}")
                valid_ids.append(row[0])  #Lägger till ID i listan
            return valid_ids  #Returnerar listan med ID:n

        else:
            print("You have nothing saved yet")

    def delete_advice(self) -> None:
        """
        Raderar ett visdomsord baserat på användarens valda ID.
        Funktion:
            Visar alla sparade råd med ID, ber användaren ange ett ID att radera.
            Kontrollerar att ID:t är giltigt innan radering.
            Uppdaterar nummerordningen på råd efter radering.
        """

        # Skriv ut alla sparade råd med respektive ID
        valid_ids = self.show_all_advice()
        if not valid_ids:
            return  # Ingen att radera

        while True:
            try:
                advice_id = int(input("\nType the ID of the advice you want to delete: ").strip())
            except ValueError:
                print(" Please enter a valid number.")
                continue

            if advice_id not in valid_ids:
                print(" ID not found. Please enter a valid ID from the list.")
                continue

            # Ta bort rådet
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM advice WHERE id = ?", (advice_id,))
            conn.commit()
            conn.close()
            print(f" Advice with ID {advice_id} has been deleted.")
            self.resequence_advice_ids()  # Uppdatera nummerordningen på råd
            break

    def resequence_advice_ids(self) -> None:
        """
        Uppdaterar nummerordningen på sparade råd så att första rådet = 1, andra = 2 osv.
        Funktion:
            Hämtar alla råd sorterade på id, raderar tabellen, och skriver tillbaka dem
            med sekventiella id:n som börjar på 1.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Hämta alla råd sorterade på id
        cursor.execute("SELECT advice_id, advice_text, date_added FROM advice ORDER BY id ASC")
        rows = cursor.fetchall()

        # Temporärt behåll alla råd
        temp_advice = [(advice_id, advice_text, date_added) for advice_id, advice_text, date_added in rows]

        # Radera allt i tabellen
        cursor.execute("DELETE FROM advice")
        conn.commit()

        # Reset autoincrement i SQLite (så att id börjar på 1)
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='advice'")
        conn.commit()

        # Skriv tillbaka alla råd
        for advice in temp_advice:
            advice_id, advice_text, date_added = advice
            cursor.execute(
                "INSERT INTO advice (advice_id, advice_text, date_added) VALUES (?, ?, ?)",
                (advice_id, advice_text, date_added)
            )
        conn.commit()
        conn.close()
        print("All advice IDs have been resequenced starting from 1.")

    def random_advice_from_db(self) -> None:
        """
        Visar ett slumpmässigt visdomsord från databasen.
        Funktion:
        Hämtar alla visdomsord (API och manuella) och väljer ett slumpmässigt.
        Meddelar om databasen är tom.
        """

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, advice_text FROM advice")
        rows: list[tuple[int, str]] = cursor.fetchall()
        conn.close()

        if rows:
            random_row: tuple[int, str] = random.choice(rows)
            print(f'Random advice (ID: {random_row[0]}): {random_row[1]}')
        else:
            print("There are nothing saved in the database.")

    def search_for_advice(self, keyword: str) -> None:
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
            ('%' + keyword + '%',)      #Lägger till % wildcard före och efter keyword för att matcha var som helst i texten
        )
        rows: list[tuple[int, str]] = cursor.fetchall()
        conn.close()

        if rows:
            print(f'Found the following advice containing "{keyword}":')
            for row in rows:
                print(f'\t {row[1]}')
        else:
            print(f'Advices containing "{keyword}" could not be found.')
