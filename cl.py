import random
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("your mongo db key")
db = client['bank']
collection1 = db['currentaccount']
collection2 = db['savingaccount']
collection3 = db['cards']
collection4 = db['creditcards']
collection5 = db['termdeposits']
collection6 = db['mpin']

def generate_account_number():
    return random.randint(1000000000, 9999999999)

class Account:
    def __init__(self, name, cnic, contact, balance, dob, account_number):
        self.name = name
        self.cnic = cnic
        self.contact = contact
        self.balance = balance
        self.dob = dob
        self.account_number = account_number

    def new_customer(self):
        print("Enter your full name:")
        self.name = input()
        print("Enter your CNIC:")
        self.cnic = input()
        print("Enter your contact number:")
        self.contact = input()
        print("Enter your date of birth (DD-MM-YYYY):")
        self.dob = input()
        print("Enter the amount you wish to deposit initially:")

        while True:
            try:
                self.balance = float(input())
                if self.balance < 500:
                    print("Minimum deposit for new customers is 500 rupees. Please enter again:")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        self.account_number = generate_account_number()
        print(f"Customer created: {self.name}, {self.contact}, {self.balance}, {self.dob}, {self.account_number}")

        # Save the customer to the database
        self.save_to_db()
        self.generate_debitcard()
        self.generate_user_credentials()


    def save_to_db(self):
        customer_data = {
            "name": self.name,
            "cnic": self.cnic,
            "contact": self.contact,
            "balance": self.balance,
            "dob": self.dob,
            "account_number": self.account_number
        }
        # Insert into the appropriate collection based on account type
        if isinstance(self, SavingAccount):
            collection2.insert_one(customer_data)
        elif isinstance(self, CurrentAccount):
            collection1.insert_one(customer_data)
        print("Customer data saved to the database.")

    def show_balance(self):
        print("Your available balance is $", self.balance)

    def show_accnumber(self):
        print("Your account number is", self.account_number)

    def deposit(self, amount):
        self.balance += amount
        print("Your new balance is $", self.balance)

    def generate_debitcard(self):
            choice = 0
            while choice not in [1, 2]:
                choice = int(input("Which type of card do you desire?\n1) VISA\n2) MASTERCARD\n"))

                if choice == 1:
                    cnum = "4123"
                    type="visa"
                elif choice == 2:
                    cnum = "5412"
                    type="master"
                else:
                    print("Invalid choice. Please select a valid card.")
                    return

                rnd = [str(random.randint(0, 9)) for _ in range(11)]
                dcnum = cnum + ''.join(rnd)
                print("Your Debit card number is:", dcnum)
                self.save_debitcard_to_db(dcnum,type)

    def save_debitcard_to_db(self, dcnum,type):
            card_data = {
                "account_number": self.account_number,
                "card_number": dcnum,
                "type": type
            }
            collection3.insert_one(card_data)
            print("Debit card data saved to the database.")
    def generate_user_credentials(self):
        print(f"Welcome {self.name} Please enter a username of Your choice along with a 4 digit pin number\n.")
        print("Enter your username\n")
        username = input().lower()
        print("Enter your pin\n")
        password = int(input())
        print("reenter your pin\n")
        pass2=int(input())
        if pass2==password:
            print("Pin matched successfully")
        else:
             while pass2!=password:
                print("pin dosent match please try again")
                print("Enter your pin\n")
                password = int(input())
                print("reenter your pin\n")
                pass2 = int(input())

        ea=self.dob[0:2]
        username=username+ea
        print(f"your username is: {username}")
        save_mpin_to_db(self,username,password)


def save_mpin_to_db(self, username, password):


    mpin = {
        "account_number": self.account_number,
        "username": username,
        "password": password
    }


    collection6.insert_one(mpin)

class CurrentAccount(Account):
    def __init__(self, name, cnic, contact, balance, dob, account_number):
        super().__init__(name, cnic, contact, balance, dob, account_number)

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
            return
        self.balance -= amount
        print("Your new balance is $", self.balance)

    def generate_creditcard(self):
        lchoice = 0
        while lchoice not in [1, 2, 3, 4]:
            lchoice = int(input("Which type of card do you desire?\n1) Classic\n2) Gold\n3) Platinum\n4) Titanium\n"))

            if lchoice == 1 and self.balance >= 50000:
                limit = 50000
            elif lchoice == 2 and self.balance >= 100000:
                limit = 100000
            elif lchoice == 3 and self.balance >= 250000:
                limit = 250000
            elif lchoice == 4 and self.balance >= 500000:
                limit = 500000
            else:
                print("You are not eligible for the selected credit card.")
                return

        c = 0
        while c not in [1, 2, 3]:
            c = int(input("Which type of card do you desire?\n1) AMEX\n2) VISA\n3) MASTERCARD\n"))

            if c == 1:
                cnum = "3456"
            elif c == 2:
                cnum = "4123"
            elif c == 3:
                cnum = "5412"
            else:
                print("Invalid choice. Please select a valid option.")
                return

            rnd = [str(random.randint(0, 9)) for _ in range(11)]
            ccnum = cnum + ''.join(rnd)
            print("Your credit card number is:", ccnum)
            self.save_creditcard_to_db(ccnum)

    def save_creditcard_to_db(self, ccnum):
        card_data = {
            "account_number": self.account_number,
            "card_number": ccnum,
            "type": "Credit Card"
        }
        collection4.insert_one(card_data)
        print("Credit card data saved to the database.")

class SavingAccount(CurrentAccount):
    def __init__(self, name, cnic, contact, balance, dob, account_number):
        super().__init__(name, cnic, contact, balance, dob, account_number)

    def term_deposit(self):
        print("Enter the amount you want to deposit:")
        d = int(input())
        ch = 0
        while ch not in [1, 2, 3]:
            print("Enter the amount of time you want to invest:\n1) 3 months at 5%\n2) 6 months at 15%\n3) 12 months at 30%")
            ch = int(input())
            if ch == 1:
                interest = 5
            elif ch == 2:
                interest = 15
            elif ch == 3:
                interest = 30
            else:
                print("Invalid choice. Please select a valid option.")
                return
        mr = d / 100 * interest / 12
        print(f"Your deposit amount is {d} at {interest}%")
        print(f"Your Monthly profit is set at ${mr}")
        self.save_term_deposit_to_db(d, interest)

    def save_term_deposit_to_db(self, amount, interest):
        deposit_data = {
            "account_number": self.account_number,
            "amount": amount,
            "interest_rate": interest
        }
        collection5.insert_one(deposit_data)
        print("Term deposit data saved to the database.")

def check_credentials(self, username, password):
        user_data = collection6.find_one({"username": username})
        user_data = collection6.find_one({"password": password})
        numot = 0
        while numot < 4:
            if user_data != None:
                numot = numot + 1
                print(f"invalid credientials please try again{numot - 4}tries left")
                print("Enter your username:")
                us = input()
                print("Enter your password:")
                pwd = input()
                if user_data != None:
                    numot = numot + 1
                    print(f"invalid credientials please try again{numot - 4}tries left")
                    print("Enter your username:")
                    us = input()
                    print("Enter your password:")
                    pwd = input()
                if user_data != None:
                    numot = numot + 1
                    print(f"invalid credientials please try again{numot - 4}tries left")
                    print("Enter your username:")
                    us = input()
                    print("Enter your password:")
                    pwd = input()
        else:
            numot = 4
        pass

def main():
    running = True
    current_account = None  # To store the logged-in account object

    while running:
        print("Welcome to Bank App")
        print("Select an option: \n1) Login \n2) Signup \n3) Exit")
        c1 = int(input())

        while c1 not in [1, 2, 3]:
            print("Enter a valid option (1, 2, or 3)")
            c1 = int(input())

        if c1 == 1:  # Login
            print("Enter your username:")
            us = input().lower()
            print("Enter your password:")
            pwd = int(input())

            # Check credentials
            if Account.check_credentials(us, pwd):
                print(f"Welcome back, {us}!")

                # Retrieve the logged-in user's account
                user_data = collection6.find_one({"username": us})
                account_number = user_data['account_number']

                # Load the account based on account number
                account_data = collection1.find_one({"account_number": account_number}) or collection2.find_one(
                    {"account_number": account_number})

                if account_data:
                    # Create an instance of the correct account type (Current or Saving)
                    if 'balance' in account_data:  # This assumes 'balance' field is always present
                        if collection2.find_one(
                                {"account_number": account_number}):  # Check if the account is a Saving account
                            current_account = SavingAccount(
                                account_data['name'],
                                account_data['cnic'],
                                account_data['contact'],
                                account_data['balance'],
                                account_data['dob'],
                                account_data['account_number']
                            )
                        else:
                            current_account = CurrentAccount(
                                account_data['name'],
                                account_data['cnic'],
                                account_data['contact'],
                                account_data['balance'],
                                account_data['dob'],
                                account_data['account_number']
                            )
                    else:
                        print("Error: Account data not found.")
                        running = False
                        break
                else:
                    print("Error: Account not found.")
                    running = False
                    break

                # Now the user is logged in, offer them account options
                while True:
                    print("\nWhat would you like to do?")
                    print("1) Deposit")
                    print("2) Withdraw")
                    print("3) Apply for a credit card")
                    print("4) Book a term deposit")
                    print("5) Show balance")
                    print("6) Show account number")
                    print("7) Log out")

                    choice = int(input())
                    if choice == 1:
                        print("Enter the amount you want to deposit:")
                        amount = float(input())
                        current_account.deposit(amount)
                    elif choice == 2:
                        print("Enter the amount you want to withdraw:")
                        amount = float(input())
                        current_account.withdraw(amount)
                    elif choice == 3:
                        current_account.generate_creditcard()
                    elif choice == 4:
                        print("this feature is only available for saving account holders\n")
                    elif choice == 5:
                        current_account.show_balance()
                    elif choice == 6:
                        current_account.show_accnumber()
                    elif choice == 7:
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Please try again.")

            else:
                print("Invalid credentials. Please try again.")

        elif c1 == 2:  # Signup
            account_type = input("Select account type (1 for Current, 2 for Saving): ")
            if account_type == "1":
                new_account = CurrentAccount("", "", "", 0, "", generate_account_number())
                new_account.new_customer()
            elif account_type == "2":
                new_account = SavingAccount("", "", "", 0, "", generate_account_number())
                new_account.new_customer()
            else:
                print("Invalid account type selected.")

        elif c1 == 3:  # Exit
            print("Exiting the bank application.")
            running = False


if __name__ == "__main__":
    main()
