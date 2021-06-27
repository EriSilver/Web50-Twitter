from .models import *
from django.core.paginator import Paginator

def getposts(apage, postss):
    #print(postss)

    postss= Paginator(postss, 10)
    p = postss.num_pages
    if apage:
        if apage > p:
            return "Page does not exist.", "x", p
        thepage = apage
    
    else:
        thepage = 1

    #print(f"*********** {postss.page(thepage).object_list}")


    return postss, thepage, p