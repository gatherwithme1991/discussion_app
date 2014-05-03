import urllib
import pickle
from xml.dom import minidom
from article import Article

from vectorizer import Vectorizer
from kmeans import KMeansClusterer

SHARE_WEIGHT = 0.75
COMMENT_WEIGHT = 0.15
LIKE_WEIGHT = 0.10

FACEBOOK_SHARE_API = "http://api.facebook.com/restserver.php?method=links.getStats&urls="
PICKELED_RECENT_ARTICLES_ALL_TOPICS = 'data/collected_articles.dat'


def setArticleVectors(article_list, article_matrix):
	article_num = 0
	for current_article in article_list:
		current_article.vector = article_matrix[article_num]
		article_num += 1


def groupTrendingArticlesByTopic(trending_articles):
	grouping = {}
	num_groups = 0


	# for i in range(0,len(trending_articles)):
	# 	if clustering[i] not in grouping:
	# 		grouping[clustering[i]] = [] 
		
	# 	grouping[clustering[i]].append(trending_articles[i])

	# return grouping

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


def findTrending(category_file):
	recent_articles_list = pickle.load(open(category_file, 'r'))

	#Add all articles into a dictionary with score as the value
	article_score_dict = {}
	article_counter = 0
	for article in recent_articles_list:
		score = calculateScore([article.link])
		article_score_dict[article] = score
		article.score = score
		article_counter += 1
		if article_counter % 100 == 0:
		 	print "Calculated score for article ", article_counter

		# if article_counter == 2:
		# 	break

	relevance_sorted_articles = sorted(article_score_dict.items(), key= lambda x:x[1])

	sorted_article_list = []
	for article, score in relevance_sorted_articles:
		print "Id: ", article.id_num
		print "Link: ", article.link
		print "Description: ", article.description
		print article.title ,":",score
		print '\n\n\n'
		sorted_article_list.append(article)
	return sorted_article_list



#==================FINDING TRENDING ARTICLES=================
trending_articles = findTrending(PICKELED_RECENT_ARTICLES_ALL_TOPICS)

vectorizer = Vectorizer()
vectorized_trending_articles = vectorizer.vectorize(trending_articles)

setArticleVectors(trending_articles, vectorized_trending_articles)

# for article in trending_articles:
# 	print article.description, article.vector

dimensions = str(len(vectorized_trending_articles)) + " x " + str(len(vectorized_trending_articles[0]))
print "Term document matrix with" +  dimensions + ": \n", vectorized_trending_articles

#==================KMEANS STARTS HERE=======================
# print "Calculating kmeans..."

# kmeans_calculator = KMeansClusterer()

# predicted_clustering = kmeans_calculator.calculateKMeans(vectorized_trending_articles, 30)


# calculated_grouping = groupTrendingArticlesByTopic(predicted_clustering, trending_articles)

# sorted_calculated_grouping = sorted(calculated_grouping.items(), key= lambda x:sum(art.score for art in x[1]))

# print sorted_calculated_grouping

# for grouping_num, article_collection in sorted_calculated_grouping:
# 	print "Grouping " + str(grouping_num)
# 	for current_article in article_collection:
# 		print "Link: ", current_article.link
# 		print "Description: ", current_article.description
# 		print current_article.title ,":", current_article.score
# 		print '\n\n\n'	  
##==================KMEANS ENDS HERE==========================




