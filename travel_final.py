import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ------------------ RESEARCHER AGENT ------------------
def researcher(destination, days):
    if not destination.strip() or days <= 0:
        return None

    return {
        "destination": destination,
        "days": days,
        "places": ["City Tour", "Local Market", "Beach", "Museum"]
    }

# ------------------ PLANNER AGENT ------------------
def planner(data):
    if not data:
        return []

    itinerary = []
    for i in range(data["days"]):
        place = data["places"][i % len(data["places"])]
        itinerary.append(f"Day {i+1}: Visit {place}")
    return itinerary

# ------------------ COST ESTIMATOR ------------------
def estimate_cost(days, tier):
    rates = {
        "Budget": (2000, 800, 500),
        "Mid-range": (4000, 1500, 1000),
        "Luxury": (8000, 3000, 2500)
    }

    if tier not in rates or days <= 0:
        return None

    hotel, food, transport = rates[tier]
    return {
        "Hotel": hotel * days,
        "Food": food * days,
        "Transport": transport * days,
        "Total": (hotel + food + transport) * days
    }

# ------------------ MAIN CONTROLLER ------------------
def generate_plan():
    output_box.delete("1.0", tk.END)

    destination = dest_entry.get()
    tier = tier_var.get()

    try:
        days = int(days_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Days must be a valid number.")
        return

    data = researcher(destination, days)
    if not data:
        output_box.insert(tk.END, "❌ Invalid destination or number of days.\n")
        return

    itinerary = planner(data)
    cost = estimate_cost(days, tier)

    if not cost:
        output_box.insert(tk.END, "❌ Invalid travel tier.\n")
        return

    output_box.insert(tk.END, f"📍 Destination: {destination}\n")
    output_box.insert(tk.END, f"🗓️ Duration: {days} days\n\n")

    output_box.insert(tk.END, "🗺️ Itinerary:\n")
    for day in itinerary:
        output_box.insert(tk.END, f"• {day}\n")

    output_box.insert(tk.END, "\n💰 Cost Breakdown:\n")
    for k, v in cost.items():
        output_box.insert(tk.END, f"{k}: ₹{v}\n")

# ------------------ GUI SETUP ------------------
root = tk.Tk()
root.title("AI Travel Agent")
root.geometry("650x700")
root.resizable(False, False)

# ------------------ BACKGROUND IMAGE ------------------
bg_img = Image.open("bg.gif")
bg_img = bg_img.resize((650, 700), Image.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(root, width=650, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_image, anchor="nw")
canvas.bg_image = bg_image  # IMPORTANT: keep reference

# ------------------ TITLE ------------------
canvas.create_text(
    325, 40,
    text="✈️ AI Travel Agent",
    font=("Helvetica", 22, "bold"),
    fill="white"
)

# ------------------ INPUT CARD ------------------
card = tk.Frame(root, bg="white", bd=2, relief="groove")
canvas.create_window(325, 160, window=card, width=520, height=200)

tk.Label(card, text="Destination", bg="white").pack(pady=5)
dest_entry = tk.Entry(card, width=40)
dest_entry.pack()

tk.Label(card, text="Number of Days", bg="white").pack(pady=5)
days_entry = tk.Entry(card, width=40)
days_entry.pack()

tk.Label(card, text="Travel Tier", bg="white").pack(pady=5)
tier_var = tk.StringVar(value="Budget")
tk.OptionMenu(card, tier_var, "Budget", "Mid-range", "Luxury").pack()

tk.Button(
    card,
    text="🧠 Generate Travel Plan",
    command=generate_plan,
    bg="#27ae60",
    fg="white",
    font=("Arial", 11, "bold"),
    width=25
).pack(pady=10)

# ------------------ OUTPUT CARD ------------------
output_frame = tk.Frame(root, bg="white", bd=2, relief="groove")
canvas.create_window(325, 460, window=output_frame, width=520, height=360)

output_box = tk.Text(
    output_frame,
    font=("Courier New", 10),
    wrap="word",
    height=18,
    width=60
)
output_box.pack(padx=10, pady=10)

# ------------------ START APP ------------------
root.mainloop()
