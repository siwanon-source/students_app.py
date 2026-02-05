import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

# =========================
# SQLite init
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "students.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    major TEXT NOT NULL
)
""")
conn.commit()

# =========================
# Functions (SQLite CRUD)
# =========================
def fetch_data():
    # clear table
    for row in tree.get_children():
        tree.delete(row)

    try:
        cursor.execute("SELECT id, name, age, major FROM students ORDER BY id DESC")
        for row in cursor.fetchall():
            tree.insert("", "end", values=row)
    except Exception as e:
        messagebox.showerror("Error", f"อ่านข้อมูลไม่ได้: {e}")

def add_data():
    name = name_var.get().strip()
    age = age_var.get().strip()
    major = major_var.get().strip()

    if not name or not age or not major:
        messagebox.showwarning("Warning", "กรุณากรอกข้อมูลให้ครบ")
        return

    try:
        age_int = int(age)
    except:
        messagebox.showwarning("Warning", "Age ต้องเป็นตัวเลขจำนวนเต็ม")
        return

    try:
        cursor.execute(
            "INSERT INTO students (name, age, major) VALUES (?, ?, ?)",
            (name, age_int, major)
        )
        conn.commit()
        fetch_data()
        clear_form()
    except Exception as e:
        messagebox.showerror("Error", f"เพิ่มข้อมูลไม่ได้: {e}")

def update_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "กรุณาเลือกข้อมูล")
        return

    values = tree.item(selected, "values")
    student_id = values[0]  # SQLite id

    name = name_var.get().strip()
    age = age_var.get().strip()
    major = major_var.get().strip()

    if not name or not age or not major:
        messagebox.showwarning("Warning", "กรุณากรอกข้อมูลให้ครบ")
        return

    try:
        age_int = int(age)
    except:
        messagebox.showwarning("Warning", "Age ต้องเป็นตัวเลขจำนวนเต็ม")
        return

    try:
        cursor.execute(
            "UPDATE students SET name=?, age=?, major=? WHERE id=?",
            (name, age_int, major, student_id)
        )
        conn.commit()
        fetch_data()
        clear_form()
    except Exception as e:
        messagebox.showerror("Error", f"แก้ไขข้อมูลไม่ได้: {e}")

def delete_data():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Warning", "กรุณาเลือกข้อมูล")
        return

    values = tree.item(selected, "values")
    student_id = values[0]

    if not messagebox.askyesno("Confirm", "ต้องการลบข้อมูลนี้ใช่ไหม?"):
        return

    try:
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        fetch_data()
        clear_form()
    except Exception as e:
        messagebox.showerror("Error", f"ลบข้อมูลไม่ได้: {e}")

def clear_form():
    name_var.set("")
    age_var.set("")
    major_var.set("")

def select_item(event):
    selected = tree.focus()
    if selected:
        student_id, name, age, major = tree.item(selected, "values")
        name_var.set(name)
        age_var.set(age)
        major_var.set(major)

def on_close():
    # ปิด DB ก่อนปิดโปรแกรม (มารยาทที่ดี)
    try:
        conn.close()
    except:
        pass
    root.destroy()

# =========================
# UI (Tkinter)
# =========================
root = tk.Tk()
root.title("CRUD Tkinter - SQLite (students)")
root.geometry("780x420")
root.protocol("WM_DELETE_WINDOW", on_close)

name_var = tk.StringVar()
age_var = tk.StringVar()
major_var = tk.StringVar()

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Name").grid(row=0, column=0, sticky="w")
tk.Entry(frame_form, textvariable=name_var, width=30).grid(row=0, column=1, padx=6)

tk.Label(frame_form, text="Age").grid(row=1, column=0, sticky="w")
tk.Entry(frame_form, textvariable=age_var, width=30).grid(row=1, column=1, padx=6)

tk.Label(frame_form, text="Major").grid(row=2, column=0, sticky="w")
tk.Entry(frame_form, textvariable=major_var, width=30).grid(row=2, column=1, padx=6)

frame_btn = tk.Frame(root)
frame_btn.pack(pady=10)

tk.Button(frame_btn, text="Add", width=10, command=add_data).grid(row=0, column=0, padx=5)
tk.Button(frame_btn, text="Update", width=10, command=update_data).grid(row=0, column=1, padx=5)
tk.Button(frame_btn, text="Delete", width=10, command=delete_data).grid(row=0, column=2, padx=5)
tk.Button(frame_btn, text="Clear", width=10, command=clear_form).grid(row=0, column=3, padx=5)
tk.Button(frame_btn, text="Refresh", width=10, command=fetch_data).grid(row=0, column=4, padx=5)

# Table (ID is numeric)
columns = ("ID", "Name", "Age", "Major")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.pack(fill="both", expand=True, padx=10, pady=5)

for col in columns:
    tree.heading(col, text=col)

tree.column("ID", width=80, anchor="center")
tree.column("Name", width=220)
tree.column("Age", width=80, anchor="center")
tree.column("Major", width=200)

tree.bind("<<TreeviewSelect>>", select_item)

fetch_data()
root.mainloop()
