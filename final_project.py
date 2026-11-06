import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns


class smart_expense_tracker:
    def __init__(self,path):
        self.df= pd.read_csv(path)
        self.menu()
    
    def menu(self):
        user_choice= int(input("""Chooose what do you want to do
        1. add new expense
        2. get summary
        3. filter expense
        4. genrate report
        5. exit
        """)) 

        if user_choice == 1:
            self.add_new_expense()
        elif user_choice == 2:
            self.get_summary()
        elif user_choice == 3:        
            self.filter_expense()
        elif user_choice == 4:
            self.generate_report()     
        elif user_choice == 5:
            print("Exiting the program")
            self.exit()
        else:
            print("Invalid choice, please try again")
            self.menu() 


    def add_new_expense(self):
        date= input('Enter the date of expense in YYYY-MM-DD format')
        if len(date)!=10:
            print("date should be in YYYY-MM-DD format")
            date= input('enter the date of expense in YYYY-MM-DD format')

        amount= float(input("enter the amount of expense"))
        if amount<=0:
            print('Amount should be greater than 0')
            amount= float(input('enter the amount of expense'))


        category= input("Enter the category of expense")
        if category not in self.df['Category'].unique():
            print("Category not found in the existing categories")
            print("choose from these categories : ",self.df['Category'].unique())
            category= input("Enter the category of expense")


        description= input("enter the description of expense")

        new_row= {'Date':[date],'Amount':[amount],'Category':[category], 'Description': [description]}
        new_row= pd.DataFrame(new_row)
        self.df= pd.concat([self.df,new_row],ignore_index=True  )
        print("Expense added successfully")

        self.menu()

    def get_summary(self):
        total_expense= self.df['Amount'].sum() 
        print("Total expense: ", total_expense)
        category_summary= self.df.groupby('Category')['Amount'].sum()
        print("Expense summary by category: ")
        print(category_summary)

        self.menu()



    def filter_expense(self):
        filter_choice= int(input("""Choose how do you want to filter the expenses
        1. by date
        2. by category
        3. by date range
        """))
        min_date= self.df['Date'].min()
        max_date= self.df['Date'].max() 
        print('The date range of expenses is from ', min_date, 'to ', max_date)
        if filter_choice==1:
            date= input("what is the date of expense you want to check")
            filtered_df= self.df[self.df['Date']==date]
            print(filtered_df)
        elif filter_choice==2:
            category= input(" category of expense")
            filtered_df= self.df[self.df['Category']==category]
            print(filtered_df)
        elif filter_choice==3:
            self.df['Date'] = pd.to_datetime(self.df['Date'])
            start_date= input("Enter the start date in YYYY-MM-DD format")
            end_date= input("Enter the end date in YYYY-MM-DD format")
            filtered_df= self.df[(self.df['Date']>=start_date) & (self.df['Date']<=end_date)]
            print(filtered_df)
        else:
            print("Invalid choice, please try again")
            self.filter_expense()


        self.menu()


    def generate_report(self):

        self.df['Date'] = pd.to_datetime(self.df['Date'])
        print("========== EXPENSE SUMMARY ==========")
        print(" ")
        print("total expense :", np.sum(self.df['Amount']))
        print("average expense :", np.mean(self.df['Amount']))
        print("maximum expense :", np.max(self.df['Amount']))
        print("minimum expense :", np.min(self.df['Amount']))

        print("total transactions:", len(self.df))
        print("unique categories:", self.df['Category'].nunique())

        print("Statistical Summary:")
        print(self.df['Amount'].describe())
        print(" ")

        print("========== CATEGORY ANALYSIS ==========")

        category_expense = self.df.groupby('Category')['Amount'].sum()

        print(category_expense)

        category_expense.plot(kind='barh',title='category Wise Expenses', xlabel='Amount', ylabel='Category')
        plt.show()

        print(" ")
        print("========== CATEGORY PERCENTAGE ==========")

        percentage = (category_expense / category_expense.sum()) * 100

        print(percentage.round(2))

        category_expense.plot(kind='pie',title='category Wise Expenses',xlabel='Amount', ylabel='Category',autopct='%1.1f%%',figsize=(8, 8))
        plt.show()

        print("\n========== DAILY EXPENSE ==========\n")

        daily_expense = self.df.groupby('Date')['Amount'].sum()

        print(daily_expense)

        daily_expense.plot(kind='line',marker='o',title='Daily expense chart')
        plt.tight_layout()
        plt.show()

        print("\n========== MONTHLY EXPENSE ==========\n")
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.df['month']= self.df['Date'].dt.to_period('M')

        monthly_expense = self.df.groupby(['month'])['Amount'].sum()

        print(monthly_expense)

        monthly_expense.plot(kind='bar', title='monthly expense',xlabel='Month',ylabel='amount')
        plt.show()

        print("\n========== DATE WISE CATEGORY ANALYSIS ==========\n")

        date_wise_category = self.df.groupby(['month', 'Category'] )['Amount'].sum().unstack(fill_value=0)

        print(date_wise_category)

        date_wise_category.plot(kind='line',title='monthly Expense Per Category',figsize=(12, 6),xlabel='Month',ylabel='Amount' ,marker='o')
        plt.tight_layout()
        plt.show()

        print("\n========== Histogram ==========\n")

        self.df['Amount'].plot(kind='hist',title='Expense Histogram',xlabel='Amount',ylabel='Frequency')
        plt.show()




        self.menu()



    def exit(self):
        self.df.to_csv('expenses.csv', index=False)
        print("xiting the program")
        exit()
    

        
a= smart_expense_tracker('expenses.csv')
    