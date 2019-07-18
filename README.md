# vuln_app
CS-GY 9163 assignment.

# What it does
Web application vulnerable to SQLI and XSS

# Requirements
* Python 3.7
* Pip 3

Windows or Linux. On windows, ensure `set-executionpolicy unrestricted` is run with admin privileges in powershell

# How to Install
Retrieve from git by gui or run the command below:
```
git clone https://github.com/rpz214/vuln_app.git
```
Run the following to install vuln_app (relative to vuln_app directory):
```
pip install virtualenv
python -m virtualenv env
./env/scripts/activate
pip install vuln_app
```

# How to Run
```
./env/scripts/activate
cd vuln_app
flask run
```