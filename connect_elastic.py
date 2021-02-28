from elasticsearch import Elasticsearch

es = Elasticsearch([{"host": "localhost", "port": 9200}])


def elastic(message, i):
    dic = {}
    dic["id"] = i
    dic["message"] = message
    es.index(index="kafka", id=i, body=dic)


def search(q):

    body = {"query": {"prefix": {"message": {"value": q}}}}
    m = es.search(index="kafka", body=body)
    # len of search :
    size = len(m["hits"]["hits"])
    #print(es.get(index='kafka',id=5))
    i = 0
    for i in range(0, size):

        print('id = ',m["hits"]["hits"][i]["_id"],'\n',m["hits"]["hits"][i]["_source"]["message"])
        i += 1
    if size!=0:
        return 1