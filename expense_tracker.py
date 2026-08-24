# Mini Expense Tracker
# A simple Python project to manage daily expenses
# Saves data to a file so expenses aren't lost after closing the program

import json
import csv
from datetime import datetime

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

budget = 5000
expenses = []
CATEGORIES = ["Food", "Travel", "Shopping", "Other"]


# ---------- FILE HANDLING ----------

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: expenses.json was corrupted. Starting with an empty list.")
        return []


def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


# ---------- VALIDATION HELPERS ----------

def get_valid_amount():
    while True:
        raw = input("Enter expense amount: ₹").strip()
        try:
            amount = float(raw)
        except ValueError:
            print("Invalid input. Please enter a numeric amount (e.g., 250 or 99.50).")
            continue

        if amount <= 0:
            print("Amount must be greater than zero.")
            continue

        return round(amount, 2)


def get_valid_category():
    options = "/".join(CATEGORIES)
    while True:
        category = input(f"Enter category ({options}): ").strip().title()
        if category in CATEGORIES:
            return category
        print(f"Invalid category. Please choose from: {options}")


def get_valid_date():
    """
    Lets the user pick today's date automatically, or type a custom
    date in DD-MM-YYYY format. Validates the format and that it's a
    real calendar date.
    """
    choice = input("Use today's date? (y/n): ").strip().lower()
    if choice != "n":
        return datetime.now().strftime("%d-%m-%Y")

    while True:
        date_str = input("Enter date (DD-MM-YYYY): ").strip()
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return date_str
        except ValueError:
            print("Invalid date format. Please use DD-MM-YYYY, e.g. 24-08-2026.")


def get_valid_expense_name():
    while True:
        name = input("Enter expense name: ").strip()
        if name:
            return name
        print("Expense name cannot be empty.")


# ---------- CORE FEATURES ----------

def add_expense():
    print()
    expense_name = get_valid_expense_name()
    category = get_valid_category()
    amount = get_valid_amount()
    date = get_valid_date()

    expense = {
        "name": expense_name,
        "category": category,
        "amount": amount,
        "date": date
    }

    expenses.append(expense)
    save_expenses()
    print("Expense added successfully!")


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


def calculate_total():
    return sum(expense["amount"] for expense in expenses)


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


# ---------- #4: MONTHLY BUDGET VS ACTUAL SPENDING REPORT ----------

def monthly_budget_report():
    if len(expenses) == 0:
        print("\nNo expenses added yet, nothing to report.")
        return

    # Group spending by month (MM-YYYY), based on each expense's date
    monthly_totals = {}
    for expense in expenses:
        try:
            date_obj = datetime.strptime(expense["date"], "%d-%m-%Y")
        except ValueError:
            continue  # skip malformed dates from old data
        month_key = date_obj.strftime("%m-%Y")
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + expense["amount"]

    print("\n========== MONTHLY BUDGET VS ACTUAL ==========")
    print(f"{'Month':<10}{'Budget (₹)':<15}{'Actual (₹)':<15}{'Status'}")
    print("-" * 55)

    for month_key in sorted(monthly_totals, key=lambda m: datetime.strptime(m, "%m-%Y")):
        actual = monthly_totals[month_key]
        diff = budget - actual
        if diff < 0:
            status = f"Over by ₹{abs(diff):.2f}"
        else:
            status = f"Under by ₹{diff:.2f}"
        print(f"{month_key:<10}{budget:<15}{actual:<15.2f}{status}")


# ---------- #5: CSV EXPORT ----------

def export_to_csv():
    if len(expenses) == 0:
        print("\nNo expenses to export yet.")
        return

    filename = "expenses_export.csv"
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["name", "category", "amount", "date"])
        writer.writeheader()
        writer.writerows(expenses)

    print(f"\nExpenses exported successfully to {filename}!")


# ---------- #6: GRAPHICAL SUMMARY WITH MATPLOTLIB ----------

def show_graphical_summary():
    if not MATPLOTLIB_AVAILABLE:
        print("\nMatplotlib is not installed. Run: pip install matplotlib")
        return

    if len(expenses) == 0:
        print("\nNo expenses to visualize yet.")
        return

    # Aggregate spending by category
    category_totals = {}
    for expense in expenses:
        cat = expense["category"]
        category_totals[cat] = category_totals.get(cat, 0) + expense["amount"]

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Bar chart: spending by category
    axes[0].bar(categories, amounts, color="#4C72B0")
    axes[0].set_title("Spending by Category")
    axes[0].set_xlabel("Category")
    axes[0].set_ylabel("Amount (₹)")

    # Pie chart: share of total spending
    axes[1].pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    axes[1].set_title("Spending Distribution")

    plt.tight_layout()
    plt.savefig("expense_summary.png")
    print("\nGraph saved as expense_summary.png")

    try:
        plt.show()
    except Exception:
        pass  # in headless environments, show() may not work - the saved PNG still exists


# ---------- MAIN PROGRAM ----------

def main():
    global expenses

    print("================================")
    print("      MINI EXPENSE TRACKER")
    print("================================")

    expenses = load_expenses()

    menu_actions = {
        "1": add_expense,
        "2": show_expenses,
        "3": show_summary,
        "4": monthly_budget_report,
        "5": export_to_csv,
        "6": show_graphical_summary,
    }

    while True:
        print("\n1. Add Expense")
        print("2. Show Expenses")
        print("3. Show Summary")
        print("4. Monthly Budget vs Actual Report")
        print("5. Export to CSV")
        print("6. Graphical Summary (Matplotlib)")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "7":
            print("\nThank you for using Mini Expense Tracker!")
            break
        elif choice in menu_actions:
            menu_actions[choice]()
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()