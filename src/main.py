from src.config import config
from src.dbmanager import DBManager


def main():
    params = config()
    db = DBManager(**params)
    db.create_table()
    db.save_to_database()


if __name__ == "__main__":
    main()
