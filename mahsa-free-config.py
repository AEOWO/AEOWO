import requests
from base64 import b64decode

groups_names = ["mci", "mtn"]
base_url = "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/{group}/sub_{i}.txt"

sub = ""
count = 0

for g in groups_names:
    i = 1
    while True:
        url = base_url.format(group=g, i=i)
        resp = requests.get(url)
        if resp.status_code != 200:
            break
        i += 1

        decoded = b64decode(resp.text).decode()
        sub += decoded
        count += decoded.count("vmess://") + decoded.count("vless://") + decoded.count("trojan://")

        if not sub.endswith("\r") and not sub.endswith("\n"):
            sub += "\n"

with open("mahsa-free-config.txt", "w", encoding="utf-8") as f:
    f.write(sub)

print(f"✅ mahsa-free-config.txt ساخته شد! ({count} configs collected)")
