# Importing necessary modules
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import csv
import matplotlib.pyplot as plt

# Define the Financial Application class
class FinacialApp(tk.Tk): 
    # Constructor method
    def __init__(self): 
        super().__init__() # Call the constructor of the parent class 
        self.title("Finacial App") # Set the title of the application window
        self.geometry("400x400") # Set the size of the application window#
        self.configure(bg="#1f1ab0") # Set the background color of the window
        self.cats = [ # List of categories
            "Groceries",
            "Utilities",
            "Living",
            "Transport",
            "Entertainment",
            "Healthcare",
            "Shopping",
            "Travel",
            "Education",
            "Other"
        ]
        self.trans = [] # List to store transactions 
        self.cat_var = tk.StringVar(self) # Variable to store the selected category 
        self.cat_var.set(self.cats[0]) # Set the default category
        self.widgets() # Call the widgets method to create the GUI 
 
    # Method to create GUI widgets
    def widgets(self): 
        # Labels and input fields for transaction details
        self.lab = tk.Label( # Create a label for the title
            self, text="Finacial Tracker with Pi Chart!", font=("Courier New", 18, "bold") # Set the text and font
        )
        self.lab.pack(pady=10) # Add padding to the label
        self.frame_in = tk.Frame(self) # Create a frame for input fields
        self.frame_in.pack(pady=10) # Add padding to the frame
        self.trans_lab = tk.Label( # Create a label for transaction amount
            self.frame_in, text="Trans Amount:", font=("Courier New", 12) # Set the text and font
        )
        self.trans_lab.grid(row=0, column=0, padx=5) # Add the label to the grid
        self.trans_ent = tk.Entry( # Create an entry widget for transaction amount
            self.frame_in, font=("Courier New", 12), width=15 # Set the font and width
        )
        self.trans_ent.grid(row=0, column=1, padx=5) # Add the entry widget to the grid
        self.item_lab = tk.Label( # Create a label for item description
            self.frame_in, text="Item Desc:", font=("Courier New", 12) # Set the text and font
        )
        self.item_lab.grid(row=0, column=2, padx=5) # Add the label to the grid
        self.item_ent = tk.Entry( # Create an entry widget for item description
            self.frame_in, font=("Courier New", 12), width=20 # Set the font and width
        )
        self.item_ent.grid(row=0, column=3, padx=5) # Add the entry widget to the grid
        self.cat_lab = tk.Label( # Create a label for category
            self.frame_in, text="Category:", font=("Courier New", 12) # Set the text and font
        )
        self.cat_lab.grid(row=0, column=4, padx=5) # Add the label to the grid
        self.cat_drop = ttk.Combobox( # Create a dropdown widget for category selection
            self.frame_in, # Add the widget to the frame
            textvariable=self.cat_var, # Set the variable to store the selected category
            values=self.cats, # Set the values of the dropdown
            font=("Courier New", 12), # Set the font
            width=15, # Set the width
        )
        self.cat_drop.grid(row=0, column=5, padx=5) # Add the dropdown widget to the grid
        self.date_lab = tk.Label( # Create a label for date
            self.frame_in, text="Date (DD-MM-YY):", font=("Courier New", 12) # Set the text and font
        )
        self.date_lab.grid(row=0, column=6, padx=5) # Add the label to the grid
        self.date_ent = tk.Entry( # Create an entry widget for date
            self.frame_in, font=("Courier New", 12), width=15 # Set the font and width
        )
        self.date_ent.grid(row=0, column=7, padx=5) # Add the entry widget to the grid
        # Buttons for adding, editing, deleting, and saving transactions
        self.add_btn = tk.Button(self, text="Add Trans", command=self.addTrans) # Create a button to add transactions
        self.add_btn.pack(pady=5) # Add the button to the window with padding
        self.frame_list = tk.Frame(self) # Create a frame for transaction list
        self.frame_list.pack(pady=10) # Add padding to the frame
        self.scroll = tk.Scrollbar(self.frame_list) # Create a scrollbar for the listbox
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y) # Add the scrollbar to the window
        self.trans_lb = tk.Listbox( # Create a listbox to display transactions
            self.frame_list, # Add the listbox to the frame
            font=("Courier New", 12), # Set the font
            width=70, # Set the width
            yscrollcommand=self.scroll.set, # Set the yscrollcommand to the scrollbar
        )
        self.trans_lb.pack(pady=5) # Add padding to the listbox
        self.scroll.config(command=self.trans_lb.yview) # Configure the scrollbar
        self.edit_btn = tk.Button( # Create a button to edit transactions
            self, text="Edit trans", command=self.editTrans # Set the text and command
        )
        self.edit_btn.pack(pady=5) # Add the button to the window with padding
        self.del_btn = tk.Button( # Create a button to delete transactions
            self, text="Del Trans", command=self.delTrans # Set the text and command
        )
        self.del_btn.pack(pady=5) # Add the button to the window with padding
        self.save_btn = tk.Button( # Create a button to save transactions
            self, text="Save Trans", command=self.saveTrans # Set the text and command
        )
        self.save_btn.pack(pady=5) # Add the button to the window with padding
        # Label for displaying total transactions
        self.total_lab = tk.Label( # Create a label for displaying total transactions
            self, text="Total Trans:", font=("Courier New", 12) # Set the text and font
        )
        self.total_lab.pack(pady=5) # Add padding to the label
        # Button for showing transaction chart
        self.show_chart_btn = tk.Button( # Create a button to show transaction chart
            self, text="Show Pie Chart", command=self.showPieChart # Set the text and command
        )
        self.show_chart_btn.pack(pady=5) # Add the button to the window with padding
        self.updateLabel() # Update the label with total transactions

    # Method to add a transaction
    def addTrans(self): 
        amount = self.trans_ent.get() # Get the transaction amount
        description = self.item_ent.get() # Get the item description
        category = self.cat_var.get() # Get the selected category
        date = self.date_ent.get() # Get the transaction date
        if not amount or not description or not date: # Check if any field is empty 
            messagebox.showerror("Error", "All fields must be filled") # Show an error message
            return # Return from the method
        try: # Try to convert the amount to a float
            amount = float(amount) # Convert the amount to a float
        except ValueError: # Handle the ValueError exception
            messagebox.showerror("Error", "Amount must be a number") # Show an error message
            return # Return from the method
        # Create a transaction string
        transaction = f"{amount} on {date}, category: {category}, description: {description}" 
        self.trans.append(transaction) # Add the transaction to the list
        self.trans_lb.insert(tk.END, transaction) # Add the transaction to the listbox
        self.updateLabel() # Update the total label
        self.trans_ent.delete(0, tk.END) # Clear the transaction entry
        self.item_ent.delete(0, tk.END) # Clear the item entry
        self.date_ent.delete(0, tk.END) # Clear the date entry
 
    # Method to edit a transaction
    def editTrans(self): 
        selected = self.trans_lb.curselection() # Get the selected transaction
        if not selected: # Check if no transaction is selected
            messagebox.showerror("Error", "No transaction selected") # Show an error message
            return # Return from the method
        index = selected[0] # Get the index of the selected transaction
        transaction = self.trans[index] # Get the selected transaction
        # Get the new description from Dthe user
        new_description = simpledialog.askstring("Edit Transaction", "Enter new description", initialvalue=transaction.split(", description: ")[1]) 
        if new_description: # Check if a new description is entered
            # Create the new transaction string
            new_transaction = f"{transaction.split('description: ')[0]}description: {new_description}" 
            self.trans[index] = new_transaction # Update the transaction in the list
            self.trans_lb.delete(index) # Delete the old transaction from the listbox
            self.trans_lb.insert(index, new_transaction) # Insert the new transaction in the listbox
            self.updateLabel() # Update the total label

    # Method to delete a transaction
    def delTrans(self): 
        selected = self.trans_lb.curselection() # Get the selected transaction
        if not selected: # Check if no transaction is selected
            messagebox.showerror("Error", "No transaction selected") # Show an error message
            return # Return from the method
        index = selected[0] # Get the index of the selected transaction
        self.trans_lb.delete(index) # Delete the transaction from the listbox
        self.trans.pop(index) # Remove the transaction from the list
        self.updateLabel() # Update the total label
 
    # Method to update the total label
    def updateLabel(self): 
        total_transactions = sum(float(transaction.split(" ")[0]) for transaction in self.trans) # Calculate the total transactions
        self.total_lab.config(text=f"Total Trans: GBP {total_transactions:.2f}") # Update the total label

    # Method to save the transactions to a CSV file
    def saveTrans(self): 
        with open("transactions.csv", "w", newline="") as file: # Open the file in write mode
            writer = csv.writer(file) # Create a CSV writer
            for transaction in self.trans: # Iterate over the transactions
                writer.writerow([transaction]) # Write the transaction to the file
        messagebox.showinfo("Success", "Transactions saved successfully") # Show a success message

    # Method to show the transactions chart
    def showPieChart(self): 
        amounts = [float(transaction.split(" ")[0]) for transaction in self.trans] # Get the amounts from the transactions
        plt.pie(amounts, labels=self.trans, startangle=140, autopct="%1.1f%%",shadow={'ox': -0.04, 'edgecolor': 'none', 'shade': 0.9}, pctdistance=1.25, labeldistance=.2) # Create a pie chart
        plt.axis("equal") # Set the aspect ratio to be equal
        plt.show() # Show the chart

# Main entry point
if __name__ == "__main__": 
    app = FinacialApp() # Create an instance of the FinApp class
    app.mainloop() # Run the application
   
