import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime


def init_db():
    conn = sqlite3.connect('todo.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL,
            priority INTEGER NOT NULL,
            due_date TEXT,
            completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)),
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        
        self.task_var = tk.StringVar()
        self.priority_var = tk.StringVar(value="1")
        self.due_date_var = tk.StringVar()
        self.category_var = tk.StringVar()
        
        self.create_widgets()
        self.display_tasks()

    def create_widgets(self):
        tk.Label(self.root, text="Task:").grid(row=0, column=0)
        tk.Entry(self.root, textvariable=self.task_var).grid(row=0, column=1)

        tk.Label(self.root, text="Priority (1-5):").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.priority_var).grid(row=1, column=1)

        tk.Label(self.root, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.due_date_var).grid(row=2, column=1)

        tk.Label(self.root, text="Category:").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.category_var).grid(row=3, column=1)

        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=4, column=0, columnspan=2)
        
        self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=5, column=0, columnspan=2)
        
        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=6, column=0)
        tk.Button(self.root, text="Mark as Completed", command=self.mark_completed).grid(row=6, column=1)
        
    def add_task(self):
        task = self.task_var.get()
        priority = self.priority_var.get()
        due_date = self.due_date_var.get()
        category = self.category_var.get()

        if task and priority.isdigit():
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (task, priority, due_date, completed, category)
                VALUES (?, ?, ?, ?, ?)
            ''', (task, int(priority), due_date, False, category))
            conn.commit()
            conn.close()
            
            self.task_var.set("")
            self.priority_var.set("1")
            self.due_date_var.set("")
            self.category_var.set("")
            
            self.display_tasks()
        else:
            messagebox.showwarning("Invalid Input", "Please enter valid task and priority.")
        
    def display_tasks(self):
        self.task_listbox.delete(0, tk.END)
        
        conn = sqlite3.connect('todo.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
        conn.close()
        
        for task in tasks:
            self.task_listbox.insert(tk.END, f"{task[1]} (Priority: {task[2]})")
        
    def delete_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.task_listbox.get(selected_task_index)
            task_name = task.split(" (Priority: ")[0]
            
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute('DELETE FROM tasks WHERE task = ?', (task_name,))
            conn.commit()
            conn.close()
            
            self.display_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
        
    def mark_completed(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            task = self.task_listbox.get(selected_task_index)
            task_name = task.split(" (Priority: ")[0]
            
            conn = sqlite3.connect('todo.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE tasks SET completed = 1 WHERE task = ?', (task_name,))
            conn.commit()
            conn.close()
            
            self.display_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

# Main application
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
