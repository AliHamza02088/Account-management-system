class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role  # 'admin', 'company_owner', 'regular_user'

class Company:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner
        self.accounts = []
        self.expenses = []
        self.income = []

    def add_account(self, account):
        self.accounts.append(account)

class Account:
    def __init__(self, company):
        self.company = company
        self.income = 0
        self.expenses = 0

    def add_income(self, amount):
        self.income += amount

    def add_expense(self, amount):
        self.expenses += amount

#only admin add income in company;
class IncomeManager:
    @staticmethod
    def add_income(user, company, amount):
        if user.role == 'admin':
            company.accounts[0].add_income(amount)
            print(f"Income of {amount} added to {company.name} account.")
        else:
            print("Unauthorized: Only admins can add income.")

#only regular_user can submit expenses amount;
class ExpenseManager:
    @staticmethod
    def submit_expense(user, company, amount):
        if user.role == 'regular_user':
            company.expenses.append((amount, 'pending'))
            print(f"Expense of {amount} submitted for approval.")
        else:
            print("Unauthorized: Only regular users can submit expenses.")


#admin have been approve expenses of companies;
    @staticmethod
    def approve_expense(user, company, index):
        if user.role == 'admin':
            if index < len(company.expenses):
                amount, status = company.expenses[index]
                company.accounts[0].add_expense(amount)
                company.expenses[index] = (amount, 'approved')
                print(f"Expense of {amount} approved.")
            else:
                print("Invalid expense index.")
        else:
            print("Unauthorized: Only admins can approve expenses.")

#only admin or company_owner have been view reports;
class ReportManager:
    @staticmethod
    def view_report(user, company):
        if user.role in ['admin', 'company_owner']:
            print(f"Report for {company.name}:")
            print(f"Income: {company.accounts[0].income}")
            print(f"Expenses: {company.accounts[0].expenses}")
        else:
            print("Access denied: You do not have permission to view this report.")

admin = User("ALi", "admin")
company_owner = User("Ahmad", "company_owner")
regular_user = User("junaid", "regular_user")

company = Company("Enigmatix", company_owner)
account = Account(company)
company.add_account(account)

#If admin add income in company so,
IncomeManager.add_income(admin, company, 1000)

#If regular_user submit an expences of company,
ExpenseManager.submit_expense(regular_user, company, 200)

#Admin approve all expences which was submited by regular_user
ExpenseManager.approve_expense(admin, company, 0)

# Company owner viewing report
ReportManager.view_report(company_owner, company)

# Unauthorized attempt
IncomeManager.add_income(regular_user, company, 500)  # Should fail

#unauthorized attempt
ReportManager.view_report(regular_user, company)  # Should fail

#Unauthorized attempt
ExpenseManager.approve_expense(regular_user , company , 200) #should fail
