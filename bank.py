import datetime

class User:
    def __init__(self, name, email, address, password) -> None:
        self.name = name
        self.email = email
        self.address = address
        self.password = password


class Transaction_History:
    def __init__(self, transaction_type, amount, to_user, from_user) -> None:
        self.transaction_type = transaction_type
        self.amount = amount
        self.to_user = to_user
        self.from_user = from_user


class Account:

    def deposit(self, account_number, amount, bank):
        if account_number in bank.users:
            bank.users[account_number].balance += amount
            bank.total_balance += amount
            transaction = Transaction_History("Deposit", amount, bank, bank.users[account_number])
            bank.users[account_number].transactions.append(transaction)
            print(f'**Amount {amount} added in the account**')
        else:
            print(f'Account {account_number} dose not exist!!')
    
    def withdraw(self, account_number, amount, bank):
        if account_number in bank.users:
            if bank.users[account_number].balance >= amount:
                if amount > bank.total_balance:
                    print('Bank is Bankrupt!!')
                else:
                    bank.users[account_number].balance -= amount
                    transaction = Transaction_History('Withdraw', amount, bank.users[account_number], bank)
                    bank.users[account_number].transactions.append(transaction)
                    print(f'Amount : {amount} is has been withdrawn from your account')
            else:
                print('Withdrawal amount exceeded!!')
        else:
            print(f'Account {account_number} dose not exist!!')
    
    def user_available_balance(self, account_number, bank):
        if account_number in bank.users:
            print(f'{bank.users[account_number].name} has balance {bank.users[account_number].balance}')
        else:
            print(f'Account {account_number} dose not exist!!')
    
    def user_transaction_history(self, account_number, bank):
        if account_number in bank.users:
            print(f'Type\tAmount\tFrom\tTo')
            for trans in bank.users[account_number].transactions:
                print(f'{trans.transaction_type}\t{trans.amount}\t{trans.from_user.name}\t{trans.to_user.name}')
        else:
            print(f'Account {account_number} dose not exist!!')

    def user_loan(self, account_number, bank, amount):
        if bank.loan_system == True:
            if account_number in bank.users:
                if bank.users[account_number].loan_count < 2:
                    if bank.total_balance >= amount:
                        bank.total_balance -= amount
                        bank.total_loan += amount
                        bank.users[account_number].balance += amount
                        bank.users[account_number].loan_count += 1
                        transaction = Transaction_History("Loan", amount, bank.users[account_number], bank)
                        bank.users[account_number].transactions.append(transaction)
                        print(f'***Loan Granted Successfully***')
                    else:
                        print(f'Bank dose not have enough money!!')
                else:
                    print(f'Loan Limit Exceeded!!')
            else:
                print(f'Account {account_number} dose not exist!!')
        else:
            print('Loan system is currently off!!')
    
    def user_transfer_money(self, from_account_number, to_account_number, amount, bank):
        if from_account_number in bank.users:
            if to_account_number in bank.users:
                if amount <= bank.users[from_account_number].balance:
                    bank.users[from_account_number].balance -= amount
                    bank.users[to_account_number].balance += amount
                    transaction = Transaction_History("Transfer", amount, bank.users[to_account_number], bank.users[from_account_number])
                    transaction2 = Transaction_History("Deposit", amount, bank.users[to_account_number], bank.users[from_account_number])
                    bank.users[from_account_number].transactions.append(transaction)
                    bank.users[to_account_number].transactions.append(transaction2)
                    print(f'**Amount {amount} Transferred Successfully**')
                else:
                    print(f'Does not have enough money in the account!!')
            else:
                print(f'Account {to_account_number} does not exist!!')
        else:
            print(f'Account {from_account_number} does not exist!!')
    
    
class AccountManagement:

    def add_admin(self, admin, bank):
        if admin.name in bank.admins:
            print(f'Admin {admin.name} already exist!!')
            return False
        else:
            bank.admins[admin.name] = admin
            print(f'***New account has been created***')
            print(f'Name : {admin.name}\tEmail : {admin.email}')
            return True

    def add_bank_user(self, bank_user, bank):
        if bank_user.account_number in bank.users:
            print(f'User {bank_user.name} already exist!!')
            return False
        else:
            bank.users[bank_user.account_number] = bank_user
            print(f'***New account has been created***')
            print(f'Name : {bank_user.name}\tAccount Number : {bank_user.account_number}')
            return True

    def delete_user_account(self, account_number, bank):
        if account_number in bank.users:
            bank.users.pop(account_number)
            print(f'**User : {account_number} has been removed**')
        else:
            print(f'User : {account_number} dose not exist!!')

    def user_log_in(self, account_number, password, bank,):
        if account_number in bank.users:
            if bank.users[account_number].password == password:
                print(f'**Log in successful**')
                return bank.users[account_number]
            else:
                print('Invalid Password!!')
                return None
        else:
            print('Account dose not exist!!')
            return None
    
    def admin_log_in(self, admin_name, password, bank,):
        if admin_name in bank.admins:
            if bank.admins[admin_name].password == password:
                print(f'**Log in successful**')
                return bank.admins[admin_name]
            else:
                print('Invalid Password!!')
                return None
        else:
            print('Account dose not exist!!')
            return None


class Bank(AccountManagement):
    def __init__(self, name, serial) -> None:
        self.name = name
        self.serial = serial
        self.users = {} # account_number : BankUser
        self.admins = {} # admin_name : Admin
        self.total_balance = 0
        self.total_loan = 0
        self.loan_system = True


class BankUser(User,Account):
    def __init__(self, name, email, address, account_type, password) -> None:
        super().__init__(name, email, address, password)
        self.account_type = account_type
        self.balance = 0
        time = datetime.datetime.now()
        self.account_number = str(time.timestamp())
        self.transactions = []
        self.loan = 0
        self.loan_count = 0

class Admin(User):
    def __init__(self, name, email, address, password) -> None:
        super().__init__(name, email, address, password)

    def delete_user(self, account_number, bank):
        bank.delete_user_account(account_number, bank)
    
    def view_user_list(self, bank):
        print(f'Name\tAccount Number\tEmail\tAddress\tAccount Type')
        for user in bank.users.values():
            print(f'{user.name}\t{user.account_number}\t{user.email}\t{user.address}\t{user.account_type}')

    def view_bank_balance(self, bank):
        print(f'Total Available Balance : {bank.total_balance}')

    def view_total_loan(self, bank):
        print(f'Total Loan Amount : {bank.total_loan}')

    def loan_system(self, bank, flag):
        if flag.lower() == 'f':
            bank.loan_system = False
            print('**Loan System Has Been Turned Off**')
        elif flag.lower() == 't':
            bank.loan_system = True
            print('**Loan System Has Been Turned On**')
        else:
            print('Invalid Input')

def bank_user_interface(bank, user):
    print(f'**Welcome to user interface**')
    while True:
        print('1. Deposit')
        print('2. Withdraw')
        print('3. Check Available Balance')
        print('4. Check Transaction History')
        print('5. Loan')
        print('6. Transfer Money')
        print('7. Exit')
        choice3 = int(input('Enter Your Choice: '))

        if choice3 == 1:
            amount = int(input('Enter Amount : '))
            user.deposit(user.account_number, amount, bank)

        elif choice3 == 2:
            amount = int(input('Enter Amount : '))
            user.withdraw(user.account_number, amount, bank)
                        
        elif choice3 == 3:
            user.user_available_balance(user.account_number, bank)

        elif choice3 == 4:
            user.user_transaction_history(user.account_number, bank)
                        
        elif choice3 == 5:
            amount = int(input('Enter Amount : '))
            user.user_loan(user.account_number, bank, amount)
                        
        elif choice3 == 6:
            account_number = str(input('Enter Receiver Account Number : '))
            amount = int(input('Enter Amount : '))
            user.user_transfer_money(user.account_number, account_number, amount, bank)
                        
        elif choice3 == 7:
            print('**Thank You**')
            break

        else:
            print('Invalid Choice!!')


def admin_user_interface(bank, admin):
    print(f"**Welcome to {bank.name}**")
    while True:
        print('1. Delete Account')
        print('2. View All User Acount : ')
        print('3. Check Total Available Balance')
        print('4. Check Total Loan')
        print('5. Turn off/on the Loan')
        print('6. Exit')
        choice3 = int(input('Enter Your Choice: '))
        if choice3 == 1:
            account_number = input('Enter Account Number :')
            admin.delete_user(account_number, bank)
                        
        elif choice3 == 2:
            admin.view_user_list(bank)

        elif choice3 == 3:
            admin.view_bank_balance(bank)
                        
        elif choice3 == 4:
            admin.view_total_loan(bank)
        elif choice3 == 5:
            print('Enter "T" to turn on the loan system')
            print('Enter "F" to turn off the loan system')
            flag = input("Enter Your Choice : ")
            admin.loan_system(bank, flag)
        elif choice3 == 6:
            print("**Thank You**")
            break
        else:
            print("Invalid Input!!")

bank = Bank('ABC Bank', 7777)

print(f'***Welcome to {bank.name}***')

while True:
    print('1. User')
    print('2. Admin')
    print('3. Exit')
    _choice = int(input('Enter Your Choice: '))
    if _choice == 1:
        print(f'**Welcome to {bank.name}**')
        while True:
            print('1. Log in')
            print('2. Sign up')
            print('3. Exit')
            choice2 = int(input('Enter Your Choice: '))
            if choice2 == 1:
                account_number = input("Enter Your Account Number : ")
                password = input('Enter Your Password : ')
                user = bank.user_log_in(account_number,password,bank)

                if user is not None:
                    bank_user_interface(bank, user)

            elif choice2 == 2:
                name = input("Enter Your Name : ")
                email = input("Enter Your Email : ")
                address = input("Enter Your Address : ")
                account_type = input("Enter Account Type : ")
                password = input("Enter Password : ")
                user = BankUser(name, email, address, account_type, password)
                choice3 = bank.add_bank_user(user, bank)

                if choice3 == True:
                    bank_user_interface(bank, user)

            elif choice2 == 3:
                print("**Thank You**")
                break

            else:
                print('Choice Invalid!!')

    elif _choice == 2:
        print(f'**Welcome to {bank.name}**')
        while True:
            print('1. Admin Log in')
            print('2. Admin Sign up')
            print('3. Exit')
            choice2 = int(input('Enter Your Choice: '))
            if choice2 == 1:
                admin_name = input("Enter Your Name : ")
                password = input('Enter Your Password : ')
                admin = bank.admin_log_in(admin.name,password,bank)
                if admin is not None:
                    admin_user_interface(bank, admin)

            elif choice2 == 2:
                name = input("Enter Your Name : ")
                email = input("Enter Your Email : ")
                address = input("Enter Your Address : ")
                password = input("Enter Your Password : ")

                admin = Admin(name, email, address, password)
                add = bank.add_admin(admin,bank)
                if add is True:
                    admin_user_interface(bank, admin)
            elif choice2 == 3:
                print("**Thank You**")
                break
            else:
                print('Invalid Input!!')

    elif _choice == 3:
        print("**Thank You For Using The System**")
        break

    else:
        print('Invalid Choice!!')