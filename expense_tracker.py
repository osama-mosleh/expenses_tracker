import json
import os

expense_file = "expenses.txt"

def add_expense(amount, category): # add expense by category and amount

    try:
        expenses = load_expenses_from_file()
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []

    new_expense = {"amount": amount, "category": category}
    expenses.append(new_expense)
    write_expenses_to_file(expenses)
    return "Expense added successfully"


def write_expenses_to_file(expenses): # write the expenses to a text file in json format
    with open(expense_file, 'w') as file:
        json.dump(expenses, file, indent=2)


def load_expenses_from_file(): # retrive expenses from the text file and return it as list of dictionaries
    if not os.path.exists(expense_file):
        return []

    with open(expense_file, 'r') as file:
        expenses = json.load(file)
        return expenses


def show_expenses(): # display the expenses from the text file to the user

    expenses = load_expenses_from_file()
    if not expenses:
        print("No expenses found.")
        return

    print(f"{'Amount':<10} {'Category'}")
    print("-" * 25)
    for expense in expenses:
        print(f"${expense['amount']:<9} {expense['category']}")


def update_expense(old_category, old_amount, new_amount=None, new_category=None): # update an existing expense

    expenses = load_expenses_from_file()

    # Find the expense to update
    expense_found = False
    for expense in expenses:
        if expense['category'] == old_category and expense['amount'] == old_amount:
            if new_amount is not None:
                expense['amount'] = new_amount
            if new_category is not None:
                expense['category'] = new_category
            expense_found = True
            break

    if expense_found:
        write_expenses_to_file(expenses)
        return "Expense updated successfully"
    else:
        return "Expense not found, please add it first"


def calculate_total_expenses(): # calculate the total amount accross all the catagories

    expenses = load_expenses_from_file()
    total = sum(expense['amount'] for expense in expenses)
    return total


def calculate_expenses_by_category(): #calculate the total expenses for each catagory

    expenses = load_expenses_from_file()
    category_totals = {}

    for expense in expenses:
        category = expense['category']
        amount = expense['amount']

        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount

    return category_totals


def main(): # user interface
    while True:
        print("\nExpense Tracker")
        print("Choose an option or type 'EXIT':")
        print("1- Add expense")
        print("2- Show expenses")
        print("3- Update expense")
        print("4- Show total expenses")
        print("5- Show expenses by category")
        print("-"*10 + 'Quick hint: the data file will be saved in the same directory you run the program from',"-"*10)

        user_input = input("\nEnter your choice: ").strip()

        if user_input.upper() == "EXIT":
            print("Goodbye!")
            break

        elif user_input == "1":
            try:
                amount = float(input("Enter amount: "))
                category = input("Enter category: ").strip()
                print(add_expense(amount, category))
            except ValueError:
                print("Please enter a valid amount")

        elif user_input == "2":
            show_expenses()

        elif user_input == "3":
            try:
                show_expenses()
                old_amount = float(input("Enter current amount of expense to update: "))
                old_category = input("Enter current category of expense to update: ").strip()

                print("What would you like to update?")
                print("1- Amount only")
                print("2- Category only")
                print("3- Both amount and category")

                update_choice = input("Enter choice (1-3): ").strip()

                new_amount = None
                new_category = None

                if update_choice in ["1", "3"]:
                    new_amount = float(input("Enter new amount: $"))
                if update_choice in ["2", "3"]:
                    new_category = input("Enter new category: ").strip()

                result = update_expense(old_category, old_amount, new_amount, new_category)
                print(result)

            except ValueError:
                print("Please enter valid values")

        elif user_input == "4":
            total = calculate_total_expenses()
            print(f"Total expenses: {total}")

        elif user_input == "5":
            category_totals = calculate_expenses_by_category()
            if category_totals:
                print(f"{'Category':<15} {'Total Amount'}")
                print("-" * 30)
                for category, total in category_totals.items():
                    print(f"{category:<15} ${total}")
            else:
                print("No expenses found")

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()