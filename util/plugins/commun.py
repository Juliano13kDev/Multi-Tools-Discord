import requests, os, sys, re, time, random, os.path, string, subprocess, random, threading, ctypes, shutil
from pystyle import Add, Center, Anime, Colors, Colorate, Write, System
from colorama import Fore
from time import sleep

THIS_VERSION = "1.2.0"

y = Fore.LIGHTYELLOW_EX
b = Fore.LIGHTBLUE_EX
w = Fore.LIGHTWHITE_EX

def setTitle(_str):
    system = os.name
    if system == 'nt':
        ctypes.windll.kernel32.SetConsoleTitleW(f"{_str} - Made By JulianoDev")
    elif system == 'posix':
        sys.stdout.write(f"\x1b]0;{_str} - Made By JulianoDev\x07")
    else:
        pass

def Spinner():
	l = ['|', '/', '-', '\\']
	for i in l+l+l:
		sys.stdout.write(f"""\r{y}[{b}#{y}]{w} Loading... {i}""")
		sys.stdout.flush()
		time.sleep(0.2)

def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    elif system == 'posix':
        os.system('clear')
    else:
        print('\n'*120)
    return

def transition():
    clear()
    Spinner()
    clear()

def getTempDir():
    system = os.name
    if system == 'nt':
        return os.getenv('temp')
    elif system == 'posix':
        return '/tmp/'

def proxy_scrape(): 
    proxieslog = []
    setTitle("Scraping Proxies")
    startTime = time.time()
    temp = getTempDir()+"\\atio_proxies"

    def fetchProxies(url, custom_regex):
        global proxylist
        try:
            proxylist = requests.get(url, timeout=5).text
        except Exception:
            pass
        finally:
            proxylist = proxylist.replace('null', '')
        custom_regex = custom_regex.replace('%ip%', '([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3})')
        custom_regex = custom_regex.replace('%port%', '([0-9]{1,5})')
        for proxy in re.findall(re.compile(custom_regex), proxylist):
            proxieslog.append(f"{proxy[0]}:{proxy[1]}")

    proxysources = [
        ["http://spys.me/proxy.txt","%ip%:%port% "],
        ["http://www.httptunnel.ge/ProxyListForFree.aspx"," target=\"_new\">%ip%:%port%</a>"],
        ["https://raw.githubusercontent.com/sunny9577/proxy-scraper/master/proxies.json", "\"ip\":\"%ip%\",\"port\":\"%port%\","],
        ["https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list", '"host": "%ip%".*?"country": "(.*?){2}",.*?"port": %port%'],
        ["https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt", '%ip%:%port% (.*?){2}-.-S \\+'],
        ["https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt", '%ip%", "type": "http", "port": %port%'],
        ["https://www.us-proxy.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://free-proxy-list.net/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://www.sslproxies.org/", "<tr><td>%ip%<\\/td><td>%port%<\\/td><td>(.*?){2}<\\/td><td class='hm'>.*?<\\/td><td>.*?<\\/td><td class='hm'>.*?<\\/td><td class='hx'>(.*?)<\\/td><td class='hm'>.*?<\\/td><\\/tr>"],
        ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=6000&country=all&ssl=yes&anonymity=all", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt", "%ip%:%port%"],
        ["https://raw.githubusercontent.com/shiftytr/proxy-list/master/proxy.txt", "%ip%:%port%"],
        ["https://proxylist.icu/proxy/", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/1", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/2", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/3", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/4", "<td>%ip%:%port%</td><td>http<"],
        ["https://proxylist.icu/proxy/5", "<td>%ip%:%port%</td><td>http<"],
        ["https://www.hide-my-ip.com/proxylist.shtml", '"i":"%ip%","p":"%port%",'],
        ["https://raw.githubusercontent.com/scidam/proxy-list/master/proxy.json", '"ip": "%ip%",\n.*?"port": "%port%",']
    ]
    threads = [] 
    for url in proxysources:
        t = threading.Thread(target=fetchProxies, args=(url[0], url[1]))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    proxies = list(set(proxieslog))
    with open(temp, "w") as f:
        for proxy in proxies:
            for i in range(random.randint(7, 10)):
                f.write(f"{proxy}\n")
    execution_time = (time.time() - startTime)
    setTitle(f"@TIO Menu v{THIS_VERSION}")

def proxy():
    temp = getTempDir()+"\\atio_proxies"
    if os.stat(temp).st_size == 0:
        proxy_scrape()
    proxies = open(temp).read().split('\n')
    proxy = proxies[0]

    with open(temp, 'r+') as fp:
        lines = fp.readlines()
        fp.seek(0)
        fp.truncate()
        fp.writelines(lines[1:])
    return ({'http://': f'http://{proxy}', 'https://': f'https://{proxy}'})

heads = [
    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:76.0) Gecko/20100101 Firefox/76.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/72.0"
    },

    {
        "Content-Type": "application/json",
        'User-Agent': 'Mozilla/5.0 (Windows NT 3.1; rv:76.0) Gecko/20100101 Firefox/69.0'
    },

    {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Debian; Linux x86_64; rv:72.0) Gecko/20100101 Firefox/76.0"
    },

    {
       "Content-Type": "application/json",
       "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
]

def getheaders(token=None):
    headers = random.choice(heads)
    if token:
        headers.update({"Authorization": token})
    return headers

def discserver():
    print(f"""{y}------------------------------------------------------------------------------------------------------------------------\n{w} {b}|{w} https://discord.gg/julianodev {b}|{w} https://github.com/Juliano13kDev {b}|{w} dc : juliano13k {b}|{w} Multi Tools Discord {b}|{w} \n{y}------------------------------------------------------------------------------------------------------------------------\n""")

def astraahometitle():
    print(f"""\n\n                                
   
   ----------------------------------  
     |   ╔═════════════╗        |                     contact me for help : discord juliano13k
     |   ███████████████════╗   |
     |   ██                 ║   |
     |   ██                 ║   |
     |   ██                 ║   |
     |   █████████████      ║   |
     |   ██                 ║   |
     |   ██                 ║   |
     |   ██                 ║   |
     |   ████████████████   ║   |                             
     |   ╚══════════════╝   ║                                  ╔════════════╗
                            ╚══════════════════════════════════  juliano13k 
  ----------------------------------                           ╚════════════╝                                                     
                           
                            \n""".replace('█', f'{b}█{y}'))
    discserver()

def selfbottitle():
    print(f"""\n\n                               ███████╗███████╗██╗     ███████╗    ██████╗  ██████╗ ████████╗
                               ██╔════╝██╔════╝██║     ██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
                               ███████╗█████╗  ██║     █████╗      ██████╔╝██║   ██║   ██║   
                               ╚════██║██╔══╝  ██║     ██╔══╝      ██╔══██╗██║   ██║   ██║   
                               ███████║███████╗███████╗██║         ██████╔╝╚██████╔╝   ██║   
                               ╚══════╝╚══════╝╚══════╝╚═╝         ╚═════╝  ╚═════╝    ╚═╝   \n""".replace('█', f'{b}█{y}'))
    discserver()

def rattitle():
    print(f"""\n\n                    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗     ██████╗  █████╗ ████████╗
                    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝
                    ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║    ██████╔╝███████║   ██║   
                    ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║    ██╔══██╗██╔══██║   ██║   
                    ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝    ██║  ██║██║  ██║   ██║   
                    ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   \n""".replace('█', f'{b}█{y}'))
    discserver()

def raidtitle():
    print(f"""\n\n                              ██████╗  █████╗ ██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     
                              ██╔══██╗██╔══██╗██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
                              ██████╔╝███████║██║██║  ██║       ██║   ██║   ██║██║   ██║██║     
                              ██╔══██╗██╔══██║██║██║  ██║       ██║   ██║   ██║██║   ██║██║     
                              ██║  ██║██║  ██║██║██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
                              ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def filegrabbertitle():
    print(f"""\n\n         ████████╗ ██████╗ ██╗ ███╗███████╗███╗   ██╗     ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
         ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
            ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║    ██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
            ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║    ██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
            ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║    ╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
            ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def imagegrabbertitle():
    print(f"""\n\n                       ██╗███╗   ███╗ █████╗  ██████╗ ███████╗     ██████╗ ██████╗  █████╗ ██████╗ 
                        ██║████╗ ████║██╔══██╗██╔════╝ ██╔════╝    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗
                        ██║██╔████╔██║███████║██║  ███╗█████╗      ██║  ███╗██████╔╝███████║██████╔╝
                        ██║██║╚██╔╝██║██╔══██║██║   ██║██╔══╝      ██║   ██║██╔══██╗██╔══██║██╔══██╗
                        ██║██║ ╚═╝ ██║██║  ██║╚██████╔╝███████╗    ╚██████╔╝██║  ██║██║  ██║██████╔╝
                        ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝     ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ \n""".replace('█', f'{b}█{y}'))
    discserver()

def fakeqrtitle():
    print(f"""\n\n                                   ███████╗ █████╗ ██╗  ██╗███████╗     ██████╗ ██████╗ 
                                   ██╔════╝██╔══██╗██║ ██╔╝██╔════╝    ██╔═══██╗██╔══██╗
                                   █████╗  ███████║█████╔╝ █████╗      ██║   ██║██████╔╝
                                   ██╔══╝  ██╔══██║██╔═██╗ ██╔══╝      ██║{b}▄▄{y} ██║██╔══██╗
                                   ██║     ██║  ██║██║  ██╗███████╗    ╚██████╔╝██║  ██║
                                   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝     ╚══{b}▀▀{y}═╝ ╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def ipgrabbertitle():
    print(f"""\n\n                                      ██╗██████╗      ██████╗ ██████╗  █████╗ ██████╗ 
                                      ██║██╔══██╗    ██╔════╝ ██╔══██╗██╔══██╗██╔══██╗
                                      ██║██████╔╝    ██║  ███╗██████╔╝███████║██████╔╝
                                      ██║██╔═══╝     ██║   ██║██╔══██╗██╔══██║██╔══██╗
                                      ██║██║         ╚██████╔╝██║  ██║██║  ██║██████╔╝
                                      ╚═╝╚═╝          ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ \n""".replace('█', f'{b}█{y}'))
    discserver()

def accountnukertitle():
    print(f"""\n\n                     ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗██████╗  █████╗ ██████╗ ███████╗
                     ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║██╔══██╗██╔══██╗██╔══██╗██╔════╝
                        ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║██████╔╝███████║██████╔╝█████╗  
                        ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║██╔══██╗██╔══██║██╔═══╝ ██╔══╝  
                        ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║██║  ██║██║  ██║██║     ███████╗
                        ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def accountdisablertitle():
    print(f"""\n\n                                ██████╗ ██╗███████╗ █████╗ ██████╗ ██╗     ███████╗██████╗ 
                                ██╔══██╗██║██╔════╝██╔══██╗██╔══██╗██║     ██╔════╝██╔══██╗
                                ██║  ██║██║███████╗███████║██████╔╝██║     █████╗  ██████╔╝
                                ██║  ██║██║╚════██║██╔══██║██╔══██╗██║     ██╔══╝  ██╔══██╗
                                ██████╔╝██║███████║██║  ██║██████╔╝███████╗███████╗██║  ██║
                                ╚═════╝ ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def accountgentitle():
    print(f"""\n\n                        ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗ ██████╗ ███████╗███╗   ██╗
                        ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║██╔════╝ ██╔════╝████╗  ██║
                           ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║██║  ███╗█████╗  ██╔██╗ ██║
                           ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║██║   ██║██╔══╝  ██║╚██╗██║
                           ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║╚██████╔╝███████╗██║ ╚████║
                           ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def settingscyclertitle():
    print(f"""\n\n                                      ██████╗██╗   ██╗ ██████╗██╗     ███████╗██████╗ 
                                     ██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔════╝██╔══██╗
                                     ██║      ╚████╔╝ ██║     ██║     █████╗  ██████╔╝
                                     ██║       ╚██╔╝  ██║     ██║     ██╔══╝  ██╔══██╗
                                     ╚██████╗   ██║   ╚██████╗███████╗███████╗██║  ██║
                                      ╚═════╝   ╚═╝    ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def tokeninfotitle():
    print(f"""\n\n                        ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗██╗███╗   ██╗███████╗ ██████╗ 
                        ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║██║████╗  ██║██╔════╝██╔═══██╗
                           ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║██║██╔██╗ ██║█████╗  ██║   ██║
                           ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║██║██║╚██╗██║██╔══╝  ██║   ██║
                           ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║██║██║ ╚████║██║     ╚██████╔╝
                           ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ \n""".replace('█', f'{b}█{y}'))
    discserver()

def autologintitle():
    print(f"""\n\n                         █████╗ ██╗   ██╗████████╗ ██████╗ ██╗      ██████╗  ██████╗ ██╗███╗   ██╗
                        ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██║     ██╔═══██╗██╔════╝ ██║████╗  ██║
                        ███████║██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║  ███╗██║██╔██╗ ██║
                        ██╔══██║██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║   ██║██║██║╚██╗██║
                        ██║  ██║╚██████╔╝   ██║   ╚██████╔╝███████╗╚██████╔╝╚██████╔╝██║██║ ╚████║
                        ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝╚═╝  ╚═══╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def tokenscheckertitle():
    print(f"""\n\n    ████████╗ ██████╗ ██╗  ██╗███████╗███╗   ██╗███████╗     ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
    ╚══██╔══╝██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║██╔════╝    ██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
       ██║   ██║   ██║█████╔╝ █████╗  ██╔██╗ ██║███████╗    ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
       ██║   ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║╚════██║    ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
       ██║   ╚██████╔╝██║  ██╗███████╗██║ ╚████║███████║    ╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
       ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚══════╝     ╚═════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def cleardmtitle():
    print(f"""\n\n                              ██████╗██╗     ███████╗ █████╗ ██████╗     ██████╗ ███╗   ███╗
                             ██╔════╝██║     ██╔════╝██╔══██╗██╔══██╗    ██╔══██╗████╗ ████║
                             ██║     ██║     █████╗  ███████║██████╔╝    ██║  ██║██╔████╔██║
                             ██║     ██║     ██╔══╝  ██╔══██║██╔══██╗    ██║  ██║██║╚██╔╝██║
                             ╚██████╗███████╗███████╗██║  ██║██║  ██║    ██████╔╝██║ ╚═╝ ██║
                              ╚═════╝╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚═╝     ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def housechangertitle():
    print(f"""\n\n                         ██╗  ██╗██╗   ██╗██████╗ ███████╗███████╗ ██████╗ ██╗   ██╗ █████╗ ██████╗ 
                         ██║  ██║╚██╗ ██╔╝██╔══██╗██╔════╝██╔════╝██╔═══██╗██║   ██║██╔══██╗██╔══██╗
                         ███████║ ╚████╔╝ ██████╔╝█████╗  ███████╗██║   ██║██║   ██║███████║██║  ██║
                         ██╔══██║  ╚██╔╝  ██╔═══╝ ██╔══╝  ╚════██║██║▄▄ ██║██║   ██║██╔══██║██║  ██║
                         ██║  ██║   ██║   ██║     ███████╗███████║╚██████╔╝╚██████╔╝██║  ██║██████╔╝
                         ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚══════╝╚══════╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def serverlookuptitle():
    print(f"""\n\n        ███████╗███████╗██████╗ ██╗   ██╗███████╗██████╗     ██╗      ██████╗  ██████╗ ██╗  ██╗██╗   ██╗██████╗ 
        ██╔════╝██╔════╝██╔══██╗██║   ██║██╔════╝██╔══██╗    ██║     ██╔═══██╗██╔═══██╗██║ ██╔╝██║   ██║██╔══██╗
        ███████╗█████╗  ██████╔╝██║   ██║█████╗  ██████╔╝    ██║     ██║   ██║██║   ██║█████╔╝ ██║   ██║██████╔╝
        ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██║     ██║   ██║██║   ██║██╔═██╗ ██║   ██║██╔═══╝ 
        ███████║███████╗██║  ██║ ╚████╔╝ ███████╗██║  ██║    ███████╗╚██████╔╝╚██████╔╝██║  ██╗╚██████╔╝██║     
        ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def massdmtitle():
    print(f"""\n\n                                 ███╗   ███╗ █████╗ ███████╗███████╗    ██████╗ ███╗   ███╗
                                 ████╗ ████║██╔══██╗██╔════╝██╔════╝    ██╔══██╗████╗ ████║
                                 ██╔████╔██║███████║███████╗███████╗    ██║  ██║██╔████╔██║
                                 ██║╚██╔╝██║██╔══██║╚════██║╚════██║    ██║  ██║██║╚██╔╝██║
                                 ██║ ╚═╝ ██║██║  ██║███████║███████║    ██████╔╝██║ ╚═╝ ██║
                                 ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝    ╚═════╝ ╚═╝     ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def groupspamtitle():
    print(f"""\n\n       ██████╗ ██████╗  ██████╗ ██╗   ██╗██████╗     ███████╗██████╗  █████╗ ███╗   ███╗███╗   ███╗███████╗██████╗ 
      ██╔════╝ ██╔══██╗██╔═══██╗██║   ██║██╔══██╗    ██╔════╝██╔══██╗██╔══██╗████╗ ████║████╗ ████║██╔════╝██╔══██╗
      ██║  ███╗██████╔╝██║   ██║██║   ██║██████╔╝    ███████╗██████╔╝███████║██╔████╔██║██╔████╔██║█████╗  ██████╔╝
      ██║   ██║██╔══██╗██║   ██║██║   ██║██╔═══╝     ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║██║╚██╔╝██║██╔══╝  ██╔══██╗
      ╚██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║         ███████║██║     ██║  ██║██║ ╚═╝ ██║██║ ╚═╝ ██║███████╗██║  ██║
       ╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝         ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def nitrogentitle():
    print(f"""\n\n                           ███╗   ██╗██╗████████╗██████╗  ██████╗  ██████╗ ███████╗███╗   ██╗
                           ████╗  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝ ██╔════╝████╗  ██║
                           ██╔██╗ ██║██║   ██║   ██████╔╝██║   ██║██║  ███╗█████╗  ██╔██╗ ██║
                           ██║╚██╗██║██║   ██║   ██╔══██╗██║   ██║██║   ██║██╔══╝  ██║╚██╗██║
                           ██║ ╚████║██║   ██║   ██║  ██║╚██████╔╝╚██████╔╝███████╗██║ ╚████║
                           ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def nitrosnipertitle():
    print(f"""\n\n                 ███╗   ██╗██╗████████╗██████╗  ██████╗     ███████╗███╗   ██╗██╗██████╗ ███████╗██████╗ 
                 ████╗  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗    ██╔════╝████╗  ██║██║██╔══██╗██╔════╝██╔══██╗
                 ██╔██╗ ██║██║   ██║   ██████╔╝██║   ██║    ███████╗██╔██╗ ██║██║██████╔╝█████╗  ██████╔╝
                 ██║╚██╗██║██║   ██║   ██╔══██╗██║   ██║    ╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝  ██╔══██╗
                 ██║ ╚████║██║   ██║   ██║  ██║╚██████╔╝    ███████║██║ ╚████║██║██║     ███████╗██║  ██║
                 ╚═╝  ╚═══╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝     ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def webhspamtitle():
    print(f"""\n\n            ██╗    ██╗███████╗██████╗ ██╗  ██╗ ██████╗  ██████╗ ██╗  ██╗    ███████╗██████╗  █████╗ ███╗   ███╗
            ██║    ██║██╔════╝██╔══██╗██║  ██║██╔═══██╗██╔═══██╗██║ ██╔╝    ██╔════╝██╔══██╗██╔══██╗████╗ ████║
            ██║ █╗ ██║█████╗  ██████╔╝███████║██║   ██║██║   ██║█████╔╝     ███████╗██████╔╝███████║██╔████╔██║
            ██║███╗██║██╔══╝  ██╔══██╗██╔══██║██║   ██║██║   ██║██╔═██╗     ╚════██║██╔═══╝ ██╔══██║██║╚██╔╝██║
            ╚███╔███╔╝███████╗██████╔╝██║  ██║╚██████╔╝╚██████╔╝██║  ██╗    ███████║██║     ██║  ██║██║ ╚═╝ ██║
             ╚══╝╚══╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝     ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

def webhremovertitle():
    print(f"""\n\n                               ██████╗ ███████╗███╗   ███╗ ██████╗ ██╗   ██╗███████╗██████╗ 
                               ██╔══██╗██╔════╝████╗ ████║██╔═══██╗██║   ██║██╔════╝██╔══██╗
                               ██████╔╝█████╗  ██╔████╔██║██║   ██║██║   ██║█████╗  ██████╔╝
                               ██╔══██╗██╔══╝  ██║╚██╔╝██║██║   ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗
                               ██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝ ╚████╔╝ ███████╗██║  ██║
                               ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝\n""".replace('█', f'{b}█{y}'))
    discserver()

banner = r"""
      ████████████████████████████████████████
      ████████████▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█████████
      █████▀▀░░░░░░░░░░░░░░░░░░░░░░░░░▀███████
      ████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░██████
      ███▀░░░░░▄▄▄░░░░░░░░▄▄▀███▄▄░░░░░░░█████
      ██░░░░░░▀▀▀███▄▄░░░█▄▄█▀█▀▀▀▀░▀░▄▄░▀▀███
      █░░▄▄░▄▄░▄░░░█▀░░░░░░░░░░▀▄▄▄█▀▀▄░▀█░░▀█
      █░░░░▄░▀▀░░▄█▀░░░░░░▄▄░░░░░░░▄▄▀██▄░█░░█
      ██░░░██░░░▀▀█▄░░░▀▀▀▄▀░▄▄▄███▀░▄█░░░▀░▄█
      ██▄░██▀█▀▄▄▄▄▄█▄▄▄▄▄▀▀█▀░░▄███▀█▀░░░▄▄██
      ███░████▄█▄░░█░░▄█░░▄▄███▀▀▀█▄▀░░░░▄████
      ███░▀██████████████▀▀▀▀█░░░▄▀▀░░░░▄█████
      ███░░██▀█▀██▀█▀░░▀█░░░░█▄█▀░░░░░▄███████
      ███░░░░▀▀▀██▄██▄▄██▀▀▀▀▀░░░░░▄▄█████████
      ██▀░░░░░░░░░░░░░░░░░░░░░░▄▄▄████████████
      ██▄░░░░░░░░░░░░░░░░░░▄▄█████████████████
      ████▄░░░░░░░░░▄▄▄▄▄█████████████████████
      ████████████████████████████████████████                 ╔════════════╗
                            ╚══════════════════════════════════  JULIANO13K 
                                                               ╚════════════╝
"""[1:]
