document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add_btn');
    const componentsBody = document.getElementById('components_body');
    const compTypeSelect = document.getElementById('component_type');
    const valHeader = document.getElementById('val_header');
    
    // Si la pagina recarga con resultados, scrolleamos a ellos
    const resultsPanel = document.getElementById('results_panel');
    if (resultsPanel) {
        resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    // Actualizar labels según tipo de componente
    compTypeSelect.addEventListener('change', (e) => {
        const type = e.target.value;
        if (type === 'resistor') {
            valHeader.textContent = 'Resistencia (Solo números)';
            updateComponentLabels('R');
        } else {
            valHeader.textContent = 'Capacitancia (Solo números)';
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
        const tr = document.createElement('tr');
        const prefix = compTypeSelect.value === 'resistor' ? 'R' : 'C';
        
        tr.innerHTML = `
            <td class="comp-label font-bold">${prefix}${componentsBody.children.length + 1}</td>
            <td>
                <input type="number" step="any" name="componentes[]" class="comp-value" placeholder="Valor numérico" required>
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

    // Inicializamos con 2 componentes
    addRow();
    addRow();

    addBtn.addEventListener('click', addRow);
});
