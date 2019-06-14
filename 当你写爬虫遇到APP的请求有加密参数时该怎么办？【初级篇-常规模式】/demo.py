import requests
import hashlib
import time

params = {
    "model": "demo",
    "version": "demo",
    "brand": "demo",
    "device": "demo",
    "ts": int(time.time())
}
sort_keys = sorted(params)
sign_str = "&".join(["{}={}".format(key, params[key]) for key in sort_keys])
sign = hashlib.md5(sign_str.encode()).hexdigest()
params["sign"] = sign
resp = requests.get("https://api.crawler-lab.com/learning/hash_sign", params=params)
print(resp.text)
