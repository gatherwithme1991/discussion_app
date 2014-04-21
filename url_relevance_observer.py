import urllib
from xml.dom import minidom

SHARE_WEIGHT = 0.75
COMMENT_WEIGHT = 0.15
LIKE_WEIGHT = 0.10

FACEBOOK_SHARE_API = "http://api.facebook.com/restserver.php?method=links.getStats&urls="

urls = ['http://www.cnn.com/2014/04/18/opinion/bell-planet-discovery/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_topstories+%28RSS%3A+Top+Stories%29']

def calculateScore(url_list):
	final_score = 0;
	for checked_url in url_list:
		read_web_content = urllib.urlopen(FACEBOOK_SHARE_API+checked_url).read()

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

	print "FINAL SCORE", final_score

calculateScore(urls)


