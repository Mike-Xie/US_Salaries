import requests
import data_io 

# curl 'https://taxee.io/api/v2/calculate/2020' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUElfS0VZX01BTkFHRVIiLCJodHRwOi8vdGF4ZWUuaW8vdXNlcl9pZCI6IjYwNWUzNDRmZGRkNWQyNTdlMDQxNmI1NCIsImh0dHA6Ly90YXhlZS5pby9zY29wZXMiOlsiYXBpIl0sImlhdCI6MTYxNjc4NjUxMX0.HYCMaMNvSb55jPEHeMXyiGLiIbZXuoCyc93svN8JdZU' -H 'Content-Type: application/x-www-form-urlencoded' --data 'state=NC&filing_status=married&pay_periods=26&pay_rate=116500&exemptions=2'

"""
    Returns Federal, FICA and state income taxes for a given state and gross income
"""
def get_income_tax(state_initial: str, filing_status: str, yearly_gross_income: int, exemptions: int):
    data = {
        'state': state_initial,
        'filing_status': filing_status, 
        'pay_periods': '26', 
        'pay_rate': yearly_gross_income, 
        'exemptions': exemptions}
    # state=NC&filing_status=married&pay_periods=26&pay_rate=116500&exemptions=2
    taxee_key = data_io.read_csv_to_list('secrets/taxee_key')[0].strip()
    # url = 'https://taxee.io/api/v2/calculate/2020'
    # req = requests.Request('GET', url)
    # req.headers['Authorization'] = "Bearer " + taxee_key
    # req.headers['Content-Type'] = 'application/x-www-form-urlencoded'
    # req.data = payload
    # prepped = req.prepare()
    # s = requests.Session()
    # response = s.send(prepped)
    headers = { 
        'Authorization' : "Bearer "+ taxee_key,
        'Content-Type' : 'application/x-www-form-urlencoded',
    }
    #response = requests.get('https://taxee.io/api/v2/calculate/2020', auth=taxee_key, json=payload)

    import requests

#     headers = {
#     'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJBUElfS0VZX01BTkFHRVIiLCJodHRwOi8vdGF4ZWUuaW8vdXNlcl9pZCI6IjYwNWUzNDRmZGRkNWQyNTdlMDQxNmI1NCIsImh0dHA6Ly90YXhlZS5pby9zY29wZXMiOlsiYXBpIl0sImlhdCI6MTYxNjc4NjUxMX0.HYCMaMNvSb55jPEHeMXyiGLiIbZXuoCyc93svN8JdZU',
#     'Content-Type': 'application/x-www-form-urlencoded',
# }

#     data = {
#   'state': 'NC',
#   'filing_status': 'married',
#   'pay_periods': '26',
#   'pay_rate': '116500',
#   'exemptions': '2'
# }
    response = requests.post('https://taxee.io/api/v2/calculate/2020', headers=headers, data=data)

    print (response.json())
    return response.json()

get_income_tax("NC", "married", "116500", "2")

