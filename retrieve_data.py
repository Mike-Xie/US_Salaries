import clean_data
import scraper
import data_io
import engineer_features
import pandas as pd
from debug_tools import *
import api_calls
from us_states_and_territories import states_only
from math import floor

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
        return engineer_features.engineer_features(data_io.read_df(job_cache_name), ppp, get_income_tax)
    # else, scrape the job, save it in the cache, then return
    else:
        salary_data = scraper.scrape_salary_table_for_job_title(job_title)
        data_io.write_df(salary_data, job_cache_name)
        return engineer_features.engineer_features(salary_data, ppp, get_income_tax)

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


floor_hundred = lambda x: floor(x/100)*100

def get_income_tax(state_initial:str, annual_salary:int, exemptions:int = 1, marital_status:str = 'single', num_pay_periods: int = 1) -> int:
#     dprint(state)
#     # TODO read cache only once

    # check if tax file exists else call api and read it if so for adding to cache later
    tax_cache_name = get_tax_cache_file_name()
    # annual.fica.amount  annual.federal.amount  annual.state.amount State Initial       State
    tax_cache_df = pd.DataFrame(columns=['annual.fica.amount','annual.federal.amount','annual.state.amount','State Initial','State']) 
    if(data_io.file_exists(tax_cache_name)):
        dprint('tax cache file exists, reading...')
        # if file does exist, read it into tax_cache_df and check if it contains the data
        tax_cache_df = data_io.read_df(tax_cache_name)
        dprint('read into tax cache the following:')
        dprint(tax_cache_df.head())
        try: 
            s = f'trying to read ({state_initial}, {floor_hundred(annual_salary)}) from cache...'
            row = tax_cache_df.loc[[(tax_cache_df['State Initial'] == state_initial) & (floor_hundred(tax_cache_df['Annual Salary']) == floor_hundred(annual_salary))]]
            # exists in cache
            dprint('no error thrown, exists in cache')
            return row
        except KeyError:
            dprint('error thrown, not in cache, reading from API instead...')
            pass
    # file doesn't exist or data doesn't exist in cache, so call API, append to tax_cache_df, and write to file
    row = api_calls.get_yearly_income_tax_from_api(state_initial,annual_salary, exemptions, marital_status)
    dprint('read from API:')
    dprint(row.head())
    tax_cache_df.append(row, ignore_index=True)
    dprint('tax cache with new row appended:')
    dprint(tax_cache_df.head())
    dprint('writing df to file...')
    data_io.write_df(tax_cache_df, tax_cache_name)
    return tax_cache_df

def get_tax_cache_file_name():
    return 'tax_cache.csv'
    