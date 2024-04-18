# Protonmail generator

### This simple script will help you automatically create a ProtonMail account.
### You can also generate an email without opening a browser window.

To start using this script, you need to:
- Have Python installed
- Download this repository to your local machine
- Than you can run it using run_app.bat
- If the application is launched for the first time, necessary dependencies will be installed first


### To find how to disable/enable the browser window mode, go to settings.py and set show_browser_window parameter
```python
filename = 'proton_accounts.csv'

# If this parameter is True, you can observe the registration process in the browser step by step
show_browser_window = False  # True or False
# waiting between creating emails
time_to_sleep_before_run_next = 30  # seconds

# Please wait a few minutes before sending email alert (in register_with_temporary_email method)
time_to_slee_if_exception_in_alert_occurred = 10  # seconds
```