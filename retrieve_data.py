import clean_data
import scraper
import data_io
import pandas as pd
from debug_tools import *
import api_calls
from us_states_and_territories import states_only

# Note: this is now a dumb function. It does not determine whether
# the query is good and return False if not. It assumes the query is
# good and will error if not. Use check_job_search_term to check first.
def get_salary_table_for_job_title(job_title: str) -> pd.DataFrame:
    ppp = get_ppp_table()

    # check if job is cached
    job_cache_name = get_job_salary_file_name(job_title)
    # if job is cached and recent enough, read from cache
    # TODO: implement cached file date checking. This should
    # always be true unless the cache is too old, because
    # the query should already be checked with check_job_search_term()
    if(data_io.file_exists(job_cache_name)):
        return clean_data.engineer_features(data_io.read_df(job_cache_name), ppp)
    # else, scrape the job, save it in the cache, then return
    else:
        salary_data = scraper.scrape_salary_table_for_job_title(job_title)
        data_io.write_df(salary_data, job_cache_name)
        return clean_data.engineer_features(salary_data, ppp)

def get_ppp_table() -> pd.DataFrame:
    ppp_name = "ppp_table.csv"
    if(data_io.file_exists(ppp_name)): 
        # dprint('reading from file instead of net')
        return data_io.read_df(ppp_name)
    else:
        ppp_table = scraper.scrape_ppp_table()
        data_io.write_df(ppp_table, ppp_name)
        return ppp_table

def check_job_search_term(job_name: str) -> bool:
    bad_query_list_file_name = "bad_queries.csv"
    job_salary_data_file_name = get_job_salary_file_name(job_name)

    # first check if file exists
    if(data_io.file_exists(job_salary_data_file_name)):
        return True

    # check cached bad searches
    if(data_io.file_exists(bad_query_list_file_name)):
        # dprint(f'file {bad_query_list_file_name} exists, reading:')
        bad_queries = data_io.read_csv_to_list(bad_query_list_file_name)
        # dprint(f'read into bad_queries:\n{bad_queries}')
    else:
        # dprint('no bad_query file, setting bad_queries = []')
        bad_queries = []
    if(job_name in bad_queries):
        # dprint('job name is a known bad query, returning False')
        return False

    # dprint('job name not in bad query list, scraping to check')

    # attempt scraping to check whether query is scrapable
    df = scraper.scrape_salary_table_for_job_title(job_name)

    # if so, return True after saving scraped data if not present already
    if(type(df) == pd.DataFrame):
        data_io.write_df(df,job_salary_data_file_name)
        return True

    # if scraping doesn't work, save in bad searches and return False
    else:
        # dprint(f'bad_queries before: {bad_queries}')
        bad_queries.append(job_name)
        # dprint(f'bad_queries after: {bad_queries}')
        data_io.write_list_to_csv(bad_queries, bad_query_list_file_name)
        return False

def get_job_salary_file_name(job_name):
    return f'salaries_{job_name}.csv'

# def get_income_tax_all_states(salary:int, marital_status:str, exemptions:int) -> pd.DataFrame:
#     # TODO implement tax caching
#     return clean_data.clean_income_tax_data(api_calls.get_yearly_income_tax_all_states(marital_status,salary,exemptions))

def get_total_income_tax(state:str, annual_salary:int, marital_status:str = 'single', exemptions:int = 1) -> int:
    dprint(state)
    # TODO implement tax caching
    df = api_calls.get_yearly_income_tax_from_api(states_only[state], marital_status,annual_salary,exemptions)
    return df['Total Annual Tax'][0] 