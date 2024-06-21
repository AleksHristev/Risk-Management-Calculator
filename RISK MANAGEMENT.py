import tkinter as tk
from tkinter import messagebox

class RiskManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Risk Management For Trading")

        self.create_widgets()

    def create_widgets(self):
        self.entries = {}

        # Creating input fields for the parameters
        self.create_input_field("Account Balance")
        self.create_input_field("Risk Percentage (as decimal, e.g., 0.02 for 2%)")
        self.create_input_field("Entry Price")
        self.create_input_field("Stop Loss Price")

        calculate_button = tk.Button(self.root, text="Calculate Risk Management", command=self.calculate_risk_management)
        calculate_button.pack(pady=10)

    def create_input_field(self, label_text):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)

        label = tk.Label(frame, text=label_text)
        label.pack(side=tk.LEFT)

        var = tk.StringVar()
        entry = tk.Entry(frame, textvariable=var)
        entry.pack(side=tk.LEFT)

        self.entries[label_text] = var

    def calculate_risk_management(self):
        def get_float_input(var, prompt):
            try:
                return float(var.get().strip())
            except ValueError:
                messagebox.showerror("Input Error", f"Please enter a valid numeric value for: {prompt}")
                return None

        account_balance = get_float_input(self.entries["Account Balance"], "Account Balance")
        risk_percentage = get_float_input(self.entries["Risk Percentage (as decimal, e.g., 0.02 for 2%)"], "Risk Percentage")
        entry_price = get_float_input(self.entries["Entry Price"], "Entry Price")
        stop_loss_price = get_float_input(self.entries["Stop Loss Price"], "Stop Loss Price")

        if None in [account_balance, risk_percentage, entry_price, stop_loss_price]:
            return

        # Calculating risk per trade
        risk_per_trade = account_balance * risk_percentage

        # Calculating position size
        if entry_price != stop_loss_price:
            position_size = risk_per_trade / abs(entry_price - stop_loss_price)
        else:
            messagebox.showerror("Input Error", "Entry price and stop loss price cannot be the same.")
            return

        # Calculating total portfolio risk (assuming single trade here)
        total_portfolio_risk = risk_per_trade

        # Display the results
        message = (f"Risk Per Trade: {risk_per_trade:.2f}\n"
                   f"Position Size: {position_size:.2f}\n"
                   f"Total Portfolio Risk: {total_portfolio_risk:.2f}")
        messagebox.showinfo("Risk Management Results", message)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = RiskManagementApp(root)
    root.mainloop()