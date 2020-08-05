# news_finder
Python3 rss news crawler

Change the config section in the main.py to setup your own directory or the code will fail  

News Crawler

This library can collect live stream feed rss from a given url/s source. 
It will collect the most recent news feed published from the sources with the use of ‘feedparser’ and ‘newspaper’.
We will manage the data with ‘pandas’ and store the output in a csv file ready for further investigation. 
The csv file will be stored in a directory choose by the user and the name of the file will contain the date and the time when the csv was dumped.

Feed

A feed is usually a xml file structure or similar and contain a list of all recent news published. It depends from the source how many news you will get on each request

Etag

The etag act as unique feed identifier, to not overload the source with requests we only get the feed if the has changed and update the etag records of the source with the news tag released. When we add the etag in the request the server will automatically return the feed if is present otherwise it will return a debug error, this won’t stop the code but the source will be skipped.

Not all the website has an etag system in place therefore special care need to be taken when changing the frequency of the whole process to not overwhelming the source server.

Csv input file variables:

1-	web_site (this is the source url this need to be a rss endpoint others format are not supported yet) 

Csv file output variables

1-	crw_news_date (the date when the code processed the news entry)
2-	published (the date when the news was published)
3-	title (the title of the news)
4-	text (the text of the news)
5-	url_news  (the original news url) 
6-	web_site (the main source web site)
7-	id_news (unique news identifier this is a hash made from string containg url+title+text)
8-	crawling_news_feed (this will be omitted in the single output csv and this entry will be the name of the file) 

Process

1-	request feed with feedparser library 
2-	extract metadata, etag and the orginal news source url (url_news)
3-	load etag for each data source in the input csv file 
4-	request the news with newspaper and parsing
5-	data export
6-	repeat the process number 1 but we add the etag in the request

Duplicates

Even with the etag in place we can get duplicate, the source server will change the etag if 1 news within all the feed is updated.


Lib (Python 3)
pip install pandas 
pip install feedparser
pip install newspaper3k
