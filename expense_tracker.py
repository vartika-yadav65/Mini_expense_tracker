# Mini Expense Tracker
# A simple Python project to manage daily expenses
# Saves data to a file so expenses aren't lost after closing the program

import json
from datetime import datetime

budget = 5000
expenses = []


# Load previously saved expenses when the program starts
def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Save current expenses list to file
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


# Add a new expense
def add_expense():
    expense_name = input("\nEnter expense name: ")
    category = input("Enter category (Food/Travel/Shopping/Other): ")

    try:
        expense_amount = float(input("Enter expense amount: ₹"))
    except ValueError:
        print("Please enter a valid number.")
        return

    date = datetime.now().strftime("%d-%m-%Y")

    expense = {
        "name": expense_name,
        "category": category,
        "amount": expense_amount,
        "date": date
    }

    expenses.append(expense)
    save_expenses()
    print("Expense added successfully!")


# Show all expenses
def show_expenses():
    if len(expenses) == 0:
        print("\nNo expenses added yet.")
        return

    print("\n========== ALL EXPENSES ==========")

    for expense in expenses:
        print(
            expense["name"],
            "|",
            expense["category"],
            "| ₹",
            expense["amount"],
            "|",
            expense["date"]
        )


# Calculate total spending
def calculate_total():
    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    return total


# Show budget summary with warnings
def show_summary():
    total = calculate_total()
    remaining = budget - total

    print("\n========== SUMMARY ==========")
    print("Monthly budget: ₹", budget)
    print("Total spent: ₹", total)
    print("Remaining budget: ₹", remaining)

    if remaining < 0:
        print("Warning: You have exceeded your budget!")
    elif remaining < 500:
        print("Warning: Your budget is almost finished!")
    else:
        print("You are within your budget.")


# Main program
print("================================")
print("      MINI EXPENSE TRACKER")
print("================================")

expenses = load_expenses()

while True:
    print("\n1. Add Expense")
    print("2. Show Expenses")
    print("3. Show Summary")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_expense()

    elif choice == "2":
        show_expenses()

    elif choice == "3":
        show_summary()

    elif choice == "4":
        print("\nThank you for using Mini Expense Tracker!")
        break

    else:
        print("Invalid choice. Please try again.")