import time
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
            loading()
            #funktioner.
        elif choice == "2":
            #funktioner.radera()
            loading()
        elif choice == "3":
            #funktioner.
        #elif choice == "4":
            #funktioner.
        #elif choice == "5":
            #funktioner.
        #elif choice == "6":
            funktioner.slumpa()
        else:
            print("Felaktigt svar")
            time.sleep(3)

"""def loading(text):
    print(text, end="", flush=True)
    for i in range(3):
        time.sleep(0.5)
        print()"""


#if__name__=="__main__":
#    show_menu()

menu()