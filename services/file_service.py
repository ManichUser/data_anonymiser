"""Service pour la gestion des fichiers"""
import pandas as pd
import io
from werkzeug.utils import secure_filename

class FileService:
    
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    @staticmethod
    def is_allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in FileService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def read_file(file):
        """Lit un fichier et retourne un DataFrame"""
        filename = secure_filename(file.filename)
        extension = filename.rsplit('.', 1)[1].lower()
        
        if extension == 'csv':
            return pd.read_csv(file)
        elif extension in ['xlsx', 'xls']:
            return pd.read_excel(file)
        else:
            raise ValueError(f"Format non supporté: {extension}")
    
    @staticmethod
    def dataframe_to_excel(df, filename):
        """Convertit un DataFrame en fichier Excel en mémoire"""
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Data')
        output.seek(0)
        return output
