import os
import sqlite3

from common import SQL_PATH


if not os.path.exists("storage"):
    os.makedirs("storage")

if not os.path.exists("logs"):
    os.makedirs("logs")

if not os.path.exists("schedule"):
    os.makedirs("schedule")

db_exists = os.path.exists(SQL_PATH)
conn = sqlite3.connect(SQL_PATH)

if not db_exists:
    cursor = conn.cursor()
    create_table_query = """
                    CREATE TABLE "t_rating" (
                        "id" INTEGER,
                        "name" TEXT NOT NULL,
                        "rating" DOUBLE NOT NULL,
                        "voters" TEXT NOT NULL,
                        PRIMARY KEY("id" AUTOINCREMENT)
                    );
                    """
    cursor.execute(create_table_query)
    conn.commit()
conn.close()
