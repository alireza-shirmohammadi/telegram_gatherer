from connect_elastic import search
def search_channel():
    q=input('search here :')
    try:
        search(q)
    except:
        print('nothing found')