#!/usr/bin/python

import config
import requests
import re
import time
import json


class Scraper():
    def __init__(self):
        self.session = requests.Session()
        self.login()

        while True:
            self.request_json()
            time.sleep(60)

    def login(self):
        r = self.session.head(config.login["url"])
        self.session_id = re.search("%s(.*)%s" % ("=", "; "),
                                    r.headers["Set-Cookie"]).group(1)

        url = "%s/goform/login" % config.login["url"]
        data = {
            "usr": config.login["username"],
            "pwd": config.login["password"],
            "preSession": self.session_id
        }
        r = self.session.post(url, data=data)
        self.session_cookie = re.search("%s(.*)%s" % ("sessionindex=", "; "),
                                        r.headers["Set-Cookie"]).group(1)
        print "%s: Logging in, %s" % (time.ctime(), self.session_cookie)

    def request_json(self):
        url = "%s/data/getConnectInfo.asp" % config.login["url"]
        cookies = {
           "preSession": self.session_id,
           "sessionindex": self.session_cookie
        }
        r = self.session.get(url, cookies=cookies, stream=True,
                             allow_redirects=False)

        if r.status_code == 302:
            self.login()
        else:
            devices = r.json()
            people = []
            for person in config.people:
                is_in = False
                for device in devices:
                    if (device["macAddr"] in person["devices"] and
                            device["online"] == "active"):
                        is_in = True
                people.append({
                    "name": person["name"],
                    "eyes": person["eyes"],
                    "in": is_in
                })

            # set absolute path if running on pi load
            with open("../eye-lighter/people.json", "w") as fp:
                json.dump(people, fp)

            print "%s: Data exported, %d devices found" % (time.ctime(),
                                                           len(devices))


# uncomment if running on pi load
# time.sleep(60)

scraper = Scraper()
