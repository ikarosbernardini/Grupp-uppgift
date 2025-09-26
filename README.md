# AdviceApp 

-------------------------------------------------------

AdviceApp är ett skript som hämtar slumpmässiga visdomsord från AdviceSlip API och erbjuder funktioner för att spara, 
läsa, söka och hantera dessa i en lokal SQLite-databas.

-------------------------------------------------------

## Instruktioner 
1. Klona repot
 skriv - "git clone https://github.com/ikarosbernardini/Grupp-uppgift" i din terminal.
 skriv sedan - "cd Grupp-uppgift"

 Skriptet använder externa moduler som requests. Installera dem med pip:
 skriv - "pip install requests"

 sen kan när du är i rätt mapp så kör du en "python main.py alternativt : python3 main.py" beroende på om du är på Windows eller Linux/Mac 


-------------------------------------------------------

## Funktioner 

-  Hämta visdomsord från ett externt API
-  Spara visdomsord i en databas (med kontroll för duplicering)
-  Läser upp alla sparade visdomsord
-  Slumpar fram ett visdomsord från databasen
-  Radera visdomsord baserat på innehåll
-  Lägg till egna visdomsord manuellt
-  Sökfunktion
-  Meny  för interaktiv användning via terminalen

--------------------------------------------------------

## Teknisk översikt
- Språk: Python 
- Databas: SQLite
- API: AdviceSlip
- Moduler: requests, sqlite3, datetime, random, time

--------------------------------------------------------

## Källor :
COPILOT & CHATGPT
API : https://api.adviceslip.com/advice
Python libary för modulerna : https://docs.python.org/3/library/sqlite3.html (SQL) 
https://docs.python.org/3/library/datetime.html (Datetime) 
https://docs.python.org/3/library/random.html (Random)
https://pypi.org/project/requests/ (Requests för API)

--------------------------------------------------------

Skapat av Arvid, Isabella, Markus, Ikaros 




