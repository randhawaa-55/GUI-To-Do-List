import json
import tkinter as tk
from tkinter import messagebox, simpledialog


class ToDoList:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append({'task': task, 'completed': False})
        self.save_tasks()

    def update_task(self, index, task):
        if 0 <= index < len(self.tasks):
            self.tasks[index]['task'] = task
            self.save_tasks()

    def complete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index]['completed'] = True
            self.save_tasks()

    def delete_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()

    def list_tasks(self):
        for i, task in enumerate(self.tasks):
            status = 'Done' if task['completed'] else 'Not Done'
            print(f"{i}. {task['task']} [{status}]")

    def save_tasks(self):
        with open('tasks.json', 'w') as f:
            json.dump(self.tasks, f)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as f:
                self.tasks = json.load(f)
        except FileNotFoundError:
            self.tasks = []


class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.todo_list = ToDoList()

        self.task_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Task:").pack()
        tk.Entry(self.root, textvariable=self.task_var).pack()

        tk.Button(self.root, text="Add Task", command=self.add_task).pack()
        tk.Button(self.root, text="List Tasks", command=self.list_tasks).pack()

        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack()

    def add_task(self):
        task = self.task_var.get()
        if task:
            self.todo_list.add_task(task)
            self.task_var.set("")
            self.list_tasks()
        else:
            messagebox.showwarning("Warning", "Task cannot be empty")

    def list_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.todo_list.tasks):
            status = 'Done' if task['completed'] else 'Not Done'
            task_label = tk.Label(self.tasks_frame, text=f"{i}. {task['task']} [{status}]")
            task_label.grid(row=i, column=0)

            tk.Button(self.tasks_frame, text="Update", command=lambda i=i: self.update_task(i)).grid(row=i, column=1)
            tk.Button(self.tasks_frame, text="Done", command=lambda i=i: self.complete_task(i)).grid(row=i, column=2)
            tk.Button(self.tasks_frame, text="Delete", command=lambda i=i: self.delete_task(i)).grid(row=i, column=3)

    def update_task(self, index):
        new_task = simpledialog.askstring("Update Task", "Enter the new task:")
        if new_task:
            self.todo_list.update_task(index, new_task)
            self.list_tasks()

    def complete_task(self, index):
        self.todo_list.complete_task(index)
        self.list_tasks()

    def delete_task(self, index):
        self.todo_list.delete_task(index)
        self.list_tasks()


def main_cli():
    todo_list = ToDoList()
    while True:
        print("\nTo-Do List Application")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Complete Task")
        print("4. Delete Task")
        print("5. List Tasks")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            task = input("Enter the task: ")
            todo_list.add_task(task)
        elif choice == '2':
            index = int(input("Enter the task number to update: "))
            task = input("Enter the new task: ")
            todo_list.update_task(index, task)
        elif choice == '3':
            index = int(input("Enter the task number to complete: "))
            todo_list.complete_task(index)
        elif choice == '4':
            index = int(input("Enter the task number to delete: "))
            todo_list.delete_task(index)
        elif choice == '5':
            todo_list.list_tasks()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    use_gui = True  # Change to False to use CLI instead

    if use_gui:
        root = tk.Tk()
        app = ToDoApp(root)
        root.mainloop()
    else:
        main_cli()
