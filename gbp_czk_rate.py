# -*- coding: utf-8 -*-
"""
Displays GBP to CZK exchange rate.

The exchange rate data comes from https://finance.idnes.cz/kurzovni-listek.aspx?typ=banky&mena=GBP 

Configuration parameters:
    cache_timeout: Refresh rate in seconds (default 600)
    format: Output format  

@author Atrament
@license BSD

SAMPLE OUTPUT
{'full_text': u'$1.061 \xa30.884 \xa5121.538'}
"""
from lxml import html
import requests
from requests.exceptions import HTTPError


class Py3status:
    cache_timeout = 600
    format = u'${USD} £{GBP} ¥{JPY}'

    def post_config_hook(self):
        self.request_timeout = 20

    def rates(self):
        try:
            page = requests.get('https://finance.idnes.cz/kurzovni-listek.aspx?typ=banky&mena=GBP')
            tree = html.fromstring(page.content)
            rate = tree.xpath('//th[@class="tar"]/text()')[0].replace(",",".")
            return {
                'full_text': "CZK: " + rate, 
                'cached_until': self.py3.time_in(self.cache_timeout),
            }

        except:
            return {
                    'full_text': "Http request error",
                    'cached_until': self.py3.time_in(10)
            }

        
if __name__ == "__main__":
    """
    Run module in test mode.
    """
    from py3status.module_test import module_test

    module_test(Py3status)
