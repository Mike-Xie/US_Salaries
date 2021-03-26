# US_Salaries

Install from conda_spec.txt with:

`conda install --file conda_spec.txt`

Then install from requirements.txt with:

`conda install --file requirements.txt`
`pip install -r requirements.txt`

This searches first from conda and pip covers the ones that are not found in conda.

When making changes:

First try to conda install new packages, then if not found use pip. 

Then update conda_spec.txt with:

`conda list --explicit > conda_spec.txt`

`pip freeze > requirements.txt`