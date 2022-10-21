import sqlite3
import mysql.connector as mysql

# -------DB PARAMETERS------- #
# MySQL db
MY_HOST = '127.0.0.1'
MY_USER = 'userName'
MY_PASSWORD = 'userPassword'

# SQLite db
sqlite_path = 'db/agency.db'  # specify the path of SQLite db  you created for migration

# -------VARIABLES------- #
from_mysql_table = 'invoice'  # Name of MySQL table you want to take information from
to_sqlite_table = 'invoice'  # Name of SQLite table you want to migrate

columns = 'usr_id, cntry_id, price'  # Columns of your choice. Several columns must be separated by a comma
'''
I suggest you to specify all the columns, except the PK (PRIMARY KEY column), otherwise the algorithm will fail.
If you want specific columns to be migrated, specify the following parameter on line 120.
# row[start_column : finish_column] 
'''


def user_agreement():
    print(f'You are trying to transfer the data'
          f'\n--- from MySQL "{from_mysql_table}" table'
          f'\n--- to SQLite "{to_sqlite_table}" table')
    user_answer = input('\nBy default the SQLite table will be cleaned before migration starts.'
                        '\nDo you wish to continue? ( "YES" - to proceed, "NO" - to cancel )'
                        '\nYour answer: ')
    if user_answer.upper() == "YES":
        main()
    elif user_answer.upper() == "NO":
        print("\nThe migration was canceled by the user.")
    else:
        print("\nThe migration was canceled. ERR: Unrecognized input.")


def main():
    # SQLite example
    sqlite_db = None
    sqlite_cur = None

    # MySQL example
    mysql_db = None
    mysql_cur = None

    # -------(?,?,?) QUESTION MARKS AUTOMATION------- #
    # values = '?, ?, ?'  # number of ? must be the same as number of columns, separated by comma and space
    col_split = columns.split(',')
    # print(col_split)
    question_marks = []
    for item in col_split:
        question_marks.append('?')
    question_marks = str(', '.join(question_marks))
    # print(question_marks)
    values = question_marks

    # -------CONNECTIONS------- #
    try:
        # SQLite connection
        sqlite_db = sqlite3.connect(str(sqlite_path))
        # SQLite cursor
        sqlite_cur = sqlite_db.cursor()

        # SQLite version
        sqlite_cur.execute('SELECT sqlite_version()')
        version = sqlite_cur.fetchone()[0]
        print(f'\nSQLite db connection successful. SQLite version {version}')
    except:
        print('SQLite db connection failed. Uncomment "raise"')
        # raise

    try:
        # MySQL connection
        mysql_db = mysql.connect(host=MY_HOST,
                                 user=MY_USER,
                                 password=MY_PASSWORD,
                                 database='agency')
        # MySQL cursor
        mysql_cur = mysql_db.cursor(buffered=True)

        # MySQL version
        mysql_cur.execute('SELECT VERSION()')
        version = mysql_cur.fetchone()[0]
        print(f'MySQL db connection successful. MySQL version {version}')
    except:
        print('MySQL db connection failed. Uncomment "raise"')
        # raise

    # -------PRINTING MYSQL MIGRATION CONTENT------- #
    try:
        mysql_cur.execute(f'SELECT count(*) FROM {from_mysql_table};')
        num_rows = mysql_cur.fetchone()[0]
        print(f'\nMySQL. Number of rows in "{from_mysql_table}" table is {num_rows}')

        mysql_cur.execute(f'SELECT {columns} FROM {from_mysql_table}')
        for row in mysql_cur:
            print(row)
    except:
        print('mysql print failed')

    # -------SQLITE DATASET CLEANING------- #
    try:
        print('')
        sqlite_cur.execute('DELETE FROM ' + to_sqlite_table + ';')
        print('Cleaning process finished, SQLite "' + to_sqlite_table + '" table is clean now.')

    except:
        print('Failed to clean ' + to_sqlite_table + ' table. Uncomment "raise"')
        # raise

    # ------- MySQL to SQLite migration------- #
    try:
        mysql_cur.execute(f'SELECT * FROM {from_mysql_table};')
        query = "INSERT INTO " + to_sqlite_table + " (" + columns + ") VALUES (" + values + ");"

        for row in mysql_cur:
            sqlite_cur.execute(query, (row[1:]))  # row[start_column : finish_column]
        sqlite_db.commit()

        mysql_cur.execute(f'SELECT count(*) FROM {from_mysql_table};')
        num_rows = mysql_cur.fetchone()[0]
        print(f'{num_rows} row(s) successfully migrated '
              f'from MySQL "{from_mysql_table}" table '
              f'to SQLite "{to_sqlite_table}" table')
    except:
        print('Migration failed. Uncomment "raise"')
        raise

    # -------CLOSING CONNECTIONS------- #
    try:
        sqlite_cur.close()
        sqlite_db.close()
        print('\nSQLite db and cur closed.')
    except:
        print('Closing SQLite db connection failed. Uncomment "raise"')
        # raise

    try:
        mysql_cur.close()
        mysql_db.close()
        print('MySQL db and cur closed.')
    except:
        print('Closing SQLite db connection failed. Uncomment "raise"')
        # raise


if __name__ == '__main__':
    user_agreement()
