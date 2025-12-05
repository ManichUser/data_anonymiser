"""Service pour la fusion des DataFrames"""
import pandas as pd

class MergeService:
    
    @staticmethod
    def find_common_columns(dfs):
        """Trouve les colonnes communes entre plusieurs DataFrames"""
        if not dfs:
            return []
        common = set(dfs[0].columns)
        for df in dfs[1:]:
            common = common.intersection(set(df.columns))
        return list(common)
    
    @staticmethod
    def merge_dataframes(dfs, on_column):
        """Fusionne plusieurs DataFrames sur une colonne commune"""
        if not dfs:
            return pd.DataFrame()
        result = dfs[0]
        for df in dfs[1:]:
            result = pd.merge(result, df, on=on_column, how='outer')
        return result
