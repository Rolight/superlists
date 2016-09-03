import re

def remove_csrf_token(content):
    p = re.compile("<.*?name='csrfmiddlewaretoken'.*?>")
    return re.sub(p, '', content)

    
def none_empty_ch(content):
    p = re.compile('\s')
    return re.sub(p, '', content)

def pure(content):
    return none_empty_ch(remove_csrf_token(content))

