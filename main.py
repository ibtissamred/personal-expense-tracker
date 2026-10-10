
import sqlite3
from datetime import date

# Create the database
connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    expense_date TEXT NOT NULL
)
""")
connection.commit()


def add_expense():
    name = input("Expense name: ")
    amount = float(input("Amount: "))
    category = input("Category: ")
    expense_date = input("Date (YYYY-MM-DD), or press Enter for today: ")

    if not expense_date:
        expense_date = date.today().isoformat()

    cursor.execute(
        "INSERT INTO expenses (name, amount, category, expense_date) VALUES (?, ?, ?, ?)",
        (name, amount, category, expense_date)
    )
    connection.commit()
    print("Expense added successfully!")


def view_expenses():
    cursor.execute("SELECT * FROM expenses ORDER BY expense_date DESC")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\nID | Name | Amount | Category | Date")
    print("-" * 55)
    for expense in expenses:
        print(
            f"{expense[0]} | {expense[1]} | "
            f"{expense[2]:.2f} | {expense[3]} | {expense[4]}"
        )


def search_category():
    category = input("Enter category to search: ")
    cursor.execute(
        "SELECT * FROM expenses WHERE category LIKE ?",
        (f"%{category}%",)
    )
    results = cursor.fetchall()

    if not results:
        print("No matching expenses found.")
        return

    for expense in results:
        print(expense)


def show_total():
    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0] or 0
    print(f"Total spending: {total:.2f}")


def main():
    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Search by category")
        print("4. Show total spending")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                add_expense()
            except ValueError:
                print("Please enter a valid amount.")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_category()
        elif choice == "4":
            show_total()
        elif choice == "5":
            print("Thank you for using the Expense Tracker!")
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()


if __name__ == "__main__":
    main()

