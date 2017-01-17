import re
import urllib

from BeautifulSoup import BeautifulSoup

wiki_url = 'https://en.wikipedia.org/wiki/Game_of_Thrones'
wiki_html = urllib.urlopen(wiki_url).read()
wiki_content = BeautifulSoup(wiki_html)

seasons_table = wiki_content.find('table', attrs={'class': 'wikitable'})
seasons = seasons_table.findAll('a', attrs={'href': re.compile('\/wiki\/Game_of_Thrones_\(season_?[0-9]+\)')})

views = 0

for season in seasons:
    season_url = 'https://en.wikipedia.org' + season['href']
    season_html = urllib.urlopen(season_url).read()
    season_content = BeautifulSoup(season_html)

    episodes_table = season_content.find('table', attrs={'class': 'wikitable plainrowheaders wikiepisodetable'})

    if episodes_table:
        episode_rows = episodes_table.findAll('tr', attrs={'class': 'vevent'})

        if episode_rows:
            for episode_row in episode_rows:
                episode_views = episode_row.findAll('td')[-1]

                views += float(re.sub(r'\[?[0-9]+\]', '', episode_views.text))

print str(views) + ' millions'
