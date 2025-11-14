from src.db_utils import initialize_db
if __name__ == '__main__':
    initialize_db('sql/schema.sql')
    print('DB initialized.')
