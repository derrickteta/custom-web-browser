from models import *
import datetime


def add_history(link,text):
    history,_ = History.get_or_create(date=datetime.date.today())
    
    Link.create(text=text, link=link,history=history)
    pass
def get_bookmarks():
    return Link.select()