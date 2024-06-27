import pandas as pd
import numpy as np
import os

# Modifier: @Lukhanyo Vena
# Date: June 2024

"""
To answer the following questions, make use of datasets: 
    'scheduled_loan_repayments.csv'
    'actual_loan_repayments.csv'
These files are located in the 'data' folder. 

All loans have a loan term of 2 years with an annual interest rate of 10%. Repayments are scheduled monthly.
A type 1 default will occur on a loan when a repayment is missed.
A type 2 default will occur on a loan when more than 15% of the expected total payments are unpaid for the year.

"""


def calculate_df_balances(df_scheduled,df_actual):
    """ 
        This is a utility function that creates a merged dataframe that will be used in the following questions. 
        This function will not be graded directly.

        Args:
            df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
            df_actual (DataFrame): Dataframe created from the 'actual_loan_repayments.csv' dataset
        
        Returns:
            DataFrame: A merged Dataframe 

            Columns after the merge should be: 
            ['RepaymentID', 'LoanID', 'Month', 'ActualRepayment', 'LoanAmount', 'ScheduledRepayment']

            Additional columns to be used in later questions should include: 
            ['UnscheduledPrincipal', 'LoanBalanceStart, 'LoanBalanceEnd'] 
            Note: 'LoanBalanceStart' for the first month of each loan should equal the 'LoanAmount'

            You may create other columns to assist you in your calculations. e.g:
            ['InterestPayment']

    """
    #Adapted from ./python.ipynb
    #deleteing starts here
    df_merged = pd.merge(df_actual, df_scheduled)

    def calculate_balance(group):
        r_monthly = 0.1 / 12  
        group = group.sort_values('Month') 
        balances = []  
        interest_payments = []
        loan_start_balances = []
        for index, row in group.iterrows():
            if balances:
                interest_payment = balances[-1] * r_monthly
                balance_with_interest = balances[-1] + interest_payment
            else:
                interest_payment = row['LoanAmount'] * r_monthly
                balance_with_interest = row['LoanAmount'] + interest_payment
                loan_start_balances.append(row['LoanAmount'])

            new_balance = balance_with_interest - row['ActualRepayment']
            interest_payments.append(interest_payment)

            new_balance = max(0, new_balance)
            balances.append(new_balance)
            
        loan_start_balances.extend(balances)
        loan_start_balances.pop()
        group['LoanBalanceStart'] = loan_start_balances
        group['LoanBalanceEnd'] = balances
        group['InterestPayment'] = interest_payments
        return group

    df_balances = df_merged.groupby('LoanID').apply(calculate_balance).reset_index(drop=True)

    df_balances['LoanBalanceEnd'] = df_balances['LoanBalanceEnd'].round(2)
    df_balances['InterestPayment'] = df_balances['InterestPayment'].round(2)
    df_balances['LoanBalanceStart'] = df_balances['LoanBalanceStart'].round(2)
    df_balances['ScheduledPrincipal'] = df_balances['ScheduledRepayment'] - df_balances['InterestPayment']
    df_balances['UnscheduledPrincipal'] = np.where(df_balances['ActualRepayment'] > df_balances['ScheduledRepayment'], df_balances['ActualRepayment'] -df_balances['ScheduledRepayment'], 0)
    #deleteing ends here
    return df_balances



#Do not edit these directories
root = os.getcwd()

if 'Task_2' in root:
    df_scheduled = pd.read_csv('data/scheduled_loan_repayments.csv')
    df_actual = pd.read_csv('data/actual_loan_repayments.csv')
else:
    df_scheduled = pd.read_csv('Task_2/data/scheduled_loan_repayments.csv')
    df_actual = pd.read_csv('Task_2/data/actual_loan_repayments.csv')

df_balances = calculate_df_balances(df_scheduled,df_actual)





def question_1(df_balances):
    """ 
        Calculate the percent of loans that defaulted as per the type 1 default definition 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        
        Returns:
            float: The percentage of defaulted loans (type 1)
    """

    loanID_with_missed_payments = len(df_balances [  df_balances['ActualRepayment'] == 0 ].drop_duplicates('LoanID', keep='first')) #DISTINCT LOAN ID's with missed payments
    total_loans = len(df_balances.drop_duplicates('LoanID', keep='first')) #total loans
    default_rate_percent = loanID_with_missed_payments/total_loans    #percentage of loans with missed payments
    return default_rate_percent






def question_2(df_scheduled, df_balances):
    """ 
        Calculate the percent of loans that defaulted as per the type 2 default definition 
        
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
            df_scheduled (DataFrame): Dataframe created from the 'scheduled_loan_repayments.csv' dataset
        
        Returns:
            float: The percentage of defaulted loans (type 2)
    """
    df_balances['TotalExpectedPayments'] = df_balances.groupby('LoanID')['ScheduledRepayment'].sum()
    df_balances['TotalActualPayments']= df_balances.groupby('LoanID')['ActualRepayment'].sum()
    df_balances['DifferenceInPayments'] = df_balances['TotalExpectedPayments']-df_balances['TotalActualPayments'] #Get difference between total payments
    total_defaulted = len(df_balances[(df_balances['DifferenceInPayments']/df_balances['TotalExpectedPayments'])>0.15]) #Difference>15% of Total_Expected_Amount
    total_loans = len(df_balances.drop_duplicates('LoanID', keep='first'))
    default_rate_percent = total_defaulted/total_loans #percentage_of_defautlt loans

    return default_rate_percent






def question_3(df_balances):
    """ 
        Calculate the anualized CPR (As a %) from the geometric mean SMM.
        SMM is calculated as: (Unscheduled Principal)/(Start of Month Loan Balance)
        CPR is calcualted as: 1 - (1- SMM_mean)^12  

        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function

        Returns:
            float: The anualized CPR of the loan portfolio as a percent.
            
    """
    SMM = df_balances['UnscheduledPrincipal']/df_balances['LoanBalanceStart']
    cpr_percent = 1-(1-SMM.mean())**12
    return cpr_percent






def question_4(df_balances):
    """ 
        Calculate the predicted total loss for the second year in the loan term.
        Use the equation: probability_of_default * total_loan_balance * (1 - recovery_rate).
        The probability_of_default value must be taken from either your question_1 or question_2 answer. 
        Decide between the two answers based on which default definition you believe to be the more useful metric.
        Assume a recovery rate of 80%         
        Args:
            df_balances (DataFrame): Dataframe created from the 'calculate_df_balances()' function
        
        Returns:
            float: The predicted total loss for the second year in the loan term.

            
         ->  I will be using the probability_of_default value calculated in question_2 (type 2 default). This value provides
            a realistic metric of the number of defaulted loans by allowing a window of the inability to make payment.
            
    """
    recovery_rate = 0.8 #recovery rate of 80% 
    total_loan_balance = (df_balances['LoanBalanceStart']- df_balances['LoanBalanceEnd']).sum() #Total_StartBalance - Total_EndBalance
    probability_of_default = question_2(df_scheduled, df_balances) #type 2 default (question_2)
    total_loss = probability_of_default * total_loan_balance * (1 - recovery_rate)

    return total_loss