import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class StudentRecordSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Record System")
        # Main dashboard is full screen
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="white")

        self.file = "students.json"
        self.students = self.load_data()
        self.student_grades = self.load_grades_data()

        # ====================== HEADER WITH CLOSE BUTTON ======================
        header = tk.Frame(root, bg="#2C2C2C", height=75)
        header.pack(fill="x")

        # Left side: Icon and Title
        left_header = tk.Frame(header, bg="#2C2C2C")
        left_header.pack(side="left", fill="y")
        tk.Label(left_header, text="💾", font=("Arial", 32), bg="#2C2C2C", fg="white").pack(side="left", padx=40, pady=12)
        tk.Label(left_header, text="Student Record System", font=("Arial", 24, "bold"), bg="#2C2C2C", fg="white").pack(side="left", pady=12)

        # Right side: Close button 
        right_header = tk.Frame(header, bg="#2C2C2C")
        right_header.pack(side="right", fill="y", padx=30)

        # White background, black border
        close_btn = tk.Button(right_header, text="✕", font=("Arial", 14, "bold"), 
                              bg="white", fg="black", relief="solid", bd=2,
                              width=2, height=1,  # Exact small size
                              cursor="hand2", command=self.close_system)
        close_btn.pack(pady=18)  

        # ====================== BODY CONTAINER ======================
        body_frame = tk.Frame(root, bg="white")
        body_frame.pack(fill="both", expand=True)

        # Sidebar
        menu = tk.Frame(body_frame, bg="#F8F8F8", width=260)
        menu.pack(side="right", fill="y", padx=(0, 30), pady=(20, 0))
        tk.Label(menu, text="MENU", font=("Arial", 16, "bold"), bg="#F8F8F8", fg="#2C2C2C").pack(pady=(20,15), padx=30, anchor="w")

        sidebar_items = [
            ("📁", "Dashboard", self.show_dashboard),
            ("👥", "Students", self.show_student_list),
            ("📚", "Subjects / Grades", self.show_subjects_grades),
            ("➕", "Add Students", self.show_add_student_form),
            ("🗑️", "Delete Students", self.show_delete_students)
        ]

        self.menu_buttons = []
        for icon, text, cmd in sidebar_items:
            item_frame = tk.Frame(menu, bg="#F8F8F8")
            item_frame.pack(fill="x", pady=2)

            icon_lbl = tk.Label(item_frame, text=icon, font=("Arial", 12), bg="#F8F8F8", fg="#2C2C2C", width=2, anchor="w")
            icon_lbl.pack(side="left", padx=(25, 0))

            btn = tk.Button(item_frame, text=text, font=("Arial", 12), bg="#F8F8F8", fg="#2C2C2C",
                      anchor="w", relief="flat", padx=5, pady=11, command=cmd)
            btn.pack(side="left", fill="x", expand=True)
            self.menu_buttons.append(btn)

        # ====================== MAIN CONTENT AREA ======================
        # This is where all modules will be displayed
        self.content_frame = tk.Frame(body_frame, bg="white")
        self.content_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        # Show dashboard by default
        self.show_dashboard()

    def clear_content(self):
        """Remove all widgets from the content area"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def close_system(self):
        if messagebox.askyesno("Exit", "Are you sure you want to close the system?"):
            self.root.destroy()

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

    # ====================== DASHBOARD ======================
    def show_dashboard(self):
        self.clear_content()

        main = tk.Frame(self.content_frame, bg="white")
        main.pack(fill="both", expand=True, padx=160, pady=50)
        tk.Label(main, text="👤", font=("Arial", 155), bg="white", fg="#1a1a1a").grid(row=1, column=1, pady=30)
        style = {"font": ("Arial", 14, "bold"), "bg": "#2C2C2C", "fg": "white", "width": 20, "height": 2, "relief": "flat"}
        tk.Button(main, text="Add Students", **style, command=self.show_add_student_form).grid(row=0, column=0, padx=40, pady=18)
        tk.Button(main, text="Subjects / Grades", **style, command=self.show_subjects_grades).grid(row=0, column=2, padx=40, pady=18)
        tk.Button(main, text="List Of Students", **style, command=self.show_student_list).grid(row=2, column=0, padx=40, pady=18)
        tk.Button(main, text="Delete Students", **style, command=self.show_delete_students).grid(row=2, column=2, padx=40, pady=18)

    # ====================== ADD STUDENT ======================
    def show_add_student_form(self):
        self.clear_content()

        main = tk.Frame(self.content_frame, bg="white")
        main.pack(fill="both", expand=True, padx=60, pady=30)

        tk.Label(main, text="Add New Students", font=("Arial", 26, "bold"), bg="white", fg="#2C2C2C")\
            .pack(anchor="w", pady=(0, 30))

        s = {"font": ("Arial", 12), "width": 38, "relief": "solid", "bd": 1}

        tk.Label(main, text="Full Name", bg="white").pack(anchor="w", pady=(0,5))
        self.name_entry = tk.Entry(main, **s)
        self.name_entry.insert(0, "e.g. Harry Jim G. Pascua")
        self.name_entry.config(fg="#AAAAAA")
        self.name_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.name_entry, "e.g. Harry Jim G. Pascua"))
        self.name_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.name_entry, "e.g. Harry Jim G. Pascua"))
        self.name_entry.pack(anchor="w", pady=(0,20), ipady=10)

        tk.Label(main, text="Student ID", bg="white").pack(anchor="w", pady=(0,5))
        self.sid_entry = tk.Entry(main, **s)
        self.sid_entry.insert(0, "e.g. 25-00123")
        self.sid_entry.config(fg="#AAAAAA")
        self.sid_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.sid_entry, "e.g. 25-00123"))
        self.sid_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.sid_entry, "e.g. 25-00123"))
        self.sid_entry.pack(anchor="w", pady=(0,20), ipady=10)

        tk.Label(main, text="Program", bg="white").pack(anchor="w", pady=(0,5))
        self.prog_entry = tk.Entry(main, **s)
        self.prog_entry.insert(0, "e.g. BS Computer Science")
        self.prog_entry.config(fg="#AAAAAA")
        self.prog_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.prog_entry, "e.g. BS Computer Science"))
        self.prog_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.prog_entry, "e.g. BS Computer Science"))
        self.prog_entry.pack(anchor="w", pady=(0,30), ipady=10)

        btnf = tk.Frame(main, bg="white")
        btnf.pack(fill="x", pady=30)

        tk.Button(btnf, text="ADD", bg="#2C2C2C", fg="white", font=("Arial",12,"bold"), width=14, height=2,
                  command=self.save_student).pack(side="left")

        tk.Button(btnf, text="CLEAR", bg="white", fg="#2C2C2C", font=("Arial",12,"bold"), width=12, height=2, relief="solid", bd=2,
                  command=self.clear_add_form).pack(side="right", padx=5)
        tk.Button(btnf, text="BACK", bg="white", fg="#2C2C2C", font=("Arial",12,"bold"), width=12, height=2, relief="solid", bd=2,
                  command=self.show_dashboard).pack(side="right", padx=5)

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def restore_placeholder(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            entry.config(fg="#AAAAAA")

    def save_student(self):
        name = self.name_entry.get().strip()
        sid = self.sid_entry.get().strip()
        prog = self.prog_entry.get().strip()

        if name and sid and prog and sid != "e.g. 25-00123":
            self.students.append({"id": sid, "name": name, "program": prog, "average": "", "remarks": ""})
            self.save_data()
            messagebox.showinfo("Success", f"Student '{name}' added successfully!")
            self.show_dashboard()
        else:
            messagebox.showwarning("Error", "Please fill all fields correctly.")

    def clear_add_form(self):
        self.name_entry.delete(0, tk.END)
        self.sid_entry.delete(0, tk.END)
        self.prog_entry.delete(0, tk.END)

    # ====================== LIST OF STUDENTS ======================
    def show_student_list(self):
        self.clear_content()

        main_frame = tk.Frame(self.content_frame, bg="white")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main_frame, text="List Of Students", font=("Arial", 22, "bold"), bg="white", fg="#2C2C2C")\
            .pack(anchor="w", pady=(0, 10))

        # Search bar
        search_frame = tk.Frame(main_frame, bg="white")
        search_frame.pack(anchor="w", pady=5)

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11), width=35, relief="solid", bd=1)
        search_entry.pack(side="left", ipady=6)
        search_entry.insert(0, "Search Student")
        search_entry.config(fg="#AAAAAA")

        def on_search_focus_in(event):
            if search_entry.get() == "Search Student":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="#2C2C2C")

        def on_search_focus_out(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Search Student")
                search_entry.config(fg="#AAAAAA")

        search_entry.bind("<FocusIn>", on_search_focus_in)
        search_entry.bind("<FocusOut>", on_search_focus_out)

        def do_search(*args):
            query = search_var.get().strip().lower()
            for item in tree.get_children():
                tree.delete(item)
            for s in self.students:
                sid = s.get("id", "").lower()
                name = s.get("name", "").lower()
                if query in sid or query in name:
                    tree.insert("", "end", values=(
                        s.get("id", ""),
                        s.get("name", ""),
                        s.get("program", ""),
                        s.get("average", "—"),
                        s.get("remarks", "—")
                    ))

        search_var.trace("w", do_search)
        search_entry.bind("<Return>", do_search)

        # Treeview with scrollbar
        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.pack(fill="both", expand=True, pady=10)

        columns = ("ID", "Name", "Course", "Average", "Remarks")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120 if col in ["ID", "Average"] else 160)

        for s in self.students:
            tree.insert("", "end", values=(
                s.get("id", ""),
                s.get("name", ""),
                s.get("program", ""),
                s.get("average", "—"),
                s.get("remarks", "—")
            ))

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Button frame 
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x", pady=(5, 0))

        tk.Button(btn_frame, text="BACK", bg="#2C2C2C", fg="white", font=("Arial", 11, "bold"), 
                  width=12, height=2, relief="flat", cursor="hand2", command=self.show_dashboard).pack(side="right")

    # ====================== SUBJECT / GRADE ======================
    def show_subjects_grades(self):
        self.clear_content()

        main_frame = tk.Frame(self.content_frame, bg="#F5F5F5")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(main_frame, text="Subject / Grade", font=("Arial", 22, "bold"), bg="#F5F5F5", fg="#2C2C2C")\
            .pack(anchor="w", pady=(0, 10))

        sf = tk.Frame(main_frame, bg="#F5F5F5")
        sf.pack(fill="x", pady=5)

        self.sg_sid_entry = tk.Entry(sf, font=("Arial", 11), width=35, relief="solid", bd=1)
        self.sg_sid_entry.insert(0, "Enter Student ID")
        self.sg_sid_entry.config(fg="#AAAAAA")
        self.sg_sid_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.sg_sid_entry, "Enter Student ID"))
        self.sg_sid_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.sg_sid_entry, "Enter Student ID"))
        self.sg_sid_entry.pack(side="left", ipady=6)

        tk.Button(sf, text="LOAD GRADES", bg="#2C2C2C", fg="white", font=("Arial", 10, "bold"), 
                  width=13, height=2, relief="flat", cursor="hand2", command=self.load_grades).pack(side="left", padx=10)

        self.selected_label = tk.Label(main_frame, text="Selected Student: None", bg="#F5F5F5", fg="#2C2C2C", font=("Arial", 10))
        self.selected_label.pack(anchor="w", pady=(3, 10))

        # Treeview
        tree_frame = tk.Frame(main_frame, bg="#F5F5F5")
        tree_frame.pack(fill="both", expand=True, pady=5)

        self.tree = ttk.Treeview(tree_frame, columns=("Subject", "Grade"), show="headings", height=8)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Grade", text="Grade (Double-click to edit)")
        self.tree.column("Subject", width=350)
        self.tree.column("Grade", width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", self.edit_cell)

        # Add grade section
        af = tk.Frame(main_frame, bg="#F5F5F5")
        af.pack(fill="x", pady=10)

        tk.Label(af, text="New Subject", bg="#F5F5F5", font=("Arial", 10)).grid(row=0, column=0, sticky="w")
        self.sub_entry = tk.Entry(af, font=("Arial", 11), width=28, relief="solid", bd=1)
        self.sub_entry.insert(0, "e.g. Web Development")
        self.sub_entry.config(fg="#AAAAAA")
        self.sub_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.sub_entry, "e.g. Web Development"))
        self.sub_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.sub_entry, "e.g. Web Development"))
        self.sub_entry.grid(row=1, column=0, padx=(0,15), ipady=6)

        tk.Label(af, text="Grade (0-100)", bg="#F5F5F5", font=("Arial", 10)).grid(row=0, column=1, sticky="w")
        self.grade_entry = tk.Entry(af, font=("Arial", 11), width=10, relief="solid", bd=1)
        self.grade_entry.insert(0, "85")
        self.grade_entry.config(fg="#AAAAAA")
        self.grade_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.grade_entry, "85"))
        self.grade_entry.bind("<FocusOut>", lambda e: self.restore_placeholder(self.grade_entry, "85"))
        self.grade_entry.grid(row=1, column=1, padx=(0,15), ipady=6)

        tk.Button(af, text="ADD GRADE", bg="#2C2C2C", fg="white", font=("Arial", 11, "bold"), 
                  width=12, height=2, relief="flat", cursor="hand2", command=self.add_new_grade).grid(row=1, column=2)

        # Button frame 
        btn_frame = tk.Frame(main_frame, bg="#F5F5F5")
        btn_frame.pack(fill="x", pady=(5, 0))

        tk.Button(btn_frame, text="BACK", bg="#2C2C2C", fg="white", font=("Arial", 11, "bold"), 
                  width=12, height=2, relief="flat", cursor="hand2", command=self.show_dashboard).pack(side="right")

    def edit_cell(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        column = self.tree.identify_column(event.x)
        if column not in ("#1", "#2"):
            return

        item_id = selected[0]
        current_values = self.tree.item(item_id, "values")
        sid = self.sg_sid_entry.get().strip()

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

            if column == "#1":
                for g in self.student_grades.get(sid, []):
                    if g["subject"] == current_values[0]:
                        g["subject"] = new_value
                        break
            else:
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
            self.update_average_and_remarks(sid)
            edit_win.destroy()
            messagebox.showinfo("Success", "Updated successfully!")

        tk.Button(edit_win, text="Save", bg="#2C2C2C", fg="white", command=save_edit).pack(pady=15)

    def load_grades(self):
        sid = self.sg_sid_entry.get().strip()
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
        sid = self.sg_sid_entry.get().strip()
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
        self.update_average_and_remarks(sid)

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

    # ====================== DELETE STUDENTS ======================
    def show_delete_students(self):
        self.clear_content()

        main_frame = tk.Frame(self.content_frame, bg="white")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Title
        tk.Label(main_frame, text="Delete Students", font=("Arial", 22, "bold"), bg="white", fg="#2C2C2C")\
            .pack(anchor="w", pady=(0, 10))

        # Search bar
        search_frame = tk.Frame(main_frame, bg="white")
        search_frame.pack(anchor="w", pady=5)

        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Arial", 11), 
                                width=35, relief="solid", bd=1)
        search_entry.pack(side="left", ipady=6)
        search_entry.insert(0, "Search Student")
        search_entry.config(fg="#AAAAAA")

        def on_search_focus_in(event):
            if search_entry.get() == "Search Student":
                search_entry.delete(0, tk.END)
                search_entry.config(fg="#2C2C2C")

        def on_search_focus_out(event):
            if search_entry.get() == "":
                search_entry.insert(0, "Search Student")
                search_entry.config(fg="#AAAAAA")

        search_entry.bind("<FocusIn>", on_search_focus_in)
        search_entry.bind("<FocusOut>", on_search_focus_out)

        # Treeview with scrollbar
        tree_frame = tk.Frame(main_frame, bg="white")
        tree_frame.pack(fill="both", expand=True, pady=10)

        # Treeview 
        columns = ("ID", "Name", "Course", "Action")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        # Configure columns with proper alignment
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Course", text="Course")
        tree.heading("Action", text="Action")

        tree.column("ID", width=120, anchor="w")
        tree.column("Name", width=220, anchor="w")
        tree.column("Course", width=220, anchor="w")
        tree.column("Action", width=100, anchor="center")

        # Style the treeview
        style = ttk.Style()
        style.configure("Treeview", 
                        font=("Arial", 11),
                        rowheight=30,
                        background="white",
                        fieldbackground="white")
        style.configure("Treeview.Heading",
                        font=("Arial", 11, "bold"),
                        background="#E8F4FD",
                        foreground="#2C2C2C")
        style.map("Treeview", background=[("selected", "#D6EAF8")])

        # Insert data
        for s in self.students:
            tree.insert("", "end", values=(
                s.get("id", ""),
                s.get("name", ""),
                s.get("program", ""),
                "DELETE"
            ), tags=("delete_row",))

        tree.tag_configure("delete_row", background="white")

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind double-click to delete
        def on_delete_click(event):
            selected = tree.selection()
            if not selected:
                return

            item = selected[0]
            values = tree.item(item, "values")
            if not values:
                return

            student_id = values[0]
            student_name = values[1]

            if messagebox.askyesno("Confirm Delete", 
                                   f"Are you sure you want to delete '{student_name}' (ID: {student_id})?"):
                # Remove from data
                self.students = [s for s in self.students if s.get("id") != student_id]
                if student_id in self.student_grades:
                    del self.student_grades[student_id]
                self.save_data()

                # Remove from tree
                tree.delete(item)
                messagebox.showinfo("Deleted", f"Student '{student_name}' has been deleted.")

        tree.bind("<Double-1>", on_delete_click)
        tree.bind("<Return>", on_delete_click)


        # BACK BUTTON 
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x", pady=(5, 0))

        back_btn = tk.Button(btn_frame, text="BACK", bg="#2C2C2C", fg="white", font=("Arial", 11, "bold"), 
                             width=12, height=2, relief="flat", cursor="hand2", command=self.show_dashboard)
        back_btn.pack(side="right")

        # Search functionality
        def do_search(*args):
            query = search_var.get().strip().lower()
            for item in tree.get_children():
                tree.delete(item)
            for s in self.students:
                sid = s.get("id", "").lower()
                name = s.get("name", "").lower()
                course = s.get("program", "").lower()
                if not query or query == "search student" or query in sid or query in name or query in course:
                    tree.insert("", "end", values=(
                        s.get("id", ""),
                        s.get("name", ""),
                        s.get("program", ""),
                        "DELETE"
                    ), tags=("delete_row",))

        search_var.trace("w", do_search)
        search_entry.bind("<Return>", do_search)


# ====================== RUN ======================
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRecordSystem(root)
    root.mainloop() 