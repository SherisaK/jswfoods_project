from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# In a real application, these would be stored in a database [cite: 27]

# Set coefficients to 0.5 as recommended[cite: 30].

coefficients = {
    'distance_coeff': 0.5,
    'weight_coeff': 0.5
}

@app.route('/')
def home():
    """Serves the main website page."""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Calculates the delivery price based on distance and weight."""
    data = request.get_json()
    distance = float(data.get('distance'))
    weight = float(data.get('weight'))

    # Formula: (distance coefficient * distance) + (package weight coefficient * package weight) [cite: 26]
    price = (coefficients['distance_coeff'] * distance) + (coefficients['weight_coeff'] * weight)
    
    return jsonify({'price': price})

@app.route('/admin')
def admin_page():
    """Serves the admin page to view/update coefficients."""
    return f"""
    <h1>Admin Page</h1>
    <p>Current Distance Coefficient: {coefficients['distance_coeff']}</p>
    <p>Current Weight Coefficient: {coefficients['weight_coeff']}</p>
    <form action="/update_coeffs" method="post">
        <label for="distance_coeff">New Distance Coefficient:</label><br>
        <input type="text" id="distance_coeff" name="distance_coeff" value="{coefficients['distance_coeff']}"><br>
        <label for="weight_coeff">New Weight Coefficient:</label><br>
        <input type="text" id="weight_coeff" name="weight_coeff" value="{coefficients['weight_coeff']}"><br><br>
        <input type="submit" value="Update Coefficients">
    </form>
    """

@app.route('/update_coeffs', methods=['POST'])
def update_coeffs():
    """Handles the update of the coefficients."""
    new_distance_coeff = request.form['distance_coeff']
    new_weight_coeff = request.form['weight_coeff']
    try:
        coefficients['distance_coeff'] = float(new_distance_coeff)
        coefficients['weight_coeff'] = float(new_weight_coeff)
        return "Coefficients updated successfully! <a href='/admin'>Go back to Admin Page</a>"
    except ValueError:
        return "Invalid input. Please enter a number. <a href='/admin'>Go back to Admin Page</a>"

if __name__ == '__main__':
    app.run(debug=True)