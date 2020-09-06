import requests

def scrapy_sched():
    req = requests.post(url="http://localhost:6800/delproject.json", data={"project": "smzdm", "spider": "smzdm_comment"})