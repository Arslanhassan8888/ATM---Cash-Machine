# This program simulates a simple Cash Machine
# Each user has a unique 4-digit PIN and a text file to store their data
"""Firstly, the program will ask to the user to  insert the PIN, then the program will match the provided PIN with PIN'S saved
in the memory of the program. Once the authentication is completed, the program will refer to the right document of text to retrieve 
last transactions and last updated balance. As final step, the program will be append all the new transactions, without deleting the olds,
so it will maintain the full history, but will updated only the balance"""

"""cash_machine is the main fuction which contain all the main program. The first part contain a main deictionary called "users" which has as keys 3 differnts pins numbers
which the user has to match to get acces to the account..as values of this dictionary there are 3 nested dcitionary, where the last key has as value the appropriate
text file called "record_transaction" """

def cash_machine():

    users = {
        "8014": {"username": "arslan", "balance": 5000, "file": "record_transaction1.txt"},
        "1234": {"username": "ali", "balance": 7000, "file": "record_transaction2.txt"},
        "5678": {"username": "sara", "balance": 9000, "file": "record_transaction3.txt"},
    }

    """Simply, this function allow to identify if the user are using the correct PIN to access the account"""
    def authentication():# I don't expect any entry for this function. When the function will called, it will run its body
        max_attempts = 4 # I set attemption allowed as 4
        for x in range(1, max_attempts + 1):#For loop for every attempt starting from 1 to 5, because teh last number is not included 
            pin = input("Please enter your 4-digit PIN: ")
            if pin in users: #If the PIN match with pin in the memory of the dictionary
                print(f"\nWelcome {users[pin]['username']}! Authentication successful.")
                return pin #Allow to the user and program to proceed. Phis pin will also allow to get access to the right text file to read balance and trasanctions
                            #After this pin, if verified will be saved below in the variable user_pin
            else:
                remaining_attempts = max_attempts - x #Counting of remaining attempt
                if remaining_attempts > 0:
                    print(f"Incorrect PIN. You have {remaining_attempts} attempt's' left.")
                else:
                    print("No more attempts available. Your account is locked.")
                    break #Break the loop
        return None #Function will stop and also the program

    user_pin = authentication()#Calling the function, if the pin is correct, it will be saved in the variable user_pin
    if not user_pin: #If the pin is incorrect return to none
        return
    


    """This function read all the data from the appropriate file """
    def get_user_data(pin):
        if pin in users: #Fist step, check if the pin exist in the dictionary as key
            filename = users[pin]["file"] # Retrieve the information from the right file and  store in the variable "filename"
            try:                           #Try, except allow to avoid the program to crash or get in error
                file = open(filename, "r")# open the  file in read mode
                lines = file.readlines() #Read all the lines in the file and save it in the variable "linez"
                file.close()  #Remember to close the file 

                if lines: # If lines exist, mean if line actually has any content
                    users[pin]["balance"] = float(lines[0].strip()) #Python read the code from the right to left. Get the content of the fisrt line, which is balance value
                    #but store as string in text file, with strip i remove blank space,new lines(\n) and the convert in float number to be usuable for the program calculation
                    #save this value in the nested dictionary balance
            except FileNotFoundError:  #This will allow the program to not crash in the case no file find. Consequently, it will create a new file
                print(f"No previous data for {users[pin]['username']}. A new record will be created.")
            except ValueError: #If in the first file the program will find unexpected value or corrupted data, will not crash or stop
                print(f"Error reading balance for {users[pin]['username']}. Resetting balance to default.")
                users[pin]["balance"] = 0.0  #This function will allow me to reset the balance to zero in the case of unexpected value


    get_user_data(user_pin)#Call the function to read the previous balance and transactions from the file.


    """At this pint, start the main program after authentication, reloaded the previous data. An infinite while loop to allow to user to perform as many actions he want
    until, he/she will select the option number 5"""
    while True:
        print( 
            "Please choose an option:\n"
            "1. Check Balance\n"
            "2. Deposit Money\n"
            "3. Withdraw Money\n"
            "4. View Transaction History\n"
            "5. Exit"
        )
        selection = input("Choose an option from above: ")

        if selection == "1":
            print(f"Your balance is: £{users[user_pin]['balance']:.2f}")#The exactly value of balance stored in the nested dictionary at key balance
                                                                        #now the key of the main dictionary has name user_pin

        elif selection == "2":
            try:
                deposit_amount = float(input("Please enter the amount to deposit: "))#User will insert value as string. Float will converted it in number with decimal places
                if deposit_amount <= 0: #Deposit cannot be negative value
                    print("Please enter a positive amount for your deposit.") #Warning message for user
                else:
                    users[user_pin]["balance"] += deposit_amount  #If value is positive, update the balance value in the dictionary
                    save_user_data(user_pin, f"Deposit: £{deposit_amount:.2f}") #Update the file with new balance value and new transaction 
                    print(f"\n£{deposit_amount:.2f} has been deposited successfully!")
                    print(f"Your new balance is: £{users[user_pin]['balance']:.2f}")
            except ValueError: #allow me to avoid the program crash in the case of user will insert wrong value, like letters insetad of numbers
                print("Invalid input entry! Please enter a valid number.")

        elif selection == "3":
            try:
                withdraw = float(input("Please enter the amount to withdraw: "))#Convert in float number
                if withdraw <= 0: #Witdraw amount must be positive
                    print("Withdrawal amount cannot be negative!")
                elif withdraw > users[user_pin]["balance"]:  #It must be greater than the balance available
                    print("\nSorry, you have insufficient balance for this transaction!")
                else:
                    users[user_pin]["balance"] -= withdraw # Balance updated
                    save_user_data(user_pin, f"Withdrawal: £{withdraw:.2f}") #Update the file with the new balance and transaction
                    print(f"\n£{withdraw:.2f} has been withdrawn successfully!")
                    print(f"Remaining balance: £{users[user_pin]['balance']:.2f}")
            except ValueError:
                print("Invalid entry! Please enter a valid number.")

        elif selection == "4":
            try:
                file = open(users[user_pin]["file"], "r")#Open in read mode the last updated file
                lines = file.readlines()[1:]  # Read every single line in teh file, but start from line 1, skipping lines 0, where is balance
                file.close()

                if not lines:# if lines list is empty
                    print("No transactions found.")
                else:
                    print("\nTransaction History:")
                    x = 1 #Start counting, with general index
                    for y in lines:
                        print(f"{x}. {y.strip()}")#  Print the counter and the stripped line. Strip eliminate whitespace or newlines
                        x += 1  # Increment the counter after each iteration
            except FileNotFoundError:
                print("No transaction history found.")

        elif selection == "5":
            save_user_data(user_pin)# before exi, make sure to save everything again
            print("Thank you for using the Cash Machine. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

    """The main purpose of this function save data about new balance and transactions in the righ file text"""

    def save_user_data(pin, transaction=None):# the function is expecting 2 values, but the second one can be also absent or optional because the NONE
                                            # if transaction =none mean will be not values to save in the text file
        if pin in users: #re checking the pin if exist the dictionary to save data in the right file
            filename = users[pin]["file"]# Before to save o wright new things in the file, make sure you are taking data from the right file to update
            try:
                file = open(filename, "r") #So again I am opening and reading the file.
                lines = file.readlines() # The purpose to read the content again before save new content is keep the old trasaction history
                file.close()
            except FileNotFoundError:  
                lines = [] #If file doesn't exist it will create a new file with an empty list

            file = open(filename, "w") # open file in write mode ---purpose is ovewrite the content of the balance
            file.write(f"{users[pin]['balance']:.2f}\n") # write the balance value, exactly same value that you can find the nested dictionary rounded to decimal places
            #plus start new lines after(\n)

            # Keep old transactions and append the new one if provided
            if len(lines) > 1: #let's check the lenght of lines. lines contain  the textfile, for lenght mean how many lines of string  are in text file
                                #if lenght == 0 empty file, if ==1 only balance if >1 some deposit o witdraws
                file.writelines(lines[1:]) # writelines allow to write multistring. [1:] write starting to the index 1 back in the variable "file",
                # which contain text file, because at index 0 there is balance value
                #writes the existing transactions to the file. This ensures that the history of transactions is preserved and appended to the updated balance.

            if transaction:#Append New Transaction (if any) t this point file is tsill open, we a;reade wrote the updated balance value, and set to write multi-string after balance
                                #if there are transaction, (which can be also absent).. if no transactions, this part will be skipped
                file.write(transaction + "\n") #The + "\n" ensures that the transaction is written on a separate new line, 
            file.close() #i will new transsaction after balance, and old transactions


# Run the program and main function
cash_machine()
