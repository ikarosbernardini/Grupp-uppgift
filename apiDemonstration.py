#TO-DO: Dubbelkolla type hinting 
#TO-DO: Kommentera koden
#TO-DO: Implementera "with" vid databasanslutning
"""

import requests
import sqlite3
import datetime

# --- Steg 1: Hämta slumpmässigt råd ---
url = 'https://api.adviceslip.com/advice' 
response = requests.get(url) #TO-DO: Testa att implementera (url, timeout=5) för att undvika att fastna
if response.status_code != 200:
    raise Exception(f"API request failed with status code {response.status_code}")

data = response.json()
advice_id = data['slip']['id']
advice_text = data['slip']['advice']

# --- Steg 2: Skapa SQLite-databas och tabell ---
conn = sqlite3.connect("advice.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS advice (
    id INTEGER PRIMARY KEY,
    advice_id INTEGER UNIQUE,
    advice_text TEXT,
    date_added TEXT
)
''')

# --- Steg 3: Spara rådet i databasen ---
date_added = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
cursor.execute('''
INSERT OR IGNORE INTO advice (advice_id, advice_text, date_added)
VALUES (?, ?, ?)
''', (advice_id, advice_text, date_added))

# --- Steg 4: Spara och stäng ---
conn.commit()
conn.close()

print("Slumpmässigt råd har sparats i advice.db")


#TO-DO: Implementera "with" här?
# Skriv endast ut advice_text från de fem senaste råden
conn = sqlite3.connect("advice.db")
cursor = conn.cursor()
cursor.execute("SELECT * FROM advice ORDER BY date_added ASC")
print("All the wise advice:")
for row in cursor.fetchall():
    print(row[0], row[2])  # Skriv endast ut advice_text
conn.close()
"""