from sklearn.cluster import KMeans

class KMeansClusterer:

	def __init__(self):
		pass

	def calculateKMeans(self, termDocumentMatrix, k):
		clusterer = KMeans(n_clusters=k)
		print "Num clusters: ", k
		fit_predict = clusterer.fit_predict(termDocumentMatrix)
		print clusterer.fit_predict(termDocumentMatrix)
		print "Inertia: ", clusterer.inertia_
		print '\n'
		return fit_predict


	







