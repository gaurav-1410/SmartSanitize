import os

# Define base project directory
base_dir = r"D:\Smart_Sanitize"

# Define the folder structure
folders = [
    "src",
    "src/config",
    "src/domain",
    "src/services",
    "src/infrastructure",
    "src/presentation",
    "src/tests",
    "docs",
    "notebooks",
    "scripts"
]

# Define files to create
files = {
    "README.md": "# SmartSanitize\n\nA data cleaning and preprocessing tool.",
    "LICENSE": "MIT License",
    ".gitignore": "__pycache__/\n.env\n*.log\n",
    "requirements.txt": "streamlit\npandas\nnumpy\nscikit-learn\nmatplotlib\nseaborn\npytest\nreportlab\n",
    "src/__init__.py": "",
    "src/main.py": "if __name__ == '__main__':\n    print('SmartSanitize App Running...')",
    "src/config/settings.py": "import os\n\n# Configuration settings go here",
    "src/config/logger.py": "import logging\n\nlogging.basicConfig(level=logging.INFO)",
    "src/domain/__init__.py": "",
    "src/domain/data_file.py": "# Defines data file structure",
    "src/domain/validation_rules.py": "# Validation rules",
    "src/services/__init__.py": "",
    "src/services/data_validation.py": "# File integrity checks",
    "src/services/quality_analysis.py": "# Missing values, duplicates, etc.",
    "src/services/preprocessing.py": "# Scaling, feature selection, augmentation",
    "src/services/anonymization.py": "# Masking sensitive data",
    "src/infrastructure/__init__.py": "",
    "src/infrastructure/file_loader.py": "# Handles file uploads",
    "src/infrastructure/report_export.py": "# Export as PDF, JSON",
    "src/presentation/__init__.py": "",
    "src/presentation/ui.py": "# Streamlit UI layout",
    "src/presentation/charts.py": "# Visualization components",
    "src/tests/__init__.py": "",
    "src/tests/test_validation.py": "# Test file validation",
    "src/tests/test_quality_analysis.py": "# Test data quality analysis",
    "src/tests/test_preprocessing.py": "# Test preprocessing",
    "src/tests/test_anonymization.py": "# Test anonymization",
}

# Create folders
for folder in folders:
    os.makedirs(os.path.join(base_dir, folder), exist_ok=True)

# Create files with initial content
for file, content in files.items():
    file_path = os.path.join(base_dir, file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ SmartSanitize project structure created successfully!")
