import data_io
import pandas as pd 
import requests
from typing import List 
from debug_tools import *

"""
    Function that takes as input a job title and returns a dataframe
    with the average salary by state for that job title.

"""

cookie_data_copied_from_chrome_packet = data_io.read_csv_to_list('secrets/ziprecruiter_cookie')[0].strip()

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",

    "upgrade-insecure-requests": "1",
    "dnt": "1",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",

    "authority":" www.ziprecruiter.com",
    "method":" GET",
    "path":" /Salaries/What-Is-the-Average-Chemist-Salary-by-State",
    "scheme":" https",
    "accept":" text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding":" gzip, deflate, br",
    "accept-language":" en-US,en;q=0.9",
    "cookie":cookie_data_copied_from_chrome_packet,
}

def scrape_salary_table_for_job_title(job_name: str) -> pd.DataFrame:
    if(job_name):
        query = job_name.replace(" ", "-")
    else:
        return False
    job_url = "https://ziprecruiter.com/Salaries/What-Is-the-Average-" + query + "-Salary-by-State"
    job_response = requests.get(job_url,  headers=headers, timeout=10)
    dprint(job_response)
    if "ind=null" in job_response.url or "Moved Permanently" in job_response.url:
        return False
    elif job_response.status_code == 301:
        return False 
    elif job_response.status_code == 403:
        dprint('page couldn\'t load, access denied w/ 403')
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
