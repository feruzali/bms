from connection import con,cur

sql = """create table customers(
                customer_id integer primary key,
                name text,
                status text,
                login_attempts integer,
                password text)"""
cur.execute(sql)


sql = """create table accounts(
                customer_id integer,
                account_no integer primary key,
                opened_on date,
                account_type text,
                status text,
                balance integer,
                withdrawals_left integer,
                constraint fk_acc foreign key(customer_id) references customers(customer_id))"""
cur.execute(sql)

sql = """create table fd(
                account_no integer primary key,
                amount integer,
                deposit_term integer,
                constraint fk_fd_acc foreign key(account_no) references accounts(account_no))"""
cur.execute(sql)

sql = """create table loans(
                customer_account_no integer,
                loan_id integer primary key,
                loan_amount integer,
                repay_term integer,
                constraint fk_loan_acc foreign key(customer_account_no) references accounts(account_no))"""
cur.execute(sql)

sql = """create table transactions(
                transaction_id integer primary key,
                account_no integer,
                type text,
                amount integer,
                balance integer,
                transaction_date date,
                constraint fk_transaction_account_no foreign key(account_no) references accounts(account_no))"""
cur.execute(sql)

sql = """create table admin(
                admin_id integer unique,
                password text)"""
cur.execute(sql)

sql = """create table closed_accounts(
                account_no integer,
                closed_on date,
                constraint fk_closed_acc foreign key(account_no) references accounts(account_no))"""
cur.execute(sql)

sql = """create view accounts_fd as
            select a.customer_id,a.account_no,fd.amount,fd.deposit_term from accounts a,fd where a.account_no = fd.account_no"""
cur.execute(sql)

sql = """create view accounts_loans as
            select a.customer_id,a.account_no,loans.loan_id,loans.loan_amount,loans.repay_term from accounts a,loans
            where a.account_no = loans.customer_account_no"""
cur.execute(sql)

sql = "insert into admin values(12204578, 'feruz123')"
cur.execute(sql)

con.commit()
