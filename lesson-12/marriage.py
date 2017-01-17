import urllib

from BeautifulSoup import BeautifulSoup


topic_url = 'http://quotes.yourdictionary.com/theme/marriage/'
topic_html = urllib.urlopen(topic_url).read()
topic_soup = BeautifulSoup(topic_html)

quotes = topic_soup.findAll('p', attrs={'class': 'quoteContent'})

for quote in quotes:
    print quote.text