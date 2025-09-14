import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Google Sheets Setup ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1WfZh4mgFAF5TggTf0z7Dt34qQKq0QMgdmkQosvhBzf8/edit?usp=sharing"
CREDENTIALS_FILE = "credentials.json"

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
gc = gspread.authorize(creds)
sh = gc.open_by_url(SHEET_URL)
ws = sh.sheet1  # first sheet

# --- Headers & Columns ---
HEADERS = ["Cookie Name", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
           "Daily Avg", "Daily Mean", "Thur/Sat Totals", "Sales", "Projected Totals"]
DAY_COLS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# --- Sheet Functions ---
def get_all_data():
    all_rows = ws.get_all_values()
    records = []
    for row in all_rows[1:]:
        record = {HEADERS[i]: row[i] if i < len(row) else "" for i in range(len(HEADERS))}
        records.append(record)
    return records

def update_cookie_count(cookie_name, day, count):
    all_rows = ws.get_all_values()
    day_col = HEADERS.index(day) + 1
    row_index = None
    for i, row in enumerate(all_rows[1:], start=2):
        if row[0].strip().lower() == cookie_name.strip().lower():
            row_index = i
            break
    if row_index is None:
        new_row = [cookie_name] + [""] * (len(HEADERS)-1)
        ws.append_row(new_row)
        row_index = len(all_rows) + 1
    ws.update_cell(row_index, day_col, count)
    return True

def rename_cookie(old_name, new_name):
    all_rows = ws.get_all_values()
    row_index = None
    for i, row in enumerate(all_rows[1:], start=2):
        if row[0].strip().lower() == old_name.strip().lower():
            row_index = i
            break
    if row_index:
        ws.update_cell(row_index, 1, new_name)
        return True
    return False

def save_to_html():
    records = get_all_data()
    html = f"""<html>
<head><title>Cookie Totals</title></head>
<body>
<h1>Cookie Totals</h1>
<p>Last updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
<table border="1" cellpadding="5" cellspacing="0">
<tr>{''.join([f'<th>{h}</th>' for h in HEADERS])}</tr>
"""
    for r in records:
        try:
            mon, tue, wed = int(r["Monday"] or 0), int(r["Tuesday"] or 0), int(r["Wednesday"] or 0)
            avg = (mon + tue + wed) / 3
            r["Daily Avg"] = f"{avg:.1f}"
            proj = int(avg * 1.6)
            r["Projected Totals"] = proj
        except Exception:
            r["Daily Avg"] = ""
            r["Projected Totals"] = ""
        html += "<tr>" + "".join(f"<td>{r[h]}</td>" for h in HEADERS) + "</tr>\n"

    html += "</table></body></html>"
    with open("cookieweather.html", "w", encoding="utf-8") as f:
        f.write(html)
    messagebox.showinfo("Exported", "cookieweather.html has been generated!")

class CookieTrackerApp:
    def __init__(self, root):
        self.root = root
        root.title("Cookie Tracker")

        # Treeview
        self.tree = ttk.Treeview(root, columns=HEADERS, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        for col in HEADERS:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", stretch=True)

        # Input Frame
        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Cookie Name:").grid(row=0, column=0, sticky="w")
        self.cookie_entry = tk.Entry(input_frame)
        self.cookie_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Day:").grid(row=1, column=0, sticky="w")
        self.day_var = tk.StringVar()
        self.day_menu = ttk.Combobox(input_frame, textvariable=self.day_var, values=DAY_COLS)
        self.day_menu.grid(row=1, column=1)

        tk.Label(input_frame, text="Count:").grid(row=2, column=0, sticky="w")
        self.count_entry = tk.Entry(input_frame)
        self.count_entry.grid(row=2, column=1)

        tk.Button(input_frame, text="Update / Add", command=self.on_update).grid(row=3, column=0, columnspan=2, pady=5)

        # Buttons
        tk.Button(root, text="Refresh Data", command=self.load_data).pack(padx=10, pady=(0,5))
        tk.Button(root, text="Export HTML", command=save_to_html).pack(padx=10, pady=(0,5))
        tk.Button(root, text="Clear Table", fg="red", command=lambda: self.clear_table()).pack(padx=10, pady=(0,10))

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.on_double_click)
        self.edit_entry = None

        # Bind resize to adjust columns
        root.bind("<Configure>", self.resize_columns)

        self.load_data()

    def clear_table(self):
        """Reset cookie names and Mon–Sat counts to defaults."""
        all_rows = ws.get_all_values()
        num_rows = len(all_rows) - 1
        if num_rows <= 0:
            messagebox.showinfo("Info", "No rows to clear.")
            return

        # Cookie Name + Monday–Saturday counts = 7 columns
        batch_values = [[f"Example #{i+1}"] + [0]*6 for i in range(num_rows)]

        # Use named arguments to avoid DeprecationWarning
        ws.update(range_name=f"A2:G{num_rows+1}", values=batch_values)

        self.load_data()
        messagebox.showinfo("Cleared", "Cookie names and day counts reset.")



    def __init__(self, root):
        self.root = root
        root.title("Cookie Tracker")

        # Treeview
        self.tree = ttk.Treeview(root, columns=HEADERS, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=5)
        for col in HEADERS:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", stretch=True)

        # Input Frame
        input_frame = tk.Frame(root)
        input_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(input_frame, text="Cookie Name:").grid(row=0, column=0, sticky="w")
        self.cookie_entry = tk.Entry(input_frame)
        self.cookie_entry.grid(row=0, column=1)

        tk.Label(input_frame, text="Day:").grid(row=1, column=0, sticky="w")
        self.day_var = tk.StringVar()
        self.day_menu = ttk.Combobox(input_frame, textvariable=self.day_var, values=DAY_COLS)
        self.day_menu.grid(row=1, column=1)

        tk.Label(input_frame, text="Count:").grid(row=2, column=0, sticky="w")
        self.count_entry = tk.Entry(input_frame)
        self.count_entry.grid(row=2, column=1)

        tk.Button(input_frame, text="Update / Add", command=self.on_update).grid(row=3, column=0, columnspan=2, pady=5)

        # Buttons
        tk.Button(root, text="Refresh Data", command=self.load_data).pack(padx=10, pady=(0,5))
        tk.Button(root, text="Export HTML", command=save_to_html).pack(padx=10, pady=(0,5))
        # FIX: use self.clear_table
        tk.Button(root, text="Clear Table", command=self.clear_table, fg="red").pack(padx=10, pady=(0,10))

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.on_double_click)
        self.edit_entry = None

        # Bind resize to adjust columns
        root.bind("<Configure>", self.resize_columns)

        self.load_data()


    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            records = get_all_data()
            for r in records:
                self.tree.insert("", "end", values=[r[h] for h in HEADERS])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {e}")

    def on_update(self):
        cookie = self.cookie_entry.get().strip()
        day = self.day_var.get().strip()
        count = self.count_entry.get().strip()
        if not cookie or not day or not count.isdigit():
            messagebox.showerror("Error", "Enter valid Cookie Name, Day, and numeric Count")
            return
        update_cookie_count(cookie, day, int(count))
        self.load_data()

    def on_double_click(self, event):
        row_id = self.tree.focus()
        col = self.tree.identify_column(event.x)
        col_index = int(col.replace("#","")) - 1
        values = list(self.tree.item(row_id)['values'])
        if col_index < 0 or col_index >= len(values):
            return
        x, y, width, height = self.tree.bbox(row_id, f"#{col_index+1}")
        self.edit_entry = tk.Entry(self.tree)
        self.edit_entry.place(x=x, y=y, width=width, height=height)
        self.edit_entry.insert(0, values[col_index])
        self.edit_entry.focus()

        def save_edit(event=None):
            new_value = self.edit_entry.get().strip()
            self.edit_entry.destroy()
            old_cookie_name = values[0]
            try:
                if col_index == 0:  # Cookie Name
                    if old_cookie_name.strip().lower() != new_value.strip().lower():
                        if rename_cookie(old_cookie_name, new_value):
                            values[0] = new_value
                            self.tree.item(row_id, values=values)
                        else:
                            messagebox.showerror("Error", "Failed to rename cookie in sheet")
                            return
                elif HEADERS[col_index] in DAY_COLS:
                    update_cookie_count(values[0], HEADERS[col_index], int(new_value))
                    values[col_index] = new_value
                    self.tree.item(row_id, values=values)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update sheet: {e}")

        self.edit_entry.bind("<Return>", save_edit)
        self.edit_entry.bind("<FocusOut>", save_edit)

    def resize_columns(self, event=None):
        width = self.tree.winfo_width()
        n_cols = len(HEADERS)
        for col in HEADERS:
            self.tree.column(col, width=int(width / n_cols))

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x600")
    app = CookieTrackerApp(root)
    root.mainloop()
