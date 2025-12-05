let filesData = {};
let currentStep = 1;

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
    
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function showStep(step) {
    document.querySelectorAll('.step').forEach(s => s.classList.remove('active'));
    document.getElementById('step' + step).classList.add('active');
    currentStep = step;
}

function generateFileInputs() {
    const count = parseInt(document.getElementById('fileCount').value);
    const container = document.getElementById('fileInputs');
    container.innerHTML = '';
    
    for (let i = 0; i < count; i++) {
        container.innerHTML += `
            <div class="file-input-wrapper">
                <label>Fichier ${i + 1}</label>
                <input type="file" id="file${i}" accept=".csv,.xlsx,.xls" required>
            </div>
        `;
    }
    
    showStep(2);
}

async function uploadFiles() {
    const count = parseInt(document.getElementById('fileCount').value);
    const formData = new FormData();
    
    for (let i = 0; i < count; i++) {
        const fileInput = document.getElementById('file' + i);
        if (!fileInput.files[0]) {
            alert('Veuillez sélectionner tous les fichiers');
            return;
        }
        formData.append('files', fileInput.files[0]);
    }
    
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<div class="spinner"></div><p>Analyse des fichiers...</p>';
    document.getElementById('step2').appendChild(loadingDiv);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        filesData = data;
        
        displayColumnSelectors(data);
        showStep(3);
    } catch (error) {
        alert('Erreur lors du téléversement: ' + error);
    } finally {
        loadingDiv.remove();
    }
}

function displayColumnSelectors(data) {
    const container = document.getElementById('columnSelectors');
    const mergeSelect = document.getElementById('mergeColumn');
    container.innerHTML = '';
    mergeSelect.innerHTML = '';
    
    const commonCols = data.common_columns;
    commonCols.forEach(col => {
        mergeSelect.innerHTML += `<option value="${col}">${col}</option>`;
    });
    
    data.files.forEach((file, idx) => {
        const div = document.createElement('div');
        div.innerHTML = `
            <h3>📄 ${file.name}</h3>
            <div class="column-selector" id="columns${idx}"></div>
        `;
        container.appendChild(div);
        
        const colContainer = document.getElementById('columns' + idx);
        file.columns.forEach(col => {
            colContainer.innerHTML += `
                <label class="checkbox-label">
                    <input type="checkbox" name="col${idx}" value="${col}">
                    ${col}
                </label>
            `;
        });
    });
}

async function processAnonymization() {
    const selections = [];
    const count = filesData.files.length;
    
    for (let i = 0; i < count; i++) {
        const checked = Array.from(document.querySelectorAll(`input[name="col${i}"]:checked`))
            .map(cb => cb.value);
        selections.push(checked);
    }
    
    const mergeColumn = document.getElementById('mergeColumn').value;
    
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = '<div class="spinner"></div><p>Anonymisation en cours...</p>';
    document.getElementById('step3').appendChild(loadingDiv);
    
    try {
        const response = await fetch('/anonymize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                selections: selections,
                merge_column: mergeColumn
            })
        });
        
        const data = await response.json();
        displayResults(data);
        showStep(4);
    } catch (error) {
        alert('Erreur lors de l\'anonymisation: ' + error);
    } finally {
        loadingDiv.remove();
    }
}

function displayResults(data) {
    const container = document.getElementById('results');
    container.innerHTML = '<div class="alert alert-info">✅ Anonymisation réussie ! Visualisez et téléchargez vos résultats ci-dessous.</div>';
    
    data.results.forEach((result, idx) => {
        const div = document.createElement('div');
        div.innerHTML = `
            <h3>${result.name}</h3>
            <button class="btn btn-success" onclick="downloadFile(${idx})">📥 Télécharger</button>
            <div class="preview-container">
                ${result.preview}
            </div>
        `;
        container.appendChild(div);
    });
}

async function downloadFile(index) {
    window.location.href = `/download/${index}`;
}
