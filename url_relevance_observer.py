import urllib
import pickle
from xml.dom import minidom
from article import Article

SHARE_WEIGHT = 0.75
COMMENT_WEIGHT = 0.15
LIKE_WEIGHT = 0.10

FACEBOOK_SHARE_API = "http://api.facebook.com/restserver.php?method=links.getStats&urls="
PICKELED_RECENT_ARTICLES = 'data/collected_articles.dat'

#urls = ['http://www.cnn.com/2014/04/18/opinion/bell-planet-discovery/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_topstories+%28RSS%3A+Top+Stories%29']



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

relevance_sorted_articles = sorted(article_score_dict.items(), key= lambda x:x[1])

for article, score in relevance_sorted_articles:
	print article.title ,":",score







