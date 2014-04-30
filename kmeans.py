from sklearn.cluster import KMeans


def calculateKMeans(termDocumentMatrix):
	for k in range(1, min(30, len(termDocumentMatrix))):
		clusterer = KMeans(n_clusters=k)
		print "Num clusters: ", k
		print clusterer.fit_predict(termDocumentMatrix)
		print "Inertia: ", clusterer.inertia_
		print '\n'

points = [ [13,12], [1,2], [1,1], [0,1], [12,12], [10,12]]


print calculateKMeans(points)


	







