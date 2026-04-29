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
            valHeader.textContent = 'Resistencia (ej: 4.7K, 100, 33n)';
            updateComponentLabels('R');
        } else {
            valHeader.textContent = 'Capacitancia (ej: 100u, 3.3n, 47p)';
            updateComponentLabels('C');
        }
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
                <div class="flex items-center gap-2">
                    <input type="text" inputmode="decimal" name="componentes[]" class="bg-transparent border-none color-white focus:ring-0 p-0 w-20 comp-value" placeholder="Ej: 4.7" required>
                    <select name="prefijos[]" class="bg-zinc-800 border border-pink-900 rounded px-2 py-1 text-slate-200 text-xs focus:border-pink-500 outline-none prefix-select" style="min-width:60px;">
                        <option value="G">G (Giga)</option>
                        <option value="M">M (Mega)</option>
                        <option value="K">K (Kilo)</option>
                        <option value="" selected>— (Base)</option>
                        <option value="m">m (mili)</option>
                        <option value="u">u (micro)</option>
                        <option value="n">n (nano)</option>
                        <option value="p">p (pico)</option>
                    </select>
                    <span class="text-slate-400 text-xs ml-1 unit-label">${unit}</span>
                </div>
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
