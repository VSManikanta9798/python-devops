import requests
from datetime import datetime, timedelta

now = datetime.now()
past_2_days = now - timedelta(days=2)
url_log_date_str = past_2_days.strftime('%Y.%m.%d')
url = 'https://<vpc_url>.eu-west-1.es.amazonaws.com/cwl-' + url_log_date_str
print(url)
response = requests.delete(url)