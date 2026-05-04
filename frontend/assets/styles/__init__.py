import os

def load_stylesheet(filename: str) -> str:
    """Load QSS stylesheet from file"""
    style_dir = os.path.dirname(__file__)
    filepath = os.path.join(style_dir, filename)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Stylesheet not found: {filepath}")
        return ""

# Load main stylesheet
MAIN_STYLE = load_stylesheet("main.qss")