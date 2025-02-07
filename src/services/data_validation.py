import pandas as pd


class FileValidation:
    """
    Validates file format and integrity.
    """

    def validate_file_format(self, uploaded_file):
        """
        Validates and reads the uploaded file based on format.
        """
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith((".xls", ".xlsx")):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith(".json"):
                df = pd.read_json(uploaded_file)
            else:
                return None

            return df
        except Exception:
            return None
