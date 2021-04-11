import pandas as pd
import us_states_and_territories as states
from clean_data import replace_dollar_with_float
from debug_tools import dprint
from math import floor

# note that the tax_table should contain a value for every state in the salary table - it is on another module to determine
# the correct tax (engineer_features is agnostic to marital status, etc.) - all tables should be indexed by state by the
# time they are passed here. This needs to combine ppp, tax table, and base salary table with the right column names
def engineer_features(base_salary_table: pd.DataFrame, ppp_table: pd.DataFrame, tax_table: pd.DataFrame) -> pd.DataFrame:

    # salary_table_with_ppp = base_salary_table.merge(ppp_table, on='State')

    # need State initials because taxee_api and dash both use them 
    salary_table_with_ppp['State Initial'] = salary_table_with_ppp['State'].map(states.states_only)
    salaries_by_state = dict.zip(salary_table_with_ppp['State Initial'].values.tolist()
    sal_tax_ppp = salary_table_with_ppp.merge(tax_table, on='State Initial')

    # create new features
    # sal_tax_ppp['Total Annual Tax'] = sal_tax_ppp['annual.fica.amount'] + sal_tax_ppp['annual.federal.amount'] + sal_tax_ppp['annual.state.amount']
    sal_tax_ppp['Post Tax Annual Salary'] = (sal_tax_ppp['Annual Salary'] - sal_tax_ppp['Total Annual Tax'])
    sal_tax_ppp['Post Tax Annual Salary'] = sal_tax_ppp['Post Tax Annual Salary'].astype(int).apply(lambda x: floor(x / 100) * 100)
    sal_tax_ppp['Annual Salary Rounded'] = sal_tax_ppp['Annual Salary'].apply(lambda x: floor(x/100) / 10).astype(str).apply(lambda s: s+'k')

    return sal_tax_ppp
