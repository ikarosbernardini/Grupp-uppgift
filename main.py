import time
from adviceAPI import AdviceApp
#import funktioner

def menu():
    while True:
        print("\n=== Menu ===")
        print("1. Get words of wisdom")
        print("2. Delete")
        print("3. Save in a txt-file?")
        print("4. Search")
        print("5. Read all saved")
        print("6. Randomize words of wisdom from a file")

        choice = input("")

        if choice == "1":
            loading("Loading...")
            #funktioner.
        elif choice == "2":
            #funktioner.radera()
            loading("Loading...")
        elif choice == "3":
            #funktioner.
            loading("Loading...")
        #elif choice == "4":
            #funktioner.
            loading("Loading...")
        #elif choice == "5":
            #funktioner.
            loading("Loading...")
        #elif choice == "6":
            #funktioner.slumpa()
            loading("Loading...")
        else:
            print("Wrong answer")
            time.sleep(1)

def loading(text):
    print(text, end="", flush=True)
    for i in range(3):
        time.sleep(0.5)
        print()


if __name__ == "__main__":
    API_advice = AdviceApp()
    advice_id, advice_text = API_advice.get_advice()
    save = input("Do you want to save this advice? (yes/no): ").strip().lower()
    if save == "yes":
        #OBS går ej att spara än eftersom funktionen inte är utvecklad.
        API_advice.save_advice(advice_id, advice_text)
    else:
        print("Advice was not saved.")