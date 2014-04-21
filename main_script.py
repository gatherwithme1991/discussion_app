import feedparser
import pickle
import datetime




PICKELED_RSS_URLS = 'rss_urls/pickled_rss_urls.dat'

class Article:

	def __init__(self, title, link, pubDate):
		self.title = title
		self.link = link
		self.pubDate = pubDate

def parseDate(dateString):
	comma_index = dateString.index(',')
	pure_date = dateString[comma_index+1:16]
	pure_date = pure_date.strip() 
	return datetime.datetime.strptime(pure_date, '%d %b %Y')

current_rss_url_list = pickle.load(open(PICKELED_RSS_URLS, 'r'))

all_articles = []
for feed_url in current_rss_url_list:
	parsed_feed = feedparser.parse(feed_url)	
	for story in parsed_feed['entries']:
		# print story.title
		# print story.link
		try:
			# print parseDate(story.published)
			# print '\n'
			new_article = Article(story.title, story.link, parseDate(story.published))
			all_articles.append(new_article)
		except ValueError:
			print 'Couldnt parse date'
		
all_articles = sorted(all_articles, key=lambda article: article.pubDate)

for article in all_articles:
	print article.title
	print article.pubDate




