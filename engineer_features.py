import pandas as pd
import us_states_and_territories as states
from clean_data import replace_dollar_with_float
from debug_tools import dprint
def engineer_features(base_salary_table: pd.DataFrame, ppp_table: pd.DataFrame, get_income_tax) -> pd.DataFrame:

    # pre-process
    # base_salary_table = base_salary_table.set_index('State')
    base_salary_table = replace_dollar_with_float(base_salary_table)

    # ppp_table = ppp_table.set_index('State')
    ppp_table = replace_dollar_with_float(ppp_table)
    dprint('ppp table:')
    dprint(ppp_table.head())

    base_salary_table = base_salary_table.merge(ppp_table, on='State')

    dprint(base_salary_table.dtypes)

    # get income tax per state from the salary table
    income_tax_table = base_salary_table[['Annual Salary', 'State']].apply(
        lambda state_row: get_income_tax(state_row['State'], state_row['Annual Salary']), axis=1
    )
    net_income_table = base_salary_table.join(income_tax_table)

    # state initial column necessary for plotly geometry arguments & merging with tax API returned values
    net_income_table['Monthly Salary Minus Rent'] = net_income_table['Monthly Pay'] - net_income_table['Median Monthly Rent']
    net_income_table['Median Yearly Rent'] = net_income_table['Median Monthly Rent'] * 12
    net_income_table['Yearly Salary Minus Rent'] = net_income_table['Annual Salary'] - net_income_table['Median Yearly Rent']

    # Mean Wage Money left over after Expenses
    net_income_table['Median Net Income'] = net_income_table['Post Tax Annual Salary'] - net_income_table['Median Yearly Rent']
    
    return net_income_table
