import urllib.request


def scrapy_sched():
    data = urllib.parse.urlencode({"project": "smzdm", "spider": "smzdm_comment"})
    data = data.encode('ascii')
    url = "http://localhost:6800/schedule.json"
    response = urllib.request.urlopen(url, data)
    print(response.info())
