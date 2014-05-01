

import Vectorizer

def consolidateArticles(articles):
	article_term_matrix = Vectorize(articles)
	calculateKMeans(article_term_matrix)
