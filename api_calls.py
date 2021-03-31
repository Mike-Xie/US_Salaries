import requests
import data_io 

# curl 'https://taxee.io/api/v2/calculate/2020' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUElfS0VZX01BTkFHRVIiLCJodHRwOi8vdGF4ZWUuaW8vdXNlcl9pZCI6IjYwNWUzNDRmZGRkNWQyNTdlMDQxNmI1NCIsImh0dHA6Ly90YXhlZS5pby9zY29wZXMiOlsiYXBpIl0sImlhdCI6MTYxNjc4NjUxMX0.HYCMaMNvSb55jPEHeMXyiGLiIbZXuoCyc93svN8JdZU' -H 'Content-Type: application/x-www-form-urlencoded' --data 'state=NC&filing_status=married&pay_periods=26&pay_rate=116500&exemptions=2'

"""
    Returns Federal, FICA and state income taxes for a given state and gross income
    Number arguments such as yearly_gross income, exemption_amount, num_pay_periods need to be read in as strings to the API
    TODO: figure out when to cast dataframe number columns as strings, have it inside of this function for now.
    Pay periods should be 1 if income is annual, 12 if monthly, 26 if bi-weekly, etc. 
"""
def get_yearly_income_tax(state_initial: str, marital_status: str, yearly_gross_income: int, exemption_amount: int, num_pay_periods: int = 1):
    data = {
        'state': state_initial,
        'filing_status': marital_status, 
        'pay_periods': float(num_pay_periods), 
        'pay_rate': float(yearly_gross_income), 
        'exemptions': float(exemption_amount)}

    # strip removes newline character at end that is generated from read_csv_to_list
    taxee_key = data_io.read_csv_to_list('secrets/taxee_key')[0].strip()

    headers = { 
        'Authorization' : "Bearer "+ taxee_key,
        'Content-Type' : 'application/x-www-form-urlencoded',
    }
    response = requests.post('https://taxee.io/api/v2/calculate/2020', headers=headers, data=data)

    print (response.json())
    return response.json()

get_yearly_income_tax("NC", "married", 116500, 2)

