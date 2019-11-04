import sqlite3
import getpass
import re
import datetime
import random
import sys

# Final version

def main():
    global conn, c 
    path = sys.argv[1] 
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('PRAGMA foreign_keys=ON; ')
    conn.commit()
    login_screen = False
    
   
    # LOGIN SCREEN
    while login_screen == False:
        login_screen, username = login()
        if username == '':
            break
        if login_screen:
            # figuring out if user is an officer or agent and assigning it to a variable
            c.execute('SELECT utype FROM users WHERE uid LIKE ?;', (username,)) 
            utype = c.fetchone()[0]
            
            # depending on utype, run the menu until we get a valid action
            while True:
                # if the user is an agent, their action range is only from 1 - 6
                # if we get an empty input that means they want to exit out of the program
                if utype == 'a':
                    action = agent_menu()
                                
                # if the user is an officer, their action range is from 1 - 8
                elif utype == 'o':
                    action = officer_menu()
                        
                
                # run the action 
                if action == '': 
                    login_screen = False
                    break                
                elif action == 1: one(username)
                elif action == 2: two(username)
                elif action == 3: three()
                elif action == 4: four()
                elif action == 5: five()
                elif action == 6: six()
                elif action == 7: seven()
                elif action == 8: eight()    
                     
# we will return if login was successful or not and the username given to us
def login():
    # grab the information from the user
    print("Login Here!")
    print("Hit enter for both username and password to exit out of program")
    username = input("Enter username: ")
    password = getpass.getpass("Enter Password: ")
    
    if username == '' and password == '':
        return True, username
    # re.match is checking if our username and password contains alphabet, numbers and underscores ONLY
    # if that passes, we want to see if the username and password that we receive is in the database
    # if we fetch it and it is does NOT give us none, that means we found an uid and password that matches
    # if the username/password is wrong we return false
    if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
        c.execute('SELECT uid FROM users WHERE uid LIKE ? and pwd=?;', (username, password))
        if c.fetchone() != None:
            print("Login Success.")
            print('\n')
            return True, username
        else:
            print("Login failed. Try again")
            print('\n')
            return False, username
    else:
        print("Login failed. Try again")
        print('\n')
        return False, username

# the agent menu consists of seven options including the option to exit out of the program
def agent_menu():
    # these are just variables in order to create a table
    action_space = 30
    number_space = 15
    
    while True:
        print("Status: Agent")
        border = '------------------------------------------------'
        print(border)
        
        print("|%s|%s|" % ("Register a birth".center(action_space), '1'.center(number_space)))
        print(border)
        print("|%s|%s|" % ("Register a marriage".center(action_space), "2".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Renew a vehicle registration".center(action_space), "3".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Process a bill of sale".center(action_space), "4".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Process a payment".center(action_space), "5".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Get a driver abstract".center(action_space), "6".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Logout".center(action_space), "Press Enter".center(number_space)))
        print(border)
        action = input("Choose a task: ")
        
        # if the action we receive from the user is empty, we exit out of the program
        # otherwise we check if we can convert it to an integer then see if it is in the range
        # we end the loop when we get a valid action otherwise we keep prompting the menu
        if action == '':
            print('Exiting program\n')
            return action
        else:
            try:
                action = int(action)
                if action < 1 or action > 6:
                    print('Invalid action')
                else:
                    return action
            except ValueError:
                print('Invalid action')    
                
# the officer menu has 9 options including exiting the program
def officer_menu():
    # variables in order to create our table
    action_space = 30
    number_space = 15
    
    while True:
        print("Status: Officer")
        border = '------------------------------------------------'
        print(border)
        print("|%s|%s|" % ("Register a birth".center(action_space), '1'.center(number_space)))
        print(border)
        print("|%s|%s|" % ("Register a marriage".center(action_space), "2".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Renew a vehicle registration".center(action_space), "3".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Process a bill of sale".center(action_space), "4".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Process a payment".center(action_space), "5".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Get a driver abstract".center(action_space), "6".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Issue a ticket".center(action_space), "7".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Find a car owner".center(action_space), "8".center(number_space)))
        print(border)
        print("|%s|%s|" % ("Logout".center(action_space), "Press Enter".center(number_space)))
        print(border)    
        action = input("Choose a task: ")
        
        # validation similar to agent except our range increases up to 8
        if action == '':
            print('Exiting program')
            return action
        else:
            try:
                action = int(action)
                if action < 1 or action > 8:
                    print('Invalid action')
                else:
                    return action
            except ValueError:
                print('Invalid action')
 
# Register a birth:
# 1. Check if the name already exists in the persons table
# 2. If the mom and dad do not exist in the database, get some values in order to register them
# 3. Insert into the persons table first and then into the births table in order to uphold foreign key constraints
def one(user):
    print("You have chosen to register a birth")
    print('Note that first and last names are a maximum of 12 characters')
    print("To go back to the menu, press enter")
    # Receive information about birth information
    # Most of the validation is checking the length restricted to whatever it is in the database
    # or checking that a name only consists of letters, numbers and dashes and is not empty
    while True:
        fname = input("Please provide a first name: ")
        if fname == '':
            return
        elif len (fname) <= 12 and re.match("^[A-Za-z0-9-]*$", fname):
            break
        else:
            print("Incorrect format")
    
    while True:
        lname = input("Please provide a last name: ")
        if lname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", lname) and len(lname) <= 12 :
            break 
        else:
            print("Incorrect format")
    
    # check to see if this name already exists in the database
    # if they exist, deny the birth registration
    if find_person(fname, lname) != None:
        print('There is already a {} {} that exists in the database'.format(fname,lname))
        print('Birth registration rejected.\n')
        return;
    
    # check gender, simple m or f
    while True:
        gender = input("Please provide the gender (M/F): ")
        if gender == '':
            return
        elif gender.upper() == 'F' or gender.upper() == 'M':
            break
        else:
            print('Incorrect format')
    
    # Using datetime module to validate date
    # datetime does not account for months (1-9) having a 0 at the front ex. 01 - January
    # if our input passes the datetime function and the length is one, then concatenate a 0 at the front
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        if bdate == '':
            return
        try:
            year, month, day = bdate.split('-')
            datetime.datetime(int(year),int(month),int(day))
            if len(month) == 1:
                month = "0" + month
            if len(day) == 1:
                day = "0" + day           
            bdate = year +'-' + month +'-'+ day
            break
        except ValueError:
            print("Invalid Date")
    
    # validate and receive the birth place
    while True:
        bplace = input("Please provide a birth place (max character length is 20): ")
        if bplace == '':
            return
        elif bplace.isalpha() and len(bplace) <= 20:
            break    
        else:
            print('Incorrect format')
            
    # validate and receive mother's name
    while True:
        mot_fname = input("Please provide mother's first name: ")
        if mot_fname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", mot_fname) and len(mot_fname) <= 12:
            break
        else:
            print("Incorrect format")
        
    while True:
        mot_lname = input("Please provide mother's last name: ")
        if mot_lname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", mot_lname) and len(mot_lname) <= 12:
            break
        else:
            print("Incorrect format")
    
    # checking to see if mom already exists in the database
    mom_name = find_person(mot_fname, mot_lname)       
    if mom_name == None:
        mom_name = missing_person_info(mot_fname, mot_lname)    
    
    # validate and receive father's name
    while True:
        fat_fname = input("Please provide father's first name: ")
        if fat_fname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", fat_fname) and len(fat_fname) <= 12:
            break 
        else:
            print("Incorrect format")
        
    while True:
        fat_lname = input("Please provide father's last name: ")
        if fat_lname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", fat_lname) and len(fat_lname) <= 12:
            break
        else:
            print("Incorrect format")
    
    # this is checking if the dad is in the database
    dad_name = find_person(fat_fname, fat_lname)
    if dad_name == None:
        dad_name = missing_person_info(fat_fname, fat_lname)
     
     
    # REGISTERING AS A PERSON
    # We need to grab address and phone number from mom
    # note that address and phone number is in an indexed list called result
    c.execute('SELECT address, phone FROM persons where fname LIKE ? and lname LIKE ?;', (mom_name[0], mom_name[1]))
    result = c.fetchone()
    c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
                  VALUES
                  (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, result[0], result[1]))
    conn.commit()
    
    # REGISTERING BIRTH
    # use datetime function for registration date and use a query to find the regplace
    regdate = datetime.date.today()
    c.execute('SELECT city FROM users where uid = ?;', (user,))
    regplace = c.fetchone()[0]
    
    # creating unique registration number
    # we find the current highest registration number and add 1 
    c.execute('SELECT regno FROM births ORDER BY regno DESC')
    reg_num = c.fetchone()[0] + 1    
    
    c.execute(''' INSERT INTO births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)
                  VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                (reg_num, fname, lname, regdate, regplace, gender, dad_name[0], dad_name[1], mom_name[0], mom_name[1]))
    conn.commit()
    
    print("Birth registration successful\n")
    
# this function checks if this person exists in the database already
# note that it will either return None or the first and last name which (if saved into a variable) can be treated as a list
def find_person(fname, lname):
    c.execute('SELECT fname, lname FROM persons WHERE fname LIKE ? and lname LIKE ?;', (fname, lname))
    return c.fetchone()

# we need first name, last name, birth date, birth place, address and phone. for each parent any column other than first and last can be null
# we know the user has hit enter if our input is an empty string, if it is set the variable to NULL
def missing_person_info(fname, lname):
    print('\n')
    print("There seems to be no record of {} {} in our database".format(fname,lname))
    print("Please fill out the information down below. \nHit enter if you do not want to fill this out.\n")  
    while True:
        bdate = input("Please provide a birth date (YYYY-MM-DD): ")
        if bdate == '':
            bdate =  'NULL'
            break
        else:
            try:
                year, month, day = bdate.split('-')
                datetime.datetime(int(year),int(month),int(day))
                if len(month) == 1:
                    month = "0" + month  
                if len(day) == 1:
                    day = "0" + day                      
                bdate = year +'-' + month +'-'+ day                    
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
            if re.match("^[ A-Za-z0-9-]*$", fat_lname) and len(address) <= 30:
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
                      
                
    # at the very end we want to insert this into our database
    c.execute(''' INSERT INTO persons(fname, lname, bdate, bplace, address, phone)
                  VALUES
                  (?,?,?,?,?,?)''', (fname, lname, bdate, bplace, address, phone_number))
    conn.commit()
    
    print('\n')
    return fname, lname


# Register a marriage:
# 1. Check if both of the partners' names already exists in the persons table
# 2. If they don't exist in database get information to register them in the persons table first(optional)
# 3. Insert into the persons table first and then into the marriages table in order to uphold foreign key constraints    
def two(username):
    print("You have chosen to register a marriage")
    print("To go back to the menu, press enter")
    
    # Prompt user to input first name of Partner 1
    while True:
        prt1_fname = input("Please provide Partner 1's first name: ")
        if prt1_fname == '':
            return
        elif len(prt1_fname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt1_fname):
            break
        else:
            print("Incorrect format")
    
    # Prompt user to input first name of Partner 1
    while True:
        prt1_lname = input("Please provide Partner 1's last name: ")
        if prt1_lname == '':
            return
        elif len(prt1_lname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt1_lname):
            break 
        else:
            print("Incorrect format")
            
    # check to see if partner_one exists in the database and if they don't, go to missing_person_info function to register them in persons table      
    partner_one = find_person(prt1_fname, prt1_lname)
    if partner_one == None:
        partner_one = missing_person_info(prt1_fname, prt1_lname)
    
    # Prompt user to input first name of Partner 2         
    while True:
        prt2_fname = input("Please provide Partner 2's first name: ")
        if prt2_fname == '':
            return
        elif len(prt2_fname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt2_fname):
            break
        else:
            print("Incorrect format")
    
    # Prompt user to input first name of Partner 2
    while True:
        prt2_lname = input("Please provide Partner 2's last name: ")
        if prt2_lname == '':
            return
        elif len(prt2_lname) <= 12 and re.match("^[A-Za-z0-9-]*$", prt2_lname):
            break 
        else:
            print("Incorrect format")
            
    # check to see if partner_one exists in the database and if they don't, go to missing_person_info function to register them in persons table
    partner_two = find_person(prt2_fname, prt2_lname)    
    if partner_two == None:
        partner_two = missing_person_info(prt2_fname, prt2_lname)
        
        
    # use datetime function to get and set registration date to today and use a query to find the registration place from users table
    registdate = datetime.date.today()
    c.execute('SELECT city FROM users where uid = ?;', (username,))
    registplace = c.fetchone()[0]
    
    # find the highest regno and add one in order to create a new regno (always unique)
    c.execute('SELECT regno FROM marriages ORDER BY regno DESC')
    regno = c.fetchone()[0] + 1
    
    # add marraige information into the marriages table in the database
    c.execute(''' INSERT INTO marriages(regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)
                  VALUES (?,?,?,?,?,?,?)''', 
                (regno, registdate, registplace, partner_one[0], partner_one[1], partner_two[0], partner_two[1]))
    conn.commit()

    print("Marriage registration successful.\n")
    
def three():
    # Provide existing registration number, and renew the registration.
    # If the current registration has expired or expires today set the new expiry date to one year from today's date
    # Otherwise, set the new expiry to one year after the current expiry date.
    print("You have chosen to renew a vehicle registration.")
    print("To go back to the menu, press enter.")
    entry_exists = False
    while not entry_exists:
        current_regno = input('Enter an existing registration number: ')
        current_regno = current_regno.strip()
        if current_regno == '':
            return
        c.execute('SELECT expiry FROM registrations WHERE regno = ?;', (current_regno,))
        db_expiry = c.fetchone()
        if db_expiry == None:
            print('This registration number is not registered in the database')
        else:
            db_expiry = db_expiry[0]
            db_expiry = datetime.datetime.strptime(db_expiry, "%Y-%m-%d")
            entry_exists = True


    if datetime.datetime.today() >= db_expiry:
        # Registration has expired or expires today, set new expiry date to one year from today
        print("Current registration has expired, system is setting new expiry date to one year from today")
        today = datetime.date.today()
        today_string = today.strftime("%Y-%m-%d")
        set_db_regyear = datetime.date.today().year + 1
        year, month, day = today_string.split('-')
        new_expiry = str(set_db_regyear) + '-' + month + '-' + day
        c.execute("UPDATE registrations SET expiry = ? WHERE regno = ?;", (new_expiry, current_regno))
    
    else:
        print("Setting the new expiry date to a year from current expiry date")
        c.execute("SELECT expiry FROM registrations WHERE regno = ?;", (current_regno,))
        old_expiry_str = c.fetchone()[0]
        exp_year, exp_month, exp_day = old_expiry_str.split('-')
        exp_year = int(exp_year) + 1
        new_exp = str(exp_year) + '-' + exp_month + '-' + exp_day
        c.execute("UPDATE registrations SET expiry = ? WHERE regno = ?;", (new_exp, current_regno))
        
    conn.commit()

def four():
    print('You have chosen to process a bill of sale')
    print("To go back to the menu, press enter.")
    
    # grab and validate information
    # grabbing vin
    while True:
        vin = input('What is the vehicle identification number (vin)? ')
        if vin == '':
            return
        elif vin != '' and len(vin) <= 5:
            break
        else:
            print('Invalid input')
            
    # grabbing current owner
    while True:
        current_fname = input('What is the first name of the current owner? ')
        if current_fname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", current_fname) and len(current_fname) <= 12:
            break
        else:
            print('Invalid input')

    
    while True:
        current_lname = input('What is the last name of the current owner? ')
        if current_lname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", current_lname) and len(current_lname) <= 12:
            break
        else:
            print('Invalid input') 
            
    # check to see if current owner is in the database
    if find_person(current_fname, current_lname) == None:
        print('There is no {} {} in the database'.format(current_fname, current_lname))
        print('New sale rejected.\n')
        return;      
    
    # getting new owner
    while True:
        new_fname = input('What is the first name of the new owner? ')
        if new_fname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", new_fname) and len(new_fname) <= 12:
            break
        else:
            print('Invalid input')
            
    while True:
        new_lname = input('What is the last name of the new owner? ')
        if new_lname == '':
            return
        elif re.match("^[A-Za-z0-9-]*$", new_lname) and len(new_lname) <= 12:
            break
        else:
            print('Invalid input')  
            
    # check to see if the new person is in the database      
    new_person = find_person(new_fname, new_lname)
    if new_person == None:
        print('There is no {} {} in the database'.format(new_fname, new_lname))
        print('New sale rejected.\n')
        return;    
            
    while True:
        plate = input('What is the plate number? ')
        if plate == '':
            return
        elif len(plate) <= 7:
            break
        else:
            print('Invalid input')
            

            
    # checking to see if there is such a registration with the vin and plate
    # if there is no registration that exists, reject the sale
    # we are also grabbing the name of the most recent registration of that vin and plate number
    c.execute('SELECT fname, lname, regno, vin FROM registrations WHERE vin LIKE ? and plate LIKE ? ORDER BY regdate DESC;', (vin, plate))
    result = c.fetchone()
    if result == None:
        print('There is no current registration under that vin, plate, and name')
        print('New sale rejected.\n')
        return
    # check to see if the latest person is the current person
    if result[0].lower() != current_fname.lower() and result[1].lower() != current_lname.lower():
        print("That is not the most recent owner of this vehicle.")
        print("New sale rejected.\n")
        return
    
    # assign vin
    # change expiry date of old owner's car to today's date
    vin = result[3]
    regno = result[2]
    today = datetime.date.today()
    c.execute('UPDATE registrations SET expiry = ? WHERE regno = ?;', (today, regno))
    
    # a new registration: new owners name, registration date = today, expiry = a year from now, unique reg number, vin will be copied from current reg to the new on 
    today_string = today.strftime("%Y-%m-%d")
    set_db_regyear = datetime.date.today().year + 1
    year, month, day = today_string.split('-')
    new_expiry = str(set_db_regyear) + '-' + month + '-' + day    
    
    # creating a unique regno
    c.execute('SELECT regno FROM registrations ORDER BY regno DESC')
    regno = c.fetchone()[0] + 1
    
    # inserting new registration
    c.execute('INSERT INTO registrations(regno, regdate, expiry, plate, vin, fname, lname) VALUES (?,?,?,?,?,?,?);', (regno, today, new_expiry, plate, vin, new_person[0], new_person[1]))
    conn.commit()
    print("Bill of Sale successful.\n")


# Making a payment on a ticket
# 1. Ask user to input ticket number, validate and if it doesn't exist break out of function and into main menu
# 2. If ticket exists in tickets table, get fine amount from tickets table and ask user to select payment amount, then validate amount
# 3. Record payment amount in payments table and tickets table, then exit function
def five():
    print("You have chosen to process a payment")
    print("To go back to the menu, press enter")
    
    # Prompt user for ticket number they'd like to make a payment to and validate the inputted value
    while True:
        ticket_no = input("Please provide the ticket number you'd like to make a payment to: ")
        if ticket_no == '':
            return
        elif ticket_no.isdigit() == True:
            break
        else:
            print("Invalid ticket number")
    
    # If ticket does not exist in database, print "Invalid entry" and break out of the function and into main menu
    # If ticket exists, iterate through the find_fine function and return to main menu if find_fine function returns False
    if find_ticket(ticket_no) != None:
        if find_fine(ticket_no) == False:
            return
    else:
        print("This ticket number does not exist in the database.")
        

# Check to see if ticket exists in the tickets table in the database       
def find_ticket(tno):
    c.execute('SELECT tno FROM tickets WHERE tno =?;', (tno,))
    return c.fetchone()


def find_fine(tno):
    # Get the fine amount from the tickets table in the database   
    c.execute('SELECT fine FROM tickets WHERE tno =?;', (tno,))
    fine_leftover = int(c.fetchone()[0])
    
    print("\nThe fine amount outstanding for this ticket number is ${}".format(fine_leftover))
    
    # Use datetime function to assign today's date to pay_date
    pay_date = datetime.date.today()
    # Check to see if tno exists in payments table already then get pdate from payments table
    c.execute('SELECT pdate FROM tickets t, payments p WHERE t.tno = p.tno AND t.tno = ?;', (tno,))
    old_paydate = c.fetchall()
    
    # while statement to check if old_paydate in payments table is same as today's date
    while True:   
        if len(old_paydate) == 0:
            break
        else:
            for i in old_paydate:
                if (str(i) == str(pay_date)):
                    break
            else:
                # if old_paydate is same as today's date, print below statement and break out of function five into main menu
                print("\nYou have already made a payment on ticket {} today".format(tno))
                print("Please try payment on this ticket again another day")
                return False

    # Prompt user to input amount they'd like to pay towards fine
    while True:
        pay_amount = input("Please provide the amount you would like to pay: ")
        # validate the pay_amount entered
        if pay_amount != '' and pay_amount.isdigit() == True:
            pay_amount = int(pay_amount)
            payment_balance = int(fine_leftover - pay_amount)
            # if payment_balance is 0, then user has completed payment of ticket, iterate to fine_paidinfull function and then exit function five
            if payment_balance == 0:
                fine_paidinfull(tno, pay_date, pay_amount)
                return False
            # check to see if pay_amount is less than fine amount
            elif payment_balance < 0:
                print("Invalid amount")
            else:
                print("\nYou are making a payment of ${} to ticket number {}".format(pay_amount, tno))
                print("Your new balance of the ticket fine is ${}".format(payment_balance))
            break
        else:
            print("Invalid amount")
 
    # register the users payment information in the payments table
    payment_register = 'INSERT INTO payments(tno, pdate, amount) VALUES (?,?,?)'
    c.execute(payment_register, (tno, pay_date, pay_amount))
    conn.commit()
    
    # update the tickets table with the new payment_balance amount
    update_tickets = 'UPDATE tickets SET fine=? WHERE tno=?;'
    c.execute(update_tickets, (payment_balance, tno))
    conn.commit()
    
    return
    conn.commit()

# if the payment_balance is 0 after user makes payment, update the tickets table and payments table in the database
# then print following statement    
def fine_paidinfull(tno, pay_date, pay_amount):
    # update the payments table with the transaction
    payment_register = 'INSERT INTO payments(tno, pdate, amount) VALUES (?,?,?)'
    c.execute(payment_register, (tno, pay_date, pay_amount))
    conn.commit()
    
    # update the tickets table with the new payment_balance amount
    update_tickets = 'UPDATE tickets SET fine=? WHERE tno=?;'
    c.execute(update_tickets, (payment_balance, tno))
    conn.commit()
    
    print("\nYou have completed the payment of your fine!")
    
    
    
def six():
    # Enter a first name and a last name to get a driver abstract
    # Driver abstract contains number of tickets, number of demerit notices, total number of demerit points received both within the past 2 years and within the lifetime. 
    # Given the option to see the tickets ordered from the latest to the oldest. 
    # For each ticket, you will report the ticket number, the violation date, the violation description, the fine, the registration number and the make and model of the car for which the ticket is issued. 
    # If there are more than 5 tickets, at most 5 tickets will be shown at a time, and the user can select to see more.
    
    # Validate user exists in database
    entry_exists = False
    print("You have chosen to get a driver abstract")
    while not entry_exists:
        f_name = input("Enter first name. Press enter to return to menu. ").strip()
        if f_name == '':
            return
        l_name = input("Enter last name. Press enter to return to menu. ").strip()
        if l_name == '':
            return

        person = find_person(f_name, l_name)
        if person != None:
            entry_exists = True
            f_name = person[0]
            l_name = person[1]
        
    print('-' * 50)
    print("Driver abstract:")
    print('-' * 50)

    # Get number of tickets
    c.execute('''SELECT count(t.tno)
                FROM tickets t, registrations r
                WHERE t.regno = r.regno
                AND r.fname LIKE ? AND r.lname LIKE ?;''', (f_name, l_name))
    num_tickets = c.fetchone()[0]
    print("Number of tickets:", num_tickets)
    

    # Get number of demerit notices
    c.execute('''SELECT count(ddate)
                FROM demeritNotices
                WHERE fname LIKE ? AND lname LIKE ?;''', (f_name, l_name))
    print("Number of demerit notices:", c.fetchone()[0])

    # Get number of demerit points within the last 2 years
    two_years_ago = datetime.date.today()
    two_years_ago = two_years_ago.replace(year = two_years_ago.year - 2)

    c.execute('''SELECT sum(points)
                FROM demeritNotices
                WHERE ddate > ? 
                AND fname LIKE ? AND lname LIKE ?;''', (two_years_ago, f_name, l_name))
    print("Number of demerit points within the last 2 years:", c.fetchone()[0])

    # Get number of demerit points within the lifetime
    # ASSUMES THAT ENTRY IN DEMERITNOTICES CANNOT EXISTER FOR A PERSON BEFORE THEY WERE BORN
    c.execute('''SELECT sum(points)
                FROM demeritNotices
                WHERE fname LIKE ? AND lname LIKE ?;''', (f_name, l_name))
    print("Total number of demerit points:", c.fetchone()[0])

    see_tickets = input('Would you like to see the user\'s tickets? y to continue: ')
    if see_tickets == 'y':
        # Print 5 tickets at a time latest to oldest. 
        # For each ticket, get ticket number, violation date, violation description, fine, reg no., make of car, and model of car
        c.execute('''SELECT t.tno, t.vdate, t.violation, t.fine, t.regno, v.make, v.model
                    FROM tickets t, registrations r, vehicles v
                    WHERE t.regno = r.regno 
                    AND r.vin = v.vin
                    AND r.fname = ? AND r.lname = ?
                    ORDER BY vdate DESC; ''', (f_name, l_name))
        all_tickets = c.fetchall()
        ticket_counter = 0
        next_five_bool = True
        while ticket_counter < num_tickets and next_five_bool:
            for i in range(5):
                print('-' * 50)
                print('Ticket number:', all_tickets[ticket_counter][0])
                print('Violdation date:', all_tickets[ticket_counter][1])
                print('Violation description:', all_tickets[ticket_counter][2])
                print('Fine:', all_tickets[ticket_counter][3])
                print('Registration Number:', all_tickets[ticket_counter][4])
                print('Car make:', all_tickets[ticket_counter][5])
                print('Car model:', all_tickets[ticket_counter][6])
                ticket_counter += 1
                if ticket_counter == num_tickets:
                    break
            if ticket_counter < num_tickets:
                next_five_bool = input('Would you like to see the remaining tickets? y to continue: ')
                if next_five_bool != 'y':
                    next_five_bool = False
    
    print("All tickets printed. Returning to main menu")
    print()

    conn.commit()


# ISSUE A TICKET
# given a regnum
# print out persons fname and lname, make model year and color registered to the car
# can add a ticket (INSERT into tickets) by giving violation date, violation text and fine amount
# unique ticket number is assigned automatically and ticket should be recorded
# violation date is set to today's date if not provided
def seven():
    print("You have chosen to issue a ticket:")
    print("Press enter to return to main menu")
    
    # receive a registration number from the officer 
    # first we check that it is not empty and that the input is all digits
    # convert our variable into an int type then check to see if there is a registration number in the database
    while True:
        regno = input("Please provide a valid registration number: ")
        if regno == '':
            return
        
        elif regno.isdigit():
            regno = int(regno)
            c.execute('SELECT regno FROM registrations WHERE regno = ?;', (regno,))
            regno = c.fetchone()
            if regno == None:
                print('That registration number does not exist in the database')
                return
            else:
                regno = regno[0]
                break
        else:
            print("Invalid input format")
            
    c.execute('SELECT r.fname, r.lname, v.make, v.model, v.year, v.color FROM registrations r, vehicles v WHERE r.vin = v.vin and r.regno = ?', (regno,))
    result = c.fetchone()
    print('Persons Name: {} {}\nMake: {}\nModel: {}\nYear: {}\nColor: {}\n'.format(result[0],result[1],result[2], result[3],result[4],result[5]))
    
    # Grabbing information for the ticket 
    print("Please fill out the following information down below.\n")
    while True:
        vdate = input("Please provide a violation date (YYYY-MM-DD). Hit enter if not applicable (will not exit action): ")
        if vdate == '':
            vdate =  datetime.date.today()
            break
        else:
            try:
                year, month, day = vdate.split('-')
                datetime.datetime(int(year),int(month),int(day))
                if len(month) == 1:
                    month = "0" + month   
                if len(day) == 1:
                    day = "0" + day                      
                vdate = year +'-' + month +'-'+ day                    
                break
            except ValueError:
                print("Invalid Date")
                
    while True:
        violation = input('Please provide the violation description: ')
        if violation != '':
            break
        else:
            return
    
    while True:
        fine = input('Please provide a fine amount (minimum: $1): ')
        if fine == '':
            return
        try:
            fine = int(fine)
            if fine > 1:
                break
            else:
                print('Invalid input')
        except:
            print("Invalid input")
            
    # creating a tno
    # find the current highest ticket number and increase it by 1
    c.execute('SELECT tno FROM tickets ORDER BY tno DESC')
    tno = c.fetchone()[0] + 1
    
    c.execute('INSERT INTO tickets(tno,regno,fine,violation,vdate) VALUES (?, ?, ?, ?, ?)', (tno, regno, fine, violation, vdate))
    conn.commit()
    print("Issue a ticket successful\n")
    
          
def eight():
    print("You have chosen to find a car owner")
    # Finds a car owner given the one or more of the make, model, year, color, and plate of the car
    make = input('Enter a make. Leave blank if you do not wish to search by make. Type exit to return to menu. ').strip()
    if make == 'exit':
        return
    elif make == '':
        make = '%'
    model = input('Enter a model. Leave blank if you do not wish to search by make. Type exit to return to menu. ').strip()
    if model == 'exit':
        return
    elif model == '':
        model = '%'
    year = input('Enter a year. Leave blank if you do not wish to search by make. Type exit to return to menu. ').strip()
    if year == 'exit':
        return
    elif year == '':
        year = '%'
    color = input('Enter a color. Leave blank if you do not wish to search by make. Type exit to return to menu. ').strip()
    if color == 'exit':
        return
    elif color == '':
        color = '%'
    plate = input('Enter a plate. Leave blank if you do not wish to search by make. Type exit to return to menu. ').strip()
    if plate == 'exit':
        return
    elif plate == '':
        plate = '%'
    if make == '%' and model == '%' and year == '%' and color == '%' and plate == '%':
        print('You have not entered any values. Returning to main menu')
        return
    
    c.execute('''SELECT fname||' '||lname, MAX(r.regdate), r.vin, v.make, v.model, v.year, v.color, r.plate, r.expiry
                FROM registrations r, vehicles v
                WHERE r.vin = v.vin
                AND v.make LIKE ? AND v.model LIKE ? AND v.year LIKE ? AND v.color LIKE ? AND r.plate LIKE ?
                GROUP BY r.vin;''', (make, model, year, color, plate))
    results = c.fetchall()
 

    if len(results) >= 4:
        user_number = 1
        for user in results:
            print('-' * 50)
            print("Entry:", user_number)
            function_eight_results(user)
            user_number += 1
        valid_input = False
        while not valid_input:
            print()
            selected_user = int(input("Select a user number: "))
            if selected_user <= user_number:
                valid_input = True
        print()
        print_extra_results(results[selected_user-1])

    else:
        for user in results:
            print_extra_results(user)
        
def function_eight_results(user):
    print("Make:", user[3])
    print("Model:", user[4])
    print("Year:", user[5])
    print("Color:", user[6])
    print("Plate:", user[7])

def print_extra_results(user):
    print('-' * 50)
    print("Selected User:", user[0])
    function_eight_results(user)
    print("Latest registration date:", user[1])
    print("Expiry date:", user[8])


if __name__ == "__main__":
    main()