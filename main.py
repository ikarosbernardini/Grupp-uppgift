from time import sleep
from adviceAPI import AdviceApp
def menu():
    while True:
        print("\n=== Menu ===")
        print("1. Recive new words of advice from the wise API")
        print("2. Delete advice from database")
        print("3. Print all saved words of advice")
        print("4. Search for specific words of advice")
        print("5. Randomize words of advice from a file")
        print("6. Leave the wise API")
        print("Please enter your choice (1-6): ")

        choice = input("")

        if choice == "1":
            API_advice.get_advice()
        elif choice == "2":
            API_advice.delete_advice()   
        elif choice == "3":
            API_advice.show_all()
        elif choice == "4":
            keyword = input("Enter a keyword to search for: ")
            API_advice.search_for_advice(keyword)
        elif choice == "5":
            API_advice.random_from_db()
        elif choice == "6":
            print("Leaving the wise API. Good riddance! Goodbye!")
            break
            #funktioner.slumpa()
            
        else:
            print("Invalid choice, please try again.")
            return 
            time.sleep(1)


if __name__ == "__main__":
    API_advice = AdviceApp()
    menu()