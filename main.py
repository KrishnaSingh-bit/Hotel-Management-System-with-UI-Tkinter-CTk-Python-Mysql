import random
import csv
import customtkinter as ctk
import mysql.connector as k 
from tkinter import messagebox,PhotoImage

# -------------------- CONFIG --------------------
DB_CONFIG = {
    "host": "LocalHost",
    "user": "root",       # change if needed
    "password": "sqlKrishna",       # your MySQL password
    "database": "bank_db"
}

ctk.set_default_color_theme("blue")

# ---------- DATABASE CONNECTOR ----------
def get_db_connection():
    return k.connect(**DB_CONFIG)

# create a global connection to reuse
try:
    db_conn = get_db_connection()
    db_cursor = db_conn.cursor()
except Exception as e:
    messagebox.showerror("DB Connection Error", f"Could not connect to database:\n{e}")
    raise SystemExit("Database not available") from e

# ------------------ APP --------------------
class BankApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Krishna Bank — Management System")
        self.geometry("980x620")
        self.minsize(900, 560)
        self.configure(fg_color = "#791465")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._create_left_sidebar()
        self._create_topbar()
        self._create_content_area()
        self.show_create_account()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
    # ------------------ Sidebar ------------------
    def _create_left_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=12,fg_color="#000000")
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=14, pady=14)
        self.sidebar.grid_rowconfigure(10, weight=1)

        ctk.CTkLabel(self.sidebar, text="Krishna BANK", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=12, pady=(12, 4), sticky="w")
        ctk.CTkLabel(self.sidebar, text="Management Panel", font=ctk.CTkFont(size=13)).grid(row=1, column=0, padx=12, pady=(0,12), sticky="w")

        btn_kwargs = dict(width=180, height=44, corner_radius=10,fg_color="#00ae60", hover_color="#6BDB76")
        self.btn_create = ctk.CTkButton(self.sidebar, text="Create Account", command=self.show_create_account, **btn_kwargs)
        self.btn_display = ctk.CTkButton(self.sidebar, text="Display Account", command=self.show_display_account,**btn_kwargs)
        self.btn_deposit = ctk.CTkButton(self.sidebar, text="Deposit Money", command=self.show_deposit, **btn_kwargs)
        self.btn_withdraw = ctk.CTkButton(self.sidebar, text="Withdraw Money", command=self.show_withdraw, **btn_kwargs)
        self.btn_delete = ctk.CTkButton(self.sidebar, text="Delete Account", command=self.show_delete, **btn_kwargs)
        self.btn_export = ctk.CTkButton(self.sidebar, text="Export CSV", command=self.export_csv, **btn_kwargs)
        self.btn_exit = ctk.CTkButton(self.sidebar, text="Exit", command=self._on_close, fg_color="#ff4d4d", hover_color="#ff6b6b", width=180, height=44, corner_radius=10)

        self.btn_create.grid(row=2, column=0, padx=16, pady=(4,6))
        self.btn_display.grid(row=3, column=0, padx=16, pady=6)
        self.btn_deposit.grid(row=4, column=0, padx=16, pady=6)
        self.btn_withdraw.grid(row=5, column=0, padx=16, pady=6)
        self.btn_delete.grid(row=6, column=0, padx=16, pady=6)
        self.btn_export.grid(row=7, column=0, padx=16, pady=6)
        self.btn_exit.grid(row=9, column=0, padx=16, pady=20)

    # ------------------ Topbar -------------------
    def _create_topbar(self):
        self.topbar = ctk.CTkFrame(self, height=70, corner_radius=10,fg_color="#000000")
        self.topbar.grid(row=0, column=1, sticky="new", padx=(0,14), pady=(14,50))
        self.topbar.grid_columnconfigure(0, weight=1)
        self.lbl_page = ctk.CTkLabel(self.topbar, text="Create Account", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_page.grid(row=0, column=0, padx=16, pady=12, sticky="w")
        self.lbl_status = ctk.CTkLabel(self.topbar, text="Welcome — select an action from the left", font=ctk.CTkFont(size=11))
        self.lbl_status.grid(row=1, column=0, padx=16, sticky="w")

    # ---------------- Content Area ----------------
    def _create_content_area(self):
        self.content = ctk.CTkFrame(self, corner_radius=0,fg_color="#000000")
        self.content.grid(row=0, column=1, sticky="nswe", padx=(0,14), pady=(84,14))
        self.content.grid_columnconfigure(0, weight=1)

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()
    # ---------------- Create Account Page ----------------
    def show_create_account(self):
        self.lbl_page.configure(text="Create Account")
        self.lbl_status.configure(text="Create a new customer account")
        self.clear_content()

        card = ctk.CTkFrame(self.content, corner_radius=12, fg_color="#000000")
        card.pack(padx=24, pady=18, fill="both", expand=True)

        form_frame = ctk.CTkFrame(card, fg_color="#000000", corner_radius=10, width=620, height=380)
        form_frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(form_frame, text="New Account", font=ctk.CTkFont(size=25, weight="bold")).place(x=18, y=14)

        # Form fields
        lbl_name = ctk.CTkLabel(form_frame, text="Full Name")
        lbl_name.place(x=20, y=64)
        self.e_name = ctk.CTkEntry(form_frame, width=260, placeholder_text="e.g. Aisha Sharma")
        self.e_name.place(x=20, y=92)

        lbl_age = ctk.CTkLabel(form_frame, text="Age")
        lbl_age.place(x=320, y=64)
        self.e_age = ctk.CTkEntry(form_frame, width=120, placeholder_text="18")
        self.e_age.place(x=320, y=92)

        lbl_gender = ctk.CTkLabel(form_frame, text="Gender")
        lbl_gender.place(x=460, y=64)
        self.e_gender = ctk.CTkEntry(form_frame, width=120, placeholder_text="M / F")
        self.e_gender.place(x=460, y=92)

        lbl_dep = ctk.CTkLabel(form_frame, text="Initial Deposit (₹)")
        lbl_dep.place(x=20, y=140)
        self.e_deposit = ctk.CTkEntry(form_frame, width=200, placeholder_text="0.00")
        self.e_deposit.place(x=20, y=168)

        # Submit button
        btn_create = ctk.CTkButton(form_frame, text="Create Account", width=220, height=44,
                                   fg_color="#6a00ff", hover_color="#8922ff", corner_radius=12,
                                   command=self.create_account_action)
        btn_create.place(x=360, y=160)

        # Tip note
        note = ctk.CTkFrame(form_frame, corner_radius=8, fg_color="#3DAE66", width=560, height=110)
        note.place(x=20, y=230)
        nlabel = ctk.CTkLabel(note, text="Tip: Account number is generated automatically and shown after creation.",
                              wraplength=520, justify="left")
        nlabel.place(x=12, y=12)

    def create_account_action(self):
        name = self.e_name.get().strip()
        age = self.e_age.get().strip()
        gender = self.e_gender.get().strip()
        deposit = self.e_deposit.get().strip()

        if not (name and age and gender and deposit):
            messagebox.showerror("Validation Error", "All fields are required.")
            return
        try:
            age_i = int(age)
            deposit_f = float(deposit)
        except ValueError:
            messagebox.showerror("Validation Error", "Age and deposit must be numbers.")
            return

        # retry for unique account number
        for _ in range(5):
            acc_no = random.randint(10000, 99999)
            try:
                db_cursor.execute(
                    "INSERT INTO accounts (acc_no, name, age, gender, balance) VALUES (%s,%s,%s,%s,%s)",
                    (acc_no, name, age_i, gender, deposit_f)
                )
                db_conn.commit()
                break
            except k.IntegrityError:
                continue
        else:
            messagebox.showerror("DB Error", "Could not generate unique account number.")
            return

        messagebox.showinfo("Account Created", f"Account successfully created!\nAccount Number: {acc_no}")
        self.lbl_status.configure(text=f"Created account #{acc_no}")
        self.e_name.delete(0, "end")
        self.e_age.delete(0, "end")
        self.e_gender.delete(0, "end")
        self.e_deposit.delete(0, "end")

    # ---------------- Display Account Page ----------------
    def show_display_account(self):
        self.lbl_page.configure(text="Display Account")
        self.lbl_status.configure(text="Look up account details")
        self.clear_content()

        card = ctk.CTkFrame(self.content, corner_radius=12, fg_color="#000000")
        card.pack(padx=24, pady=18, fill="both", expand=True)

        frame = ctk.CTkFrame(card, fg_color="#000000", corner_radius=8, width=700, height=320)
        frame.place(relx=0.5, rely=0.45, anchor="center")

        ctk.CTkLabel(frame, text="Search Account", font=ctk.CTkFont(size=25, weight="bold")).place(x=20, y=12)
        ctk.CTkLabel(frame, text="Account Number").place(x=20, y=58)
        self.e_search_acc = ctk.CTkEntry(frame, width=200, placeholder_text="12345")
        self.e_search_acc.place(x=20, y=86)

        btn_find = ctk.CTkButton(frame, text="Find", width=120, command=self.display_account_action,
                                 fg_color="#00aaff", hover_color="#00c0ff", corner_radius=10)
        btn_find.place(x=240, y=84)

        # Results area
        self.result_card = ctk.CTkFrame(frame, corner_radius=8, fg_color="#000000", width=660, height=150)
        self.result_card.place(x=20, y=140)
        self.result_label = ctk.CTkLabel(self.result_card, text="No results yet.", justify="left", wraplength=620)
        self.result_label.place(x=12, y=12)

    def display_account_action(self):
        acc = self.e_search_acc.get().strip()
        if not acc:
            messagebox.showerror("Validation Error", "Enter account number.")
            return
        try:
            acc_i = int(acc)
        except ValueError:
            messagebox.showerror("Validation Error", "Account number must be numeric.")
            return

        try:
            db_cursor.execute("SELECT acc_no, name, age, gender, balance FROM accounts WHERE acc_no=%s", (acc_i,))
            res = db_cursor.fetchone()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not fetch data:\n{e}")
            return

        if not res:
            self.result_label.configure(text="Account not found.")
            self.lbl_status.configure(text="Account lookup failed")
            return

        txt = (f"Account No: {res[0]}\n"
               f"Name      : {res[1]}\n"
               f"Age       : {res[2]}\n"
               f"Gender    : {res[3]}\n"
               f"Balance   : ₹{res[4]:.2f}")
        self.result_label.configure(text=txt)
        self.lbl_status.configure(text=f"Displayed account #{res[0]}")

    # ---------------- Deposit Money Page ----------------
    def show_deposit(self):
        self.lbl_page.configure(text="Deposit Money")
        self.lbl_status.configure(text="Add money to an account")
        self.clear_content()

        card = ctk.CTkFrame(self.content, corner_radius=12, fg_color="#000000")
        card.pack(padx=24, pady=18, fill="both", expand=True)

        f = ctk.CTkFrame(card, fg_color="#5F7A69", corner_radius=8, width=640, height=260)
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="Deposit", font=ctk.CTkFont(size=25, weight="bold")).place(x=20, y=12)
        ctk.CTkLabel(f, text="Account Number").place(x=20, y=58)
        self.e_deposit_acc = ctk.CTkEntry(f, width=200)
        self.e_deposit_acc.place(x=20, y=86)

        ctk.CTkLabel(f, text="Amount (₹)").place(x=240, y=58)
        self.e_deposit_amt = ctk.CTkEntry(f, width=200)
        self.e_deposit_amt.place(x=240, y=86)

        btn_deposit = ctk.CTkButton(f, text="Deposit", width=160, fg_color="#50ae97", hover_color="#58c5ab",
                                    command=self.deposit_action, corner_radius=10)
        btn_deposit.place(x=450, y=87)

    def deposit_action(self):
        acc = self.e_deposit_acc.get().strip()
        amt = self.e_deposit_amt.get().strip()
        if not (acc and amt):
            messagebox.showerror("Validation Error", "All fields are required.")
            return
        try:
            acc_i = int(acc)
            amt_f = float(amt)
            if amt_f <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid account or amount.")
            return

        # Transaction-safe deposit
        try:
            db_conn.start_transaction()
            db_cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s FOR UPDATE", (acc_i,))
            row = db_cursor.fetchone()
            if not row:
                messagebox.showerror("Not Found", "Account does not exist.")
                db_conn.rollback()
                return
            new_bal = float(row[0]) + amt_f
            db_cursor.execute("UPDATE accounts SET balance=%s WHERE acc_no=%s", (new_bal, acc_i))
            db_conn.commit()
        except Exception as e:
            db_conn.rollback()
            messagebox.showerror("DB Error", f"Could not deposit:\n{e}")
            return

        messagebox.showinfo("Deposited", f"₹{amt_f:.2f} deposited to account #{acc_i}.\nNew Balance: ₹{new_bal:.2f}")
        self.lbl_status.configure(text=f"Deposited ₹{amt_f:.2f} to #{acc_i}")
        self.e_deposit_acc.delete(0, "end")
        self.e_deposit_amt.delete(0, "end")

    # ---------------- Withdraw Money Page ----------------
    def show_withdraw(self):
        self.lbl_page.configure(text="Withdraw Money")
        self.lbl_status.configure(text="Withdraw from an account")
        self.clear_content()

        card = ctk.CTkFrame(self.content, corner_radius=12, fg_color="#000000")
        card.pack(padx=24, pady=18, fill="both", expand=True)

        f = ctk.CTkFrame(card, fg_color="#5F7A69", corner_radius=8, width=640, height=260)
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="Withdraw", font=ctk.CTkFont(size=25, weight="bold")).place(x=20, y=12)
        ctk.CTkLabel(f, text="Account Number").place(x=20, y=58)
        self.e_withdraw_acc = ctk.CTkEntry(f, width=200)
        self.e_withdraw_acc.place(x=20, y=86)

        ctk.CTkLabel(f, text="Amount (₹)").place(x=240, y=58)
        self.e_withdraw_amt = ctk.CTkEntry(f, width=200)
        self.e_withdraw_amt.place(x=240, y=86)

        btn_with = ctk.CTkButton(f, text="Withdraw", width=160, fg_color="#ff9a00", hover_color="#ffb33a",
                                 command=self.withdraw_action, corner_radius=10)
        btn_with.place(x=450, y=87)

    def withdraw_action(self):
        acc = self.e_withdraw_acc.get().strip()
        amt = self.e_withdraw_amt.get().strip()
        if not (acc and amt):
            messagebox.showerror("Validation Error", "All fields are required.")
            return
        try:
            acc_i = int(acc)
            amt_f = float(amt)
            if amt_f <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid account or amount.")
            return

        # Transaction-safe withdraw
        try:
            db_conn.start_transaction()
            db_cursor.execute("SELECT balance FROM accounts WHERE acc_no=%s FOR UPDATE", (acc_i,))
            row = db_cursor.fetchone()
            if not row:
                messagebox.showerror("Not Found", "Account does not exist.")
                db_conn.rollback()
                return
            current = float(row[0])
            if amt_f > current:
                messagebox.showerror("Insufficient Funds", "Cannot withdraw more than the current balance.")
                db_conn.rollback()
                return
            new_bal = current - amt_f
            db_cursor.execute("UPDATE accounts SET balance=%s WHERE acc_no=%s", (new_bal, acc_i))
            db_conn.commit()
        except Exception as e:
            db_conn.rollback()
            messagebox.showerror("DB Error", f"Could not withdraw:\n{e}")
            return

        messagebox.showinfo("Withdrawn", f"₹{amt_f:.2f} withdrawn from account #{acc_i}.\nRemaining Balance: ₹{new_bal:.2f}")
        self.lbl_status.configure(text=f"Withdrew ₹{amt_f:.2f} from #{acc_i}")
        self.e_withdraw_acc.delete(0, "end")
        self.e_withdraw_amt.delete(0, "end")

    # ---------------- Delete Account Page ----------------
    def show_delete(self):
        self.lbl_page.configure(text="Delete Account")
        self.lbl_status.configure(text="Permanently remove an account")
        self.clear_content()

        card = ctk.CTkFrame(self.content, corner_radius=18, fg_color="#000000")
        card.pack(padx=24, pady=18, fill="both", expand=True)

        f = ctk.CTkFrame(card, fg_color="#5A0000", corner_radius=8, width=520, height=200)
        f.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(f, text="Delete Account", font=ctk.CTkFont(size=25, weight="bold")).place(x=20, y=12)
        ctk.CTkLabel(f, text="Account Number").place(x=20, y=58)
        self.e_delete_acc = ctk.CTkEntry(f, width=200)
        self.e_delete_acc.place(x=20, y=86)

        btn_del = ctk.CTkButton(f, text="Delete Account", width=180, fg_color="#ff4d4d", hover_color="#ff6b6b",
                                command=self.delete_action, corner_radius=10)
        btn_del.place(x=260, y=82)

    def delete_action(self):
        acc = self.e_delete_acc.get().strip()
        if not acc:
            messagebox.showerror("Validation Error", "Enter account number.")
            return
        try:
            acc_i = int(acc)
        except ValueError:
            messagebox.showerror("Validation Error", "Invalid account number.")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete account #{acc_i}? This cannot be undone.")
        if not confirm:
            return

        try:
            db_cursor.execute("SELECT acc_no FROM accounts WHERE acc_no=%s", (acc_i,))
            if not db_cursor.fetchone():
                messagebox.showinfo("Not Found", "Account not found.")
                return
            db_cursor.execute("DELETE FROM accounts WHERE acc_no=%s", (acc_i,))
            db_conn.commit()
        except Exception as e:
            db_conn.rollback()
            messagebox.showerror("DB Error", f"Could not delete account:\n{e}")
            return

        messagebox.showinfo("Deleted", f"Account #{acc_i} deleted.")
        self.lbl_status.configure(text=f"Deleted account #{acc_i}")
        self.e_delete_acc.delete(0, "end")

    # ---------------- Export CSV ----------------
    def export_csv(self):
        try:
            db_cursor.execute("SELECT acc_no, name, age, gender, balance FROM accounts")
            rows = db_cursor.fetchall()
        except Exception as e:
            messagebox.showerror("DB Error", f"Could not read data:\n{e}")
            return

        if not rows:
            messagebox.showinfo("No Data", "No accounts to export.")
            return

        # --- Save to CSV ---
        try:
            with open("bank_backup.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Account No", "Name", "Age", "Gender", "Balance"])
                writer.writerows(rows)
        except Exception as e:
            messagebox.showerror("File Error", f"Could not write CSV:\n{e}")
            return

        self.lbl_status.configure(text="Exported data to CSV")

        # --- Display in a Scrollable Popup Table ---
        popup = ctk.CTkToplevel(self)
        popup.title("All Accounts")
        popup.geometry("750x400")

        # Make the popup appear on top of the main window
        popup.transient(self)     # ties it to main window
        popup.grab_set()          # makes popup modal
        popup.focus_force()       # force focus
        popup.lift()              # bring to front

        # Scrollable frame setup
        canvas = ctk.CTkCanvas(popup, bg="#000000", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ctk.CTkScrollbar(popup, orientation="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        table_frame = ctk.CTkFrame(canvas, corner_radius=10, fg_color="#000000")
        canvas.create_window((0, 0), window=table_frame, anchor="nw")

        # Headers (still labels)
        headers = ["Acc No", "Name", "Age", "Gender", "Balance"]
        for c, h in enumerate(headers):
            lbl = ctk.CTkLabel(table_frame, text=h, font=ctk.CTkFont(weight="bold"))
            lbl.grid(row=0, column=c, padx=8, pady=6)

        # Data rows (CTkEntry for copyable data)
        for r, row in enumerate(rows, start=1):
            for c, val in enumerate(row):
                entry = ctk.CTkEntry(table_frame, width=120, fg_color="#000000", border_width=0, text_color="white")
                entry.grid(row=r, column=c, padx=8, pady=4)
                entry.insert(0, str(val))
                entry.configure(state="readonly")  # makes it readonly but selectable

                # Update scroll region
        table_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        messagebox.showinfo("Exported", "Saved backup as 'bank_backup.csv' and displayed all accounts.")

    # ---------------- Close Handler ----------------
    def _on_close(self):
        try:
            if db_cursor:
                db_cursor.close()
            if db_conn:
                db_conn.close()
        except Exception:
            pass
        self.destroy()

# ----------------- Run App -----------------
if __name__ == "__main__":
    app = BankApp()
    app.mainloop()

# Thank You!!