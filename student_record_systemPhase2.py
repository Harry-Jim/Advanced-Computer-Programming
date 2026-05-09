import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class StudentRecordSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record System")
        self.root.geometry("1100x720")
        self.root.configure(bg="white")

        self.file = "students.json"
        self.students = self.load_data()
        self.student_grades = self.load_grades_data()

        # Header
        header = tk.Frame(root, bg="#2C2C2C", height=75)
        header.pack(fill="x")
        tk.Label(header, text="💾", font=("Arial", 32), bg="#2C2C2C", fg="white").pack(side="left", padx=40, pady=12)
        tk.Label(header, text="Student Record System", font=("Arial", 24, "bold"), bg="#2C2C2C", fg="white").pack(side="left", pady=12)

        # Sidebar
        menu = tk.Frame(root, bg="#F8F8F8", width=260)
        menu.pack(side="right", fill="y", padx=(0, 30), pady=(20, 0))
        tk.Label(menu, text="MENU", font=("Arial", 16, "bold"), bg="#F8F8F8", fg="#2C2C2C").pack(pady=(20,15), padx=35, anchor="w")
        for text, cmd in [
            ("📁 Dashboard", self.dashboard),
            ("👥 Students", self.students_menu),
            ("📚 Subjects / Grades", self.open_subjects_grades),
            ("➕ Add Students", self.open_add_student_form),
            ("🗑️ Delete Students", self.delete_students)
        ]:
            tk.Button(menu, text=text, font=("Arial", 12), bg="#F8F8F8", fg="#2C2C2C",
                      anchor="w", relief="flat", padx=35, pady=11, command=cmd).pack(fill="x", pady=2)

        # Main Dashboard
        main = tk.Frame(root, bg="white")
        main.pack(fill="both", expand=True, padx=180, pady=50)
        tk.Label(main, text="👤", font=("Arial", 155), bg="white", fg="#1a1a1a").grid(row=1, column=1, pady=30)
        style = {"font": ("Arial", 14, "bold"), "bg": "#2C2C2C", "fg": "white", "width": 20, "height": 2, "relief": "flat"}
        tk.Button(main, text="Add Students", **style, command=self.open_add_student_form).grid(row=0, column=0, padx=40, pady=18)
        tk.Button(main, text="Subjects / Grades", **style, command=self.open_subjects_grades).grid(row=0, column=2, padx=40, pady=18)
        tk.Button(main, text="List Of Students", **style, command=self.show_student_list).grid(row=2, column=0, padx=40, pady=18)
        tk.Button(main, text="Delete Students", **style, command=self.delete_students).grid(row=2, column=2, padx=40, pady=18)

    def load_data(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    data = json.load(f)
                    return data.get("students", [])
            except:
                return []
        return []

    def load_grades_data(self):
        if os.path.exists(self.file):
            try:
                with open(self.file, "r") as f:
                    data = json.load(f)
                    return data.get("grades", {})
            except:
                return {}
        return {}

    def save_data(self):
        data = {"students": self.students, "grades": self.student_grades}
        with open(self.file, "w") as f:
            json.dump(data, f, indent=4)

    # ====================== ADD STUDENT ======================
    def open_add_student_form(self):
        win = tk.Toplevel(self.root)
        win.title("Add New Students")
        win.geometry("620x580")
        win.configure(bg="white")
        win.grab_set()

        tk.Label(win, text="Add New Students", font=("Arial", 26, "bold"), bg="white", fg="#2C2C2C")\
            .pack(anchor="w", padx=60, pady=(40, 30))

        s = {"font": ("Arial", 12), "width": 38, "relief": "solid", "bd": 1}

        tk.Label(win, text="Full Name", bg="white").pack(anchor="w", padx=60, pady=(0,5))
        self.name_entry = tk.Entry(win, **s)
        self.name_entry.insert(0, "e.g. Harry Jim G. Pascua")
        self.name_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.name_entry, "e.g. Harry Jim G. Pascua"))
        self.name_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.name_entry, "e.g. Harry Jim G. Pascua"))
        self.name_entry.pack(anchor="w", padx=60, pady=(0,20), ipady=10)

        tk.Label(win, text="Student ID", bg="white").pack(anchor="w", padx=60, pady=(0,5))
        self.sid_entry = tk.Entry(win, **s)
        self.sid_entry.insert(0, "e.g. 25-00123")
        self.sid_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.sid_entry, "e.g. 25-00123"))
        self.sid_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.sid_entry, "e.g. 25-00123"))
        self.sid_entry.pack(anchor="w", padx=60, pady=(0,20), ipady=10)

        tk.Label(win, text="Program", bg="white").pack(anchor="w", padx=60, pady=(0,5))
        self.prog_entry = tk.Entry(win, **s)
        self.prog_entry.insert(0, "e.g. BS Computer Science")
        self.prog_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.prog_entry, "e.g. BS Computer Science"))
        self.prog_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.prog_entry, "e.g. BS Computer Science"))
        self.prog_entry.pack(anchor="w", padx=60, pady=(0,30), ipady=10)

        btnf = tk.Frame(win, bg="white")
        btnf.pack(fill="x", padx=60, pady=30)

        tk.Button(btnf, text="ADD", bg="#2C2C2C", fg="white", font=("Arial",12,"bold"), width=14, height=2,
                  command=lambda: self.save_student(win)).pack(side="left")

        tk.Button(btnf, text="CLEAR", bg="white", fg="#2C2C2C", font=("Arial",12,"bold"), width=12, height=2, relief="solid", bd=2,
                  command=self.clear_add_form).pack(side="right", padx=5)
        tk.Button(btnf, text="BACK", bg="white", fg="#2C2C2C", font=("Arial",12,"bold"), width=12, height=2, relief="solid", bd=2,
                  command=win.destroy).pack(side="right", padx=5)

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def restore_placeholder(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="gray")

    def save_student(self, win):
        name = self.name_entry.get().strip()
        sid = self.sid_entry.get().strip()
        prog = self.prog_entry.get().strip()

        if name and sid and prog and sid != "e.g. 25-00123":
            self.students.append({"id": sid, "name": name, "program": prog, "average": "", "remarks": ""})
            self.save_data()
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
            win.destroy()
        else:
            messagebox.showwarning("Error", "Please fill all fields correctly.")

    def clear_add_form(self):
        self.name_entry.delete(0, tk.END)
        self.sid_entry.delete(0, tk.END)
        self.prog_entry.delete(0, tk.END)

    # ====================== LIST OF STUDENTS ======================
    def show_student_list(self):
        win = tk.Toplevel(self.root)
        win.title("List Of Students")
        win.geometry("950x620")
        win.configure(bg="white")
        win.grab_set()

        tk.Label(win, text="List Of Students", font=("Arial", 26, "bold"), bg="white", fg="#2C2C2C")\
            .pack(anchor="w", padx=50, pady=(30,15))

        tk.Entry(win, font=("Arial",12), width=40, relief="solid", bd=1).pack(anchor="w", padx=50, pady=10, ipady=8)

        columns = ("ID", "Name", "Course", "Average", "Remarks")
        tree = ttk.Treeview(win, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140 if col in ["ID", "Average"] else 180)

        for s in self.students:
            tree.insert("", "end", values=(
                s.get("id", ""),
                s.get("name", ""),
                s.get("program", ""),
                s.get("average", "—"),
                s.get("remarks", "—")
            ))

        tree.pack(fill="both", expand=True, padx=50, pady=10)

        tk.Button(win, text="BACK", bg="#2C2C2C", fg="white", font=("Arial",12,"bold"), width=14, height=2,
                  command=win.destroy).pack(side="right", padx=60, pady=20)

    # ====================== SUBJECT / GRADE ======================
    def open_subjects_grades(self):
        win = tk.Toplevel(self.root)
        win.title("Subject / Grade")
        win.geometry("820x680")
        win.configure(bg="#F5F5F5")
        win.grab_set()

        tk.Label(win, text="Subject / Grade", font=("Arial", 26, "bold"), bg="#F5F5F5", fg="#2C2C2C")\
            .pack(anchor="w", padx=50, pady=(30,10))

        sf = tk.Frame(win, bg="#F5F5F5")
        sf.pack(fill="x", padx=50, pady=10)

        self.sid_entry = tk.Entry(sf, font=("Arial", 12), width=40, relief="solid", bd=1)
        self.sid_entry.insert(0, "Enter Student ID")
        self.sid_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.sid_entry, "Enter Student ID"))
        self.sid_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.sid_entry, "Enter Student ID"))
        self.sid_entry.pack(side="left", ipady=8)

        tk.Button(sf, text="LOAD GRADES", bg="#2C2C2C", fg="white", font=("Arial",11,"bold"), width=15, height=2,
                  command=self.load_grades).pack(side="left", padx=15)

        self.selected_label = tk.Label(win, text="Selected Student: None", bg="#F5F5F5", fg="#2C2C2C", font=("Arial",11))
        self.selected_label.pack(anchor="w", padx=50, pady=(5,15))

        self.tree = ttk.Treeview(win, columns=("Subject", "Grade"), show="headings", height=10)
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Grade", text="Grade (Double-click to edit)")
        self.tree.column("Subject", width=400)
        self.tree.column("Grade", width=150, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=50, pady=10)

        self.tree.bind("<Double-1>", self.edit_cell)

        af = tk.Frame(win, bg="#F5F5F5")
        af.pack(fill="x", padx=50, pady=20)

        tk.Label(af, text="New Subject", bg="#F5F5F5").grid(row=0, column=0, sticky="w")
        self.sub_entry = tk.Entry(af, font=("Arial",12), width=30, relief="solid", bd=1)
        self.sub_entry.insert(0, "e.g. Web Development")
        self.sub_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.sub_entry, "e.g. Web Development"))
        self.sub_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.sub_entry, "e.g. Web Development"))
        self.sub_entry.grid(row=1, column=0, padx=(0,20), ipady=8)

        tk.Label(af, text="Grade (0-100)", bg="#F5F5F5").grid(row=0, column=1, sticky="w")
        self.grade_entry = tk.Entry(af, font=("Arial",12), width=12, relief="solid", bd=1)
        self.grade_entry.insert(0, "85")
        self.grade_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.grade_entry, "85"))
        self.grade_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.grade_entry, "85"))
        self.grade_entry.grid(row=1, column=1, padx=(0,20), ipady=8)

        tk.Button(af, text="ADD GRADE", bg="#2C2C2C", fg="white", font=("Arial",12,"bold"), width=15, height=2,
                  command=self.add_new_grade).grid(row=1, column=2)

        tk.Button(win, text="BACK", bg="#2C2C2C", fg="white", font=("Arial",12,"bold"), width=14, height=2,
                  command=win.destroy).pack(side="right", padx=60, pady=30)

    def edit_cell(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        column = self.tree.identify_column(event.x)
        if column not in ("#1", "#2"):
            return

        item_id = selected[0]
        current_values = self.tree.item(item_id, "values")
        sid = self.sid_entry.get().strip()

        if not sid or sid == "Enter Student ID":
            messagebox.showwarning("Error", "Please load a student first")
            return

        edit_win = tk.Toplevel(self.root)
        edit_win.title("Edit")
        edit_win.geometry("350x180")
        edit_win.grab_set()

        field = "Subject" if column == "#1" else "Grade"
        tk.Label(edit_win, text=f"Edit {field}:", font=("Arial", 12)).pack(pady=10)

        entry = tk.Entry(edit_win, font=("Arial", 12), width=25)
        entry.insert(0, current_values[0 if column == "#1" else 1])
        entry.pack(pady=8)

        def save_edit():
            new_value = entry.get().strip()
            if not new_value:
                messagebox.showwarning("Error", "Cannot be empty")
                return

            if column == "#1":  # Subject
                for g in self.student_grades.get(sid, []):
                    if g["subject"] == current_values[0]:
                        g["subject"] = new_value
                        break
            else:  # Grade
                try:
                    grade = int(new_value)
                    if not 0 <= grade <= 100:
                        raise ValueError
                    for g in self.student_grades.get(sid, []):
                        if g["subject"] == current_values[0]:
                            g["grade"] = grade
                            break
                except:
                    messagebox.showwarning("Error", "Grade must be 0-100")
                    return

            self.save_data()
            self.load_grades()
            self.update_average_and_remarks(sid)   # ← Updated here
            edit_win.destroy()
            messagebox.showinfo("Success", "Updated successfully!")

        tk.Button(edit_win, text="Save", bg="#2C2C2C", fg="white", command=save_edit).pack(pady=15)

    def load_grades(self):
        sid = self.sid_entry.get().strip()
        if not sid or sid == "Enter Student ID":
            messagebox.showwarning("Error", "Please enter a Student ID")
            return

        student = next((s for s in self.students if s["id"] == sid), None)
        if not student:
            messagebox.showwarning("Not Found", f"No student found with ID: {sid}")
            return

        self.selected_label.config(text=f"Selected Student: {student['name']} ({sid})")

        for item in self.tree.get_children():
            self.tree.delete(item)

        if sid in self.student_grades:
            for g in self.student_grades[sid]:
                self.tree.insert("", "end", values=(g["subject"], g["grade"]))

    def add_new_grade(self):
        sid = self.sid_entry.get().strip()
        subject = self.sub_entry.get().strip()
        grade_str = self.grade_entry.get().strip()

        if not sid or sid == "Enter Student ID":
            messagebox.showwarning("Error", "Please load a student first")
            return
        if not subject or subject == "e.g. Web Development" or not grade_str:
            messagebox.showwarning("Error", "Please enter subject and grade")
            return

        try:
            grade = int(grade_str)
            if not 0 <= grade <= 100:
                raise ValueError
        except:
            messagebox.showwarning("Error", "Grade must be a number between 0 and 100")
            return

        if sid not in self.student_grades:
            self.student_grades[sid] = []

        self.student_grades[sid].append({"subject": subject, "grade": grade})
        self.save_data()
        self.load_grades()
        self.update_average_and_remarks(sid)        # ← Updated here

        self.sub_entry.delete(0, tk.END)
        self.grade_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Added '{subject}' with grade {grade}")

    def update_average_and_remarks(self, sid):
        if sid not in self.student_grades or not self.student_grades[sid]:
            return

        grades = [g["grade"] for g in self.student_grades[sid]]
        average = round(sum(grades) / len(grades), 2)
        remarks = "Pass" if average >= 75 else "Fail"

        for student in self.students:
            if student["id"] == sid:
                student["average"] = str(average)
                student["remarks"] = remarks
                break

        self.save_data()

    def delete_students(self):
        messagebox.showinfo("Delete Students", "Coming Soon")

    def dashboard(self):
        messagebox.showinfo("Dashboard", "Welcome")

    def students_menu(self):
        self.show_student_list()


# ====================== RUN ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordSystem(root)
    root.mainloop()