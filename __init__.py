'''
THIS SOFTWARE IS PROVIDED AS IT IS WITH NO WARRANTY 
IT IS TO BE USED AS IT IS OR EDITED PROVIDED ALL 
TERMS AND CONDITIONS ARE MET.

PLEASE ADHERE TO LISCENCES OF PyQt, icons8, Postgresql
and Python. Read them before editing the code.

Author: Koech Allan K.
Email : lalan2205@gmail.com

Libraries used :
    > PyQt5 (user interface)
    > psycopg2 (postgres database)
    > pendulum (date and time module)


'''

# ENTRY POINT


from msale.main import main
from msale.database import db

if __name__ == "__main__":
    try:
        db.CreateDb() # Create Database mysale if it doesnt exist
        main()        # Start the main UI application

    except Exception as e:
        print(e)