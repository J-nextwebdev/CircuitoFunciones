from flask import Flask, render_template, request, jsonify
from circuito_calc import solve_circuit

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        comp_type = data.get('component_type')
        connection = data.get('connection_type')
        v_battery = data.get('battery_voltage')
        components = data.get('components', [])
        
        if not v_battery or not components:
            return jsonify({'error': 'Faltan datos. Asegúrate de ingresar el voltaje y al menos un componente.'}), 400
            
        result = solve_circuit(comp_type, connection, v_battery, components)
        
        if 'error' in result:
            return jsonify({'error': result['error']}), 400
            
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
