#T153
#Domain: Agriculture



#Title:
#Assured Contract Farming System for Stable Market Access



#Description: Background: Farmers often face uncertainties in market access, leading to fluctuating incomes. Contract farming can provide stability by ensuring farmers have guaranteed buyers for their produce. Description: Develop a comprehensive platform that facilitates assured contract farming agreements between farmers and buyers. This platform will enable transparent communication, secure contracts, and timely payments, ensuring farmers have a reliable market for their crops. Expected Solution: An online marketplace that connects farmers with potential buyers, offering tools for contract management, price negotiation, and secure payment processing, thereby enhancing income stability and reducing market risks

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk

contracts = []

class ContractFarmingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🌾 Assured Contract Farming System")
        self.root.geometry("800x550")
        self.root.configure(bg="#eef9f1")

        self.user_type = tk.StringVar()
        self.current_user = None

        self.setup_login()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_image(self, path, size):
        try:
            img = Image.open(path)
            img = img.resize(size, Image.ANTIALIAS)
            return ImageTk.PhotoImage(img)
        except:
            return None

    def title_label(self, text):
        return tk.Label(self.root, text=text, font=("Helvetica", 18, "bold"), fg="#2e7d32", bg="#eef9f1")

    def button_style(self, text, command):
        return tk.Button(self.root, text=text, font=("Arial", 12), bg="#66bb6a", fg="white",
                         activebackground="#43a047", padx=10, pady=5, borderwidth=0, command=command)

    def setup_login(self):
        self.clear_window()

        banner_img = self.load_image("banner.png", (780, 100))
        if banner_img:
            tk.Label(self.root, image=banner_img, bg="#eef9f1").pack(pady=10)
            self.root.banner_img = banner_img  # prevent garbage collection

        self.title_label("🌾 Assured Contract Farming System").pack(pady=10)

        tk.Label(self.root, text="Login as:", font=("Arial", 14), bg="#eef9f1").pack(pady=10)

        frame = tk.Frame(self.root, bg="#eef9f1")
        frame.pack(pady=10)

        farmer_img = self.load_image("farmer.png", (60, 60))
        buyer_img = self.load_image("buyer.png", (60, 60))

        tk.Label(frame, image=farmer_img, bg="#eef9f1").grid(row=0, column=0, padx=10)
        ttk.Radiobutton(frame, text="Farmer", variable=self.user_type, value="Farmer").grid(row=1, column=0, padx=10)
        tk.Label(frame, image=buyer_img, bg="#eef9f1").grid(row=0, column=1, padx=10)
        ttk.Radiobutton(frame, text="Buyer", variable=self.user_type, value="Buyer").grid(row=1, column=1, padx=10)

        self.root.farmer_img = farmer_img
        self.root.buyer_img = buyer_img

        self.button_style("Login / Register", self.login_register).pack(pady=20)

    def login_register(self):
        if not self.user_type.get():
            messagebox.showwarning("Select Role", "Please select a role: Farmer or Buyer")
            return

        user = simpledialog.askstring("Login", f"Enter your {self.user_type.get()} Name:")
        if user:
            self.current_user = user
            self.dashboard()

    def dashboard(self):
        self.clear_window()
        self.title_label("🌱 Dashboard").pack(pady=15)

        tk.Label(self.root, text=f"Welcome, {self.current_user} ({self.user_type.get()})", font=("Arial", 12),
                 bg="#eef9f1", fg="#388e3c").pack(pady=10)

        if self.user_type.get() == "Farmer":
            self.button_style("➕ Create New Contract", self.create_contract).pack(pady=10)
        if self.user_type.get() == "Buyer":
            self.button_style("📋 View Available Contracts", self.view_contracts).pack(pady=10)

        self.button_style("🚪 Logout", self.setup_login).pack(pady=40)

    def create_contract(self):
        details = simpledialog.askstring(
            "New Contract",
            "Enter contract details:\nFormat: Crop, Quantity (kg), Price per kg\nExample: Wheat, 100, 25.5"
        )

        if details:
            try:
                crop, qty, price = map(str.strip, details.split(","))
                qty = int(qty)
                price = float(price)

                contract = {
                    "farmer": self.current_user,
                    "crop": crop,
                    "quantity": qty,
                    "price": price,
                    "buyer": None,
                    "status": "Open"
                }
                contracts.append(contract)
                messagebox.showinfo("✅ Success", "Contract Created Successfully!")

            except ValueError:
                messagebox.showerror("❌ Error", "Invalid format! Please use: Crop, Quantity, Price")

    def view_contracts(self):
        view_win = tk.Toplevel(self.root)
        view_win.title("📃 Available Contracts")
        view_win.geometry("700x300")
        view_win.configure(bg="#f4fbe9")

        tree = ttk.Treeview(view_win, columns=("Farmer", "Crop", "Qty", "Price", "Status"), show='headings')
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=25)

        tree.heading("Farmer", text="Farmer")
        tree.heading("Crop", text="Crop")
        tree.heading("Qty", text="Qty (kg)")
        tree.heading("Price", text="Price (Rs)")
        tree.heading("Status", text="Status")

        for contract in contracts:
            if contract["status"] == "Open":
                tree.insert('', tk.END, values=(contract["farmer"], contract["crop"], contract["quantity"], contract["price"], contract["status"]))

        tree.pack(pady=10, fill="x")

        self.button_style("🤝 Accept Selected Contract", lambda: self.accept_contract(tree)).pack(pady=10)

    def accept_contract(self, tree):
        selected_item = tree.focus()
        if selected_item:
            values = tree.item(selected_item)['values']
            for contract in contracts:
                if contract["farmer"] == values[0] and contract["crop"] == values[1] and contract["status"] == "Open":
                    contract["buyer"] = self.current_user
                    contract["status"] = "Accepted"
                    messagebox.showinfo("✅ Accepted", f"You accepted contract from {contract['farmer']}.\nPayment Initiated.")
                    break
            tree.delete(selected_item)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContractFarmingApp(root)
    root.mainloop()
