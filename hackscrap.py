from bs4 import BeautifulSoup
import requests
import pprint

def scrape_hacker_news(url):
	res = requests.get(url)
	soup = BeautifulSoup(res.text, 'html.parser')
	links = soup.select('.titleline')
	subtext = soup.select('.subtext')

	def sort_stories_by_votes(hnlist):
		return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

	def custom_news(links, subtext):
		hn = []
		for idx, item in enumerate(links):

			title = item.getText()
			href = item.find('a')['href'] if item.find('a') else None
			vote = subtext[idx].select('.score')
			if len(vote):
				points = int(vote[0].getText().replace(' points', ''))
				if points > 99:
					hn.append({'title': title, 'link': href, 'votes': points})
		return sort_stories_by_votes(hn)

	return custom_news(links, subtext)


urls = [
    "https://news.ycombinator.com/",
    "https://news.ycombinator.com/news?p=2"
]

for url in urls:
	scraped_data = scrape_hacker_news(url)
	pprint.pprint(scraped_data)