import requests
import data_io 
import json 
import pandas as pd
from pandas import json_normalize
from us_states_and_territories import states_only

"""
    Returns Federal, FICA and state income taxes for a given state and gross income
    Number arguments such as yearly_gross income, exemption_amount, num_pay_periods need to be read in as strings to the API
    TODO: figure out when to cast dataframe number columns as strings, have it inside of this function for now.
    Pay periods should be 1 if income is annual, 12 if monthly, 26 if bi-weekly, etc. 
"""
def get_yearly_income_tax_from_api(state_initial: str, marital_status: str, yearly_gross_income: int, exemption_amount: int, num_pay_periods: int = 1):
    data = {
        'state': state_initial,
        'filing_status': marital_status, 
        'pay_periods': num_pay_periods, 
        'pay_rate': yearly_gross_income, 
        'exemptions': exemption_amount}

    # strip removes newline character at end that is generated from read_csv_to_list
    taxee_key = data_io.read_csv_to_list('secrets/taxee_key')[0].strip()

    headers = { 
        'Authorization' : "Bearer "+ taxee_key,
        'Content-Type' : 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://taxee.io/api/v2/calculate/2020', headers=headers, data=data)
    df = json_normalize(response.json())
    df['State Initial'] = state_initial
    return df

def get_yearly_income_tax_all_states(marital_status: str, yearly_gross_income: int, exemption_amount: int, num_pay_periods: int = 1):
    df = pd.DataFrame()
    for state in states_only:
        df = df.append(get_yearly_income_tax_from_api(states_only[state],marital_status,yearly_gross_income,exemption_amount,num_pay_periods))
    return df
