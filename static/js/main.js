document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add_btn');
    const calcBtn = document.getElementById('calculate_btn');
    const componentsBody = document.getElementById('components_body');
    const compTypeSelect = document.getElementById('component_type');
    const valHeader = document.getElementById('val_header');
    const resultsPanel = document.getElementById('results_panel');
    
    let componentCount = 0;

    // Actualizar labels según tipo de componente
    compTypeSelect.addEventListener('change', (e) => {
        const type = e.target.value;
        if (type === 'resistor') {
            valHeader.textContent = 'Resistencia (Ej. 10 k, 500)';
            updateComponentLabels('R');
        } else {
            valHeader.textContent = 'Capacitancia (Ej. 10 uF, 50 nF)';
            updateComponentLabels('C');
        }
    });

    function updateComponentLabels(prefix) {
        const rows = componentsBody.querySelectorAll('tr');
        rows.forEach((row, index) => {
            row.querySelector('.comp-label').textContent = `${prefix}${index + 1}`;
        });
    }

    // Añadir fila
    function addRow() {
        componentCount++;
        const tr = document.createElement('tr');
        const prefix = compTypeSelect.value === 'resistor' ? 'R' : 'C';
        
        tr.innerHTML = `
            <td class="comp-label font-bold">${prefix}${componentsBody.children.length + 1}</td>
            <td>
                <input type="text" class="comp-value" placeholder="Valor (ej. 10k, 5 u)" required>
            </td>
            <td>
                <button type="button" class="btn btn-danger remove-btn">Eliminar</button>
            </td>
        `;
        
        tr.querySelector('.remove-btn').addEventListener('click', () => {
            tr.remove();
            updateComponentLabels(compTypeSelect.value === 'resistor' ? 'R' : 'C');
        });
        
        componentsBody.appendChild(tr);
    }

    // Inicializar con 2 componentes
    addRow();
    addRow();

    addBtn.addEventListener('click', addRow);

    // Calcular
    calcBtn.addEventListener('click', async () => {
        const batteryVoltage = document.getElementById('battery_voltage').value.trim();
        const componentType = document.getElementById('component_type').value;
        const connectionType = document.getElementById('connection_type').value;
        
        const inputs = componentsBody.querySelectorAll('.comp-value');
        const components = Array.from(inputs).map(input => input.value.trim()).filter(val => val !== '');
        
        if (!batteryVoltage) {
            alert('Por favor, ingresa el voltaje de la batería.');
            return;
        }

        if (components.length === 0) {
            alert('Por favor, ingresa al menos un componente.');
            return;
        }

        try {
            calcBtn.disabled = true;
            calcBtn.textContent = 'Calculando...';

            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    battery_voltage: batteryVoltage,
                    component_type: componentType,
                    connection_type: connectionType,
                    components: components
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Error en el cálculo');
            }

            displayResults(data, componentType, connectionType);

        } catch (error) {
            alert(error.message);
        } finally {
            calcBtn.disabled = false;
            calcBtn.textContent = 'Calcular Circuito';
        }
    });

    function displayResults(data, compType, connType) {
        resultsPanel.style.display = 'block';
        
        // Totales
        document.getElementById('res_total_title_1').textContent = data.total_title_1;
        document.getElementById('res_total_val_1').textContent = data.total_val_1;
        document.getElementById('res_total_title_2').textContent = data.total_title_2;
        document.getElementById('res_total_val_2').textContent = data.total_val_2;
        
        // Tabla de resultados individuales
        const theadTr = document.getElementById('results_thead_tr');
        const tbody = document.getElementById('results_tbody');
        
        theadTr.innerHTML = '';
        tbody.innerHTML = '';
        
        // Configurar cabeceras
        theadTr.innerHTML += `<th>Componente</th>`;
        
        if (compType === 'resistor') {
            theadTr.innerHTML += `<th>Voltaje</th><th>Corriente</th>`;
        } else {
            theadTr.innerHTML += `<th>Carga</th><th>Voltaje</th>`;
        }
        
        // Configurar filas
        data.individual_results.forEach(res => {
            const tr = document.createElement('tr');
            tr.innerHTML += `<td><strong>${res.component}</strong></td>`;
            
            if (compType === 'resistor') {
                tr.innerHTML += `<td>${res.voltage}</td><td>${res.current}</td>`;
            } else {
                tr.innerHTML += `<td>${res.charge}</td><td>${res.voltage}</td>`;
            }
            
            tbody.appendChild(tr);
        });

        // Scroll a los resultados
        resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
});
