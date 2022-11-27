import re
import netaddr
from bisect import bisect
import pandas as pd
ip2location = pd.read_csv("ip2location.csv")
def lookup_region(ipaddr):
    ip = re.sub(r"[a-zA-Z]","0", ipaddr)
    num = int(netaddr.IPAddress(ip))
    idx = bisect(ip2location.low, num)
    return ip2location.iloc[idx-1].region

class Filing:
    def __init__(self, html):
        dates = re.findall(r"19\d{2}-\d{2}-\d{2}|20\d{2}-\d{2}-\d{2}", html)
        self.dates = dates
        
        s = re.findall(r"SIC=(\d+)", html)
        if s != []:
            sic = int(s[0])
        else:
            sic = None
        self.sic = sic
        addresses = []
        for addr_html in re.findall(r'<div class="mailer">[\s\S]+?</div>', html):
            lines = []
            mailerAddress = re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html)
            if mailerAddress != []:
                for line in mailerAddress:
                    lines.append(line.strip())
                addresses.append("\n".join(lines))
            else:
                continue
        self.addresses = addresses
        
        
    def state(self):
        global i
        for address in self.addresses:
            ab = re.findall(r'([A-Z]{2}) \d{5}', address)
            if ab != []:
                return ab[0]
            else:
                continue
        return None
