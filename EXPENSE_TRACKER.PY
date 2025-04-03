import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
import pymysql, random


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.iconbitmap("C:/Users/sehra/Downloads/hell.ico")
        self.geometry("1300x600")
        self.expenses = []
        self.categories = [
            "Food",
            "Transportation",
            "Utilities",
            "Entertainment",
            "Other",
        ]
        self.category_var = tk.StringVar(self)
        self.category_var.set(self.categories[0])
        self.create_widgets()
        self.db = pymysql.connect(
            host="localhost",
            user="root",
            password="harsh12345",
            database="expense_tracker"
        )
        self.cursor = self.db.cursor()


    def create_widgets(self):
        self.label = tk.Label(
            self, text="Expense Tracker", font=("Helvetica", 20, "bold")
        )
        self.label.pack(pady=10)
        self.frame_input = tk.Frame(self)
        self.frame_input.pack(pady=10)
        self.expense_label = tk.Label(
            self.frame_input, text="Expense Amount:", font=("Helvetica", 12)
        )
        self.expense_label.grid(row=0, column=0, padx=5)
        self.expense_entry = tk.Entry(
            self.frame_input, font=("Helvetica", 12), width=15
        )
        self.expense_entry.grid(row=0, column=1, padx=5)
        self.item_label = tk.Label(
            self.frame_input, text="Item Description:", font=("Helvetica", 12)
        )
        self.item_label.grid(row=0, column=2, padx=5)
        self.item_entry = tk.Entry(self.frame_input, font=("Helvetica", 12), width=20)
        self.item_entry.grid(row=0, column=3, padx=5)
        self.category_label = tk.Label(
            self.frame_input, text="Category:", font=("Helvetica", 12)
        )
        self.category_label.grid(row=0, column=4, padx=5)
        self.category_dropdown = ttk.Combobox(
            self.frame_input,
            textvariable=self.category_var,
            values=self.categories,
            font=("Helvetica", 12),
            width=15,
        )
        self.category_dropdown.grid(row=0, column=5, padx=5)
        self.date_label = tk.Label(
            self.frame_input, text="Date:", font=("Helvetica", 12)
        )
        self.date_label.grid(row=0, column=6, padx=5)

        # Use Tkinter Calendar for date selection
        self.date_entry = DateEntry(
            self.frame_input,
            font=("Helvetica", 12),
            date_pattern="yyyy-mm-dd",
            width=15,
            background="darkblue",
            foreground="white",
            borderwidth=2,
        )
        self.date_entry.grid(row=0, column=7, padx=5)
        self.add_button = tk.Button(self, text="Add Expense", command=self.add_expense)
        self.add_button.pack(pady=5)
        self.frame_list = tk.Frame(self)
        self.frame_list.pack(pady=10)

        # Create vertical scrollbar
        self.vertical_scrollbar = tk.Scrollbar(self.frame_list)
        self.vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create horizontal scrollbar
        self.horizontal_scrollbar = tk.Scrollbar(self.frame_list, orient=tk.HORIZONTAL)
        self.horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.expense_listbox = tk.Listbox(
            self.frame_list,
            font=("Helvetica", 12),
            width=70,
            yscrollcommand=self.vertical_scrollbar.set,
            xscrollcommand=self.horizontal_scrollbar.set  # Set horizontal scrollbar
        )
        self.expense_listbox.pack(pady=5)

        # Configure vertical scrollbar
        self.vertical_scrollbar.config(command=self.expense_listbox.yview)

        # Configure horizontal scrollbar
        self.horizontal_scrollbar.config(command=self.expense_listbox.xview)

        self.edit_button = tk.Button(
            self, text="Edit Expense", command=self.edit_expense
        )
        self.edit_button.pack(pady=5)
        self.delete_button = tk.Button(
            self, text="Delete Expense", command=self.delete_expense
        )
        self.delete_button.pack(pady=5)
        self.save_button = tk.Button(
            self, text="Save Expenses", command=self.save_expenses
        )
        self.save_button.pack(pady=5)
        self.total_label = tk.Label(
            self, text="Total Expenses:", font=("Helvetica", 12)
        )
        self.total_label.pack(pady=5)
        self.show_chart_button = tk.Button(
            self, text="Show Expenses Chart", command=self.show_expenses_chart
        )
        self.show_chart_button.pack(pady=5)
        
        self.show_graph_button = tk.Button(
            self, text="Show Expenses Graph", command=self.show_expenses_bar_graph
        )
        self.show_graph_button.pack(pady=5)
        self.update_total_label()
    def add_expense(self):
        global id
        expense = self.expense_entry.get()
        item = self.item_entry.get()
        category = self.category_var.get()
        date = self.date_entry.get()
        
        if expense and date:
            index = len(self.expenses) + 1  # Calculate the next index
            self.expenses.append((expense, item, category, date))
            self.expense_listbox.insert(
                tk.END, f"{index}. ₹{expense} - {item} - {category}   ({date})"
            )
            self.expense_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.date_entry.delete(0, tk.END)
            id=random.randint(99,9999)
            self.cursor.execute(f"insert into expenses values({id},{expense},'{item}','{category}','{date}')")
            self.db.commit()
        else:
            messagebox.showwarning("Warning", "Expense and Date cannot be empty.")
        self.update_total_label()

    def edit_expense(self):
        global new_expense
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_expense = self.expenses[selected_index]
            new_expense = simpledialog.askstring(
                "Edit Expense", "Enter new expense:", initialvalue=selected_expense[0]
            )
            if new_expense:
                updated_expense = (
                    new_expense,
                    selected_expense[1],
                    selected_expense[2],
                    selected_expense[3],
                )
                self.expenses[selected_index] = updated_expense
                self.refresh_list()
                self.update_total_label()


    def delete_expense(self):
        selected_index = self.expense_listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            del self.expenses[selected_index]
            self.expense_listbox.delete(selected_index)
            self.update_total_label()
    
    def refresh_list(self):
        self.expense_listbox.delete(0, tk.END)
        for index, (expense, item, category, date) in enumerate(self.expenses, start=1):
            display_string = f"{index}. ₹{expense} - {item} - {category} ({date})"
            self.expense_listbox.insert(tk.END, display_string)

    def update_total_label(self):
        total_expenses = sum(float(expense[0]) for expense in self.expenses)
        self.total_label.config(text=f"Total Expenses: ₹ {total_expenses:.2f}")

    def save_expenses(self):
        # with open("expenses.csv", "w", newline="") as csvfile:
        #     writer = csv.writer(csvfile)
        #     column_headers = ["Expense Amount", "Item Description", "Category", "Date"]
        #     writer.writerow(column_headers)
        #     for expense in self.expenses:
        #         writer.writerow(expense)

        query = f'''
                UPDATE expenses
                SET expense_amount = {new_expense}
                WHERE expense_id = {id};
                '''
        self.cursor.execute(query)
        self.db.commit()
        print('saved to sql!')




    def show_expenses_chart(self):
        category_totals = {}
        for expense, _, category, _ in self.expenses:
            try:
                amount = float(expense)
            except ValueError:
                continue
            category_totals[category] = category_totals.get(category, 0) + amount

        categories = list(category_totals.keys())
        expenses = list(category_totals.values())

        plt.figure(figsize=(8, 6))
        plt.pie(
            expenses, labels=categories, autopct="%1.1f%%", startangle=140, shadow=True
        )
        plt.axis("equal")
        plt.title(f"Expense Categories Distribution (Rupees)")
        plt.show()
    def show_expenses_bar_graph(self):
        category_totals = {}
        for expense, _, category, _ in self.expenses:
            try:
                amount = float(expense)
            except ValueError:
                continue
            category_totals[category] = category_totals.get(category, 0) + amount

        categories = list(category_totals.keys())
        expenses = list(category_totals.values())

        plt.figure(figsize=(8, 6))
        plt.bar(categories, expenses)
        plt.xlabel("Expense Categories")
        plt.ylabel("Total Expenses (Rupees)")
        plt.title(f"Expense Categories Distribution (Rupees) - Bar Graph")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
