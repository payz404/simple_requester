from fake_headers import Headers
import requests, os, json


class Requester(requests.Session):

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.proxies = {}
        self.live_proxies = {}



    def set_proxies(self, proxies=None, proxies_file=None, debug:bool=False):
        
        return f"[Error]: {proxies_file} is Does Exists" if proxies_file is not None and os.path.exists(proxies_file) is not True else (self.get_proxies(proxies,debug) if proxies is not None else ([self.get_proxies(x.rstrip(),debug) for x in open(proxies_file, "r").readlines()]) if os.path.exists(proxies_file) else None)



    def get_proxies(self, proxies, debug):
        
        self.proxies['http'] = "http://",proxies
        self.proxies['https'] = "https://",proxies
        i = 0
        if self.check(proxies=self.proxies) == True:
            return self.session.proxies.update(self.proxies)
        else:
            if debug:
                print(f"\x1b[K [BAD PROXY]: {self.proxies['http']} -> Program will Automatically Rotate to Next Proxy", flush=True, end="\r")
            pass
        


    def check(self, **kwargs):
        
        kwargs.update(kwargs)
        proxies = kwargs['proxies']

        try:
            x = super().get('https://httpbin.org/ip', proxies=proxies, timeout=2).json()
            return True
        except Exception as e:
            return False
        """
        Full Handler for Check Proxies !
        except requests.exceptions.ConnectionError as e:
            print(f"[DIE]: Invalid Proxy")
        except requests.exceptions.Timeout as e:
            print(f"[DIE]: Proxy Time Out -> {e}")
        except requests.ProxyError as e:
            print(f"[DIE]: Invalid Proxy or Die Proxy{e}")
        else:
            print("proxies: None")
        """



    def my_requester(self, url=None, method="get", header=None, payloads=None, output=None, csrf_key="x-csrf-token",**kwargs):


        myheaders = Headers(
            browser="chrome",
            os="win",
            headers=True).generate() if header !=None and header.lower() == "auto" else (header if header != "" else None)
           
        proxy = self.session.proxies
        if (c:= self.cookies.get("CSRFToken")):
            myheaders[csrf_key] = c
            
        
        return super().post(url, headers=myheaders, data=payloads, proxies=proxy,**kwargs) if method.lower() == "post" else super().get(url, headers=myheaders, params=payloads, proxies=proxy,**kwargs)



class Scrapper():

    def __init__(self,
            url=None,
            method="get",
            header=None,
            payloads=None,
            proxies=None,
            proxies_file=None,
            csrf_key=None,
            debug=False,
            **kwargs):

        with Requester() as app:

            app.set_proxies(proxies,proxies_file, debug) if proxies is not None or proxies_file is not None else None
            (r := app.my_requester(url, method, header, payloads, **kwargs)).raise_for_status()
            print("\x1b[K ", end="\r")
            self.response = r








