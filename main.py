import requests
from bs4 import BeautifulSoup as BS

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

def get_proxy():
    data_link = {"https": '1', "submit": 'Search'}
    r = requests.get("https://www.iplocation.net/proxy-list", data=data_link, headers=header)
    proxy_list = []
    if r.status_code == 200:
        soup = BS(r.text, 'html.parser')
        table = soup.select_one('table.table.table-hover')
        rows = table.select('tr')[1:]
        for row in rows[1:]:
            columns = row.find_all('td')
            ip_address = columns[0].get_text().strip()
            port = columns[1].get_text().strip()
            location = columns[3].get_text().strip()
            proxy_info = (ip_address, port, location)
            proxy_list.append(proxy_info)

        return proxy_list
    else:
        return []


def output_proxy(proxy_list):
    with open('proxy.txt', 'w') as file:
        for proxy in proxy_list:
            ip_address, port, location = proxy
            file.write('*' * 30 + '\n')
            file.write(f'{ip_address}:{port:5}\n')
            file.write(f'Location: {location:14}\n')
            file.write('*' * 30 + '\n')

    print('[+] Saved in the text file “proxy.txt”')

def log_info():
    print("[!] Proxy search started...")
    proxy_list = get_proxy()
    if proxy_list:
        output_proxy(proxy_list)
    else:
        print("[!] Failed to connect...")

if __name__ == "__main__":
    log_info()

