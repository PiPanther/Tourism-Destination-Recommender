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
    (15, 'Gaurav', 26, 'Lucknow'),
    (16, 'Meera', 42, 'Nagpur'),
    (17, 'Ajay', 34, 'Indore'),
    (18, 'Sneha', 38, 'Thane'),
    (19, 'Vishal', 37, 'Bhopal'),
    (20, 'Kirti', 41, 'Visakhapatnam'),
    (21, 'Sameer', 30, 'Patna'),
    (22, 'Anjali', 29, 'Vadodara'),
    (23, 'Ravi', 44, 'Ghaziabad'),
    (24, 'Anita', 36, 'Ludhiana'),
    (25, 'Rahul', 33, 'Agra'),
    (26, 'Nitin', 27, 'Noida'),
(27, 'Arjun', 35, 'Delhi'),
(28, 'Smita', 29, 'Pune'),
(29, 'Divya', 31, 'Mumbai'),
(30, 'Aarav', 24, 'Bangalore'),
(31, 'Kiran', 40, 'Hyderabad'),
(32, 'Aryan', 26, 'Chennai'),
(33, 'Shreya', 33, 'Kolkata'),
(34, 'Mehak', 28, 'Lucknow'),
(35, 'Kabir', 37, 'Surat'),
(36, 'Prachi', 36, 'Jaipur'),
(37, 'Rohan', 32, 'Ahmedabad'),
(38, 'Isha', 30, 'Nagpur'),
(39, 'Yash', 39, 'Indore'),
(40, 'Tanya', 34, 'Thane'),
(41, 'Riya', 41, 'Bhopal'),
(42, 'Sahil', 38, 'Visakhapatnam'),
(43, 'Jiya', 29, 'Patna'),
(44, 'Dev', 28, 'Vadodara'),
(45, 'Aashi', 43, 'Ghaziabad'),
(46, 'Ritvik', 35, 'Ludhiana'),
(47, 'Kavya', 33, 'Agra'),
(48, 'Arnav', 36, 'Noida'),
(49, 'Anaya', 31, 'Delhi'),
(50, 'Vihaan', 30, 'Pune'),
(51, 'Aarna', 25, 'Mumbai'),
(52, 'Viraj', 39, 'Bangalore'),
(53, 'Myra', 28, 'Hyderabad'),
(54, 'Advik', 34, 'Chennai'),
(55, 'Zara', 32, 'Kolkata'),
(56, 'Reyansh', 27, 'Lucknow'),
(57, 'Avni', 40, 'Surat'),
(58, 'Dhruv', 29, 'Jaipur'),
(59, 'Aaradhya', 38, 'Ahmedabad'),
(60, 'Aryan', 36, 'Nagpur'),
(61, 'Amaira', 31, 'Indore'),
(62, 'Ahaan', 37, 'Thane'),
(63, 'Anika', 42, 'Bhopal'),
(64, 'Ayaan', 33, 'Visakhapatnam'),
(65, 'Anvi', 34, 'Patna'),
(66, 'Kiaan', 27, 'Vadodara'),
(67, 'Ishani', 25, 'Ghaziabad'),
(68, 'Rudra', 39, 'Ludhiana'),
(69, 'Anvi', 28, 'Agra'),
(70, 'Rachit', 26, 'Noida'),
(71, 'Niyati', 40, 'Delhi'),
(72, 'Aaryan', 29, 'Pune'),
(73, 'Mihika', 31, 'Mumbai'),
(74, 'Aradhya', 24, 'Bangalore'),
(75, 'Saanvi', 38, 'Hyderabad'),
(76, 'Rian', 33, 'Chennai'),
(77, 'Aadhya', 27, 'Kolkata'),
(78, 'Rivaan', 35, 'Lucknow'),
(79, 'Veer', 37, 'Surat'),
(80, 'Anaisha', 36, 'Jaipur'),
(81, 'Reeva', 32, 'Ahmedabad'),
(82, 'Aaryan', 29, 'Nagpur'),
(83, 'Ridhima', 39, 'Indore'),
(84, 'Nandini', 34, 'Thane'),
(85, 'Aarush', 41, 'Bhopal'),
(86, 'Anushka', 38, 'Visakhapatnam'),
(87, 'Aarav', 33, 'Patna'),
(88, 'Nehal', 26, 'Vadodara'),
(89, 'Aaditya', 43, 'Ghaziabad'),
(90, 'Kashvi', 35, 'Ludhiana'),
(91, 'Shivansh', 32, 'Agra'),
(92, 'Manya', 26, 'Noida'),
(93, 'Aarnav', 40, 'Delhi'),
(94, 'Ishika', 29, 'Pune'),
(95, 'Arav', 31, 'Mumbai'),
(96, 'Avyan', 24, 'Bangalore'),
(97, 'Kabir', 38, 'Hyderabad'),
(98, 'Anaisha', 27, 'Chennai'),
(99, 'Darsh', 33, 'Kolkata'),
(100, 'Navya', 28, 'Lucknow')

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
    (25, 'Victoria Memorial', 'Kolkata', 'Monument'),
    (26, 'Red Fort', 'Delhi', 'Monument'),
    (27, 'Amer Fort', 'Jaipur', 'Fort'),
    (28, 'India Gate', 'Delhi', 'Monument'),
    (29, 'Chandni Chowk', 'Delhi', 'Market'),
    (30, 'Jama Masjid', 'Delhi', 'Mosque'),
    (31, 'Humayun\'s Tomb', 'Delhi', 'Monument'),
    (32, 'Mehrangarh Fort', 'Jodhpur', 'Fort'),
    (33, 'Umaid Bhawan Palace', 'Jodhpur', 'Palace'),
    (34, 'City Palace', 'Jaipur', 'Palace'),
    (35, 'Nahargarh Fort', 'Jaipur', 'Fort'),
    (36, 'Jantar Mantar', 'Jaipur', 'Observatory'),
    (37, 'Golkonda Fort', 'Hyderabad', 'Fort'),
    (38, 'Salar Jung Museum', 'Hyderabad', 'Museum'),
    (39, 'Chowmahalla Palace', 'Hyderabad', 'Palace'),
    (40, 'Hussain Sagar', 'Hyderabad', 'Lake'),
    (41, 'Charminar', 'Hyderabad', 'Monument'),
    (42, 'Ramoji Film City', 'Hyderabad', 'Theme Park'),
    (43, 'Marine Drive', 'Mumbai', 'Promenade'),
    (44, 'Chhatrapati Shivaji Maharaj Vastu Sangrahalaya', 'Mumbai', 'Museum'),
    (45, 'Sanjay Gandhi National Park', 'Mumbai', 'Park'),
    (46, 'EsselWorld', 'Mumbai', 'Theme Park'),
    (47, 'Gir National Park', 'Gujarat', 'Wildlife Sanctuary'),
    (48, 'Somnath Temple', 'Gujarat', 'Temple'),
    (49, 'Statue of Unity', 'Gujarat', 'Monument'),
    (50, 'Laxmi Vilas Palace', 'Gujarat', 'Palace')
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
    (34, 17, 21, 4),
    (35, 14, 15, 5),
    (36, 14, 6, 5),# Ajay rated Charminar 
    (37, 20, 24, 7),   # Kirti rated Lotus Temple 7
    (38, 21, 25, 8),   # Sameer rated Victoria Memorial 8
    (39, 22, 26, 9),   # Anjali rated Red Fort 9
    (40, 23, 27, 10),  # Ravi rated Amer Fort 10
    (41, 24, 28, 11),  # Anita rated India Gate 11
    (42, 25, 29, 12),  # Rahul rated Chandni Chowk 12
    (43, 26, 30, 13),  # Priya rated Jama Masjid 13
    (44, 27, 31, 14),  # Amit rated Humayun's Tomb 14
    (45, 28, 32, 15),  # Neha rated Mehrangarh Fort 15
    (46, 29, 33, 16),  # Vikram rated Umaid Bhawan Palace 16
    (47, 30, 34, 17),  # Anita rated City Palace 17
    (48, 31, 35, 18),  # Sanjay rated Nahargarh Fort 18
    (49, 32, 36, 19),  # Kavita rated Jantar Mantar 19
    (50, 33, 37, 20),  # Rajesh rated Golkonda Fort 20
    (51, 34, 38, 21),  # Pooja rated Salar Jung Museum 21
    (52, 35, 39, 22),  # Gaurav rated Chowmahalla Palace 22
    (53, 36, 40, 23),  # Meera rated Hussain Sagar 23
    (54, 37, 41, 24),  # Ajay rated Charminar 24
    (55, 38, 42, 25),  # Sneha rated Ramoji Film City 25
    (56, 39, 43, 26),  # Vishal rated Marine Drive 26
    (57, 40, 44, 27),  # Kirti rated Chhatrapati Shivaji Maharaj Vastu Sangrahalaya 27
    (58, 41, 45, 28),  # Sameer rated Sanjay Gandhi National Park 28
    (59, 42, 46, 29),  # Anjali rated EsselWorld 29
    (60, 43, 47, 30),  # Ravi rated Gir National Park 30
    (61, 44, 48, 31),  # Anita rated Somnath Temple 31
    (62, 45, 49, 32),  # Rahul rated Statue of Unity 32
    (63, 46, 50, 33),  # Priya rated Laxmi Vilas Palace 33
    (64, 47, 6, 34),   # Amit rated Taj Mahal 34
    (65, 48, 7, 35),   # Neha rated Hawa Mahal 35
    (66, 49, 8, 36),   # Vikram rated Qutub Minar 36
    (67, 50, 9, 37),   # Anita rated Gateway of India 37
    (68, 51, 10, 38),  # Sanjay rated Mysore Palace 38
    (69, 52, 11, 39),  # Kavita rated Kerala Backwaters 39
    (70, 53, 12, 40),  # Rajesh rated Goa Beaches 40
    (71, 54, 13, 41),  # Pooja rated Darjeeling Tea Gardens 41
    (72, 55, 14, 42),  # Gaurav rated Taj Mahal Palace 42
    (73, 56, 15, 43),  # Meera rated Varanasi Ghats 43
    (74, 57, 16, 44),  # Ajay rated Golden Temple 44
    (75, 58, 17, 45),  # Sneha rated Rann of Kutch 45
    (76, 59, 18, 46),  # Vishal rated Jim Corbett National Park 46
    (77, 60, 19, 47),  # Kirti rated Elephanta Caves 47
    (78, 61, 20, 48),  # Sameer rated Ajanta and Ellora Caves 48
    (79, 62, 21, 49),  # Anjali rated Charminar 49
    (80, 63, 22, 50),  # Ravi rated City Palace 50
    (81, 64, 23, 51),  # Anita rated Jaisalmer Fort 51
    (82, 65, 24, 52),  # Rahul rated Lotus Temple 52
    (83, 66, 25, 53),  # Priya rated Victoria Memorial 53
    (84, 67, 26, 54),  # Amit rated Red Fort 54
    (85, 68, 27, 55),  # Neha rated Amer Fort 55
    (86, 69, 28, 56),  # Vikram rated India Gate 56
    (87, 70, 29, 57),  # Anita rated Chandni Chowk 57
    (88, 71, 30, 58),  # Sanjay rated Jama Masjid 58
    (89, 72, 31, 59),  # Kavita rated Humayun's Tomb 59
    (90, 73, 32, 60),  # Rajesh rated Mehrangarh Fort 60
    (91, 74, 33, 61),  # Pooja rated Umaid Bhawan Palace 61
    (92, 75, 34, 62),  # Gaurav rated City Palace 62
    (93, 76, 35, 63),  # Meera rated Nahargarh Fort 63
    (94, 77, 36, 64),  # Ajay rated Jantar Mantar 64
    (95, 78, 37, 65),  # Sneha rated Golkonda Fort 65
    (96, 79, 38, 66),  # Vishal rated Salar Jung Museum 66
    (97, 80, 39, 67),  # Kirti rated Chowmahalla Palace 67
    (98, 81, 40, 68),   # Sameer rated Hussain Sagar 68
    (99, 82, 41, 69),   # Anjali rated Charminar 69
    (100, 83, 42, 70),  # Ravi rated Ramoji Film City 70
    (101, 84, 43, 71),  # Anita rated Marine Drive 71
    (102, 85, 44, 72),  # Rahul rated Chhatrapati Shivaji Maharaj Vastu Sangrahalaya 72
    (103, 86, 45, 73),  # Priya rated Sanjay Gandhi National Park 73
    (104, 87, 46, 74),  # Amit rated EsselWorld 74
    (105, 88, 47, 75),  # Neha rated Gir National Park 75
    (106, 89, 48, 76),  # Vikram rated Somnath Temple 76
    (107, 90, 49, 77),  # Anita rated Statue of Unity 77
    (108, 91, 50, 78),  # Sanjay rated Laxmi Vilas Palace 78
    (109, 92, 6, 79),   # Kavita rated Taj Mahal 79
    (110, 93, 7, 80),   # Rajesh rated Hawa Mahal 80
    (111, 94, 8, 81),   # Pooja rated Qutub Minar 81
    (112, 95, 9, 82),   # Gaurav rated Gateway of India 82
    (113, 96, 10, 83),  # Meera rated Mysore Palace 83
    (114, 97, 11, 84),  # Ajay rated Kerala Backwaters 84
    (115, 98, 12, 85),  # Sneha rated Goa Beaches 85
    (116, 99, 13, 86),  # Vishal rated Darjeeling Tea Gardens 86
    (117, 100, 14, 87), # Kirti rated Taj Mahal Palace 87
    (118, 81, 15, 88),  # Sameer rated Varanasi Ghats 88
    (119, 82, 16, 89),  # Anjali rated Golden Temple 89
    (120, 83, 17, 90),  # Ravi rated Rann of Kutch 90
    (121, 84, 18, 91),  # Anita rated Jim Corbett National Park 91
    (122, 85, 19, 92),  # Rahul rated Elephanta Caves 92
    (123, 86, 20, 93),  # Priya rated Ajanta and Ellora Caves 93
    (124, 87, 21, 94),  # Amit rated Charminar 94
    (125, 88, 22, 95),  # Neha rated City Palace 95
    (126, 89, 23, 96),  # Vikram rated Jaisalmer Fort 96
    (127, 90, 24, 97),  # Anita rated Lotus Temple 97
    (128, 91, 25, 98),  # Sanjay rated Victoria Memorial 98
    (129, 92, 26, 99),  # Kavita rated Red Fort 99
    (130, 93, 27, 100), # Rajesh rated Amer Fort 100

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
     (26, 4, 7),    # Sara visited Hawa Mahal
    (27, 5, 8),    # Rahul visited Qutub Minar
    (28, 6, 10),   # Priya visited Mysore Palace
    (29, 7, 9),    # Amit visited Gateway of India
    (30, 8, 12),   # Neha visited Goa Beaches
    (31, 9, 10),   # Vikram visited Mysore Palace
    (32, 10, 11),  # Anita visited Kerala Backwaters
    (33, 11, 13),  # Sanjay visited Darjeeling Tea Gardens
    (34, 12, 15),  # Kavita visited Varanasi Ghats
    (35, 13, 12),  # Rajesh visited Goa Beaches
    (36, 14, 9),   # Pooja visited Gateway of India
    (37, 15, 17),  # Gaurav visited Rann of Kutch
    (38, 16, 18),  # Meera visited Jim Corbett National Park
    (39, 17, 20),  # Ajay visited Ajanta and Ellora Caves
    (40, 18, 21),  # Sneha visited Charminar
    (41, 19, 22),  # Vishal visited City Palace
    (42, 20, 23),  # Kirti visited Jaisalmer Fort
    (43, 21, 24),  # Sameer visited Lotus Temple
    (44, 22, 25),  # Anjali visited Victoria Memorial
    (45, 23, 10),  # Ravi visited Mysore Palace
    (46, 24, 11),  # Anita visited Kerala Backwaters
    (47, 25, 12),  # Rahul visited Goa Beaches
    (48, 26, 7),   # Meera visited Hawa Mahal
    (49, 27, 8),   # Ajay visited Qutub Minar
    (50, 28, 10),  # Vishal visited Mysore Palace
    (51, 29, 9),   # Kirti visited Gateway of India
    (52, 30, 12),  # Anjali visited Goa Beaches
    (53, 31, 10),  # Ravi visited Mysore Palace
    (54, 32, 11),  # Anita visited Kerala Backwaters
    (55, 33, 13),  # Gaurav visited Darjeeling Tea Gardens
    (56, 34, 15),  # Sameer visited Varanasi Ghats
    (57, 35, 12),  # Neha visited Goa Beaches
    (58, 36, 9),   # Priya visited Gateway of India
    (59, 37, 17),  # Amit visited Rann of Kutch
    (60, 38, 18),  # Rajesh visited Jim Corbett National Park
    (61, 39, 20),  # Pooja visited Ajanta and Ellora Caves
    (62, 40, 21),  # Sanjay visited Charminar
    (63, 41, 22),  # Vikram visited City Palace
    (64, 42, 23),  # Anita visited Jaisalmer Fort
    (65, 43, 24),  # Rahul visited Lotus Temple
    (66, 44, 25),  # Neha visited Victoria Memorial
    (67, 45, 10),  # Kavita visited Mysore Palace
    (68, 46, 11),  # Rajesh visited Kerala Backwaters
    (69, 47, 12),  # Gaurav visited Goa Beaches
    (70, 48, 13),  # Amit visited Darjeeling Tea Gardens
    (71, 49, 15),  # Neha visited Varanasi Ghats
    (72, 50, 12),  # Rajesh visited Goa Beaches
    (73, 51, 9),   # Meera visited Gateway of India
    (74, 52, 17),  # Vishal visited Rann of Kutch
    (75, 53, 18),  # Kirti visited Jim Corbett National Park
    (76, 54, 20),  # Anjali visited Ajanta and Ellora Caves
    (77, 55, 21),  # Ravi visited Charminar
    (78, 56, 22),  # Anita visited City Palace
    (79, 57, 23),  # Rahul visited Jaisalmer Fort
    (80, 58, 24),  # Neha visited Lotus Temple
    (81, 59, 25),  # Priya visited Victoria Memorial
    (82, 60, 10),  # Amit visited Mysore Palace
    (83, 61, 11),  # Rajesh visited Kerala Backwaters
    (84, 62, 12),  # Gaurav visited Goa Beaches
    (85, 63, 13),  # Neha visited Darjeeling Tea Gardens
    (86, 64, 15),  # Sanjay visited Varanasi Ghats
    (87, 65, 12),  # Meera visited Goa Beaches
    (88, 66, 9),   # Rajesh visited Gateway of India
    (89, 67, 17),  # Gaurav visited Rann of Kutch
    (90, 68, 18),  # Sneha visited Jim Corbett National Park
    (91, 69, 20),  # Vishal visited Ajanta and Ellora Caves
    (92, 70, 21),  # Kirti visited Charminar
    (93, 71, 22),  # Anita visited City Palace
    (94, 72, 23),  # Rahul visited Jaisalmer Fort
    (95, 73, 24),  # Neha visited Lotus Temple
    (96, 74, 25),  # Priya visited Victoria Memorial
    (97, 75, 10),  # Amit visited Mysore Palace
    (98, 76, 11),  # Rajesh visited Kerala Backwaters
    (99, 77, 12),  # Gaurav visited Goa Beaches
    (100, 78, 13), # Neha visited Darjeeling Tea Gardens
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
