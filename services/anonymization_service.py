"""Service responsable de l'anonymisation des données"""
import pandas as pd
import hashlib

class AnonymizationService:
    
    @staticmethod
    def anonymize_value(value):
        """Anonymise une valeur en utilisant SHA-256"""
        if pd.isna(value):
            return value
        return hashlib.sha256(str(value).encode()).hexdigest()[:16]
    
    @staticmethod
    def anonymize_dataframe(df, columns):
        """Anonymise les colonnes spécifiées d'un DataFrame"""
        df_copy = df.copy()
        for col in columns:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].apply(AnonymizationService.anonymize_value)
        return df_copy
