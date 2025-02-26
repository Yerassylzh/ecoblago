from catalog.models import *

def run():
    from django.db import connection

    def get_database_encoding():
        vendor = connection.vendor  # Returns 'postgresql', 'mysql', 'sqlite', etc.
        
        if vendor == 'postgresql':
            with connection.cursor() as cursor:
                cursor.execute("SHOW SERVER_ENCODING;")
                return cursor.fetchone()[0]
                
        elif vendor == 'mysql':
            with connection.cursor() as cursor:
                cursor.execute("SHOW VARIABLES LIKE 'character_set_database';")
                return cursor.fetchone()[1]
                
        elif vendor == 'sqlite':
            # SQLite always uses UTF-8 encoding
            return 'UTF-8'
            
        else:
            return f"Unsupported database: {vendor}"

    # Usage
    print("Database encoding:", get_database_encoding())
