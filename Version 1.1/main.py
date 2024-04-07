import sqlite3
import tkinter as tk
from tkinter import messagebox
from Data import Users, Ratings, Destinations, Travel_History

# Create tables for users, destinations, ratings, and travel history
conn = sqlite3.connect('main.db')
c = conn.cursor()

# Create Users, Destinations, Ratings, and TravelHistory table
c.execute('''CREATE TABLE IF NOT EXISTS Users (
             user_id INTEGER PRIMARY KEY,
             username TEXT,
             age INTEGER,
             location TEXT,
             category_pref TEXT  -- Add category_pref column
             )''')
c.execute('''CREATE TABLE IF NOT EXISTS Destinations (
             destination_id INTEGER PRIMARY KEY,
             name TEXT,
             location TEXT,
             category TEXT,
             season TEXT  -- Add season column
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

# Insert sample data into tables
c.executemany('''INSERT INTO Users (user_id, username, age, location, category_pref)
                  VALUES (?, ?, ?, ?, ?)''', Users.users_data)
c.executemany('''INSERT INTO Destinations (destination_id, name, location, category, season)
                  VALUES (?, ?, ?, ?, ?)''', Destinations.destinations_data)
c.executemany('''INSERT INTO Ratings (rating_id, user_id, destination_id, rating)
                  VALUES (?, ?, ?, ?)''', Ratings.ratings_data)
c.executemany('''INSERT INTO TravelHistory (history_id, user_id, destination_id)
                  VALUES (?, ?, ?)''', Travel_History.travel_history_data)


def get_recommendations(user_id, selected_season, include_category_pref=True):
    # Retrieve user's location and travel history
    print(include_category_pref)
    c.execute('''SELECT location FROM Users WHERE user_id = ?''', (user_id,))
    user_location_row = c.fetchone()
    if user_location_row is None:
        return "User not found."

    user_location = user_location_row[0]

    # Retrieve user's travel history
    c.execute('''SELECT destination_id FROM TravelHistory WHERE user_id = ?''', (user_id,))
    travel_history = [row[0] for row in c.fetchall()]  # List of visited destination_ids

    # Include category preference in the SQL query if specified
    if include_category_pref:
        c.execute('''SELECT category_pref FROM Users WHERE user_id = ?''', (user_id,))
        user_category_pref_row = c.fetchone()
        if user_category_pref_row is None:
            return "User category preference not found."
        user_category_pref = user_category_pref_row[0]
        category_clause = "AND u.category_pref = ?"
        
        query_params = (user_location, user_category_pref, selected_season, *travel_history)
    else:
        category_clause = ""
        query_params = (user_location, selected_season, *travel_history)  # Adjusted query params here

    print(query_params)
    # Retrieve destinations visited by users with similar preferences and travel history
    query = f'''SELECT DISTINCT d.name, d.location, d.category
                FROM Destinations d
                JOIN Ratings r ON d.destination_id = r.destination_id
                JOIN Users u ON r.user_id = u.user_id
                WHERE u.location = ? {category_clause} AND d.season = ? AND d.destination_id NOT IN ({",".join("?" for _ in travel_history)})
                ORDER BY r.rating DESC
                LIMIT 5'''
    c.execute(query, query_params)
    recommendations = c.fetchall()

    # Formulate recommendation explanation
    recommendation_explanation = f"Recommendations based on your location ({user_location}), preferences for {selected_season}, and travel history:\n"
    for recommendation in recommendations:
        recommendation_explanation += f"- Name: {recommendation[0]}, Location: {recommendation[1]}, Category: {recommendation[2]}\n"

    return recommendation_explanation


def show_recommendations():
    try:
        user_id = int(entry_user_id.get())
        selected_season = season_var.get()
        include_category_pref = include_category_pref_var.get()
        recommendation_message = get_recommendations(user_id, selected_season, include_category_pref)
        if recommendation_message:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, recommendation_message)
            result_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("No Recommendations", "No recommendations found for the user.")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid user ID.")


# Tkinter GUI setup
root = tk.Tk()
root.title("Tourism Destination Recommender")
root.geometry("600x400")

label_user_id = tk.Label(root, text="Enter User ID:")
label_user_id.pack(pady=10)

entry_user_id = tk.Entry(root, width=20)
entry_user_id.pack()

label_season = tk.Label(root, text="Select Season:")
label_season.pack()

season_var = tk.StringVar()
season_var.set("Winter")  # Default season selection
season_options = ["Spring", "Summer", "Monsoon", "Winter"]  # Update with your seasons
season_dropdown = tk.OptionMenu(root, season_var, *season_options)
season_dropdown.pack()

include_category_pref_var = tk.BooleanVar()
include_category_pref_var.set(True)  # Default is to include category preference
include_category_check = tk.Checkbutton(root, text="Include Category Preference", variable=include_category_pref_var)
include_category_check.pack()

recommend_button = tk.Button(root, text="Get Recommendations", command=show_recommendations)
recommend_button.pack(pady=10)

result_text = tk.Text(root, height=15, width=60, state=tk.DISABLED)
result_text.pack(pady=10)

# Keep the GUI running until closed
root.mainloop()

# Close the database connection when the window is closed
conn.close()
