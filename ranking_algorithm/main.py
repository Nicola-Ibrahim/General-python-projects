from pathlib import Path

from core import run

if __name__ == "__main__":
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent

    run(BASE_DIR)
