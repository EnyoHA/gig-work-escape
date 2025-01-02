from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#db = SQLAlchmey()

app = Flask(__name__)

app.config['SQLALchemy_DATABASE_URI'] = 'sqlite:///budget.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Budget:

    budget_history = {
        'income_value':[], 'income_category':[], 'income_date':[],
        'expense_value':[], 'expense_category':[], 'expense_date':[]
    }

    def __init__(self, balance):
        self.balance = balance


    def addIncome(self, income, category, date):

        self.balance += income

        self.budget_history['income_value'].append(income)
        self.budget_history['income_category'].append(category)
        self.budget_history['income_date'].append(date)

    def addExpense(self, expense, category, date):

        self.balance -= expense

        self.budget_history['expense_value'].append(expense)
        self.budget_history['expense_category'].append(category)
        self.budget_history['expense_date'].append(date)

'''
    def plotExpenseEvolution(self):

        X = [x.day for x in self.budget_history['expense_date']]

        Y = self.budget_history['expense_value']

        plt.plot(X, Y, '-o')

        plt.xlabel('Day of month')

        plt.ylabel('Expense amount in GBP')

        plt.title('Expense overview - December')

    def plotExpenseAllocation(self):

        plt.pie(self.budget_history['expense_value'],
        labels = self.budget_history['expense_category'],
        autopct = '%1.1f%%')

        plt.title('Expense allocation January')
'''
