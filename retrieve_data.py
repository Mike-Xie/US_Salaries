import clean_data
import scraper
import data_io
import pandas as pd
from debug_tools import *

def get_salary_table_for_job_title(job_title: str) -> pd.DataFrame:
    salary_data = scraper.scrape_salary_table_for_job_title(job_title)
    if (type(salary_data) == pd.DataFrame):
        ppp = scraper.scrape_ppp_table()
        return clean_data.engineer_features(salary_data, ppp)
    else:
        return None

def get_ppp_table() -> pd.DataFrame:
    ppp_name = "ppp_table.csv"
    if(data_io.file_exists(ppp_name)): 
        dprint('reading from file instead of net')
        return data_io.read_df(ppp_name)
    else:
        ppp_table = scraper.scrape_ppp_table()
        data_io.write_df(ppp_table, ppp_name)
        return ppp_table