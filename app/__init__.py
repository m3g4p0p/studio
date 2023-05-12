try:
    import dotenv
    dotenv.load_dotenv()
except ImportError:
    pass

from .main import app  # noqa
