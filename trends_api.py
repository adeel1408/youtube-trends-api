import requests

proxies = [
    'http://93.190.138.107:46182',
    'http://57.129.81.201:8080',
    # ...add more here
]

for proxy in proxies:
    try:
        r = requests.get("https://www.google.com", proxies={
            "http": proxy,
            "https": proxy
        }, timeout=5)
        print(f"✅ Proxy works: {proxy}")
    except Exception as e:
        print(f"❌ Failed: {proxy} - {e}")
