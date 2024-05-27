import os

def db_exists() -> bool:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    instance_directory = os.path.join(current_directory, '..', 'instance')
    instance_directory = os.path.abspath(instance_directory)
    database_file_path = os.path.join(instance_directory, 'database.sqlite3')
    
    if os.path.isfile(database_file_path):
        return True
    else:
        return False