from flask import Flask, render_template, request
from circuito_calc import resolver_circuito

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        tipo_comp = request.form.get('component_type')
        conexion = request.form.get('connection_type')
        v_bateria = request.form.get('battery_voltage')
        
        componentes = request.form.getlist('componentes[]')
        
        # Filtramos posibles valores vacíos
        componentes = [c for c in componentes if c.strip()]
        
        if not v_bateria or not componentes:
            return render_template('index.html', error='Faltan datos. Asegúrate de ingresar el voltaje y al menos un componente.')
            
        resultado = resolver_circuito(tipo_comp, conexion, v_bateria, componentes)
        
        if 'error' in resultado:
            return render_template('index.html', error=resultado['error'])
            
        return render_template('index.html', resultados=resultado, tipo_comp=tipo_comp)
        
    except Exception as e:
        return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
