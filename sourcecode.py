import sqlite3
import getpass
import re

def main():
    global conn, c 
    # path = sysargv[1] 
    # conn = sqlite3.connect(path)
    conn = sqlite3.connect('./database_test.db')
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON; ')
    conn.commit()
    login_screen = False

    # LOGIN SCREEN
    while login_screen == False:
        login_screen = login()
    
        

def login():
    print("Login Here!")
    username = input("Enter username: ")
    password = getpass.getpass("Enter Password: ")
    
    # re.match is checking if our username and password contains alphabet, numbers and underscores ONLY
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute('SELECT uid FROM users WHERE uid=? and pwd=?;', (username, password))
        if c.fetchone() != None:
            print("Login Success.")
            return True
        else:
            print("Login failed. Try again")
            return False
    else:
        print("Login failed. Try again")
        return False
    
def one():
    pass
def two():
    pass
def three():
    pass
def four():
    pass
def five():
    pass
def six():
    pass
def seven():
    pass
def eight():
    pass

if __name__ == "__main__":
    main()