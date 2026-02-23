from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Predefined rates
DATA = {
    "bike": {"efficiency": 30, "fuel_price": 109.52},
    "car": {"efficiency": 11, "fuel_price": 101.32},
    "food": 270,
    "stay": 700
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    req = request.get_json()
    dist = float(req.get('distance', 0))
    members = int(req.get('members', 1))
    days = int(req.get('days', 1))
    v_type = req.get('vehicle', 'bike')

    # Fuel Logic
    v = DATA[v_type]
    fuel_cost = (dist / v['efficiency']) * v['fuel_price']
    
    # Personal Logic
    food_cost = members * DATA['food'] * days
    # Stay is usually per night (days - 1)
    stay_cost = members * DATA['stay'] * (days - 1 if days > 1 else 0)

    return jsonify({
        "labels": ["Fuel", "Food", "Stay"],
        "values": [round(fuel_cost, 2), round(food_cost, 2), round(stay_cost, 2)]
    })

if __name__ == '__main__':
    app.run(debug=True)