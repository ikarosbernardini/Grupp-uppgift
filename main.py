from time import sleep
from adviceAPI import AdviceApp
def menu():
    while True:
        print("\n=== Menu ===")
        print("1. Get new advice from API")
        print("2. Add your own advice")
        print("3. Print all saved advices")
        print("4. Search for saved advice")
        print("5. Show a random saved advice")
        print("6. Delete an advice")
        print("7. Exit")

        choice = int(input("Please enter your choice (1-7): "))

        try:

            if choice == 1:
                API_advice.get_advice()
            elif choice == 2:
                API_advice.add_advice_manually()
            elif choice == 3:
                API_advice.show_all_advice()
            elif choice == 4:
                keyword = input("Enter a keyword to search for: ").strip()
                API_advice.search_for_advice(keyword)
            elif choice == 5:
                API_advice.random_advice_from_db()
            elif choice == 6:
                API_advice.delete_advice()
            elif choice == 7:
                print("Leaving the wise API. Goodbye!")
                break            
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Invalid input, please enter a number between 1 and 7.")
        
        sleep(1)  # Pausar en sekund innan menyn visas igen

        


if __name__ == "__main__":
    API_advice = AdviceApp()
    menu()