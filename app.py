from flask import Flask, render_template, request
import sqlite3, random

app = Flask(__name__)

STATIONS = {
    "VSKP": "Visakhapatnam", "DVD": "Duvvada", "AKP": "Anakapalle", 
    "SLO": "Samalkot", "RJY": "Rajahmundry", "BZA": "Vijayawada", 
    "HYB": "Hyderabad", "SC": "Secunderabad", "GNT": "Guntur"
}

def find_trains(src, dest):
    conn = sqlite3.connect('railway.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            s.t_no, t.t_name, 
            s.departure as dept_time, d.arrival as arr_time,
            (d.distance_from_origin - s.distance_from_origin) as travel_dist
        FROM routes s
        JOIN routes d ON s.t_no = d.t_no
        JOIN trains t ON s.t_no = t.t_no
        WHERE s.stn_code = ? AND d.stn_code = ? AND d.stop_order > s.stop_order
    '''
    
    cursor.execute(query, (src, dest))
    rows = cursor.fetchall()
    
    results = []
    for row in rows:
        dist = abs(row['travel_dist'])
        t_no = row['t_no']
        
        # --- DYNAMIC FARE LOGIC FOR ALL TRAIN TYPES ---
        if t_no == '20833': # VANDE BHARAT
            fares = {
                'CC': max(450, int(dist * 2.5 + 200)),
                'EC': max(900, int(dist * 4.5 + 400))
            }
        elif t_no == '12739': # GARIB RATH
            fares = {
                '3A': max(200, int(dist * 0.95 + 100))
            }
        else: 
            # ALL OTHER TRAINS (Godavari, Janmabhoomi, etc.)
            fares = {
                'SL': max(60, int(dist * 0.45 + 50)),
                '3A': max(180, int(dist * 1.15 + 120)),
                '2A': max(350, int(dist * 2.05 + 200)),
                '1A': max(600, int(dist * 3.55 + 350))
            }

        results.append({
            'no': t_no, 'name': row['t_name'],
            'dept': row['dept_time'], 'arr': row['arr_time'],
            'dist': dist, 'fares': fares
        })
    conn.close()
    return results

@app.route('/')
def index():
    src = request.args.get('src')
    dest = request.args.get('dest')
    train_results = find_trains(src, dest) if src and dest else []
    return render_template('index.html', stations=STATIONS, trains=train_results)

@app.route('/book', methods=['POST'])
def book():
    return render_template('book.html', tix=request.form.to_dict())

@app.route('/confirm', methods=['POST'])
def confirm():
    d = request.form.to_dict()
    names = request.form.getlist('p_name[]')
    ages = request.form.getlist('p_age[]')
    
    psgn_list = []
    selected_class = d.get('class', 'SL')

    # 1. Assign Coach prefix based on the selected class
    coach_map = {'SL': 'S', '3A': 'B', '2A': 'A', '1A': 'H', 'CC': 'C', 'EC': 'E'}
    prefix = coach_map.get(selected_class, 'S')

    # 2. Build the passenger list (only including non-empty names)
    for i in range(len(names)):
        if names[i].strip():
            psgn_list.append({
                'name': names[i], 
                'age': ages[i],
                'berth': random.randint(1, 72),
                'coach': f"{prefix}{random.randint(1, 15)}"
            })

    # 3. CALCULATE TOTAL FARE
    # Get the base price per person from the form
    base_price = int(d.get('price', 0))
    # Multiply by the number of passengers
    total_fare = base_price * len(psgn_list)
    
    # Update the dictionary to include the total fare
    d['total_fare'] = total_fare
    d['passenger_count'] = len(psgn_list)

    return render_template('ticket.html', 
                           tix=d, 
                           passengers=psgn_list, 
                           pnr=str(random.randint(1000000000, 9999999999)))

if __name__ == '__main__':
    app.run(debug=True)