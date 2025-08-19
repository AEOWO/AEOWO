import requests
from base64 import b64decode

groups_names = ["mci", "mtn"]
base_url = "https://raw.githubusercontent.com/mahsanet/MahsaFreeConfig/refs/heads/main/{group}/sub_{i}.txt"

sub = ""

for g in groups_names:
    i = 1
    while True:
        url = base_url.format(group=g, i=i)
        resp = requests.get(url)
        if resp.status_code != 200:
            break
        i += 1
        sub += b64decode(resp.text).decode()
        if not sub.endswith("\r") and not sub.endswith("\n"):
            sub += "\n"

with open("mahsa-free-config.txt", "w", encoding="utf-8") as f:
    f.write(sub)

print("✅ mahsa-free-config.txt ساخته شد!")"ignore")
        return json.loads(data_json)
    except Exception:
        return None


def build_vmess(node: dict):
    data_b64 = base64.b64encode(json.dumps(node, ensure_ascii=False).encode()).decode()
    return "vmess://" + data_b64


def build_subscription():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    grouped = {}
    filtered_links = []

    for link in lines:
        if link.startswith("vmess://"):
            node = parse_vmess(link)
            if not node or "ps" not in node:
                continue
            name = node["ps"]
            if name not in grouped:
                grouped[name] = []
            if len(grouped[name]) < 5:
                grouped[name].append(link)
                filtered_links.append(build_vmess(node))
        else:
            filtered_links.append(link)

    subscription = "\n".join(filtered_links)
    subscription_b64 = base64.b64encode(subscription.encode()).decode()
    return subscription_b64


def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    payload = {
        "files": {
            FILENAME: {"content": content}
        }
    }
    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        gist_url = resp.json()["files"][FILENAME]["raw_url"]
        print(f"✅ Subscription updated! Link: {gist_url}")
    else:
        print("❌ Update failed:", resp.text)


if __name__ == "__main__":
    sub = build_subscription()
    update_gist(sub)
