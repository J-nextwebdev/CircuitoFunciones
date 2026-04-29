import sympy as sp


def resolver_resistores_serie(voltaje_bateria, resistores):
    """
    Calcula la resistencia equivalente, corriente total y valores individuales
    para un circuito de resistores conectados en SERIE.
    """
    cantidad_resistores = len(resistores)

    # --- Paso 1: Crear los símbolos algebraicos para cada resistor (R1, R2, ..., Rn) ---
    simbolos_resistores = sp.symbols(f'R1:{cantidad_resistores + 1}')
    if cantidad_resistores == 1:
        simbolos_resistores = (simbolos_resistores,)

    simbolo_resistencia_equivalente, simbolo_voltaje, simbolo_corriente = sp.symbols('R_eq V I')

    # --- Paso 2: Construir la ecuación simbólica de resistencia equivalente en serie ---
    # R_eq = R1 + R2 + ... + Rn
    ecuacion_resistencia_equivalente = sp.Eq(
        simbolo_resistencia_equivalente,
        sum(simbolos_resistores)
    )

    # --- Paso 3: Construir el procedimiento paso a paso ---
    pasos_procedimiento = []

    # Paso 3a: Mostrar la fórmula genera
    formula_latex = sp.latex(ecuacion_resistencia_equivalente)
    pasos_procedimiento.append(
        f"<strong>Fórmula del circuito (Resistencia Equivalente en Serie):</strong><br>$${formula_latex}$$"
    )

    # Paso 3b: Sustituir los valores numéricos y calcular la resistencia equivalente
    partes_sustitucion = []
    for resistor in resistores:
        partes_sustitucion.append(str(resistor))
    texto_sustitucion = " + ".join(partes_sustitucion)

    resistencia_equivalente = sum(resistores)

    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$R_{{eq}} = {texto_sustitucion} = {resistencia_equivalente:.4g} \\ \\Omega$$"
    )

    # Paso 3c: Mostrar la Ley de Ohm 
    ecuacion_ley_ohm = sp.Eq(simbolo_corriente, simbolo_voltaje / simbolo_resistencia_equivalente)
    formula_ohm_latex = sp.latex(ecuacion_ley_ohm)
    pasos_procedimiento.append(
        f"<strong>Ley de Ohm (Corriente Total):</strong><br>$${formula_ohm_latex}$$"
    )

    # Paso 3d: Calcular la corriente total del circuito
    if resistencia_equivalente > 0:
        corriente_total = voltaje_bateria / resistencia_equivalente
        pasos_procedimiento.append(
            f"<strong>Sustitución:</strong><br>"
            f"$$I = \\frac{{{voltaje_bateria}}}{{{resistencia_equivalente:.4g}}} = {corriente_total:.4g} \\ \\text{{A}}$$"
        )
    else:
        corriente_total = 0
        pasos_procedimiento.append(
            f"<strong>Sustitución:</strong><br>$$R_{{eq}}$$ es 0, hay un cortocircuito."
        )

    # --- Paso 4: Calcular el voltaje individual en cada resistor (V = I * R) ---
    voltajes_individuales = []
    for resistor in resistores:
        voltaje_en_resistor = corriente_total * resistor
        voltajes_individuales.append(voltaje_en_resistor)

    # --- Paso 5: lista de resultados individuales 
    resultados_individuales = []
    for indice, voltaje_individual in enumerate(voltajes_individuales):
        nombre_componente = f"R{indice + 1}"
        resultado_componente = {
            'componente': nombre_componente,
            'voltaje': f"{voltaje_individual:.4g} V",
            'corriente': f"{corriente_total:.4g} A"
        }
        resultados_individuales.append(resultado_componente)

    # --- Se  mete too en dicionario se retorna ---
    resultados_completos = {
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': f"{resistencia_equivalente:.4g} Ω",
        'total_title_2': 'Corriente Total',
        'total_val_2': f"{corriente_total:.4g} A",
        'individual_results': resultados_individuales,
        'procedimiento': pasos_procedimiento
    }
    return resultados_completos


def resolver_resistores_paralelo(voltaje_bateria, resistores):
    """
    Calcula la resistencia equivalente, corriente total y valores individuales
    para un circuito de resistores conectados en PARALELO.
    """
    cantidad_resistores = len(resistores)

    # --- Paso 1: Crear los símbolos algebraicos para cada resistor ---
    simbolos_resistores = sp.symbols(f'R1:{cantidad_resistores + 1}')
    if cantidad_resistores == 1:
        simbolos_resistores = (simbolos_resistores,)

    simbolo_resistencia_equivalente, simbolo_voltaje, simbolo_corriente_total = sp.symbols('R_eq V I_total')

    # --- Paso 2: Construir la ecuación simbólica inversa (1/R_eq = 1/R1 + 1/R2 + ...) ---
    suma_inversos_simbolica = sum(1 / simbolo for simbolo in simbolos_resistores)
    ecuacion_inversa = sp.Eq(1 / simbolo_resistencia_equivalente, suma_inversos_simbolica)

    # --- Paso 3: Construir el procedimiento paso a paso ---
    pasos_procedimiento = []

    # Paso 3a: Fórmula general
    formula_latex = sp.latex(ecuacion_inversa)
    pasos_procedimiento.append(
        f"<strong>Fórmula del circuito (Resistencia Equivalente en Paralelo):</strong><br>$${formula_latex}$$"
    )

    # Paso 3b: Sustituir valores numéricos y calcular la suma de inversos
    partes_sustitucion_latex = []
    for resistor in resistores:
        fraccion_latex = f"\\frac{{1}}{{{resistor}}}"
        partes_sustitucion_latex.append(fraccion_latex)
    texto_sustitucion = " + ".join(partes_sustitucion_latex)

    lista_inversos = []
    for resistor in resistores:
        inverso = 1 / resistor
        lista_inversos.append(inverso)
    suma_inversos_numerica = sum(lista_inversos)

    if suma_inversos_numerica > 0:
        resistencia_equivalente = 1 / suma_inversos_numerica
    else:
        resistencia_equivalente = 0

    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$\\frac{{1}}{{R_{{eq}}}} = {texto_sustitucion} = {suma_inversos_numerica:.4g} \\ \\Omega^{{-1}}$$"
    )
    pasos_procedimiento.append(
        f"$$R_{{eq}} = \\frac{{1}}{{{suma_inversos_numerica:.4g}}} = {resistencia_equivalente:.4g} \\ \\Omega$$"
    )

    # Paso 3c: Ley de Ohm simbólica
    ecuacion_ley_ohm = sp.Eq(simbolo_corriente_total, simbolo_voltaje / simbolo_resistencia_equivalente)
    formula_ohm_latex = sp.latex(ecuacion_ley_ohm)
    pasos_procedimiento.append(
        f"<strong>Ley de Ohm (Corriente Total):</strong><br>$${formula_ohm_latex}$$"
    )

    # --- Paso 4: Calcular la corriente individual en cada resistor (I = V / R) ---
    corrientes_individuales = []
    for resistor in resistores:
        corriente_en_resistor = voltaje_bateria / resistor
        corrientes_individuales.append(corriente_en_resistor)

    corriente_total = sum(corrientes_individuales)

    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$I_{{total}} = \\frac{{{voltaje_bateria}}}{{{resistencia_equivalente:.4g}}} = {corriente_total:.4g} \\ \\text{{A}}$$"
    )

    # --- Paso 5: Construir la lista de resultados individuales ---
    resultados_individuales = []
    for indice in range(cantidad_resistores):
        nombre_componente = f"R{indice + 1}"
        resultado_componente = {
            'componente': nombre_componente,
            'voltaje': f"{voltaje_bateria:.4g} V",
            'corriente': f"{corrientes_individuales[indice]:.4g} A"
        }
        resultados_individuales.append(resultado_componente)

    # --- eL dicionario a retornar ---
    resultados_completos = {
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': f"{resistencia_equivalente:.4g} Ω",
        'total_title_2': 'Corriente Total',
        'total_val_2': f"{corriente_total:.4g} A",
        'individual_results': resultados_individuales,
        'procedimiento': pasos_procedimiento
    }
    return resultados_completos


def resolver_capacitores_serie(voltaje_bateria, capacitores):
    """
    Calcula la capacitancia equivalente, carga total y valores individuales
    para un circuito de capacitores conectados en SERIE.
    """
    cantidad_capacitores = len(capacitores)

    # --- Paso 1: Crear los símbolos algebraicos para cada capacitor ---
    simbolos_capacitores = sp.symbols(f'C1:{cantidad_capacitores + 1}')
    if cantidad_capacitores == 1:
        simbolos_capacitores = (simbolos_capacitores,)

    simbolo_capacitancia_equivalente, simbolo_voltaje, simbolo_carga = sp.symbols('C_eq V Q')

    # --- Paso 2: Construir la ecuación simbólica inversa 
    suma_inversos_simbolica = sum(1 / simbolo for simbolo in simbolos_capacitores)
    ecuacion_inversa = sp.Eq(1 / simbolo_capacitancia_equivalente, suma_inversos_simbolica)

    # --- Paso 3: Construir el procedimiento paso a paso 
    pasos_procedimiento = []

    # Paso 3a: Fórmula general
    formula_latex = sp.latex(ecuacion_inversa)
    pasos_procedimiento.append(
        f"<strong>Fórmula del circuito (Capacitancia Equivalente en Serie):</strong><br>$${formula_latex}$$"
    )

    # Paso 3b: Sustituir valores numéricos y calcular la suma de inversos
    partes_sustitucion_latex = []
    for capacitor in capacitores:
        fraccion_latex = f"\\frac{{1}}{{{capacitor}}}"
        partes_sustitucion_latex.append(fraccion_latex)
    texto_sustitucion = " + ".join(partes_sustitucion_latex)

    # Calcular la suma de los inversos de cada capacitor
    lista_inversos = []
    for capacitor in capacitores:
        inverso = 1 / capacitor
        lista_inversos.append(inverso)
    suma_inversos_numerica = sum(lista_inversos)

    if suma_inversos_numerica > 0:
        capacitancia_equivalente = 1 / suma_inversos_numerica
    else:
        capacitancia_equivalente = 0

    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$\\frac{{1}}{{C_{{eq}}}} = {texto_sustitucion} = {suma_inversos_numerica:.4g} \\ \\text{{F}}^{{-1}}$$"
    )
    pasos_procedimiento.append(
        f"$$C_{{eq}} = \\frac{{1}}{{{suma_inversos_numerica:.4g}}} = {capacitancia_equivalente:.4g} \\ \\text{{F}}$$"
    )

    # Paso 3c: Fórmula de carga simbólica
    ecuacion_carga = sp.Eq(simbolo_carga, simbolo_capacitancia_equivalente * simbolo_voltaje)
    formula_carga_latex = sp.latex(ecuacion_carga)
    pasos_procedimiento.append(
        f"<strong>Fórmula de Carga (Carga Total):</strong><br>$${formula_carga_latex}$$"
    )

    # Paso 3d: Calcular la carga total del circuito
    carga_total = capacitancia_equivalente * voltaje_bateria
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$Q = {capacitancia_equivalente:.4g} \\times {voltaje_bateria} = {carga_total:.4g} \\ \\text{{C}}$$"
    )

    # --- Paso 4: Calcular el voltaje individual en cada capacitor ---
    voltajes_individuales = []
    for capacitor in capacitores:
        voltaje_en_capacitor = carga_total / capacitor
        voltajes_individuales.append(voltaje_en_capacitor)

    # --- Paso 5: Construir la lista de resultados individuales ---
    resultados_individuales = []
    for indice, voltaje_individual in enumerate(voltajes_individuales):
        nombre_componente = f"C{indice + 1}"
        resultado_componente = {
            'componente': nombre_componente,
            'carga': f"{carga_total:.4g} C",
            'voltaje': f"{voltaje_individual:.4g} V"
        }
        resultados_individuales.append(resultado_componente)

    # --- Dicionario a retornar --- 
    resultados_completos = {
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': f"{capacitancia_equivalente:.4g} F",
        'total_title_2': 'Carga Total',
        'total_val_2': f"{carga_total:.4g} C",
        'individual_results': resultados_individuales,
        'procedimiento': pasos_procedimiento
    }
    return resultados_completos


def resolver_capacitores_paralelo(voltaje_bateria, capacitores):
    """
    Calcula la capacitancia equivalente, carga total y valores individuales
    para un circuito de capacitores conectados en PARALELO.
    """
    cantidad_capacitores = len(capacitores)

    # --- Paso 1: Crear los símbolos algebraicos para cada capacitor ---
    simbolos_capacitores = sp.symbols(f'C1:{cantidad_capacitores + 1}')
    if cantidad_capacitores == 1:
        simbolos_capacitores = (simbolos_capacitores,)

    simbolo_capacitancia_equivalente, simbolo_voltaje, simbolo_carga = sp.symbols('C_eq V Q')

    # --- Paso 2: Construir la ecuación simbólica directa  ---
    ecuacion_capacitancia = sp.Eq(
        simbolo_capacitancia_equivalente,
        sum(simbolos_capacitores)
    )

    # --- Paso 3: Construir el procedimiento paso a paso ---
    pasos_procedimiento = []

    # Paso 3a: Fórmula general 
    formula_latex = sp.latex(ecuacion_capacitancia)
    pasos_procedimiento.append(
        f"<strong>Fórmula del circuito (Capacitancia Equivalente en Paralelo):</strong><br>$${formula_latex}$$"
    )

    # Paso 3b: Sustituir valores numéricos y sumar
    partes_sustitucion = []
    for capacitor in capacitores:
        partes_sustitucion.append(str(capacitor))
    texto_sustitucion = " + ".join(partes_sustitucion)

    capacitancia_equivalente = sum(capacitores)

    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$C_{{eq}} = {texto_sustitucion} = {capacitancia_equivalente:.4g} \\ \\text{{F}}$$"
    )

    # Paso 3c: Fórmula de carga simbólica 
    ecuacion_carga = sp.Eq(simbolo_carga, simbolo_capacitancia_equivalente * simbolo_voltaje)
    formula_carga_latex = sp.latex(ecuacion_carga)
    pasos_procedimiento.append(
        f"<strong>Fórmula de Carga (Carga Total):</strong><br>$${formula_carga_latex}$$"
    )

    # Paso 3d: Calcular la carga total
    carga_total = capacitancia_equivalente * voltaje_bateria
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$Q = {capacitancia_equivalente:.4g} \\times {voltaje_bateria} = {carga_total:.4g} \\ \\text{{C}}$$"
    )

    # --- Paso 4: Calcular la carga individual en cada capacitor 
    cargas_individuales = []
    for capacitor in capacitores:
        carga_en_capacitor = capacitor * voltaje_bateria
        cargas_individuales.append(carga_en_capacitor)

    # --- Paso 5: Construir la lista de resultados individuales ---
    resultados_individuales = []
    for indice, carga_individual in enumerate(cargas_individuales):
        nombre_componente = f"C{indice + 1}"
        resultado_componente = {
            'componente': nombre_componente,
            'carga': f"{carga_individual:.4g} C",
            'voltaje': f"{voltaje_bateria:.4g} V"
        }
        resultados_individuales.append(resultado_componente)

    # --- Dicionario a retornar ---
    resultados_completos = {
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': f"{capacitancia_equivalente:.4g} F",
        'total_title_2': 'Carga Total',
        'total_val_2': f"{carga_total:.4g} C",
        'individual_results': resultados_individuales,
        'procedimiento': pasos_procedimiento
    }
    return resultados_completos


def resolver_circuito(tipo_componente, tipo_conexion, voltaje_bateria, componentes):
    """
    Función principal que recibe los datos del formulario, valida los valores,
    y redirige al cálculo correcto según el tipo de componente y conexión.
    """

    try:
        voltaje_bateria = float(voltaje_bateria)

        valores_numericos = []
        for valor_texto in componentes:
            valor_numerico = float(valor_texto)
            valores_numericos.append(valor_numerico)
        componentes = valores_numericos

    except ValueError:
        return {"error": "Solo se permiten números."}

    if not componentes:
        return {"error": "No hay componentes o los valores son inválidos."}

    # --- Validar que el voltaje y todos los componentes sean positivos ---
    if voltaje_bateria <= 0:
        return {"error": "El voltaje de la batería debe ser un valor positivo."}

    for indice, valor in enumerate(componentes):
        if valor <= 0:
            return {"error": f"El componente #{indice + 1} tiene un valor inválido ({valor}). Todos los valores deben ser positivos."}

    # --- Seleccionar la función de cálculo apropiada ---
    if tipo_componente == 'resistor':
        if tipo_conexion == 'series':
            return resolver_resistores_serie(voltaje_bateria, componentes)
        elif tipo_conexion == 'parallel':
            return resolver_resistores_paralelo(voltaje_bateria, componentes)

    elif tipo_componente == 'capacitor':
        if tipo_conexion == 'series':
            return resolver_capacitores_serie(voltaje_bateria, componentes)
        elif tipo_conexion == 'parallel':
            return resolver_capacitores_paralelo(voltaje_bateria, componentes)

    return {"error": "Tipo de componente o conexión inválidos."}
