from connect_elastic import search


def search_channel():
    q = input("search here :")
    try:
        result=search(q)
        if result is None:
            print('nothing found !')


    except:
        print("something bad happend!!!")


