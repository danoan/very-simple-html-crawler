from html.parser import HTMLParser
import urllib.request
import urllib.parse

def escape(text):
  return urllib.parse.quote(text)

def get(link):
  headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
             'Accept-Encoding': 'identity',
             'Cache-Control': 'no-cache',
             'Connection': 'keep-alive',
             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
              }

  request = urllib.request.Request(link, headers=headers)
  charset = "utf-8"
  with urllib.request.urlopen(request) as response:
      response_headers = response.info()
      ct = response_headers['Content-Type']
      if ct.find("charset=")>=0:
          charset = ct.split("charset=")[1]
          print(charset)

      html = response.read().decode(charset)     

  return html


# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def __init__(self,parse_events_list=[]):
        HTMLParser.__init__(self)
        self.parse_events_list = parse_events_list

    def add_parse_event(self,event):
        self.parse_events_list.append(event)

    def handle_starttag(self, tag, attrs):
        #print("Encountered a start tag:", tag)
        for e in self.parse_events_list:
            e.process(tag,attrs)

    def handle_endtag(self, tag):
        #print("Encountered an end tag :", tag)
        pass

    def handle_data(self, data):
        #print("Encountered some data  :", data)
        pass