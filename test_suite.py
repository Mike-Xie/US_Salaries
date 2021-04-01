from debug_tools import dprint
import scraper
import clean_data
import retrieve_data
import pandas as pd 
import api_calls
from data_io import *
from engineer_features import engineer_features

def test_write():
    df = scraper.scrape_salary_table_for_job_title("Programmer")
    ppp = scraper.scrape_ppp_table()
    name = "test_prog_salaries.csv"
    write_df(df, name)
    df_from_file = read_df(name)
    # dprint(df.head())
    # dprint(df_from_file.head())
    assert(df.equals(df_from_file))

# def test_engineer_features():
#     df = scraper.get_salary_table_for_job_title("Programmer")
#     ppp = scraper.get_ppp_table()
    # clean_data.engineer_features(df, ppp_table, income_tax_table)
    

def test_taxee_tax_column_format():
    df = api_calls.get_yearly_income_tax_all_states('single',180000,1)
    dprint(df).head()

def test_engineer_features():
    raw_salary = scraper.scrape_salary_table_for_job_title('Programmer')
    ppp = scraper.scrape_ppp_table()
    income_tax_table_function = retrieve_data.get_total_income_tax
    df = engineer_features(raw_salary, ppp, income_tax_table_function)
    dprint(df.head())

test_engineer_features()