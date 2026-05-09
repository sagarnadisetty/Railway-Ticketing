import sqlite3

def setup():
    conn = sqlite3.connect('railway.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS trains')
    cursor.execute('''CREATE TABLE trains (t_no TEXT PRIMARY KEY, t_name TEXT)''')

    cursor.execute('DROP TABLE IF EXISTS routes')
    cursor.execute('''CREATE TABLE routes (
        t_no TEXT, stn_code TEXT, stn_name TEXT, 
        arrival TEXT, departure TEXT, 
        distance_from_origin INTEGER, stop_order INTEGER
    )''')

    # Train List
    trains = [
        ('12727', 'Godavari Express'),
        ('20833', 'Vande Bharat Express'),
        ('12739', 'Garib Rath Express'),
        ('12805', 'Janmabhoomi Express')
    ]

    # Route Data
    route_data = [
        # GODAVARI EXPRESS (All stops)
        ('12727', 'VSKP', 'Visakhapatnam', 'START', '17:20', 0, 1),
        ('12727', 'DVD', 'Duvvada', '17:48', '17:50', 17, 2),
        ('12727', 'AKP', 'Anakapalle', '18:03', '18:05', 33, 3),
        ('12727', 'SLO', 'Samalkot', '19:43', '19:45', 151, 4),
        ('12727', 'RJY', 'Rajahmundry', '20:33', '20:35', 201, 5),
        ('12727', 'BZA', 'Vijayawada', '23:30', '23:45', 350, 6),
        ('12727', 'HYB', 'Hyderabad', '06:15', 'END', 710, 7),

        # VANDE BHARAT (Fast - fewer stops)
        ('20833', 'VSKP', 'Visakhapatnam', 'START', '05:45', 0, 1),
        ('20833', 'RJY', 'Rajahmundry', '07:55', '07:57', 201, 2),
        ('20833', 'BZA', 'Vijayawada', '10:00', '10:05', 350, 3),
        ('20833', 'SC', 'Secunderabad', '14:15', 'END', 690, 4),

        # GARIB RATH (Intermediate stops)
        ('12739', 'VSKP', 'Visakhapatnam', 'START', '20:40', 0, 1),
        ('12739', 'DVD', 'Duvvada', '21:08', '21:10', 17, 2),
        ('12739', 'AKP', 'Anakapalle', '21:23', '21:25', 33, 3),
        ('12739', 'RJY', 'Rajahmundry', '23:33', '23:35', 201, 4),
        ('12739', 'BZA', 'Vijayawada', '02:05', '02:20', 350, 5),
        ('12739', 'SC', 'Secunderabad', '08:10', 'END', 690, 6),

        # JANMABHOOMI (Day train)
        ('12805', 'VSKP', 'Visakhapatnam', 'START', '06:15', 0, 1),
        ('12805', 'DVD', 'Duvvada', '06:43', '06:45', 17, 2),
        ('12805', 'AKP', 'Anakapalle', '06:58', '07:00', 33, 3),
        ('12805', 'SLO', 'Samalkot', '08:33', '08:35', 151, 4),
        ('12805', 'RJY', 'Rajahmundry', '09:23', '09:25', 201, 5),
        ('12805', 'BZA', 'Vijayawada', '12:10', '12:25', 350, 6),
        ('12805', 'GNT', 'Guntur', '13:10', 'END', 382, 7)
    ]

    cursor.executemany('INSERT INTO trains VALUES (?,?)', trains)
    cursor.executemany('INSERT INTO routes VALUES (?,?,?,?,?,?,?)', route_data)
    
    conn.commit()
    conn.close()
    print("Database updated with 4 major trains and full route logic!")

setup()