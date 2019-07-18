from setuptools import setup

setup(name='vuln_app',
      version='1.0',
      description='Vulnerable web app with capability to login and upload posts',
      install_requires=['flask', 'python-dotenv', 'flask_wtf', 'wtforms']
      )
