import pandas as pd
import us_states_and_territories as states
from clean_data import replace_dollar_with_float
from debug_tools import dprint
from api_calls import get_yearly_income_tax_from_api
from math import floor

def engineer_features(base_salary_table: pd.DataFrame, ppp_table: pd.DataFrame, get_income_tax) -> pd.DataFrame:

    # pre-process
    base_salary_table = replace_dollar_with_float(base_salary_table)

    ppp_table = replace_dollar_with_float(ppp_table)
  #  dprint('ppp table:')
  #  dprint(ppp_table.head())

    salary_cola_table = base_salary_table.merge(ppp_table, on='State')

    # need State initials because taxee_api and dash both use them 
    salary_cola_table['State Initial'] = salary_cola_table['State'].map(states.states_only)
    print(salary_cola_table.head())
   # dprint(base_salary_table.dtypes)

    # get income tax per state from the salary table
    # salary cola dataframe
    all_tax_df = salary_cola_table.merge(salary_cola_table[['Annual Salary', 'State Initial']].apply(
        lambda state_row: get_income_tax(state_row['State Initial'], state_row['Annual Salary']).squeeze(), axis=1)
        # lambda state_row: pd.Series(get_income_tax(state_row['State Initial'], state_row['Annual Salary']).to_numpy()[0], index=get_income_tax(state_row['State Initial'],state_row['Annual Salary']).columns), axis=1, result_type='expand'
    )

    # create new features
    all_tax_df['Total Annual Tax'] = all_tax_df['annual.fica.amount'] + all_tax_df['annual.federal.amount'] + all_tax_df['annual.state.amount']
    all_tax_df['Post Tax Annual Salary'] = (all_tax_df['Annual Salary'] - all_tax_df['Total Annual Tax'])
    all_tax_df['Post Tax Annual Salary'] = all_tax_df['Post Tax Annual Salary'].astype(int).apply(lambda x: floor(x / 100) * 100)
    all_tax_df['Annual Salary Rounded'] = all_tax_df['Annual Salary'].apply(lambda x: floor(x/100) / 10).astype(str).apply(lambda s: s+'k')

    # dprint(all_tax_all_tax_df.head())
    return all_tax_df

    
    # net_income_table = salary_cola_table.join(income_tax_table)

    # # state initial column necessary for plotly geometry arguments & merging with tax API returned values
    # net_income_table['Monthly Salary Minus Rent'] = net_income_table['Monthly Pay'] - net_income_table['Median Monthly Rent']
    # net_income_table['Median Yearly Rent'] = net_income_table['Median Monthly Rent'] * 12
    # net_income_table['Yearly Salary Minus Rent'] = net_income_table['Annual Salary'] - net_income_table['Median Yearly Rent']

    # # Mean Wage Money left over after Expenses
    # net_income_table['Median Net Income'] = net_income_table['Post Tax Annual Salary'] - net_income_table['Median Yearly Rent']
    
    # return net_income_table
