import urllib
import pickle
from xml.dom import minidom
from article import Article

from vectorizer import Vectorizer

SHARE_WEIGHT = 0.75
COMMENT_WEIGHT = 0.15
LIKE_WEIGHT = 0.10

FACEBOOK_SHARE_API = "http://api.facebook.com/restserver.php?method=links.getStats&urls="
PICKELED_RECENT_ARTICLES = 'data/collected_articles.dat'


def calculateScore(url_list):
	final_score = 0;
	for url in url_list:
		read_web_content = urllib.urlopen(FACEBOOK_SHARE_API+url).read()

		xmldoc = minidom.parseString(read_web_content)

		share_count_item = xmldoc.getElementsByTagName('share_count') 
		like_count_item = xmldoc.getElementsByTagName('like_count') 
		comment_count_item = xmldoc.getElementsByTagName('comment_count') 

		share_count = share_count_item[0].firstChild.nodeValue
		like_count = like_count_item[0].firstChild.nodeValue
		comment_count = comment_count_item[0].firstChild.nodeValue

		final_score += SHARE_WEIGHT * float(share_count) + \
		              LIKE_WEIGHT * float(like_count) + \
		              COMMENT_WEIGHT * float(comment_count)

	return final_score


def findTrending():
	recent_articles_list = pickle.load(open(PICKELED_RECENT_ARTICLES, 'r'))

	#Add all articles into a dictionary with score as the value
	article_score_dict = {}
	article_counter = 0
	for article in recent_articles_list:
		score = calculateScore([article.link])
		article_score_dict[article] = score
		article_counter += 1
		if article_counter % 100 == 0:
		 	print "Calculated score for article ", article_counter
		if article_counter == 10:
			break

	relevance_sorted_articles = sorted(article_score_dict.items(), key= lambda x:x[1])

	sorted_article_list = []
	for article, score in relevance_sorted_articles:
		print article.link
		print article.description
		print article.title ,":",score
		print '\n\n\n'
		sorted_article_list.append(article)
	return sorted_article_list

#trending_articles = findTrending()

vectorizer = Vectorizer()
#vectorized_trending_articles = vectorizer.vectorize(trending_articles)

article1 = Article(1, "Hello", "www.hello.com", 0,"Hello hello world")
article5 = Article(5, "Nah", "www.hello.com", 0,"Nah dont want it")
article11 = Article(11, "World", "www.hello.com", 0,"World is big and I say hello to it")

vectorized_trending_articles = vectorizer.vectorize([article1, article5, article11])

print vectorized_trending_articles




