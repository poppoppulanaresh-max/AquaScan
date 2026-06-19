import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

# Project Root and Paths
ROOT_DIR = Path(__file__).resolve().parents[2]
MODELS_DIR = ROOT_DIR / "models"
WEIGHTS_DIR = MODELS_DIR / "weights"
DATA_DIR = ROOT_DIR / "data"

# Application Settings
APP_TITLE = os.getenv("APP_TITLE", "AquaScan")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEFAULT_LAT = float(os.getenv("DEFAULT_LAT", "16.3067"))
DEFAULT_LON = float(os.getenv("DEFAULT_LON", "80.4365"))
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"

# Database Configuration
SQLITE_DB_PATH = os.getenv("SQLITE_DB_PATH", str(DATA_DIR / "aquascan.db"))
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

# Model Parameters
MODEL_PATH = os.getenv("MODEL_PATH", str(WEIGHTS_DIR / "best.pt"))
MOCK_MODE_ENV = os.getenv("MOCK_MODE", "auto").lower()

# Theme UI Colors
RIVER_BLUE = "#00B4D8"
DEEP_OCEAN = "#023E8A"
SURFACE = "#03045E"
GLASS_CARD = "rgba(0,180,216,0.08)"
TEXT_PRIMARY = "#E0F7FA"
TEXT_SECONDARY = "#90CAF9"
BORDER = "rgba(0,180,216,0.25)"

# Severity Color Mappings
SEVERITY_COLORS = {
    'low': '#00C853',       # River Green
    'medium': '#FFC107',    # Warning Amber
    'high': '#FF5722',      # Danger Orange
    'critical': '#D50000'   # Critical Red
}

# Regional Target Rivers in Guntur / Andhra Pradesh
TARGET_RIVERS = ["Krishna River", "Godavari River", "Musi River", "Other / Unknown"]
