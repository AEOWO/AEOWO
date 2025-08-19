import base64
import json
import requests
import os

# فایل ورودی شامل همه لینک‌ها (با اسکریپت قبلی ساخته میشه)
INPUT_FILE = "mahsa-free-config.txt"

# توکن GitHub از Secrets → اسمش رو GOTHUB_TOKEN گذاشتی
GITHUB_TOKEN = os.environ.get("GOTHUB_TOKEN")

# شناسه Gist و اسم فایل داخلش
GIST_ID = "e73b64c672753f7736e001a6e3a014d0"
FILENAME = "subscription_v2ray.txt"


def parse_vmess(link: str):
    if not link.startswith("vmess://"):
        return None
    data_b64 = link[8:].strip()
    try:
        # اضافه کردن padding برای base64 در صورت نیاز
        data_json = base64.b64decode(data_b64 + "==").decode("utf-8", errors="ignore")
        return json.loads(data_json)
    except Exception:
        return None


def build_vmess(node: dict):
    data_b64 = base64.b64encode(json.dumps(node, ensure_ascii=False).encode()).decode()
    return "vmess://" + data_b64


def build_subscription():
    # می‌خوانیم فایل و آخرین لینک‌ها اولویت دارند
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]

    # برعکس می‌کنیم تا جدیدترین لینک‌ها اولویت داشته باشند
    lines.reverse()

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
            # محدودیت ۵ لینک بر اساس remark
            if len(grouped[name]) < 5:
                grouped[name].append(link)
                filtered_links.append(build_vmess(node))
        else:
            filtered_links.append(link)

    # برمی‌گردانیم به ترتیب اصلی (قدیمی‌ترین به جدیدترین)
    filtered_links.reverse()

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
    subscription = build_subscription()
    update_gist(subscription)    grouped = {}  # محدودیت تعداد لینک‌ها بر اساس remark
    filtered_links = []

    # اضافه کردن لینک‌ها با رعایت محدودیت 5 لینک برای هر remark
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

    # حذف لینک‌های تکراری و نگه داشتن جدیدترین‌ها
    filtered_links = list(dict.fromkeys(filtered_links[::-1]))[::-1]

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
    subscription = build_subscription()
    update_gist(subscription)    grouped = {}  # برای محدود کردن تعداد لینک‌ها بر اساس remark
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

    # آخرین لینک‌ها در بالای لیست قرار می‌گیرند
    filtered_links = list(dict.fromkeys(filtered_links[::-1]))[::-1]

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
    subscription = build_subscription()
    update_gist(subscription)    grouped = {}

    # بررسی از آخر به اول برای نگه داشتن جدیدترین لینک‌ها
    for link in reversed(lines):
        if link.startswith("vmess://"):
            node = parse_vmess(link)
            if not node or "ps" not in node:
                continue
            name = node["ps"]
            if name not in grouped:
                grouped[name] = []
            if len(grouped[name]) < 5:
                grouped[name].append(link)

    # بازگرداندن لینک‌ها به ترتیب اصلی
    filtered_links = []
    for name_links in grouped.values():
        filtered_links.extend(reversed(name_links))

    subscription = "\n".join(filtered_links)
    subscription_b64 = base64.b64encode(subscription.encode()).decode()
    return subscription_b64


def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    payload = {"files": {FILENAME: {"content": content}}}

    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        gist_url = resp.json()["files"][FILENAME]["raw_url"]
        print(f"✅ Subscription updated! Link: {gist_url}")
    else:
        print("❌ Update failed:", resp.text)


if __name__ == "__main__":
    subscription = build_subscription()
    update_gist(subscription)    grouped = {}
    filtered_links = []

    # بررسی از آخر به اول تا جدیدترین‌ها اول باشند
    for link in reversed(lines):
        if link.startswith("vmess://"):
            node = parse_vmess(link)
            if not node or "ps" not in node:
                continue
            name = node["ps"]
            if name not in grouped:
                grouped[name] = []
            # محدودیت 5 کانفیگ برای هر remark
            if len(grouped[name]) < 5:
                grouped[name].append(link)
                filtered_links.append(build_vmess(node))
        else:
            filtered_links.append(link)

    # برگرداندن ترتیب اصلی
    filtered_links.reverse()

    subscription = "\n".join(filtered_links)
    subscription_b64 = base64.b64encode(subscription.encode()).decode()
    return subscription_b64


def update_gist(content):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    payload = {"files": {FILENAME: {"content": content}}}

    resp = requests.patch(url, headers=headers, json=payload)
    if resp.status_code == 200:
        gist_url = resp.json()["files"][FILENAME]["raw_url"]
        print(f"✅ Subscription updated! Link: {gist_url}")
    else:
        print("❌ Update failed:", resp.text)


if __name__ == "__main__":
    subscription = build_subscription()
    update_gist(subscription)
