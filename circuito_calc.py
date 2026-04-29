import re
import sympy as sp


PREFIJOS_METRICOS = {
    'p': 1e-12,
    'n': 1e-9,
    'u': 1e-6,
    'm': 1e-3,
    'K': 1e3,
    'M': 1e6,
    'G': 1e9,
}


PATRON_VALOR_PREFIJO = re.compile(
    r'^\s*([+-]?\d+\.?\d*)\s*([pnumKMG])?\s*$'
)


def parsear_valor_con_prefijo(texto):
    texto = texto.strip()
    coincidencia = PATRON_VALOR_PREFIJO.match(texto)

    if not coincidencia:
        raise ValueError(
            f"Formato inválido: '{texto}'. "
            f"Use un número seguido opcionalmente de un prefijo (p, n, u, m, K, M, G)."
        )

    parte_numerica = float(coincidencia.group(1))
    prefijo = coincidencia.group(2)

    if prefijo:
        multiplicador = PREFIJOS_METRICOS[prefijo]
        return parte_numerica * multiplicador
    else:
        return parte_numerica


def formatear_con_prefijo(valor, unidad):
    
    
    if valor == 0:
        return f"0 {unidad}"

    valor_abs = abs(valor)

    prefijos_ordenados = [
        ('p', 1e-12),
        ('n', 1e-9),
        ('u', 1e-6),
        ('m', 1e-3),
        ('', 1),
        ('K', 1e3),
        ('M', 1e6),
        ('G', 1e9),
    ]

    mejor_prefijo = ''
    mejor_multiplicador = 1

    for simbolo, multiplicador in prefijos_ordenados:
        if valor_abs >= multiplicador * 0.999:
            mejor_prefijo = simbolo
            mejor_multiplicador = multiplicador

    valor_formateado = valor / mejor_multiplicador
    return f"{valor_formateado:.4g} {mejor_prefijo}{unidad}"


def _prefijo_info(valor):
    if valor == 0:
        return (0, '')

    valor_abs = abs(valor)
    prefijos_ordenados = [
        ('p', 1e-12), ('n', 1e-9), ('u', 1e-6), ('m', 1e-3),
        ('', 1), ('K', 1e3), ('M', 1e6), ('G', 1e9),
    ]
    mejor_prefijo = ''
    mejor_multiplicador = 1
    for simbolo, multiplicador in prefijos_ordenados:
        if valor_abs >= multiplicador * 0.999:
            mejor_prefijo = simbolo
            mejor_multiplicador = multiplicador
    return (valor / mejor_multiplicador, mejor_prefijo)


def _latex_val(valor, unidad):
    escalado, prefijo = _prefijo_info(valor)
    return f"{escalado:.4g} \\ \\text{{{prefijo}{unidad}}}"


def _num_con_prefijo(valor, unidad=''):
    escalado, prefijo = _prefijo_info(valor)
    if unidad:
        return f"{escalado:.4g} \\ \\text{{{prefijo}{unidad}}}"
    return f"{escalado:.4g}{prefijo}"



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
        escalado, prefijo = _prefijo_info(resistor)
        partes_sustitucion.append(f"{escalado:.4g} \\ \\text{{{prefijo}\\Omega}}")
    texto_sustitucion = " + ".join(partes_sustitucion)

    resistencia_equivalente = sum(resistores)

    escalado_req, prefijo_req = _prefijo_info(resistencia_equivalente)
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$R_{{eq}} = {texto_sustitucion} = {escalado_req:.4g} \\ \\text{{{prefijo_req}\\Omega}}$$"
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
        esc_v, pre_v = _prefijo_info(voltaje_bateria)
        esc_r, pre_r = _prefijo_info(resistencia_equivalente)
        esc_i, pre_i = _prefijo_info(corriente_total)
        pasos_procedimiento.append(
            f"<strong>Sustitución:</strong><br>"
            f"$$I = \\frac{{{esc_v:.4g} \\ \\text{{{pre_v}V}}}}{{{esc_r:.4g} \\ \\text{{{pre_r}\\Omega}}}} = {esc_i:.4g} \\ \\text{{{pre_i}A}}$$"
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
            'voltaje': formatear_con_prefijo(voltaje_individual, 'V'),
            'corriente': formatear_con_prefijo(corriente_total, 'A')
        }
        resultados_individuales.append(resultado_componente)

    # --- Se  mete too en dicionario se retorna ---
    resultados_completos = {
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': formatear_con_prefijo(resistencia_equivalente, 'Ω'),
        'total_title_2': 'Corriente Total',
        'total_val_2': formatear_con_prefijo(corriente_total, 'A'),
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
        esc_r, pre_r = _prefijo_info(resistor)
        fraccion_latex = f"\\frac{{1}}{{{esc_r:.4g} \\ \\text{{{pre_r}\\Omega}}}}"
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

    esc_sum, pre_sum = _prefijo_info(suma_inversos_numerica)
    esc_req, pre_req = _prefijo_info(resistencia_equivalente)
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$\\frac{{1}}{{R_{{eq}}}} = {texto_sustitucion} = {esc_sum:.4g} \\ \\text{{{pre_sum}\\Omega^{{-1}}}}$$"
    )
    pasos_procedimiento.append(
        f"$$R_{{eq}} = \\frac{{1}}{{{esc_sum:.4g} \\ \\text{{{pre_sum}\\Omega^{{-1}}}}}} = {esc_req:.4g} \\ \\text{{{pre_req}\\Omega}}$$"
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

    esc_v, pre_v = _prefijo_info(voltaje_bateria)
    esc_r, pre_r = _prefijo_info(resistencia_equivalente)
    esc_it, pre_it = _prefijo_info(corriente_total)
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$I_{{total}} = \\frac{{{esc_v:.4g} \\ \\text{{{pre_v}V}}}}{{{esc_r:.4g} \\ \\text{{{pre_r}\\Omega}}}} = {esc_it:.4g} \\ \\text{{{pre_it}A}}$$"
    )

    # --- Paso 5: Construir la lista de resultados individuales ---
    resultados_individuales = []
    for indice in range(cantidad_resistores):
        nombre_componente = f"R{indice + 1}"
        resultado_componente = {
            'componente': nombre_componente,
            'voltaje': formatear_con_prefijo(voltaje_bateria, 'V'),
            'corriente': formatear_con_prefijo(corrientes_individuales[indice], 'A')
        }
        resultados_individuales.append(resultado_componente)

    # --- eL dicionario a retornar ---
    resultados_completos = {
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': formatear_con_prefijo(resistencia_equivalente, 'Ω'),
        'total_title_2': 'Corriente Total',
        'total_val_2': formatear_con_prefijo(corriente_total, 'A'),
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
        esc_c, pre_c = _prefijo_info(capacitor)
        fraccion_latex = f"\\frac{{1}}{{{esc_c:.4g} \\ \\text{{{pre_c}F}}}}"
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

    esc_sum, pre_sum = _prefijo_info(suma_inversos_numerica)
    esc_ceq, pre_ceq = _prefijo_info(capacitancia_equivalente)
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$\\frac{{1}}{{C_{{eq}}}} = {texto_sustitucion} = {esc_sum:.4g} \\ \\text{{{pre_sum}F^{{-1}}}}$$"
    )
    pasos_procedimiento.append(
        f"$$C_{{eq}} = \\frac{{1}}{{{esc_sum:.4g} \\ \\text{{{pre_sum}F^{{-1}}}}}} = {esc_ceq:.4g} \\ \\text{{{pre_ceq}F}}$$"
    )

    # Paso 3c: Fórmula de carga simbólica
    ecuacion_carga = sp.Eq(simbolo_carga, simbolo_capacitancia_equivalente * simbolo_voltaje)
    formula_carga_latex = sp.latex(ecuacion_carga)
    pasos_procedimiento.append(
        f"<strong>Fórmula de Carga (Carga Total):</strong><br>$${formula_carga_latex}$$"
    )

    # Paso 3d: Calcular la carga total del circuito
    carga_total = capacitancia_equivalente * voltaje_bateria
    esc_ceq2, pre_ceq2 = _prefijo_info(capacitancia_equivalente)
    esc_vb, pre_vb = _prefijo_info(voltaje_bateria)
    esc_qt, pre_qt = _prefijo_info(carga_total)
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$Q = {esc_ceq2:.4g} \\ \\text{{{pre_ceq2}F}} \\times {esc_vb:.4g} \\ \\text{{{pre_vb}V}} = {esc_qt:.4g} \\ \\text{{{pre_qt}C}}$$"
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
            'carga': formatear_con_prefijo(carga_total, 'C'),
            'voltaje': formatear_con_prefijo(voltaje_individual, 'V')
        }
        resultados_individuales.append(resultado_componente)

    # --- Dicionario a retornar --- 
    resultados_completos = {
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': formatear_con_prefijo(capacitancia_equivalente, 'F'),
        'total_title_2': 'Carga Total',
        'total_val_2': formatear_con_prefijo(carga_total, 'C'),
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
        esc_c, pre_c = _prefijo_info(capacitor)
        partes_sustitucion.append(f"{esc_c:.4g} \\ \\text{{{pre_c}F}}")
    texto_sustitucion = " + ".join(partes_sustitucion)

    capacitancia_equivalente = sum(capacitores)

    esc_ceq, pre_ceq = _prefijo_info(capacitancia_equivalente)
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$C_{{eq}} = {texto_sustitucion} = {esc_ceq:.4g} \\ \\text{{{pre_ceq}F}}$$"
    )

    # Paso 3c: Fórmula de carga simbólica 
    ecuacion_carga = sp.Eq(simbolo_carga, simbolo_capacitancia_equivalente * simbolo_voltaje)
    formula_carga_latex = sp.latex(ecuacion_carga)
    pasos_procedimiento.append(
        f"<strong>Fórmula de Carga (Carga Total):</strong><br>$${formula_carga_latex}$$"
    )

    # Paso 3d: Calcular la carga total
    carga_total = capacitancia_equivalente * voltaje_bateria
    esc_ceq2, pre_ceq2 = _prefijo_info(capacitancia_equivalente)
    esc_vb, pre_vb = _prefijo_info(voltaje_bateria)
    esc_qt, pre_qt = _prefijo_info(carga_total)
    pasos_procedimiento.append(
        f"<strong>Sustitución:</strong><br>"
        f"$$Q = {esc_ceq2:.4g} \\ \\text{{{pre_ceq2}F}} \\times {esc_vb:.4g} \\ \\text{{{pre_vb}V}} = {esc_qt:.4g} \\ \\text{{{pre_qt}C}}$$"
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
            'carga': formatear_con_prefijo(carga_individual, 'C'),
            'voltaje': formatear_con_prefijo(voltaje_bateria, 'V')
        }
        resultados_individuales.append(resultado_componente)

    # --- Dicionario a retornar ---
    resultados_completos = {
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': formatear_con_prefijo(capacitancia_equivalente, 'F'),
        'total_title_2': 'Carga Total',
        'total_val_2': formatear_con_prefijo(carga_total, 'C'),
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
        voltaje_bateria = parsear_valor_con_prefijo(str(voltaje_bateria))

        valores_numericos = []
        for valor_texto in componentes:
            valor_numerico = parsear_valor_con_prefijo(str(valor_texto))
            valores_numericos.append(valor_numerico)
        componentes = valores_numericos

    except ValueError as error_valor:
        return {"error": f"Error en los valores ingresados: {error_valor}"}

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
