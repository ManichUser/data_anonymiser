"""
Application Flask pour l'anonymisation de données sensibles
Structure modulaire et évolutive
"""

from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max
app.config['UPLOAD_FOLDER'] = 'uploads'

# Importer les services
from services.anonymization_service import AnonymizationService
from services.file_service import FileService
from services.merge_service import MergeService

# Stockage temporaire en mémoire
session_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Traite l'upload des fichiers et retourne les colonnes"""
    try:
        files = request.files.getlist('files')
        dataframes = []
        file_info = []
        
        for file in files:
            if not FileService.is_allowed_file(file.filename):
                return jsonify({'error': f'Format non supporté: {file.filename}'}), 400
            
            df = FileService.read_file(file)
            dataframes.append(df)
            file_info.append({
                'name': secure_filename(file.filename),
                'columns': list(df.columns)
            })
        
        # Trouver colonnes communes
        common_columns = MergeService.find_common_columns(dataframes)
        
        # Stocker en session
        session_id = str(datetime.now().timestamp())
        session_data[session_id] = {
            'dataframes': dataframes,
            'file_names': [f['name'] for f in file_info]
        }
        
        return jsonify({
            'session_id': session_id,
            'files': file_info,
            'common_columns': common_columns
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/anonymize', methods=['POST'])
def anonymize():
    """Effectue l'anonymisation et la jointure"""
    try:
        data = request.json
        selections = data['selections']
        merge_column = data['merge_column']
        
        session_id = list(session_data.keys())[-1]
        session = session_data[session_id]
        
        anonymized_dfs = []
        results = []
        
        # Anonymiser chaque fichier
        for idx, (df, cols_to_anonymize) in enumerate(zip(session['dataframes'], selections)):
            anon_df = AnonymizationService.anonymize_dataframe(df, cols_to_anonymize)
            anonymized_dfs.append(anon_df)
            
            preview_html = anon_df.head(10).to_html(classes='table', index=False)
            
            results.append({
                'name': session['file_names'][idx],
                'preview': preview_html,
                'index': idx
            })
        
        # Créer fichier de jointure
        merged_df = MergeService.merge_dataframes(anonymized_dfs, merge_column)
        merged_preview = merged_df.head(10).to_html(classes='table', index=False)
        
        results.append({
            'name': 'Fichier_Jointure.xlsx',
            'preview': merged_preview,
            'index': len(anonymized_dfs)
        })
        
        session['anonymized'] = anonymized_dfs
        session['merged'] = merged_df
        
        return jsonify({'results': results})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<int:index>')
def download(index):
    """Télécharge un fichier anonymisé"""
    try:
        session_id = list(session_data.keys())[-1]
        session = session_data[session_id]
        
        if index < len(session['anonymized']):
            df = session['anonymized'][index]
            filename = session['file_names'][index]
        else:
            df = session['merged']
            filename = 'Fichier_Jointure.xlsx'
        
        output = FileService.dataframe_to_excel(df, filename)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
