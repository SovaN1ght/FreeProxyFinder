import requests
from bs4 import BeautifulSoup
from colorama import Fore
from art import tprint

class ProxyFinder():
    def __init__(self, url="www.example.com") -> None:
        self.check_url = url

    _proxies_url = "https://free-proxy-list.net/"
    _proxy_headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"
    }

    def getProxyList(self):
        response = requests.get(url=self._proxies_url,
                                headers=self._proxy_headers)
        proxy_page = BeautifulSoup(response.text, "lxml")
        data = proxy_page.find(class_="form-control")
        proxies = data.text.split("\n")
        # Format proxy list
        proxies.remove("Free proxies from free-proxy-list.net")
        proxies.remove('')
        del proxies[0], proxies[-1]
        return proxies

    def findWorkedProxy(self, proxy_list):
        for proxy in proxy_list:
            checked_proxy = {
                "https": f"{proxy}"
            }
            try:
                response = requests.get(self.check_url, proxies=checked_proxy)
            except Exception as e:
                print(Fore.RED + f"{proxy} - BAD!")
                continue

            if response.status_code == 200:
                return checked_proxy

            print(Fore.RED + f"{proxy} - BAD!")


def main():
    tprint("Proxy Finder", font="bulbhead")
    main_url = input("Enter the URL here --> ")
    proxyFinder = ProxyFinder(main_url)
    print(Fore.BLUE + "Getting actual proxy list...")
    proxy_list = proxyFinder.getProxyList()
    print(Fore.GREEN + "Successful!")
    print(Fore.BLUE + "Trying to find worked proxy...")
    worked_proxy = proxyFinder.findWorkedProxy(proxy_list=proxy_list)
    print(Fore.GREEN + "Worked proxy finded!")
    print()
    print(Fore.GREEN + worked_proxy["https"])
    print()


if __name__ == "__main__":
    main()
