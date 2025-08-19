import requests
from base64 import b64decode

groups_names = ["mci", "mtn"]

base_url = "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/{group}/sub_{i}.txt"

sub = ""

for g in groups_names:
    i = 1
    while 1:
        url = base_url.format(group=g, i=i)
        resp = requests.get(url)
        print(resp, url)
        if resp.status_code != 200:
            break
        i += 1

        sub += b64decode(resp.text).decode()
        if not sub.endswith("\r") or not sub.endswith("\n"):
            sub += "\n"

with open("mahsa-free-config.txt", "w") as f:
    f.write(sub)
