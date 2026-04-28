import re

PREFIX_MULTIPLIERS = {
    'p': 1e-12,
    'n': 1e-9,
    'u': 1e-6,
    'm': 1e-3,
    'k': 1e3,
    'K': 1e3,
    'M': 1e6,
    'G': 1e9
}

def parse_value(val_str):
    """
    Parses a string like '53 mV' or '10k' and returns a float.
    Extracts the number and any known prefix.
    """
    if not isinstance(val_str, str):
        val_str = str(val_str)
    
    val_str = val_str.strip()
    # Match number (including decimals) and optional prefix/unit part
    match = re.match(r'^([\d\.]+)\s*([a-zA-Z]*)$', val_str)
    
    if not match:
        try:
            return float(val_str)
        except ValueError:
            return 0.0

    number_str = match.group(1)
    suffix = match.group(2)
    
    value = float(number_str)
    
    if suffix:
        # Check first character of suffix for prefix
        first_char = suffix[0]
        if first_char in PREFIX_MULTIPLIERS:
            value *= PREFIX_MULTIPLIERS[first_char]
            
    return value

def format_value(value, unit_type):
    """
    Format a value using appropriate prefixes (m, u, n, p, k, M) based on magnitude.
    """
    abs_val = abs(value)
    if abs_val == 0:
        return f"0 {unit_type}"
    elif abs_val >= 1e6:
        return f"{value / 1e6:.3g} M{unit_type}"
    elif abs_val >= 1e3:
        return f"{value / 1e3:.3g} k{unit_type}"
    elif abs_val >= 1:
        return f"{value:.3g} {unit_type}"
    elif abs_val >= 1e-3:
        return f"{value * 1e3:.3g} m{unit_type}"
    elif abs_val >= 1e-6:
        return f"{value * 1e6:.3g} µ{unit_type}"
    elif abs_val >= 1e-9:
        return f"{value * 1e9:.3g} n{unit_type}"
    else:
        return f"{value * 1e12:.3g} p{unit_type}"


def solve_resistors_series(v_battery, resistors):
    """
    Resistors in series.
    Returns:
    - req: Equivalent resistance
    - i_battery: Current through battery
    - v_each: Voltage across each resistor
    """
    req = sum(resistors)
    
    if req > 0:
        i_battery = v_battery / req
    else:
        i_battery = 0
        
    v_each = [i_battery * r for r in resistors]
    
    return {
        'req': format_value(req, 'Ω'),
        'i_battery': format_value(i_battery, 'A'),
        'individual_results': [
            {'component': f'R{i+1}', 'voltage': format_value(v, 'V'), 'current': format_value(i_battery, 'A')}
            for i, v in enumerate(v_each)
        ],
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': format_value(req, 'Ω'),
        'total_title_2': 'Corriente Total',
        'total_val_2': format_value(i_battery, 'A')
    }

def solve_resistors_parallel(v_battery, resistors):
    """
    Resistors in parallel.
    Returns:
    - req: Equivalent resistance
    - i_battery: Current through battery
    - i_each: Current through each resistor
    """
    sum_inv = 0
    i_each = []
    
    for r in resistors:
        if r > 0:
            sum_inv += 1 / r
            i_each.append(v_battery / r)
        else:
            i_each.append(float('inf'))
            
    if sum_inv > 0:
        req = 1 / sum_inv
    else:
        req = 0
        
    i_battery = sum(i_each) if all(i != float('inf') for i in i_each) else float('inf')
    
    return {
        'req': format_value(req, 'Ω'),
        'i_battery': format_value(i_battery, 'A'),
        'individual_results': [
            {'component': f'R{i+1}', 'voltage': format_value(v_battery, 'V'), 'current': format_value(i_each[i], 'A')}
            for i in range(len(resistors))
        ],
        'total_title_1': 'Resistencia Equivalente',
        'total_val_1': format_value(req, 'Ω'),
        'total_title_2': 'Corriente Total',
        'total_val_2': format_value(i_battery, 'A')
    }

def solve_capacitors_series(v_battery, capacitors):
    """
    Capacitors in series.
    Returns:
    - ceq: Equivalent capacitance
    - q_each: Charge on each capacitor
    - v_each: Voltage across each capacitor
    """
    sum_inv = 0
    for c in capacitors:
        if c > 0:
            sum_inv += 1 / c
        else:
            sum_inv += float('inf')
            
    if sum_inv > 0:
        ceq = 1 / sum_inv
    else:
        ceq = 0
        
    q_total = ceq * v_battery
    
    v_each = []
    for c in capacitors:
        if c > 0:
            v_each.append(q_total / c)
        else:
            v_each.append(0)
            
    return {
        'ceq': format_value(ceq, 'F'),
        'q_total': format_value(q_total, 'C'),
        'individual_results': [
            {'component': f'C{i+1}', 'charge': format_value(q_total, 'C'), 'voltage': format_value(v, 'V')}
            for i, v in enumerate(v_each)
        ],
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': format_value(ceq, 'F'),
        'total_title_2': 'Carga Total',
        'total_val_2': format_value(q_total, 'C')
    }

def solve_capacitors_parallel(v_battery, capacitors):
    """
    Capacitors in parallel.
    Returns:
    - ceq: Equivalent capacitance
    - q_total: Total charge
    - q_each: Charge on each capacitor
    """
    ceq = sum(capacitors)
    q_total = ceq * v_battery
    
    q_each = [c * v_battery for c in capacitors]
    
    return {
        'ceq': format_value(ceq, 'F'),
        'q_total': format_value(q_total, 'C'),
        'individual_results': [
            {'component': f'C{i+1}', 'charge': format_value(q, 'C'), 'voltage': format_value(v_battery, 'V')}
            for i, q in enumerate(q_each)
        ],
        'total_title_1': 'Capacitancia Equivalente',
        'total_val_1': format_value(ceq, 'F'),
        'total_title_2': 'Carga Total',
        'total_val_2': format_value(q_total, 'C')
    }

def solve_circuit(comp_type, connection, v_str, components_str_list):
    """
    Main entry point for calculating.
    """
    v_battery = parse_value(v_str)
    components = [parse_value(c) for c in components_str_list if str(c).strip()]
    
    if not components:
        return {"error": "No components provided or values invalid."}
        
    if comp_type == 'resistor':
        if connection == 'series':
            return solve_resistors_series(v_battery, components)
        elif connection == 'parallel':
            return solve_resistors_parallel(v_battery, components)
    elif comp_type == 'capacitor':
        if connection == 'series':
            return solve_capacitors_series(v_battery, components)
        elif connection == 'parallel':
            return solve_capacitors_parallel(v_battery, components)
            
    return {"error": "Invalid component or connection type."}
