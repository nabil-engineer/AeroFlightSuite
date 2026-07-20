from config.config import PROJECT_TITLE
from database.database_manager import create_database
from core.menu import run_menu

if __name__ == "__main__":
    print(PROJECT_TITLE)
    create_database()
    run_menu()
