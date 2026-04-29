document.addEventListener('DOMContentLoaded', () => {
    const addBtn = document.getElementById('add_btn');
    const componentsBody = document.getElementById('components_body');
    const compTypeSelect = document.getElementById('component_type');
    const valHeader = document.getElementById('val_header');
    
    // scroll a resultados
    const resultsPanel = document.getElementById('results_panel');
    if (resultsPanel) {
        resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

   
    if (typeof MathJax !== 'undefined' && resultsPanel) {
        MathJax.typeset();
    }

    //Cambio de labels
    compTypeSelect.addEventListener('change', (e) => {
        const type = e.target.value;
        if (type === 'resistor') {
            valHeader.textContent = 'Resistencia (Solo números)';
            updateComponentLabels('R');
        } else {
            valHeader.textContent = 'Capacitancia (Solo números)';
            updateComponentLabels('C');
        }
        //  unidades en filas existentes
        const unit = type === 'resistor' ? 'Ω' : 'F';
        componentsBody.querySelectorAll('.unit-label').forEach(span => {
            span.textContent = unit;
        });
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
        const unit = compTypeSelect.value === 'resistor' ? 'Ω' : 'F';
        
        tr.innerHTML = `
            <td class="py-4 text-slate-500 font-mono comp-label">${prefix}${componentsBody.children.length + 1}</td>
            <td class="py-4">
                <input type="number" step="any" name="componentes[]" class="bg-transparent border-none text-slate-800 font-mono focus:ring-0 p-0 w-24 comp-value" placeholder="Valor" required>
                <span class="text-slate-400 text-xs ml-1 unit-label">${unit}</span>
            </td>
            <td class="py-4 text-right">
                <button type="button" class="material-symbols-outlined text-slate-400 hover:text-rose-500 transition-colors remove-btn">delete</button>
            </td>
        `;
        
        tr.querySelector('.remove-btn').addEventListener('click', () => {
            tr.remove();
            updateComponentLabels(compTypeSelect.value === 'resistor' ? 'R' : 'C');
        });
        
        componentsBody.appendChild(tr);
    }

    addRow();
    addRow();

    addBtn.addEventListener('click', addRow);
});
