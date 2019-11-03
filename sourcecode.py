import sqlite3
import getpass
import re
import datetime
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
    """
    while login_screen == False:
        login_screen = login()
    """
        
    #USER MENU
    print("To register a birth, type in 1")
    print("To register a marriage, type in 2")
    print("To renew a vehicle registration, type in 3")
    print("To process a bill of sale, type in 4")
    print("To process a payment, type in 5")
    print("To get a driver abstract,type in 6")
    print("To issue a ticket, type in 7")
    print("To find a car owner, type in 8")
    action = input("Choose a task: ")
    
    if int(action) == 1: one()
    elif int(action) == 2: two()
    elif int(action) == 3: three()
    elif int(action) == 4: four()
    elif int(action) == 5: five()
    elif int(action) == 6: six()
    elif int(action) == 7: seven()
    elif int(action) == 8: eight()
    
        

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
        #check to see if fname length < 12
        fname = input("Please provide a first name: ")
        if fname != '' and fname.isalpha() == True:
            break
        else:
            print("Incorrect format")
    
    while True:
        #check to see if fname length < 12
        lname = input("Please provide a last name: ")
        if lname != '' and lname.isalpha() == True:
            break 
        else:
            print("Incorrect format")
            
    while True:
        #if F/M not entered, maybe show line saying invalid entry?
        gender = input("Please provide the gender (M/F): ")
        if gender.upper() == 'F' or gender.upper() == 'M':
            break
      
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        try:
            year, month, day = bdate.split('-')
            datetime.datetime(int(year),int(month),int(day))
            break
        except ValueError:
            print("Invalid Date")
    
    
    
    while True:
        #check to see if bplace length < 20
        bplace = input("Please provide a birth place: ")
        if bplace != '' and bplace.isalpha():
            break      
        
    while True:
        #check to see if mother's fname length < 12
        mot_fname = input("Please provide mother's first name: ")
        if mot_fname != '' and mot_fname.isalpha():
            break  
        
    while True:
        #check to see if mother's lname length < 12
        mot_lname = input("Please provide mother's last name: ")
        if mot_lname != '' and mot_lname.isalpha():
            break     
      
    while True:
        #check to see if father's fname length < 12
        fat_fname = input("Please provide father's first name: ")
        if fat_fname != '' and fat_lname.isalpha():
            break     
        
    while True:
        #check to see if father's lname length < 12
        fat_lname = input("Please provide father's last name: ")
        if fat_lname != '' and fat_lname.isalpha():
            break  
    
    if find_parent(mot_fname, mot_lname) == None:
        missing_parent_info(mot_fname, mot_lname)
        
    elif find_parent(fat_fname, fat_lname) == None:
        missing_parent_info(fat_fname, fat_lname)
    
        
        
def find_parent(fname, lname):
    c.execute('SELECT fname, lname FROM persons WHERE fname =? and lname=?;', (fname, lname))
    return c.fetchone()

# we need first name, last name, birth date, birth place, address and phone. for each parent any column other than first and last can be null
def missing_parent_info(fname, lname):
    print("There seems to be no record of {} {} in our database".format(fname,lname))
    print("Please fill out the information down below. \nHit enter if you do not want to fill this out.")  
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        if bdate == '':
            bdate =  'NULL'
            break
        else:
            try:
                year, month, day = bdate.split('-')
                datetime.datetime(int(year),int(month),int(day))
                break
            except ValueError:
                print("Invalid Date")
    
    while True:
        bplace = input("Please provide a birth place: ")
        if bplace == '':
            bplace = 'NULL'
            break
        else:
        #check for length of bplace < 20?
            if bplace.isalpha():
                break      
            else:
                print("Invalid input")
                
    while True:
        address = input("Please provide an address: ")
        if address == '':
            address = 'NULL'
            break
        else:
            if address.isalpha() and len(address) < 30:
                break      
            else:
                print("Invalid input")        
                
    while True:
        phone_number = input("Please provide a phone number (123-456-7890): ")
        if phone_number == '':
            phone_number = 'NULL'
            break
        else:
        #check if length is less than or equal to 12
            if phone_number.isalpha() and len(phone_number) < 12:
                break      
            else:
                print("Invalid input")         
    parent_register = 'INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)'
    c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
                  VALUES
                  (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, address, phone_number))
    conn.commit()
       

    
    
def two():
    print("You have chosen to register a marriage")
    
    while True:
        prt1_fname = input("Please provide Partner 1's first name: ")
        if prt1_fname != '' and len(prt1_fname) <= 12 and prt1_fname.isalpha() == True:
            break
        else:
            print("Incorrect format")
    
    while True:
        prt1_lname = input("Please provide Partner 1's last name: ")
        if prt1_lname != '' and len(prt1_lname) <= 12 and prt1_lname.isalpha() == True:
            break 
        else:
            print("Incorrect format")
            
    if find_partner(prt1_fname, prt1_lname) == None:
        missing_partner_info(prt1_fname, prt1_lname)
            
    while True:
        prt2_fname = input("Please provide Partner 2's first name: ")
        if prt2_fname != '' and len(prt2_fname) <= 12 and prt2_fname.isalpha() == True:
            break
        else:
            print("Incorrect format")
    
    while True:
        prt2_lname = input("Please provide Partner 2's last name: ")
        if prt2_lname != '' and len(prt2_lname) <= 12 and prt2_lname.isalpha() == True:
            break 
        else:
            print("Incorrect format")
        
    #if find_partner(prt1_fname, prt1_lname) == None:
    #    missing_partner_info(prt1_fname, prt1_lname)
        
    if find_partner(prt2_fname, prt2_lname) == None:
        missing_partner_info(prt2_fname, prt2_lname)
        
        
def find_partner(fname, lname):
    c.execute('SELECT fname, lname FROM persons WHERE fname =? AND lname=?;', (fname, lname))
    return c.fetchone()
    

# we need first name, last name, birth date, birth place, address and phone. for each partner any column other than first and last can be null
def missing_partner_info(fname, lname):
    print("There seems to be no record of {} {} in our database".format(fname,lname))
    print("Please fill out the information down below. \nHit enter if you do not want to fill this out.")  
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        if bdate == '':
            bdate =  'NULL'
            break
        else:
            try:
                year, month, day = bdate.split('-')
                datetime.datetime(int(year),int(month),int(day))
                break
            except ValueError:
                print("Invalid Date")
    
    while True:
        bplace = input("Please provide a birth place: ")
        if bplace == '':
            bplace = 'NULL'
            break
        else:
            if bplace.isalpha() and len(bplace) <= 20:
                break      
            else:
                print("Invalid input")
                
    while True:
        address = input("Please provide an address: ")
        if address == '':
            address = 'NULL'
            break
        else:
            if address.isalpha() and len(address) <= 30:
                break      
            else:
                print("Invalid input")        
                
    while True:
        phone_number = input("Please provide a phone number (123-456-7890): ")
        if phone_number == '':
            phone_number = 'NULL'
            break
        else:
            #if validNumber(phone_number) == True:
            if len(phone_number) <= 12 and re.match("^[0-9]{3}-[0-9]{3}-[0-9]{4}$", phone_number):
                break      
            else:
                print("Invalid input")
               
                
    partner_register = 'INSERT INTO persons(fname, lname, bdate, bplace, address, phone) VALUES (?,?,?,?,?,?)'
    #c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
    #              VALUES
    #              (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, address, phone_number))
    c.execute(partner_register, (fname, lname, bdate, bplace, address, phone_number))
    conn.commit()


def three():
 # Provide existing registration number, and renew the registration.
    # If the current registration has expired or expires today set the new expiry date to one year from today's date
    # Otherwise, set the new expiry to one year after the current expiry date.

    entry_exists = False
    while not entry_exists:
        current_regno = input('Enter an existing registration number. To go back to menu press enter: ')
        current_regno = current_regno.strip()
        if current_regno == '':
            return
        c.execute('SELECT regdate FROM registrations WHERE regno = ?;', (current_regno,))
        db_regdate = c.fetchone()
        if db_regdate == None:
            print('This registration number is not registered in the database')
        else:
            db_regdate = db_regdate[0]
            db_regdate = datetime.datetime.strptime(db_regdate, "%Y-%m-%d")
            entry_exists = True


    if datetime.datetime.today() >= db_regdate:
        # Registration has expired or expires today, set new expiry date to one year from today
        print("Current registration has expired, system is setting new expiry date to one year from today")
        today = datetime.date.today()
        today_string = today.strftime("%Y-%m-%d")
        set_db_regyear = datetime.date.today().year + 1
        year, month, day = today_string.split('-')
        new_expiry = str(set_db_regyear) + '-' + month + '-' + day
        c.execute("UPDATE registrations SET regdate = ? WHERE regno = ?;", (new_expiry, current_regno))
        # TESTING
        # c.execute("SELECT regdate FROM registrations WHERE regno = ?;", (current_regno,))
        # print(c.fetchone()[0])
    
    else:
        print("Setting the new expiry date to a year from current expiry date")
        c.execute("SELECT expiry FROM registrations WHERE regno = ?;", (current_regno,))
        old_expiry_str = c.fetchone()[0]
        exp_year, exp_month, exp_day = old_expiry_str.split('-')
        exp_year = int(exp_year) + 1
        new_exp = str(exp_year) + '-' + exp_month + '-' + exp_day
        c.execute("UPDATE registrations SET regdate = ? WHERE regno = ?;", (new_exp, current_regno))
        #TESTING
        # c.execute("SELECT regdate FROM registrations WHERE regno = ?;", (current_regno,))
        # print(c.fetchone()[0])

def four():
    ## git check for nan
    pass
def five():
    pass
def six():
    # Enter a first name and a last name to get a driver abstract
    # Driver abstract contains number of tickets, number of demerit notices, total number of demerit points received both within the past 2 years and within the lifetime. 
    # Given the option to see the tickets ordered from the latest to the oldest. 
    # For each ticket, you will report the ticket number, the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. 
    # If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
    f_name = input("Enter first name: ").lower()
    l_name = input("Enter last name: ")
    c.execute('''SELECT count(t.tno)
                FROM tickets t, registrations r
                WHERE t.regno = r.regno
                AND r.fname = ? AND r.lname = ?;''', (f_name, l_name))
    print(c.fetchone()[0])


    
    
def seven():
    pass
def eight():
    pass

if __name__ == "__main__":
    main()