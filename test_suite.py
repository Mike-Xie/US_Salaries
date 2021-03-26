import scraper
import pandas as pd 

assert type(scraper.get_salary_table_for_job_title("Programmer")) == pd.DataFrame
