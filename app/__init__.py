from pathlib import Path

try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

base_path = Path(__file__).parent
