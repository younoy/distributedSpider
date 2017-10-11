from scrapy.cmdline import execute
import os
import sys

base_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_path)
execute(['scrapy','crawl','douban'])