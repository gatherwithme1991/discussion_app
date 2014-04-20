import sys
import pickle

PICKELED_RSS_URLS = 'rss_urls/pickled_rss_urls.dat'


rss_file = open(sys.argv[1], 'r')


# #Read stored URLs
# for line in stored_urls_file:
# 	current_rss_url_list.append(line)



current_rss_url_list = pickle.load(open(PICKELED_RSS_URLS, 'r'))
for line in rss_file:
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
