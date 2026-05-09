import tkinter as tk
from tkinter import messagebox, ttk

class StudentRecordSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record System")
        self.root.geometry("1100x720")
        self.root.configure(bg="white")

        self.students = []

        # ==================== HEADER ====================
        header = tk.Frame(root, bg="#2C2C2C", height=75)
        header.pack(fill="x")

        tk.Label(header, text="💾", font=("Arial", 32), bg="#2C2C2C", fg="white").pack(side="left", padx=40, pady=12)
        tk.Label(header, text="Student Record System", font=("Arial", 24, "bold"), 
                 bg="#2C2C2C", fg="white").pack(side="left", pady=12)

        # ==================== SIDEBAR ====================
        menu_frame = tk.Frame(root, bg="#F8F8F8", width=260)
        menu_frame.pack(side="right", fill="y", padx=(0, 30), pady=(20, 0))

        tk.Label(menu_frame, text="MENU", font=("Arial", 16, "bold"), 
                 bg="#F8F8F8", fg="#2C2C2C").pack(pady=(20, 15), padx=35, anchor="w")

        menu_items = [
            ("📁   Dashboard", self.dashboard),
            ("👥   Students", self.students_menu),
            ("📚   Subjects / Grades", self.subjects_grades),
            ("➕   Add Students", self.open_add_student_form),
            ("🗑️   Delete Students", self.delete_students)
        ]

        for text, cmd in menu_items:
            tk.Button(menu_frame, text=text, font=("Arial", 12), bg="#F8F8F8", fg="#2C2C2C",
                      anchor="w", relief="flat", padx=35, pady=11, command=cmd).pack(fill="x", pady=2)

        # ==================== MAIN DASHBOARD ====================
        self.main_frame = tk.Frame(root, bg="white")
        self.main_frame.pack(fill="both", expand=True, padx=180, pady=50)

        tk.Label(self.main_frame, text="👤", font=("Arial", 155), bg="white", fg="#1a1a1a")\
            .grid(row=1, column=1, pady=30)

        btn_style = {"font": ("Arial", 14, "bold"), "bg": "#2C2C2C", "fg": "white", "width": 20, "height": 2, "relief": "flat"}

        tk.Button(self.main_frame, text="Add Students", **btn_style, command=self.open_add_student_form)\
            .grid(row=0, column=0, padx=40, pady=18)

        tk.Button(self.main_frame, text="Subjects / Grades", **btn_style, command=self.subjects_grades)\
            .grid(row=0, column=2, padx=40, pady=18)

        tk.Button(self.main_frame, text="List Of Students", **btn_style, command=self.show_student_list)\
            .grid(row=2, column=0, padx=40, pady=18)

        tk.Button(self.main_frame, text="Delete Students", **btn_style, command=self.delete_students)\
            .grid(row=2, column=2, padx=40, pady=18)

    # ====================== ADD NEW STUDENTS FORM ======================
    def open_add_student_form(self):
        form = tk.Toplevel(self.root)
        form.title("Add New Students")
        form.geometry("620x580")
        form.configure(bg="white")
        form.grab_set()

        # Title - Left aligned like your photo
        tk.Label(form, text="Add New Students", font=("Arial", 26, "bold"), bg="white", fg="#2C2C2C")\
            .pack(anchor="w", padx=60, pady=(40, 30))

        # Input Fields
        field_style = {"font": ("Arial", 12), "width": 38, "relief": "solid", "bd": 1}

        # Full Name
        tk.Label(form, text="Full Name", font=("Arial", 11), bg="white").pack(anchor="w", padx=60, pady=(0, 5))
        name_entry = tk.Entry(form, **field_style)
        name_entry.pack(anchor="w", padx=60, pady=(0, 20), ipady=10)

        # Student ID
        tk.Label(form, text="Student ID", font=("Arial", 11), bg="white").pack(anchor="w", padx=60, pady=(0, 5))
        id_entry = tk.Entry(form, **field_style)
        id_entry.pack(anchor="w", padx=60, pady=(0, 20), ipady=10)

        # Program
        tk.Label(form, text="Program", font=("Arial", 11), bg="white").pack(anchor="w", padx=60, pady=(0, 5))
        program_entry = tk.Entry(form, **field_style)
        program_entry.pack(anchor="w", padx=60, pady=(0, 30), ipady=10)

        # Buttons Area
        btn_frame = tk.Frame(form, bg="white")
        btn_frame.pack(fill="x", padx=60, pady=20)

        # ADD Button (Left side)
        tk.Button(btn_frame, text="ADD", font=("Arial", 12, "bold"), bg="#2C2C2C", fg="white",
                  width=14, height=2, relief="flat", command=lambda: self.save_student(name_entry, id_entry, program_entry, form))\
            .pack(side="left")

        # CLEAR and BACK Buttons (Right side)
        right_btns = tk.Frame(btn_frame, bg="white")
        right_btns.pack(side="right")

        tk.Button(right_btns, text="CLEAR", font=("Arial", 12, "bold"), bg="white", fg="#2C2C2C",
                  width=12, height=2, relief="solid", bd=2, command=lambda: self.clear_fields(name_entry, id_entry, program_entry))\
            .pack(side="left", padx=(0, 12))

        tk.Button(right_btns, text="BACK", font=("Arial", 12, "bold"), bg="white", fg="#2C2C2C",
                  width=12, height=2, relief="solid", bd=2, command=form.destroy)\
            .pack(side="left")

    def save_student(self, name_entry, id_entry, program_entry, form):
        name = name_entry.get().strip()
        sid = id_entry.get().strip()
        program = program_entry.get().strip()

        if name and sid and program:
            self.students.append({"id": sid, "name": name, "program": program})
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
            form.destroy()
        else:
            messagebox.showwarning("Error", "Please fill all three fields!")

    def clear_fields(self, name_entry, id_entry, program_entry):
        name_entry.delete(0, tk.END)
        id_entry.delete(0, tk.END)
        program_entry.delete(0, tk.END)

    # Other functions (unchanged)
    def show_student_list(self):
        if not self.students:
            messagebox.showinfo("List of Students", "No students added yet.")
            return

        win = tk.Toplevel(self.root)
        win.title("List of Students")
        win.geometry("700x500")

        tree = ttk.Treeview(win, columns=("ID", "Name", "Program"), show="headings")
        tree.heading("ID", text="Student ID")
        tree.heading("Name", text="Full Name")
        tree.heading("Program", text="Program")

        for s in self.students:
            tree.insert("", "end", values=(s["id"], s["name"], s.get("program", "")))

        tree.pack(padx=40, pady=40, fill="both", expand=True)

    def subjects_grades(self):
        messagebox.showinfo("Subjects / Grades", "Subjects and Grades Module")

    def delete_students(self):
        messagebox.showinfo("Delete Students", "Delete Students Module")

    def dashboard(self):
        messagebox.showinfo("Dashboard", "Dashboard")

    def students_menu(self):
        self.show_student_list()


# ====================== RUN ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordSystem(root)
    root.mainloop()