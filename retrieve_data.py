import scraper
import data_io
import engineer_features
import pandas as pd
from debug_tools import *
import api_calls
from us_states_and_territories import states_only
from clean_data import replace_dollar_with_float
from math import floor

# Note: this is now a dumb function. It does not determine whether
# the query is good and return False if not. It assumes the query is
# good and will error if not. Use check_job_search_term to check first.
def get_salary_table_for_job_title(job_title: str) -> pd.DataFrame:

    # check if job is cached
    job_cache_name = get_job_salary_file_name(job_title)
    # if job is cached and recent enough, read from cache
    # TODO: implement cached file date checking. This should
    # always be true unless the cache is too old, because
    # the query should already be checked with check_job_search_term()
    if(data_io.file_exists(job_cache_name)):
        return data_io.read_df(job_cache_name)
    # else, scrape the job, save it in the cache, then return
    else:
        salary_df = scape_and_clean_salary_table(job_title)
        data_io.write_df(salary_df, job_cache_name)
        return salary_df

def get_ppp_table() -> pd.DataFrame:
    ppp_name = "ppp_table.csv"
    if(data_io.file_exists(ppp_name)): 
        return data_io.read_df(ppp_name)
    else:
        ppp_table = replace_dollar_with_float(scraper.scrape_ppp_table())
        dprint('replaced table:')
        dprint(ppp_table.head())
        data_io.write_df(ppp_table, ppp_name)
        return ppp_table

def scape_and_clean_salary_table(job_name):
    return replace_dollar_with_float(scraper.scrape_salary_table_for_job_title(job_name))

def check_job_search_term(job_name: str) -> bool:
    bad_query_list_file_name = "bad_queries.csv"
    job_salary_data_file_name = get_job_salary_file_name(job_name)

    # first check if file exists
    if(data_io.file_exists(job_salary_data_file_name)):
        return True

    # check cached bad searches
    if(data_io.file_exists(bad_query_list_file_name)):
        bad_queries = data_io.read_csv_to_list(bad_query_list_file_name)
    else:
        bad_queries = []
    if(job_name in bad_queries):
        return False

    # dprint('job name not in bad query list, scraping to check')

    # attempt scraping to check whether query is scrapable
    df = scape_and_clean_salary_table(job_name)

    # if so, return True after saving scraped data if not present already
    if(type(df) == pd.DataFrame):
        data_io.write_df(df,job_salary_data_file_name)
        return True

    # if scraping doesn't work, save in bad searches and return False
    else:
        bad_queries.append(job_name)
        data_io.write_list_to_csv(bad_queries, bad_query_list_file_name)
        return False

def get_job_salary_file_name(job_name: str):
    return f'salaries_{job_name}.csv'


# TODO needs 
def get_tax_all_states(salary_table: pd.DataFrame, marital_status: str = 'single', exemptions: int = 1) -> pd.DataFrame:
    tax_df = pd.DataFrame()
    counter = 0
    for state in salary_table['State']:
        if(counter < 5):
            # dprint('getting tax info for: '+state)
            counter += 1
        tax_df = tax_df.append(get_income_tax(state, salary_table.loc[salary_table['State']==state,'Annual Salary'].iloc[0], exemptions, marital_status))
    return tax_df

floor_hundred = lambda x: floor(int(x)/100)*100

def get_income_tax(state:str, annual_salary:int, exemptions:int = 1, marital_status:str = 'single', num_pay_periods: int = 1) -> int:
    # TODO read cache from file only once per session?
    
    state_initial = states_only[state]

    # check if tax file exists and read it if so for adding to cache later else call api
    tax_cache_name = get_tax_cache_file_name()
    # annual.fica.amount  annual.federal.amount  annual.state.amount State Initial       State
    tax_cache_df = pd.DataFrame(columns=['annual.fica.amount','annual.federal.amount','annual.state.amount','State Initial','State']) 
    if(data_io.file_exists(tax_cache_name)):
        # if file does exist, read it into tax_cache_df and check if it contains the data
        tax_cache_df = data_io.read_df(tax_cache_name)
        # dprint('read from tax cache file the following:')
        # dprint(tax_cache_df.head())
        try: 
            s = f'trying to read ({state_initial}, {floor_hundred(annual_salary)}) from cache...'
            dprint(s)
            # create a dataframe from a row in the tax cache table where annual salary rounded to 100s and state initial are the same
            row = pd.DataFrame(tax_cache_df.loc[(tax_cache_df['State Initial'] == state_initial) & (floor_hundred(tax_cache_df['Annual Salary']) == floor_hundred(annual_salary))])
            # exists in cache
            dprint('no error thrown, exists in cache')
            return row
        except KeyError:
            # dprint('error thrown, not in cache, reading from API instead...')
            pass
    # file doesn't exist or data doesn't exist in cache, so call API, append to tax_cache_df, and write to file

    row = api_calls.get_yearly_income_tax_from_api(state_initial, annual_salary, exemptions, marital_status)
    tax_cache_df = tax_cache_df.append(row)
    data_io.write_df(tax_cache_df, tax_cache_name)
    return tax_cache_df

def get_tax_cache_file_name():
    return 'tax_cache.csv'
    