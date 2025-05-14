import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Load and clean data
data = pd.read_csv("Unemployment in India (3).csv")
df = data.dropna()

# Train the model
x1 = df[[" Estimated Labour Participation Rate (%)", " Estimated Unemployment Rate (%)"]]
y1 = df[" Estimated Employed"]
x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(x1_train, y1_train)

# -------- Tkinter UI --------

def predict_employment():
    try:
        unemployment = float(unemployment_var.get())
        labor = float(labor_var.get())
        user_input = [[labor, unemployment]]  # Order must match training data
        prediction = model.predict(user_input)[0]
        messagebox.showinfo("Prediction", f"Estimated Employed Individuals: {prediction:.0f}")
    except Exception as e:
        messagebox.showerror("Input Error", str(e))

def show_graph(title, x, y, xlabel, ylabel, color="blue", rotation=0):
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(x, y, color=color)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(axis='x', rotation=rotation)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

def plot_sector_vs_unemployment():
    show_graph("Unemployment by Sector", df["Area"], df[" Estimated Unemployment Rate (%)"],
               "Sectors", "Unemployment Rate (%)", color="red")

def plot_sector_vs_employment():
    show_graph("Employment by Sector", df["Area"], df[" Estimated Employed"],
               "Sectors", "Employed", color="green")

def plot_state_vs_labor():
    show_graph("Labor Participation by State", df["Region"], df[" Estimated Labour Participation Rate (%)"],
               "States", "Labor Participation Rate (%)", color="pink", rotation=50)

def plot_state_vs_unemployment():
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(x="Region", y=" Estimated Unemployment Rate (%)", data=df, ax=ax, palette="dark")
    ax.set_title("Unemployment Rate by State")
    ax.tick_params(axis='x', rotation=55)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().pack()
    canvas.draw()

def plot_state_vs_employment():
    show_graph("Employment by State", df["Region"], df[" Estimated Employed"],
               "States", "Employed", color="yellow", rotation=55)

# Build window
root = tk.Tk()
root.title("Unemployment Analysis in India")
root.geometry("800x600")

# Input fields
frame = ttk.Frame(root)
frame.pack(pady=10)

ttk.Label(frame, text="Enter Unemployment Rate (%)").grid(row=0, column=0, padx=5, pady=5)
unemployment_var = tk.StringVar()
ttk.Entry(frame, textvariable=unemployment_var).grid(row=0, column=1, padx=5)

ttk.Label(frame, text="Enter Labor Participation Rate (%)").grid(row=1, column=0, padx=5, pady=5)
labor_var = tk.StringVar()
ttk.Entry(frame, textvariable=labor_var).grid(row=1, column=1, padx=5)

ttk.Button(frame, text="Predict Employment", command=predict_employment).grid(row=2, columnspan=2, pady=10)

# Graph buttons
ttk.Button(root, text="Sector vs Unemployment", command=plot_sector_vs_unemployment).pack(pady=3)
ttk.Button(root, text="Sector vs Employment", command=plot_sector_vs_employment).pack(pady=3)
ttk.Button(root, text="State vs Labor Participation", command=plot_state_vs_labor).pack(pady=3)
ttk.Button(root, text="State vs Unemployment", command=plot_state_vs_unemployment).pack(pady=3)
ttk.Button(root, text="State vs Employment", command=plot_state_vs_employment).pack(pady=3)

root.mainloop()
