import feedparser
import pickle
import datetime

from article import Article


def parseDate(dateString):
	comma_index = dateString.index(',')
	pure_date = dateString[comma_index+1:16]
	pure_date = pure_date.strip() 
	return datetime.datetime.strptime(pure_date, '%d %b %Y')

def parseDescription(rawDescription):

	try:
		if '<' in rawDescription:
			return rawDescription[:rawDescription.index('<')]
		else:
			return rawDescription 
	except ValueError:
		print 'Couldn parse description:'
		print rawDescription



def collect_articles():
	PICKELED_RSS_URLS = 'rss_urls/pickled_rss_urls.dat'
	PICKELED_RECENT_ARTICLES = 'data/collected_articles.dat'
	current_rss_url_list = pickle.load(open(PICKELED_RSS_URLS, 'r'))
	all_articles = []
	article_id = 0
	for feed_url in current_rss_url_list:
		parsed_feed = feedparser.parse(feed_url)	
		for story in parsed_feed['entries']:
			try:
				new_article = Article(article_id, story.title, story.link, parseDate(story.published), parseDescription(story.description) )
				all_articles.append(new_article)
			except ValueError:
				print 'Couldnt parse date'
				
	all_articles = sorted(all_articles, key=lambda article: article.pubDate)

	three_days_ago = datetime.datetime.today() - datetime.timedelta(days = 3)
	recent_articles = filter(lambda article: article.pubDate > three_days_ago, all_articles)

	recent_articles_list = []
	article_counter = 0
	for article in recent_articles:
		print article.title
		print article.pubDate
		print article.description + '\n'
		recent_articles_list.append(article)
		article_counter += 1

	print 'Number of recent articles is ', article_counter
	pickle.dump(recent_articles_list, open(PICKELED_RECENT_ARTICLES, 'w'))

collect_articles()




