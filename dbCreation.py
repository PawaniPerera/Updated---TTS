import mysql.connector
from django.db.models import query
from mysql.connector import Error


def db_connection1(hostname, username, password, databaseRP2):
    connection = None
    try:
        connection = mysql.connector.Connect(
            host=hostname,
            user=username,
            passwd=password,
            database=databaseRP2

        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = db_connection1("localhost", "root", "Sandu@96", "databaseRP2")


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print("The error '{e}' occurred")


create_database_query = "CREATE DATABASE databaseRP2"
create_database(connection, create_database_query)


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


create_details_table = """
CREATE TABLE IF NOT EXISTS segiriya (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  description TEXT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

execute_query(connection, create_details_table)


"""def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")"""

"""create_segiriya = """
"""INSERT INTO
  `segiriya` (`name`,`description`)
VALUES
  ('සීගිරිය සෑදූ රජතුමා කවුද?','කාශ්‍යප රජු'),
  ('සීගිරිය කීවෙනි ලෝක පුදුමයද?','අටවන ලෝක පුදුමය'),
  ('සීගිරියේ දක්නට ලැබෙන දේවල්?','බිතුසිතුවම්'),
  ('සීගිරිය සෑදූ කාලය කුමක්ද?','ක්‍රි.පූ 3 වන සියවස'),
  ('සීගිරිය පිහිටා ඇති නගරය කුමක්ද?','දඹුල්ල නගරය'),
  ('සීගිරිය පිහිටා ඇති දිස්ත්‍රික්කය කුමක්ද?','මාතලේ දිස්ත්‍රික්කය'), 
  ('සීගිරි බිතුසිතුවම් යනු මොනවාද?','බිත්තියක් හෝ සිවිලිමක් මත තෙත් 
    ප්ලාස්ටර් මත ජල වර්ණක වේගයෙන් කරන ලද සිතුවමක් වන අතර එමඟින් වර්ණ ප්ලාස්ටර් තුලට විනිවිද ගොස් වියළන විට ස්ථාවර වේ.'), 
  ('සීගිරියේ උස කීයද?','මීටර 349'); 

"""

"""execute_query(connection, create_segiriya)"""


"""select_users = "SELECT * from segiriya"
users = execute_read_query(connection, select_users)

for user in users:
    print(user)"""
