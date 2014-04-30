import feedparser
import pickle
import datetime
import sentenceComparator as sC
import Vectorizer as vec



PICKELED_RSS_URLS = 'rss_urls/pickled_rss_urls.dat'

class Article:

	def __init__(self, idno, title, desc, link, pubDate):
         self.title = title
         self.description = desc
         self.Id = idno
         self.link = link
         self.pubDate = pubDate

def parseDate(dateString):
	comma_index = dateString.index(',')
	pure_date = dateString[comma_index+1:16]
	pure_date = pure_date.strip() 
	return datetime.datetime.strptime(pure_date, '%d %b %Y')


current_rss_url_list = pickle.load(open(PICKELED_RSS_URLS, 'r'))

print 'loading articles...'
all_articles = []
cnt = 0
for feed_url in current_rss_url_list:
	parsed_feed = feedparser.parse(feed_url)	
	for story in parsed_feed['entries']:
		# print story.title
		# print story.link
		try:
                  new_article = Article(cnt,story.title, story.description, story.link, parseDate(story.published))
                  all_articles.append(new_article)
                  cnt += 1 
		except ValueError:
			print 'Couldnt parse date'
		
print 'sorting articles...'
all_articles = sorted(all_articles, key=lambda article: article.pubDate)

"""
print 'finding keywords...'
sC.init(1,10,[(a.title, a.link) for a in all_articles if a.pubDate>=(datetime.datetime.now() - datetime.timedelta(days=1))])
"""

vec.calculateSimilarities([a for a in all_articles if a.pubDate>=(datetime.datetime.now() - datetime.timedelta(days=1))])

#for article in all_articles:
#	print article.title




