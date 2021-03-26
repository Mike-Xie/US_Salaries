from debug_tools import dprint
import scraper
import pandas as pd 

df = scraper.get_salary_table_for_job_title("Programmer")

assert type(df) == pd.DataFrame

from data_io import *

def test_write():
    name = "test_prog_salaries.csv"
    write_df(df, name)
    df_from_file = read_df(name)
    dprint(df.head())
    dprint(df_from_file.head())
    assert(df.equals(df_from_file))
