from flask import Flask, render_template, request
import sqlite3
from Data import Users, Ratings, Destinations, Travel_History, TravelCosts

app = Flask(__name__)

# Database connection and setup (similar to your previous code)
conn = sqlite3.connect('test.db',check_same_thread=False)
c = conn.cursor()

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

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            selected_season = request.form['season']
            max_budget = float(request.form['budget']) if request.form['budget'] else None
           
            recommendation_message = get_recommendations(user_id, selected_season, max_budget)
            print(recommendation_message)
            if recommendation_message:
                return render_template('recommendations.html', message=recommendation_message)
            else:
                return render_template('recommendations.html', message="No recommendations found for the user.")
        except ValueError:
            return render_template('error.html', message="Please enter a valid user ID and budget.")

    return render_template('error.html', message="Invalid request method.")

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

    return recommendations

# Close database connection when the application exits
# @app.teardown_appcontext
# def close_connection(exception):
#     if conn is not None:
#         conn.close()

if __name__ == '__main__':
    app.run(debug=True)
