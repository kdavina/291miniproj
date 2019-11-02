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
        
    #USER MENU
    print("To register a birth, type in 1")
    action = input("Choose a task: ")
    
    if int(action) == 1:
        one()
        

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
    print("You have chosen to register a birth")
    
    while True:
        fname = input("Please provide a first name: ")
        if fname != '':
            break
    
    while True:
        lname = input("Please provide a last name: ")
        if lname != '':
            break  
            
    while True:
        gender = input("Please provide the gender: ")
        if gender.upper() == 'F' or gender.upper() == 'M':
            break
        
    bdate = input("Please provide a birth date: ")
    
    while True:
        bplace = input("Please provide a birth place: ")
        if bplace != '':
            break      
        
    mot_fname = input("Please provide mother's first name: ")
    mot_lname = input("Please provide mother's last name: ")
    fat_fname = input("Please provide father's first name: ")
    fat_fname = input("Please provide father's last name: ")
    
    
    
def two():
    ## git check
    pass
def three():
## git check
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