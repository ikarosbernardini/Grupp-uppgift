import time
from adviceAPI import AdviceApp
def menu():
    while True:
        print("\n=== Menu ===")
        print("1. Recive new words of advice from the wise API")
        print("2. Delete advice from database")
        print("3. Print all saved words of advice")
        print("4. Search for specific words of advice")
        print("6. Randomize words of advice from a file")

  #              print("3. Save in a txt-file?")


        choice = input("")

        if choice == "1":
            API_advice.get_advice()
        elif choice == "2":
            API_advice.delete()     
        elif choice == "3":
            API_advice.show_all()
            """
            #funktioner.
        #elif choice == "4":
            #funktioner.
        #elif choice == "5":
            #funktioner.
        #elif choice == "6":
            #funktioner.slumpa()
            """
        else:
            print("Invalid choice, please try again.")
            return 
            time.sleep(1)

def loading(text):
    print(text, end="", flush=True)
    for i in range(3):
        time.sleep(0.5)
        print()


if __name__ == "__main__":
    API_advice = AdviceApp()
    menu()