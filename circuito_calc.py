import sympy as sp
import numpy as np

def resolver_resistores_serie(v_bateria, resistores):
    n = len(resistores)
    # Crear símbolos usando sympy
    R_syms = sp.symbols(f'R1:{n+1}')
    if n == 1:
        R_syms = (R_syms,)
    R_eq, V, I = sp.symbols('R_eq V I')
    
    eq_req = sp.Eq(R_eq, sum(R_syms))
    
    pasos = []
    
    pasos.append(f"**Fórmula del circuito (Resistencia Equivalente en Serie):**\n$${sp.latex(eq_req)}$$")
    
    sustitucion_req = " + ".join([str(r) for r in resistores])
    req = sum(resistores)
    pasos.append(f"**Sustitución:**\n$$R_{{eq}} = {sustitucion_req} = {req:.4g} \\ \\Omega$$")
    
    eq_ohm = sp.Eq(I, V / R_eq)
    pasos.append(f"**Ley de Ohm (Corriente Total):**\n$${sp.latex(eq_ohm)}$$")
    
    if req > 0:
        i_bateria = v_bateria / req
        pasos.append(f"**Sustitución:**\n$$I = \\frac{{{v_bateria}}}{{{req:.4g}}} = {i_bateria:.4g} \\ \\text{{A}}$$")
    else:
        i_bateria = 0
        pasos.append(f"**Sustitución:**\n$$R_{{eq}}$$ es 0, hay un cortocircuito.")
        
    v_cada_uno = [i_bateria * r for r in resistores]
    
    resultados_individuales = [
        {'componente': f'R{i+1}', 'voltaje': f"{v:.4g} V", 'corriente': f"{i_bateria:.4g} A"}
        for i, v in enumerate(v_cada_uno)
    ]
    
    return {
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': f"{req:.4g} Ω",
        'total_title_2': 'Corriente Total',
        'total_val_2': f"{i_bateria:.4g} A",
        'individual_results': resultados_individuales,
        'procedimiento': pasos
    }

def resolver_resistores_paralelo(v_bateria, resistores):
    n = len(resistores)
    R_syms = sp.symbols(f'R1:{n+1}')
    if n == 1:
        R_syms = (R_syms,)
    R_eq, V, I = sp.symbols('R_eq V I_total')
    
    eq_req_inv = sp.Eq(1/R_eq, sum(1/r for r in R_syms))
    
    pasos = []
    pasos.append(f"**Fórmula del circuito (Resistencia Equivalente en Paralelo):**\n$${sp.latex(eq_req_inv)}$$")
    
    sust_req = " + ".join([f"\\frac{{1}}{{{r}}}" for r in resistores])
    sum_inv = np.sum([1/r if r > 0 else float('inf') for r in resistores])
    req = 1 / sum_inv if sum_inv > 0 else 0
    
    pasos.append(f"**Sustitución:**\n$$\\frac{{1}}{{R_{{eq}}}} = {sust_req} = {sum_inv:.4g} \\ \\Omega^{{-1}}$$")
    pasos.append(f"$$R_{{eq}} = \\frac{{1}}{{{sum_inv:.4g}}} = {req:.4g} \\ \\Omega$$")
    
    eq_ohm = sp.Eq(I, V / R_eq)
    pasos.append(f"**Ley de Ohm (Corriente Total):**\n$${sp.latex(eq_ohm)}$$")
    
    i_cada_uno = [v_bateria / r if r > 0 else float('inf') for r in resistores]
    i_bateria = sum(i_cada_uno)
    
    pasos.append(f"**Sustitución:**\n$$I_{{total}} = \\frac{{{v_bateria}}}{{{req:.4g}}} = {i_bateria:.4g} \\ \\text{{A}}$$")
    
    resultados_individuales = [
        {'componente': f'R{i+1}', 'voltaje': f"{v_bateria:.4g} V", 'corriente': f"{i_cada_uno[i]:.4g} A"}
        for i in range(n)
    ]
    
    return {
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': f"{req:.4g} Ω",
        'total_title_2': 'Corriente Total',
        'total_val_2': f"{i_bateria:.4g} A",
        'individual_results': resultados_individuales,
        'procedimiento': pasos
    }

def resolver_capacitores_serie(v_bateria, capacitores):
    n = len(capacitores)
    C_syms = sp.symbols(f'C1:{n+1}')
    if n == 1:
        C_syms = (C_syms,)
    C_eq, V, Q = sp.symbols('C_eq V Q')
    
    eq_ceq_inv = sp.Eq(1/C_eq, sum(1/c for c in C_syms))
    
    pasos = []
    pasos.append(f"**Fórmula del circuito (Capacitancia Equivalente en Serie):**\n$${sp.latex(eq_ceq_inv)}$$")
    
    sust_ceq = " + ".join([f"\\frac{{1}}{{{c}}}" for c in capacitores])
    sum_inv = np.sum([1/c if c > 0 else float('inf') for c in capacitores])
    ceq = 1 / sum_inv if sum_inv > 0 else 0
    
    pasos.append(f"**Sustitución:**\n$$\\frac{{1}}{{C_{{eq}}}} = {sust_ceq} = {sum_inv:.4g} \\ \\text{{F}}^{{-1}}$$")
    pasos.append(f"$$C_{{eq}} = \\frac{{1}}{{{sum_inv:.4g}}} = {ceq:.4g} \\ \\text{{F}}$$")
    
    eq_carga = sp.Eq(Q, C_eq * V)
    pasos.append(f"**Fórmula de Carga (Carga Total):**\n$${sp.latex(eq_carga)}$$")
    
    q_total = ceq * v_bateria
    # El usuario solicitó específicamente que la carga total sea en V, por lo tanto usamos V en lugar de C.
    pasos.append(f"**Sustitución:**\n$$Q = {ceq:.4g} \\times {v_bateria} = {q_total:.4g} \\ \\text{{V}}$$")
    
    v_cada_uno = [q_total / c if c > 0 else 0 for c in capacitores]
    
    resultados_individuales = [
        {'componente': f'C{i+1}', 'carga': f"{q_total:.4g} V", 'voltaje': f"{v:.4g} V"}
        for i, v in enumerate(v_cada_uno)
    ]
    
    return {
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': f"{ceq:.4g} F",
        'total_title_2': 'Carga Total',
        'total_val_2': f"{q_total:.4g} V",
        'individual_results': resultados_individuales,
        'procedimiento': pasos
    }

def resolver_capacitores_paralelo(v_bateria, capacitores):
    n = len(capacitores)
    C_syms = sp.symbols(f'C1:{n+1}')
    if n == 1:
        C_syms = (C_syms,)
    C_eq, V, Q = sp.symbols('C_eq V Q')
    
    eq_ceq = sp.Eq(C_eq, sum(C_syms))
    
    pasos = []
    pasos.append(f"**Fórmula del circuito (Capacitancia Equivalente en Paralelo):**\n$${sp.latex(eq_ceq)}$$")
    
    sustitucion_ceq = " + ".join([str(c) for c in capacitores])
    ceq = sum(capacitores)
    pasos.append(f"**Sustitución:**\n$$C_{{eq}} = {sustitucion_ceq} = {ceq:.4g} \\ \\text{{F}}$$")
    
    eq_carga = sp.Eq(Q, C_eq * V)
    pasos.append(f"**Fórmula de Carga (Carga Total):**\n$${sp.latex(eq_carga)}$$")
    
    q_total = ceq * v_bateria
    pasos.append(f"**Sustitución:**\n$$Q = {ceq:.4g} \\times {v_bateria} = {q_total:.4g} \\ \\text{{V}}$$")
    
    q_cada_uno = [c * v_bateria for c in capacitores]
    
    resultados_individuales = [
        {'componente': f'C{i+1}', 'carga': f"{q:.4g} V", 'voltaje': f"{v_bateria:.4g} V"}
        for i, q in enumerate(q_cada_uno)
    ]
    
    return {
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': f"{ceq:.4g} F",
        'total_title_2': 'Carga Total',
        'total_val_2': f"{q_total:.4g} V",
        'individual_results': resultados_individuales,
        'procedimiento': pasos
    }

def resolver_circuito(tipo_comp, conexion, v_bateria, componentes):
    try:
        v_bateria = float(v_bateria)
        componentes = [float(c) for c in componentes]
    except ValueError:
        return {"error": "Solo se permiten números."}
        
    if not componentes:
        return {"error": "No hay componentes o los valores son inválidos."}
        
    if tipo_comp == 'resistor':
        if conexion == 'series':
            return resolver_resistores_serie(v_bateria, componentes)
        elif conexion == 'parallel':
            return resolver_resistores_paralelo(v_bateria, componentes)
    elif tipo_comp == 'capacitor':
        if conexion == 'series':
            return resolver_capacitores_serie(v_bateria, componentes)
        elif conexion == 'parallel':
            return resolver_capacitores_paralelo(v_bateria, componentes)
            
    return {"error": "Tipo de componente o conexión inválidos."}
