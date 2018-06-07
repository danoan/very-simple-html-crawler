from crawler import utils

from crawler.google_search_click.actions_parser import FirstAction,SecondAction
from crawler.google_search_click.actions_execution import first_action,second_action


class GoogleSearchClick:
    def __init__(self,text_to_search):
        self.prepare_first_action( utils.escape(text_to_search) )

    def prepare_first_action(self,text_to_search):
        print("Begin First Action")

        M = utils.MyHTMLParser()
        M.add_parse_event( FirstAction(text_to_search,first_action,self.prepare_second_action) )

        html = utils.get("https://www.google.com.br")
        M.feed(html)    

    def prepare_second_action(self,html):
        f = open("first_action.html","w")
        f.write(html)

        print("Begin Second Action")

        M = utils.MyHTMLParser()
        M.add_parse_event( SecondAction(second_action,self.done) )
        M.feed(html)            

    def done(self,html):
        f = open("second_action.html","w")
        f.write(html)

        print("Google Search Click action is finished!")
        


