from html.parser import HTMLParser
from enum import Enum

'''
    References:
    https://docs.python.org/3/library/urllib.request.html#module-urllib.request
    https://docs.python.org/3/library/html.parser.html#module-html.parser
    https://docs.python.org/3/howto/urllib2.html

    https://developer.mozilla.org/en-US/docs/Web/API/Request/headers
    https://developer.mozilla.org/en-US/docs/Glossary/Response_header
'''

'''
    Google uses a simple get request with query parameter q to execute a serch.
    It will be sufficient to just get an html page with the q parameter set, but
    we are going to do it as a user in some browser.

    We should mine the form in which the inbut box is within.     

    It works for google.com.br   
'''
class FirstAction:
    class State(Enum):
        FORM_MINING = 1
        INPUT_SEARCH_MINING = 2
        DONE = 3
    '''
        State variables definitions
    '''
    def __init__(self,text_to_search,end_of_action_fn,callback_fn):
        self.text_to_search = text_to_search
        self.end_of_action_fn = end_of_action_fn
        self.callback_fn = callback_fn

        self.current_state = FirstAction.State.FORM_MINING        

        self.form_attrs = None
        self.input_attrs = None

    def process(self,tag,attrs):
        if self.current_state==FirstAction.State.FORM_MINING:
            self.__form_mining__(attrs)
        elif self.current_state==FirstAction.State.INPUT_SEARCH_MINING:
            self.__input_search_mining__(attrs)
        elif self.current_state==FirstAction.State.DONE:
            pass
        else:
            raise RuntimeError("Invalid state at GoogleSearchBox.")

    '''
        <form class="tsf" 
          action="/search" 
          style="overflow:visible" 
          id="tsf" 
          method="GET" 
          name="f" 
          onsubmit="return q.value!=''" 
          role="search">
    '''
    def __form_mining__(self,attrs):
        similarity = 0
        for attr in attrs:
            name,value = attr
            if name=="id" and value=="tsf":
                similarity+=1

            if name=="action" and value=="/search":
                similarity+=1

            if name=="role" and value=="search":
                similarity+=1

        if similarity==3:
            self.form_attrs = attrs
            self.current_state = FirstAction.State.INPUT_SEARCH_MINING


    '''
        <input  class="gsfi" 
                id="lst-ib" 
                maxlength="2048" 
                name="q" 
                autocomplete="off" 
                title="Pesquisar" 
                value="" 
                aria-label="Pesquisar" 
                aria-haspopup="false" 
                role="combobox" 
                aria-autocomplete="list" 
                dir="ltr" 
                spellcheck="false" 
                type="text">  
    '''
    def __input_search_mining__(self,attrs):
        similarity=0
        for attr in attrs:
            name,value = attr
            if name=="id":
                if value=="lst-ib":
                    similarity+=1

            if name=="title":
                if value=="Pesquisar":
                    similarity+=1

        if similarity==2:
            self.input_attrs = attrs
            self.current_state = FirstAction.State.DONE
            self.__done__()


    def __done__(self):
        google_home = "https://www.google.com.br"

        form_action = ""
        for attr in self.form_attrs:
            name,value = attr
            if name=="action":
                form_action = value
                break

        input_name = ""
        for attr in self.input_attrs:
            name,value = attr
            if name=="name":
                input_name = value
                break

        self.end_of_action_fn(self.callback_fn,self.text_to_search,form_action,input_name)


class SecondAction:
    class State(Enum):
        FIND_DIV_RESULTS = 1
        FIND_FIRST_DIV = 2
        FIND_FIRST_LINK = 3
        DONE = 4
    '''
        State variables definitions
    '''
    def __init__(self,end_of_action_fn,callback_fn):
        self.end_of_action_fn = end_of_action_fn
        self.callback_fn = callback_fn

        self.current_state = SecondAction.State.FIND_DIV_RESULTS        
        self.first_link_attrs = None

    def process(self,tag,attrs):
        if self.current_state==SecondAction.State.FIND_DIV_RESULTS:
            self.__find_div_results__(attrs)
        elif self.current_state==SecondAction.State.FIND_FIRST_DIV:
            self.__find_first_div__(attrs)
        elif self.current_state==SecondAction.State.FIND_FIRST_LINK:
            self.__find_first_link__(tag,attrs)            
        elif self.current_state==SecondAction.State.DONE:
            pass
        else:
            raise RuntimeError("Invalid state at GoogleSearchBox.")


    def __find_div_results__(self,attrs):
        for attr in attrs:
            name,value = attr
            if name=="id" and value=="ires":
                    self.current_state = SecondAction.State.FIND_FIRST_DIV
                    break

    def __find_first_div__(self,attrs):
        for attr in attrs:
            name,value = attr
            if name=="class" and value=="g":                
                self.current_state = SecondAction.State.FIND_FIRST_LINK
                break


    def __find_first_link__(self,tag,attrs):
        if tag=="a":
            self.first_link_attrs = attrs
            self.current_state = SecondAction.State.DONE
            self.__done__()
            


    def __done__(self):
        google_home = ""#"https://www.google.com.br"
        first_link = ""
        for attr in self.first_link_attrs:
            name,value = attr
            if name=="href":
                first_link = value
                break

        self.end_of_action_fn( "%s%s" % (google_home,first_link),self.callback_fn )
