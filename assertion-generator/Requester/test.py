a = 'https://github.com/txthinking/brook/issues/102'
import requests
from lxml import etree
issue_response = requests.get(a, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/51.0.2704.63 Safari/537.36'})
issue_tree = etree.HTML(issue_response.content)
issue_name = issue_tree.xpath('//*[@id="partial-discussion-header"]/div[1]/div/h1/span[1]/text()')[0]
print()