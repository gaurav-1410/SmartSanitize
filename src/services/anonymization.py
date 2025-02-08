import pandas as pd
import hashlib
import re

class Anonymization:
    def hash_value(self, value):
        """Hashes a string using SHA-256"""
        return hashlib.sha256(value.encode()).hexdigest()

    def anonymize_dataframe(self, df):
        """Anonymizes sensitive data such as emails and names"""
        for col in df.columns:
            if df[col].dtype == 'object':
                if df[col].str.contains('@').any():  # If it looks like an email
                    df[col] = df[col].apply(lambda x: self.hash_value(x) if isinstance(x, str) else x)
        return df
