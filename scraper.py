import data_io
import pandas as pd 
import requests
from typing import List 
from debug_tools import *

"""
    Function that takes as input a job title and returns a dataframe
    with the average salary by state for that job title.

"""

def scrape_salary_table_for_job_title(job_name: str) -> pd.DataFrame:
    if(job_name):
        query = job_name.replace(" ", "-")
    else:
        return False
    job_url = "https://ziprecruiter.com/Salaries/What-Is-the-Average-" + query + "-Salary-by-State"
    job_response = requests.get(job_url, timeout=10)
    dprint(job_response)
    if "ind=null" in job_response.url or "Moved Permanently" in job_response.url:
        return False
    elif job_response.status_code == 301:
        return False 
    else:
        job_text: List[pd.DataFrame] = pd.read_html(job_response.text)
        if(len(job_text) > 0):
            job_table: pd.DataFrame = pd.concat(job_text)
        else:
            return False
        return job_table

"""
    Static Function to pull Value of a Dollar table from patriotsoftware which 
    we join and multiply on the salary by state to find dollar adjusted jobs 
    * TODO: cache this somewhere
"""

def scrape_ppp_table() -> pd.DataFrame:
    ppp_url = "https://www.patriotsoftware.com/blog/accounting/average-cost-living-by-state/"
    ppp_response = requests.get(ppp_url, timeout=10)
    ppp_text: List[pd.DataFrame] = pd.read_html(ppp_response.text, header=0)
    ppp_table: pd.DataFrame = pd.concat(ppp_text)
    return ppp_table
