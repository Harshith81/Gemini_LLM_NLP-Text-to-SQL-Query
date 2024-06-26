# this file can be used when we want to explicitly create a database ourselves 
# and try to use it as our own data model while giving the databse as input along with prompt
# but it is feasible only for cross checking purposes of our application by creating small databases
# and executing some sql queries to verify whether the code is working properly or not.


import sqlite3

# Connect to SQLite database
conn = sqlite3.connect('students_academic.db')
cursor = conn.cursor()
    
# Create Students table
cursor.execute('''
CREATE TABLE Students (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50),
    section VARCHAR(50),
    age INTEGER
)
''')

# Create Marks table
cursor.execute('''
CREATE TABLE Marks (
    id INTEGER,
    subject VARCHAR(50),
    marks INTEGER,
    FOREIGN KEY (id) REFERENCES Students(id)
)
''')

# Create Subjects table
cursor.execute('''
CREATE TABLE Subjects (
    subject_id INTEGER PRIMARY KEY,
    subject_name VARCHAR(50),
    student_count INTEGER
)
''')

# Insert data into Students table
students_data = [
    (1, 'John Doe', 'A', 15),
    (2, 'Jane Smith', 'A', 16),
    (3, 'Sam Brown', 'B', 16),
    (4, 'Harshith', 'C', 15),
    (5, 'Avineni', 'A', 15),
    (6, 'Bunny', 'B', 17),
    (7, 'Abhi', 'C', 17),
    (8, 'Lakshmi', 'D', 17),
    (9, 'Devi', 'A', 16),    
    (10, 'Sita', 'B', 15),
    (11, 'Pavan', 'B', 18),
    (12, 'Sai', 'C', 18),  
    (13, 'Abhinav', 'A', 19),
    (14, 'Nikhil', 'B', 19),
    (15, 'Priya', 'D', 19),
    (16, 'Afzal', 'B', 19),
    (17, 'Gowtham', 'D', 19),
    (18, 'Pavanth', 'C', 19),
    (19, 'Nandan', 'B', 15),
    (20, 'Yoshik', 'A', 15),
    (21, 'Likith', 'B', 17),
    (22, 'Sasith', 'C', 17),
    (23, 'Nagesh', 'A', 16),
    (24, 'Ram', 'A', 16),
    (25, 'Shravan', 'A', 16),
    (26, 'Shiva', 'B', 17),
    (27, 'Krishna', 'A', 18),
    (28, 'Bhavana', 'A', 18),
    (29, 'Jayanthi', 'B', 18),
    (30, 'Hasitha', 'B', 18),
]

cursor.executemany('INSERT INTO Students (id, name, section, age) VALUES (?, ?, ?, ?)', students_data)

# Insert data into Marks table
marks_data = [
    (1, 'Math', 85),
    (1, 'Science', 92),
    (1, 'English', 88),
    (1, 'History', 87),
    (1, 'Geography', 94),
    
    (2, 'Math', 61),
    (2, 'Science', 72),
    (2, 'English', 98),
    (2, 'History', 57),
    (2, 'Geography', 74),
    
    (3, 'Math', 89),
    (3, 'Science', 72),
    (3, 'English', 78),
    (3, 'History', 57),
    (3, 'Geography', 74),
    
    (4, 'Math', 55),
    (4, 'Science', 92),
    (4, 'English', 78),
    (4, 'History', 89),
    (4, 'Geography', 69),
    
    (5, 'Math', 71),
    (5, 'Science', 72),
    (5, 'English', 98),
    (5, 'History', 87),
    (5, 'Geography', 84),
    
    (6, 'Math', 95),
    (6, 'Science', 72),
    (6, 'English', 78),
    (6, 'History', 97),
    (6, 'Geography', 64),
    
    (7, 'Math', 55),
    (7, 'Science', 82),
    (7, 'English', 98),
    (7, 'History', 97),
    (7, 'Geography', 64),
    
    (8, 'Math', 89),
    (8, 'Science', 72),
    (8, 'English', 68),
    (8, 'History', 97),
    (8, 'Geography', 74),
    
    (9, 'Math', 85),
    (9, 'Science', 92),
    (9, 'English', 78),
    (9, 'History', 77),
    (9, 'Geography', 74),
    
    (10, 'Math', 55),
    (10, 'Science', 95),
    (10, 'English', 85),
    (10, 'History', 65),
    (10, 'Geography', 85),
    
    (11, 'Math', 85),
    (11, 'Science', 99),
    (11, 'English', 81),
    (11, 'History', 82),
    (11, 'Geography', 83),
    
    (12, 'Math', 78),
    (12, 'Science', 72),
    (12, 'English', 78),
    (12, 'History', 77),
    (12, 'Geography', 99),
    
    (13, 'Math', 55),
    (13, 'Science', 92),
    (13, 'English', 98),
    (13, 'History', 77),
    (13, 'Geography', 74),
    
    (14, 'Math', 88),
    (14, 'Science', 91),
    (14, 'English', 81),
    (14, 'History', 80),
    (14, 'Geography', 75),
    
    (15, 'Math', 80),
    (15, 'Science', 90),
    (15, 'English', 80),
    (15, 'History', 80),
    (15, 'Geography', 90),
    
    (16, 'Math', 55),
    (16, 'Science', 62),
    (16, 'English', 78),
    (16, 'History', 67),
    (16, 'Geography', 54),
    
    (17, 'Math', 75),
    (17, 'Science', 62),
    (17, 'English', 58),
    (17, 'History', 57),
    (17, 'Geography', 94),
    
    (18, 'Math', 95),
    (18, 'Science', 92),
    (18, 'English', 58),
    (18, 'History', 57),
    (18, 'Geography', 54),
    
    (19, 'Math', 75),
    (19, 'Science', 72),
    (19, 'English', 78),
    (19, 'History', 77),
    (19, 'Geography', 74),
    
    (20, 'Math', 65),
    (20, 'Science', 62),
    (20, 'English', 68),
    (20, 'History', 67),
    (20, 'Geography', 98),
    
    (21, 'Math', 75),
    (21, 'Science', 72),
    (21, 'English', 78),
    (21, 'History', 87),
    (21, 'Geography', 78),
    
    (22, 'Math', 65),
    (22, 'Science', 61),
    (22, 'English', 78),
    (22, 'History', 61),
    (22, 'Geography', 91),
    
    (23, 'Math', 62),
    (23, 'Science', 62),
    (23, 'English', 62),
    (23, 'History', 64),
    (23, 'Geography', 90),
    
    (24, 'Math', 78),
    (24, 'Science', 72),
    (24, 'English', 78),
    (24, 'History', 67),
    (24, 'Geography', 91),
    
    (25, 'Math', 78),
    (25, 'Science', 72),
    (25, 'English', 78),
    (25, 'History', 57),
    (25, 'Geography', 68),
    
    (26, 'Math', 95),
    (26, 'Science', 92),
    (26, 'English', 58),
    (26, 'History', 57),
    (26, 'Geography', 78),
    
    (27, 'Math', 45),
    (27, 'Science', 62),
    (27, 'English', 78),
    (27, 'History', 47),
    (27, 'Geography', 48),
    
    (28, 'Math', 45),
    (28, 'Science', 52),
    (28, 'English', 48),
    (28, 'History', 87),
    (28, 'Geography', 52),
    
    (29, 'Math', 85),
    (29, 'Science', 82),
    (29, 'English', 78),
    (29, 'History', 77),
    (29, 'Geography', 78),
    
    (30, 'Math', 60),
    (30, 'Science', 60),
    (30, 'English', 67),
    (30, 'History', 98),
    (30, 'Geography', 93),
]

cursor.executemany('INSERT INTO Marks (id, subject, marks) VALUES (?, ?, ?)', marks_data)

# Insert data into Subjects table
subjects_data = [
    (1, 'Math', 50),
    (2, 'Science', 50),
    (3, 'English', 50),
    (4, 'History', 50),
    (5, 'Geography', 50)
]

cursor.executemany('INSERT INTO Subjects (subject_id, subject_name, student_count) VALUES (?, ?, ?)', subjects_data)

# Commit the changes and close the connection
conn.commit()
conn.close()
