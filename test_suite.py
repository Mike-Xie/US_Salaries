from debug_tools import dprint
import scraper
import clean_data
import retrieve_data
import pandas as pd 
import api_calls
from data_io import *

def test_write():
    df = scraper.get_salary_table_for_job_title("Programmer")
    ppp = scraper.get_ppp_table()
    name = "test_prog_salaries.csv"
    write_df(df, name)
    df_from_file = read_df(name)
    dprint(df.head())
    dprint(df_from_file.head())
    assert(df.equals(df_from_file))

def test_engineer_features():
    df = scraper.get_salary_table_for_job_title("Programmer")
    ppp = scraper.get_ppp_table()
    income_tax_table = 
    clean_data.engineer_features(df, ppp_table, income_tax_table)