import sqlite3
import tkinter as tk
from tkinter import messagebox
from Data import Users, Ratings, Destinations, Travel_History, TravelCosts

# Create tables for users, destinations, ratings, travel history, and travel costs
conn = sqlite3.connect('main.db')
c = conn.cursor()

# Create Users, Destinations, Ratings, TravelHistory, and TravelCosts tables
c.execute('''CREATE TABLE IF NOT EXISTS Users (
             user_id INTEGER PRIMARY KEY,
             username TEXT,
             age INTEGER,
             location TEXT,
             category_pref TEXT
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS Destinations (
             destination_id INTEGER PRIMARY KEY,
             name TEXT,
             location TEXT,
             category TEXT,
             season TEXT
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS Ratings (
             rating_id INTEGER PRIMARY KEY,
             user_id INTEGER,
             destination_id INTEGER,
             rating INTEGER,
             FOREIGN KEY (user_id) REFERENCES Users(user_id),
             FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id)
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS TravelHistory (
             history_id INTEGER PRIMARY KEY,
             user_id INTEGER,
             destination_id INTEGER,
             FOREIGN KEY (user_id) REFERENCES Users(user_id),
             FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id)
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS TravelCosts (
             cost_id INTEGER PRIMARY KEY,
             destination_id INTEGER,
             cost_per_person REAL,
             currency TEXT,
             FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id)
             )''')

# Insert sample data into tables (Users, Destinations, Ratings, TravelHistory, and TravelCosts)
c.executemany('''INSERT INTO Users (user_id, username, age, location, category_pref)
                  VALUES (?, ?, ?, ?, ?)''', Users.users_data)

c.executemany('''INSERT INTO Destinations (destination_id, name, location, category, season)
                  VALUES (?, ?, ?, ?, ?)''', Destinations.destinations_data)

c.executemany('''INSERT INTO Ratings (rating_id, user_id, destination_id, rating)
                  VALUES (?, ?, ?, ?)''', Ratings.ratings_data)

c.executemany('''INSERT INTO TravelHistory (history_id, user_id, destination_id)
                  VALUES (?, ?, ?)''', Travel_History.travel_history_data)

c.executemany('''INSERT INTO TravelCosts (cost_id, destination_id, cost_per_person, currency)
                  VALUES (?, ?, ?, ?)''', TravelCosts.TravelCosts)
# Define the get_recommendations function with cost feature
def get_recommendations(user_id, selected_season, max_budget=None):
    c.execute('''SELECT location FROM Users WHERE user_id = ?''', (user_id,))
    user_location_row = c.fetchone()
    if user_location_row is None:
        return "User not found."

    user_location = user_location_row[0]

    c.execute('''SELECT destination_id FROM TravelHistory WHERE user_id = ?''', (user_id,))
    travel_history = [row[0] for row in c.fetchall()]

    if max_budget is not None:
        cost_clause = "AND tc.cost_per_person <= ?"
        query_params = (user_location, selected_season,max_budget, *travel_history)
    else:
        cost_clause = ""
        query_params = (user_location, selected_season, *travel_history)

    print(query_params)

    query = f'''SELECT DISTINCT d.name, d.location, d.category, tc.cost_per_person
                FROM Destinations d
                JOIN Ratings r ON d.destination_id = r.destination_id
                JOIN Users u ON r.user_id = u.user_id
                JOIN TravelCosts tc ON d.destination_id = tc.destination_id
                WHERE u.location = ? AND d.season = ? {cost_clause}
                AND d.destination_id NOT IN ({",".join("?" for _ in travel_history)})
                ORDER BY r.rating DESC
                LIMIT 10'''
    c.execute(query, query_params)
    recommendations = c.fetchall()

    recommendation_explanation = f"Recommendations based on your location ({user_location}), preferences for {selected_season}, and travel history:\n"
    for recommendation in recommendations:
        recommendation_explanation += f"- Name: {recommendation[0]}, Location: {recommendation[1]}, Category: {recommendation[2]}, Cost per Person: {recommendation[3]}\n"

    return recommendation_explanation

# Update show_recommendations function to include max_budget parameter
def show_recommendations():
    try:
        user_id = int(entry_user_id.get())
        selected_season = season_var.get()
        max_budget = float(entry_budget.get()) if entry_budget.get() else None
        recommendation_message = get_recommendations(user_id, selected_season, max_budget)
        if recommendation_message:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, recommendation_message)
            result_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("No Recommendations", "No recommendations found for the user.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid user ID and budget.")

# Tkinter GUI setup
root = tk.Tk()
root.title("Tourism Destination Recommender")
root.geometry("1000x800")

label_user_id = tk.Label(root, text="Enter User ID:")
label_user_id.pack(pady=10)

entry_user_id = tk.Entry(root, width=20)
entry_user_id.pack()

label_season = tk.Label(root, text="Select Season:")
label_season.pack()

season_var = tk.StringVar()
season_var.set("Winter")
season_options = ["Spring", "Summer", "Monsoon", "Winter"]
season_dropdown = tk.OptionMenu(root, season_var, *season_options)
season_dropdown.pack()

label_budget = tk.Label(root, text="Enter Maximum Budget:")
label_budget.pack()

entry_budget = tk.Entry(root, width=20)
entry_budget.pack()

recommend_button = tk.Button(root, text="Get Recommendations", command=show_recommendations)
recommend_button.pack(pady=10)

result_text = tk.Text(root, height=15, width=100, state=tk.DISABLED)
result_text.pack(pady=10)

root.mainloop()

conn.close()  # Close the database connection when the window is closed
