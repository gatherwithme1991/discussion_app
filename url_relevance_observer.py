import urllib

SHARE_WEIGHT = 0.75
COMMENTS_WEIGHT = 0.15
LIKE_WEIGHT = 0.10

checked_url = "http://api.facebook.com/restserver.php?method=links.getStats&urls=http://www.cnn.com/2014/04/18/opinion/bell-planet-discovery/index.html?utm_source=feedburner&utm_medium=feed&utm_campaign=Feed%3A+rss%2Fcnn_topstories+%28RSS%3A+Top+Stories%29"


read_web_content = urllib.urlopen(checked_url).read()

print read_web_content


