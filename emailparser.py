from bs4 import BeautifulSoup
import requests
import requests.exceptions
from urllib.parse import urlsplit
from collections import deque
import re
import sys


class Crawler():
   def __init__(self):
      self.emails = set()
   def search(self,url,maxpages):
      new_urls = deque([url])
      processed_urls = set()
      i = 0
      while len(new_urls) and i <= maxpages:
         i+=1
         url = new_urls.popleft()
         processed_urls.add(url)
         parts = urlsplit(url)
         base_url = "{0.scheme}://{0.netloc}".format(parts)
         path = url[:url.rfind('/')+1] if '/' in parts.path else url
         print("Processing %s" % url) 
         try:
            response = requests.get(url)
         except:
            continue
         new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
         self.emails.update(new_emails)
         try: 
            soup = BeautifulSoup(response.text)
            for anchor in soup.find_all("a"):
               link = anchor.attrs["href"] if "href" in anchor.attrs else ''
               # resolve relative links
               if link.startswith('/'):
                  link = base_url + link
               elif not link.startswith('http'):
                  link = path + link
               if not link in new_urls and not link in processed_urls:
                  new_urls.append(link)
         except:
            pass

if len(sys.argv) < 4:
   print("Usage: emailparser.py http://foo.bar/crawlme max_pages output_file")
   sys.exit(1)

try:
   f = open(sys.argv[3],"a")
except:
   print ("Path does not exists or not allowed.")
   while 1:
      try:
         f = open(input("Enter new output file path: "))
         break
      except:
         pass

crawler = Crawler()
crawler.search(sys.argv[1],int(sys.argv[2]))
print ("Found: %s email(s)." % len(crawler.emails))
for i in crawler.emails:
   f.write(i+"\n")
f.close()
