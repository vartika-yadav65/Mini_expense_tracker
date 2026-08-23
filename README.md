📊 Mini Expense Tracker
A simple command-line Python project to track your daily expenses, check them against your monthly budget, and save everything to a file so nothing gets lost when you close the program.
📌 What the Project Does
This is a menu-driven expense tracker that runs in your terminal. You can add expenses with a name, category, and amount, view all your recorded expenses, and check a quick summary of how much you've spent versus how much budget you have left.
Every expense you add gets saved to a file called expenses.json. So even if you close the program and open it again later, your previous expenses are automatically loaded back in — the tracker "remembers" your data across sessions.
🧠 Python Concepts Used
Variables & data types (int, float, string, list, dict)
Basic operators (arithmetic, comparison)
Input & Output (input(), print())
if / elif / else conditions
while loop (menu-driven structure) & for loop (looping through expenses)
Lists (storing all expenses)
Dictionaries (storing individual expense details)
Functions (modular code — one function per task)
Exception handling (try/except for invalid amount input)
File handling (reading/writing JSON files)
Modules & libraries (json, datetime)
▶️ How to Run It
Make sure Python 3 is installed on your system.
Download the file expense_tracker.py.
Open a terminal in the same folder as the file.
Run the program:
Code
Use the on-screen menu to add expenses, view them, or check your summary.
Choose option 4 to exit the program.
An expenses.json file will automatically be created in the same folder to store your data.
✨ Features
Add expenses with name, category, amount, and auto-generated date
View all expenses in a clean, readable list
Budget summary showing total spent and remaining budget
Smart warnings:
Alerts you if you've exceeded your budget
Warns you when your budget is running low (under ₹500)
Persistent storage — expenses are saved to expenses.json and reloaded automatically the next time you run the program
Input validation — handles invalid (non-numeric) amount entries gracefully instead of crashing
Simple menu system — easy to navigate with numbered options
📂 Files in This Project
File
Description
expense_tracker.py
Main program file
expenses.json
Auto-generated file that stores all your expense records

🚀 Possible Future Improvements
Add ability to delete or edit an existing expense
Add monthly/category-wise spending breakdown
Set custom budget limits per category
Export summary as a PDF or CSV report
Built as a beginner Python project to practice core concepts through a real, usable mini-application.