from crawler import utils

def first_action(callback_fn,text_to_search,form_action,input_name):
    google_home = "https://www.google.com.br"
    google_search_link = "%s%s?%s=%s" % (google_home,form_action,input_name,text_to_search)

    print("Google Search Link: ", google_search_link)            
    html = utils.get(google_search_link)
    print("Request was successful.")    
    callback_fn(html)    
    print("Done.")  

def second_action(first_link,callback_fn):    
    print("Visiting first link: ", first_link)
    html = utils.get(first_link)
    callback_fn(html)