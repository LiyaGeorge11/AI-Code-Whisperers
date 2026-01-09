import tkinter as tk
from tkinter import messagebox

# ---------------- LOGIC ----------------
def format_todos(tasks, focus_mode=False):
    if not tasks:
        return "No tasks available."

    sections = {"Today": [], "Tomorrow": [], "Upcoming": []}

    for task in tasks:
        if not isinstance(task, str) or task.strip() == "":
            continue

        t = task.lower()
        priority = "High" if "!" in task or "urgent" in t else "Normal"

        if "urgent" in t or "today" in t or "now" in t:
            sections["Today"].append((task, priority))
        elif "tmrw" in t or "tomorrow" in t:
            sections["Tomorrow"].append((task, priority))
        elif "next week" in t:
            sections["Upcoming"].append((task, priority))
        else:
            sections["Upcoming"].append((task, priority))

    output = ""

    if focus_mode:
        output += "🔥 FOCUS MODE (Today + High Priority)\n\n"
        found = False
        for task, p in sections["Today"]:
            if p == "High":
                output += f"• {task}\n"
                found = True
        if not found:
            output += "No high-priority tasks for today."
    else:
        for sec, items in sections.items():
            output += f"{sec}:\n"
            if not items:
                output += "  None\n"
            for task, p in items:
                icon = "⚠️" if p == "High" else "✔️"
                output += f"  {icon} {task} [{p}]\n"
            output += "\n"

    return output


# ---------------- GUI ----------------
tasks = []

def add_task():
    task = task_entry.get()
    if task.strip() == "":
        messagebox.showwarning("Input Error", "Task cannot be empty.")
        return
    tasks.append(task)
    task_entry.delete(0, tk.END)
    status_label.config(text="Task added ✔", fg="#2ecc71")

def show_tasks():
    output_box.delete("1.0", tk.END)
    result = format_todos(tasks, focus_var.get())
    output_box.insert(tk.END, result)


root = tk.Tk()
root.title("Smart To-Do Formatter")
root.geometry("550x600")
root.configure(bg="#f4f6f8")

# Title
tk.Label(
    root,
    text="📝 Smart To-Do Formatter",
    font=("Helvetica", 18, "bold"),
    bg="#f4f6f8",
    fg="#34495e"
).pack(pady=15)

# Input Card
card = tk.Frame(root, bg="white", bd=2, relief="groove")
card.pack(padx=20, pady=10, fill="x")

tk.Label(card, text="Enter Task", font=("Arial", 11), bg="white").pack(pady=5)
task_entry = tk.Entry(card, width=45, font=("Arial", 11))
task_entry.pack(pady=5)

tk.Button(
    card,
    text="➕ Add Task",
    command=add_task,
    bg="#3498db",
    fg="white",
    font=("Arial", 10, "bold"),
    width=15
).pack(pady=8)

status_label = tk.Label(card, text="", bg="white", font=("Arial", 9))
status_label.pack(pady=2)

# Focus Mode
focus_var = tk.BooleanVar()
tk.Checkbutton(
    root,
    text="🔥 Enable Focus Mode (Today + High Priority)",
    variable=focus_var,
    bg="#f4f6f8",
    font=("Arial", 10)
).pack(pady=10)

# Show Button
tk.Button(
    root,
    text="📋 Format Tasks",
    command=show_tasks,
    bg="#2ecc71",
    fg="white",
    font=("Arial", 11, "bold"),
    width=20
).pack(pady=10)

# Output Card
output_card = tk.Frame(root, bg="white", bd=2, relief="groove")
output_card.pack(padx=20, pady=10, fill="both", expand=True)

output_box = tk.Text(
    output_card,
    font=("Courier New", 10),
    wrap="word"
)
output_box.pack(padx=10, pady=10, fill="both", expand=True)

root.mainloop()
