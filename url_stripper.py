import sys
import pickle

PICKELED_RSS_URLS = 'rss_urls/pickled_rss_urls.dat'

# #Read stored URLs
# for line in stored_urls_file:
# 	current_rss_url_list.append(line)


def read_file(added_file):
	global PICKELED_RSS_URLS
	current_rss_url_list = pickle.load(open(PICKELED_RSS_URLS, 'r'))
	for line in added_file:
		try:
			http_index = line.index('http')
			new_line = line[http_index:]
			space_index = 0
			tab_index = 0
			
			
			if '\t' in new_line:
				tab_index = new_line.index('\t')	

			if ' ' in new_line:
				space_index = new_line.index(' ')

			whitespace_index = min(tab_index, space_index)	
			
			if whitespace_index > 0:
				pure_url = new_line[:whitespace_index] 
			else:
				pure_url = new_line

			if pure_url:
				print pure_url
				current_rss_url_list.add(pure_url)
		except ValueError: #in case the line is not a URL
			pass

	pickle.dump(current_rss_url_list, open(PICKELED_RSS_URLS, 'w'))

def remove_url(removed_url):
	global PICKELED_RSS_URLS
	current_rss_url_list = pickle.load(open(PICKELED_RSS_URLS, 'r'))
	new_rss_url_list = []
	for item in current_rss_url_list:
		if item != removed_url:
			new_rss_url_list.append(item)
	print "Size of list before filtering is ", len(current_rss_url_list)
	print "Size of list after filtering is ", len(new_rss_url_list)
	pickle.dump(new_rss_url_list, open(PICKELED_RSS_URLS, 'w'))



if sys.argv[1] == '--remove-url':
	remove_url(sys.argv[2])
elif sys.argv[1] == '--add-url':
	add_url(sys.argv[2])
else:
	rss_file = open(sys.argv[1], 'r')
	read_file(rss_file)

