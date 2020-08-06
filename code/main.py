#Lib
import feedparser
#from pprint import pprint
import pandas as pd
import time
from newspaper import Article #pip3 install newspaper3k
from datetime import datetime
import hashlib

##### CONFIG #####
#pause_value in minutes 
minutes_pause= 180 # CHANGE HERE 
pause_value= 60*minutes_pause
path_csv_input= '/home/user/news_finder/input/source_feed_input.csv' # CHANGE HERE path where the csv input file is stored
path_directory_output= '/home/user/news-finder/output/' # CHANGE HERE path where you want to store the csv file
##################


#functions 
def Hash_news(url,title,text):
    
    # This functions is used to generate the hash 

    s= url+title+text
    my_hash= hashlib.sha256(s.encode('utf-8')).hexdigest()
    return my_hash


def all_feed(feed):
    
    # extract url news and metadata

    feed_response=feed
    feed= feed.entries
    
    print('Found ',len(feed),' feeds in response')
    my_dict={'web_site':[],'url_news':[],'published':[]}
    for f in feed: 
        
        #print(f.link)
        #print(f.published)
        my_dict['web_site'].append(feed_response.href)
        my_dict['url_news'].append(f.link)
        my_dict['published'].append(f.published)
    
    #pprint(my_dict)
    return(my_dict)

def check_feed(feed):

    # check response 
    
    if 'debug_message' in feed: 
        print(feed.debug_message)
        return(0)
    else:
        
        my_dict=all_feed(feed)
        #print(len(my_dict['url_news']))
        return(my_dict)

    

def feed_request(url,tag):
    
    # request a feed from website with etag
    
    if len(tag)==0:
    
        feed= feedparser.parse(url)
        try:
            tag= feed.etag
        except:
            tag=''
    else:   
        
        feed= feedparser.parse(url, etag=tag)
        
    stat= feed.status
    
    
    
    return(stat,tag,feed)


def parser_article(url):
    
    # get data from news
    
    try: 
        article = Article(url)
        article.download()
        article.parse()
        text=article.text
        title=article.title
        text=text.replace('\n',' ')
    except:
        text= None
        title= None
    return text,title


""" Begin code excution """

#load csv with news websites 
dfs = pd.read_csv(path_csv_input)[['web_site']]
dfs.head(5)

#create dict for tag 

my_d={}
for x in dfs['web_site']:
    
    my_d[x]=''
    

#start request loop to all url news and updating tag where possible, this run every 3 hour  
while True : 
    now = datetime.now()
    link_news=[]
    text=[]
    title=[]
    published=[]
    web_site=[]    
    crw_news=[]
    
    for url,tag in my_d.items():

        count_parsed=1        
        print('\n\n',url,'\n')
        #print(tag)
        feed_news=feed_request(url,tag)
        feed=feed_news[2]
        my_d[url]=feed_news[1] #tag
        check = check_feed(feed)

        if check == 0 :

            print('No Update')
            
        else:
            for url_news in zip(check['url_news'],check['published'],check['web_site']): 

                print("\r TOTAL EXTRACTED URL: {}".format(str(count_parsed)),end="")
                art=parser_article(url_news[0])
                text.append(art[0])
                title.append(art[1])
                published.append(url_news[1])
                link_news.append(url_news[0])
                web_site.append(url_news[2])
                crw_news.append(datetime.now())
                count_parsed+=1
              
    df=pd.DataFrame.from_dict({'crw_news_date':crw_news,
                            'published':published,
                             'title':title,
                             'text':text,
                             'url_news':link_news,
                             'web_site':web_site})
    
    # hash id 
    df['id_news']= [ Hash_news(str(url),str(title),str(text)) for url,title,text in zip(df['url_news'],df['title'],df['text'])]
    df['crawling_date_feed']= [ now for x in df['id_news']]
    
    
    path_file= path_directory_output+'news_raw_output_'+str(now).replace(':','')+'.csv'
    df.to_csv(path_file,index=False)
   
    print(df.head(5))
    print('Pausing for ',minutes_pause,' min')
    print(len(df), ' feed found')
    time.sleep(pause_value)
