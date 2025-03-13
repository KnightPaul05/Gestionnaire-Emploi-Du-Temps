import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import os

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        self.root.geometry("400x500")
        
        self.tasks = []
        self.load_tasks()
        
        self.create_widgets()
    
    def create_widgets(self):
        self.task_label = tk.Label(self.root, text="Task Name:")
        self.task_label.pack(pady=5)
        
        self.task_entry = tk.Entry(self.root)
        self.task_entry.pack(pady=5)
        
        self.duration_label = tk.Label(self.root, text="Duration (minutes):")
        self.duration_label.pack(pady=5)
        
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.pack(pady=5)
        
        self.add_task_button = tk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.pack(pady=10)
        
        self.clear_tasks_button = tk.Button(self.root, text="Clear All Tasks", command=self.clear_tasks)
        self.clear_tasks_button.pack(pady=10)
        
        self.update_task_button = tk.Button(self.root, text="Update Task Progress", command=self.update_task_progress)
        self.update_task_button.pack(pady=10)
        
        self.task_list_frame = tk.Frame(self.root)
        self.task_list_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        self.task_list = tk.Listbox(self.task_list_frame)
        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.task_list_frame, orient="vertical")
        self.scrollbar.config(command=self.task_list.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_list.config(yscrollcommand=self.scrollbar.set)
        
        for task in self.tasks:
            self.task_list.insert(tk.END, f"{task['name']} - {task['duration']} minutes")
            self.create_progress_bar(task)
    
    def add_task(self):
        task_name = self.task_entry.get()
        duration = self.duration_entry.get()
        
        if not task_name or not duration:
            messagebox.showwarning("Input Error", "Please enter both task name and duration.")
            return
        
        try:
            duration = int(duration)
        except ValueError:
            messagebox.showwarning("Input Error", "Duration must be a number.")
            return
        
        task = {"name": task_name, "duration": duration, "progress": 0}
        self.tasks.append(task)
        
        self.task_list.insert(tk.END, f"{task_name} - {duration} minutes")
        self.create_progress_bar(task)
        
        self.task_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        
        self.save_tasks()
    
    def create_progress_bar(self, task):
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(pady=5, fill=tk.X)
        
        task_label = tk.Label(progress_frame, text=task["name"])
        task_label.pack(side=tk.LEFT, padx=5)
        
        progress_bar = ttk.Progressbar(progress_frame, maximum=task["duration"])
        progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.update_progress_bar(progress_bar, task)
    
    def update_progress_bar(self, progress_bar, task):
        if task["progress"] < task["duration"]:
            task["progress"] += 1
            progress_bar["value"] = task["progress"]
            self.root.after(60000, self.update_progress_bar, progress_bar, task)
    
    def update_task_progress(self):
        selected_task_index = self.task_list.curselection()
        if not selected_task_index:
            messagebox.showwarning("Selection Error", "Please select a task to update.")
            return
        
        selected_task_index = selected_task_index[0]
        task = self.tasks[selected_task_index]
        
        progress = tk.simpledialog.askinteger("Update Progress", f"Enter progress for {task['name']} (minutes):")
        if progress is None:
            return
        
        if progress < 0 or progress > task["duration"]:
            messagebox.showwarning("Input Error", "Progress must be between 0 and the task duration.")
            return
        
        task["progress"] = progress
        self.save_tasks()
        
        self.task_list.delete(selected_task_index)
        self.task_list.insert(selected_task_index, f"{task['name']} - {task['duration']} minutes")
        
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        
        for task in self.tasks:
            self.create_progress_bar(task)
    
    def save_tasks(self):
        with open("tasks.pkl", "wb") as f:
            pickle.dump(self.tasks, f)
    
    def load_tasks(self):
        if os.path.exists("tasks.pkl"):
            with open("tasks.pkl", "rb") as f:
                self.tasks = pickle.load(f)
    
    def clear_tasks(self):
        self.tasks = []
        self.task_list.delete(0, tk.END)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        self.save_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()