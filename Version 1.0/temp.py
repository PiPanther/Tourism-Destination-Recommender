import sqlite3
import tkinter as tk
from tkinter import messagebox

# Step 1: Database Design
# Create tables for users, destinations, ratings, and travel history
conn = sqlite3.connect('tourism_recommender.db')
c = conn.cursor()

# Create Users table
c.execute('''CREATE TABLE IF NOT EXISTS Users (
             user_id INTEGER PRIMARY KEY,
             username TEXT,
             age INTEGER,
             location TEXT
             )''')

# Create Destinations table
c.execute('''CREATE TABLE IF NOT EXISTS Destinations (
             destination_id INTEGER PRIMARY KEY,
             name TEXT,
             location TEXT,
             category TEXT
             )''')

# Create Ratings table
c.execute('''CREATE TABLE IF NOT EXISTS Ratings (
             rating_id INTEGER PRIMARY KEY,
             user_id INTEGER,
             destination_id INTEGER,
             rating INTEGER,
             FOREIGN KEY (user_id) REFERENCES Users(user_id),
             FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id)
             )''')

# Create Travel History table
c.execute('''CREATE TABLE IF NOT EXISTS TravelHistory (
             history_id INTEGER PRIMARY KEY,
             user_id INTEGER,
             destination_id INTEGER,
             FOREIGN KEY (user_id) REFERENCES Users(user_id),
             FOREIGN KEY (destination_id) REFERENCES Destinations(destination_id)
             )''')


# Step 2: Data Collection and Population
# Sample data insertion code

# Sample users data
users_data = [
    (4, 'Sara', 28, 'Mumbai'),
    (5, 'Rahul', 40, 'Delhi'),
    (6, 'Priya', 35, 'Bangalore'),
    (7, 'Amit', 27, 'Chennai'),
    (8, 'Neha', 33, 'Hyderabad'),
    (9, 'Vikram', 45, 'Kolkata'),
    (10, 'Anita', 32, 'Pune'),
    (11, 'Sanjay', 39, 'Ahmedabad'),
    (12, 'Kavita', 29, 'Jaipur'),
    (13, 'Rajesh', 36, 'Surat'),
    (14, 'Pooja', 31, 'Lucknow'),
    (15, 'Gaurav', 26, 'Kanpur'),
    (16, 'Meera', 42, 'Nagpur'),
    (17, 'Ajay', 34, 'Indore'),
    (18, 'Sneha', 38, 'Thane'),
    (19, 'Vishal', 37, 'Bhopal'),
    (20, 'Kirti', 41, 'Visakhapatnam'),
    (21, 'Sameer', 30, 'Patna'),
    (22, 'Anjali', 29, 'Vadodara'),
    (23, 'Ravi', 44, 'Ghaziabad'),
    (24, 'Anita', 36, 'Ludhiana'),
    (25, 'Rahul', 33, 'Agra')
]

c.executemany('''INSERT INTO Users (user_id, username, age, location)
                  VALUES (?, ?, ?, ?)''', users_data)

# Sample destinations data
destinations_data = [
    (6, 'Taj Mahal', 'Agra', 'Sightseeing'),
    (7, 'Hawa Mahal', 'Jaipur', 'Sightseeing'),
    (8, 'Qutub Minar', 'Delhi', 'Sightseeing'),
    (9, 'Gateway of India', 'Mumbai', 'Sightseeing'),
    (10, 'Mysore Palace', 'Mysore', 'Sightseeing'),
    (11, 'Kerala Backwaters', 'Kochi', 'Nature'),
    (12, 'Goa Beaches', 'Goa', 'Beach'),
    (13, 'Darjeeling Tea Gardens', 'Darjeeling', 'Nature'),
    (14, 'Taj Mahal Palace', 'Mumbai', 'Hotel'),
    (15, 'Varanasi Ghats', 'Varanasi', 'Spiritual'),
    (16, 'Golden Temple', 'Amritsar', 'Spiritual'),
    (17, 'Rann of Kutch', 'Gujarat', 'Desert'),
    (18, 'Jim Corbett National Park', 'Nainital', 'Park'),
    (19, 'Elephanta Caves', 'Mumbai', 'Caves'),
    (20, 'Ajanta and Ellora Caves', 'Aurangabad', 'Caves'),
    (21, 'Charminar', 'Hyderabad', 'Sightseeing'),
    (22, 'City Palace', 'Udaipur', 'Sightseeing'),
    (23, 'Jaisalmer Fort', 'Jaisalmer', 'Fort'),
    (24, 'Lotus Temple', 'Delhi', 'Temple'),
    (25, 'Victoria Memorial', 'Kolkata', 'Monument')
]

c.executemany('''INSERT INTO Destinations (destination_id, name, location, category)
                  VALUES (?, ?, ?, ?)''', destinations_data)

# Sample ratings data
ratings_data = [
    (7, 4, 6, 5),   # Sara rated Taj Mahal 5
    (8, 4, 9, 4),   # Sara rated Gateway of India 4
    (9, 5, 6, 5),   # Rahul rated Taj Mahal 5
    (10, 5, 7, 4),  # Rahul rated Hawa Mahal 4
    (11, 6, 8, 5),  # Priya rated Qutub Minar 5
    (12, 6, 10, 4), # Priya rated Mysore Palace 4
    (13, 7, 6, 3),  # Amit rated Taj Mahal 3
    (14, 7, 9, 4),  # Amit rated Gateway of India 4
    (15, 8, 8, 5),  # Neha rated Qutub Minar 5
    (16, 8, 12, 4), # Neha rated Goa Beaches 4
    (17, 9, 7, 3),  # Vikram rated Hawa Mahal 3
    (18, 9, 11, 4), # Vikram rated Kerala Backwaters 4
    (19, 10, 6, 5), # Anita rated Taj Mahal 5
    (20, 10, 12, 4),# Anita rated Goa Beaches 4
    (21, 11, 8, 3), # Sanjay rated Qutub Minar 3
    (22, 11, 13, 4),# Sanjay rated Darjeeling Tea Gardens 4
    (23, 12, 9, 5), # Kavita rated Gateway of India 5
    (24, 12, 15, 4),# Kavita rated Varanasi Ghats 4
    (25, 13, 6, 3), # Rajesh rated Taj Mahal 3
    (26, 13, 12, 4),# Rajesh rated Goa Beaches 4
    (27, 14, 6, 5), # Pooja rated Taj Mahal 5
    (28, 14, 12, 4),# Pooja rated Goa Beaches 4
    (29, 15, 8, 3), # Gaurav rated Qutub Minar 3
    (30, 15, 17, 4),# Gaurav rated Rann of Kutch 4
    (31, 16, 18, 5),# Meera rated Jim Corbett National Park 5
    (32, 16, 19, 4),# Meera rated Elephanta Caves 4
    (33, 17, 20, 3),# Ajay rated Ajanta and Ellora Caves 3
    (34, 17, 21, 4),# Ajay rated Charminar 
]
c.executemany('''INSERT INTO Ratings (rating_id, user_id, destination_id, rating)
                  VALUES (?, ?, ?, ?)''', ratings_data)

                  # Sample travel history data
travel_history_data = [
    (1, 1, 1),   # John visited Eiffel Tower
    (2, 2, 2),   # Alice visited Statue of Liberty
    (3, 3, 1),   # Bob visited Eiffel Tower
    (4, 4, 6),   # Sara visited Taj Mahal
    (5, 5, 6),   # Rahul visited Taj Mahal
    (6, 6, 8),   # Priya visited Qutub Minar
    (7, 7, 7),   # Amit visited Hawa Mahal
    (8, 8, 8),   # Neha visited Qutub Minar
    (9, 9, 9),   # Vikram visited Gateway of India
    (10, 10, 6), # Anita visited Taj Mahal
    (11, 11, 8), # Sanjay visited Qutub Minar
    (12, 12, 9), # Kavita visited Gateway of India
    (13, 13, 6), # Rajesh visited Taj Mahal
    (14, 14, 6), # Pooja visited Taj Mahal
    (15, 15, 17),# Gaurav visited Rann of Kutch
    (16, 16, 18),# Meera visited Jim Corbett National Park
    (17, 17, 20),# Ajay visited Ajanta and Ellora Caves
    (18, 18, 21),# Sneha visited Charminar
    (19, 19, 22),# Vishal visited City Palace
    (20, 20, 23),# Kirti visited Jaisalmer Fort
    (21, 21, 24),# Sameer visited Lotus Temple
    (22, 22, 25),# Anjali visited Victoria Memorial
    (23, 23, 10),# Ravi visited Mysore Palace
    (24, 24, 11),# Anita visited Kerala Backwaters
    (25, 25, 12),# Rahul visited Goa Beaches
]

c.executemany('''INSERT INTO TravelHistory (history_id, user_id, destination_id)
                  VALUES (?, ?, ?)''', travel_history_data)




# Step 2: Data Collection and Population
# Sample data insertion code
# Data population code is same as provided earlier


# Step 3: User Interface using Tkinter

def get_recommendations(user_id):
    # Retrieve user's location and preferences
    c.execute('''SELECT location FROM Users WHERE user_id = ?''', (user_id,))
    user_location = c.fetchone()[0]
    
    # Retrieve user's travel history
    c.execute('''SELECT destination_id FROM TravelHistory WHERE user_id = ?''', (user_id,))
    travel_history = c.fetchall()
    
    # Retrieve destinations visited by users with similar preferences and travel history
    c.execute('''SELECT DISTINCT d.name, d.location, d.category
                 FROM Destinations d
                 JOIN Ratings r ON d.destination_id = r.destination_id
                 JOIN Users u ON r.user_id = u.user_id
                 WHERE u.location = ? AND d.destination_id NOT IN (SELECT destination_id FROM TravelHistory WHERE user_id = ?)
                 ORDER BY r.rating DESC
                 LIMIT 5''', (user_location, user_id))
    recommendations = c.fetchall()
    
    # Formulate recommendation explanation
    recommendation_explanation = f"Recommendations based on your location ({user_location}) and preferences:\n"
    for recommendation in recommendations:
        recommendation_explanation += f"- Name: {recommendation[0]}, Location: {recommendation[1]}, Category: {recommendation[2]}\n"
    
    return recommendation_explanation

def show_recommendations():
    try:
        user_id = int(entry.get())
        recommendation_message = get_recommendations(user_id)
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

label = tk.Label(root, text="Enter User ID:")
label.pack(pady=10)

entry = tk.Entry(root, width=20)
entry.pack()

recommend_button = tk.Button(root, text="Get Recommendations", command=show_recommendations)
recommend_button.pack(pady=10)

result_text = tk.Text(root, height=15, width=60, state=tk.DISABLED)
result_text.pack(pady=10)

root.mainloop()