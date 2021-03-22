import pandas as pd 
import requests
from typing import List 

"""
    Static Function that takes a job title and returns a dataframe
    with the average salary by state.

"""

def get_table_for_job_title(job_name: str) -> pd.DataFrame:
    query = job_name.replace(" ", "-")
    job_url = "https://ziprecruiter.com/Salaries/What-Is-the-Average-" + query + "-Salary-by-State"
    job_response = requests.get(job_url, timeout=10)
    print(job_url)

    job_text: List[pd.DataFrame] = pd.read_html(job_response.text)
    job_table: pd.DataFrame = pd.concat(job_text)

    return job_table

"""
    Function that takes a job title and returns True if a page
    with average salary info exists on ziprecruiter.

    To-Do: Find more sites with average salary info to try.
"""

def job_title_has_data(job_name: str) -> bool:
    query = job_name.replace(" ", "-")
    job_url = "https://ziprecruiter.com/Salaries/What-Is-the-Average-" + query + "-Salary-by-State"
    job_response = requests.get(job_url, timeout=10)
    print(job_url)
    
    if "ind=null" in job_response.url or "Moved Permanently" in job_response.url:
        return False
    elif job_response.status_code == 301:
        return False 
    else:
        return True

"""
    Static Function to pull Value of a Dollar table from patriotsoftware which 
    we join and multiply on the salary by state to find dollar adjusted jobs 
"""

def get_ppp_table():
    # ppe url table and response 
    ppp_url = "https://www.patriotsoftware.com/blog/accounting/average-cost-living-by-state/"
    ppp_response = requests.get(ppp_url, timeout=10)
    # print(ppp_response)
    ppp_text: List[pd.DataFrame] = pd.read_html(ppp_response.text, header=0)
    ppp_table: pd.DataFrame = pd.concat(ppp_text)
    # print(ppp_table.head())
    # ppp_table.to_csv("usa_ppe_by_state.csv", index=False)
    # print(type(ppp_table))
    return ppp_table


"""
    Pre-processing function to replace $ value strings with floats so we can perform arithmetic on dataframes 
"""
def replace_dollar_with_float(df):
    
    df = df.set_index('State').apply(lambda x: (x.str.replace('[$,]', '').astype(float)))

    return df 
