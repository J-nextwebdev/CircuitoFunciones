from flask import Flask, render_template, request
from circuito_calc import resolver_circuito

app = Flask(__name__)

NOMBRE_PLANTILLA = 'index.html'


@app.route('/')
def index():
    return render_template(NOMBRE_PLANTILLA)


@app.route('/calcular', methods=['POST'])
def calcular():
    """
    recibe los datos del formulario,
    llama a la lógica de cálculo, y devuelve los resultados.
    """
    try:
        tipo_componente = request.form.get('component_type')
        tipo_conexion = request.form.get('connection_type')
        voltaje_bateria = request.form.get('battery_voltage')

        lista_componentes_cruda = request.form.getlist('componentes[]')

        lista_componentes = []
        for valor in lista_componentes_cruda:
            texto_limpio = valor.strip()
            if texto_limpio:
                lista_componentes.append(texto_limpio)

        if not voltaje_bateria or not lista_componentes:
            mensaje_error = 'Faltan datos. Asegúrate de ingresar el voltaje y al menos un componente.'
            return render_template(NOMBRE_PLANTILLA, error=mensaje_error)

        resultado = resolver_circuito(tipo_componente, tipo_conexion, voltaje_bateria, lista_componentes)

        if 'error' in resultado:
            return render_template(NOMBRE_PLANTILLA, error=resultado['error'])

        return render_template(NOMBRE_PLANTILLA, resultados=resultado, tipo_comp=tipo_componente)

    except Exception as excepcion:
        return render_template(NOMBRE_PLANTILLA, error=str(excepcion))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
