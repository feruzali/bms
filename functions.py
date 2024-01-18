import database
from classes import Customer
import login_menu
import admin_menu
import database_admin as db_admin

def sign_up():
    customer = Customer()
    name = input("Enter Name: ")

    password = input("Enter password (min 8 char and max 20 char): ")
    while len(password) < 8 or len(password) > 20:
        print("Please Enter password in given range: ")
        password = input()

    customer.set_name(name)
    customer.set_password(password)
    customer.set_status("open")
    customer.set_login_attempts(3)

    id = database.sign_up_customer(customer)
    
    sign_in(id, password)

def sign_in(id=None, password=None):
    signed_up = id
    try:
        if not signed_up:
            id = int(input("Enter Customer ID: "))
    except:
        print("Invalid ID")
        return

    if db_admin.check_customer_exists(id) is True:
        customer = database.get_all_info_customer(id)
        if customer.get_status() == "locked":
            print("Sorry Your Account has been locked due to 3 unsuccessful login attempts")
            return
        if not signed_up:
            password = input("Enter Password: ")
        res = database.login_customer(id,password)
        if res is True:
            database.reset_login_attempts(id)
            if not signed_up:
                print("Login Successful")
            ch = 1
            while ch != 0:
                print("\n--- Main menu ---")
                print("1. Open New Account")
                print("2. Money Deposit")
                print("3. Money Withdrawal")
                print("4. Transfer Money")
                print("5. Account Closure")
                print("6. Avail Loan")
                print("0. Logout")

                try:
                    ch = int(input())
                except:
                    print("Invalid Choice")
                    ch = 1
                    continue

                if ch == 1:
                    login_menu.open_new_account(id)
                elif ch == 2:
                    login_menu.deposit_money(id)
                elif ch == 3:
                    login_menu.withdraw_money(id)
                elif ch == 4:
                    login_menu.transfer_money(id)
                elif ch == 5:
                    login_menu.close_account(id)
                elif ch == 6:
                    login_menu.avail_loan(id)
                elif ch == 0:
                    print("Logged Out Successfully")
                else:
                    print("Invalid Choice")

        else:
            att = customer.get_login_attempts()-1
            customer.set_login_attempts(att)
            database.update_customer(customer)
            print("Incorrect Password")

    else:
        print("Customer doesn't exist")

def admin_sign_in():
    try:
        id = input("\nEnter Admin ID: ")
    except:
        print("Invalid ID")
        return

    password = input("\nEnter Password: ")
    count = 2
    res = database.login_admin(id,password)

    while count != 0 and res == False:
        print("Wrong ID or Password")
        print("Attempts Remaining : ",count)
        try:
            id = int(input("Enter Admin ID: "))
        except:
            print("Invalid ID")
            return
        password = input("Enter Password: ")
        res = database.login_admin(id,password)
        count = count-1

    if res == True:
        print("Login Successful")
        ch = 1
        while ch != 0:
            print("\n --- Menu --- ")
            print("1. Print Closed Accounts History")
            print("2. List all customers")
            print("3. Get a customer ID by name")
            print("4. Unlock an account")
            print("5. Unlock all accounts")
            print("6. FD report of a customer")
            print("7. FD report of a customer vis-a-vis other customers")
            print("8. FD report of more than a particular FD amount")
            print("9. Loan report of a customer")
            print("10. Loan report of a customer vis-a-vis other customers")
            print("11. Loan report of more than a particular loan amount")
            print("12. Loan - FD report of customers")
            print("13. Report of customers who are yet to avail a loan")
            print("14. Report of customers who are yet to open an FD account")
            print("15. Report of customers who neither have a loan nor an FD account")
            print("16. Report of transactions")
            print("17. Report of a particular account`s transactions")
            print("0. Log Out")

            try:
                ch = int(input())
            except:
                print("Invalid Choice")
                ch = 1
                continue

            if ch == 1:
                admin_menu.print_closed_acc_history()
            elif ch == 2:
                admin_menu.list_customers()
            elif ch == 3:
                admin_menu.get_customer()
            elif ch == 4:
                admin_menu.unlock_acc()
            elif ch == 5:
                admin_menu.unlock_all()
            elif ch == 6:
                admin_menu.print_fd_report()
            elif ch == 7:
                admin_menu.print_fd_report_vis_customer()
            elif ch == 8:
                admin_menu.print_fd_report_wrt_amount()
            elif ch == 9:
                admin_menu.print_loan_report()
            elif ch == 10:
                admin_menu.print_loan_report_vis_customer()
            elif ch == 11:
                admin_menu.print_loan_report_wrt_amount()
            elif ch == 12:
                admin_menu.print_loan_fd_report()
            elif ch == 13:
                admin_menu.print_report_no_loan()
            elif ch == 14:
                admin_menu.print_report_no_fd()
            elif ch == 15:
                admin_menu.print_report_no_fd_loan()
            elif ch == 16:
                admin_menu.print_transactions()
            elif ch == 17:
                admin_menu.print_acc_transaction()
            elif ch == 0:
                print("Logged Out Successfully")
            else:
                print("Invalid Choice")

    else:
        print("Sorry all Attempts Finished")
