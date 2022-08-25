from elasticsearch import Elasticsearch
from flask import Flask,request
import json
app=Flask(__name__)
es=Elasticsearch(["http://localhost:9200"])
@app.route("/findall")
def findall():
    body={
        "query":{
            "match_all":{}
        }
    }
    result=es.search(index="employee",body=body)
    return json.dumps(result,ensure_ascii=False)
@app.route("/findByPage")
def findAllByPage():
    pageId=request.args.get("page")
    pageId=int(pageId)-1
    body={
        "query":{
            "match_all":{}
        },
        "from":pageId*5,
        "size":5
    }
    return json.dumps(es.search(index="employee",body=body),ensure_ascii=False)
@app.route("/finddept")
def findDept():
    body={
          "size":0,
          "aggs":{
            "depts":{
              "terms":{
                "field":"deptno",
                "min_doc_count":3
              },
              "aggs":{
                "sample":{
                  "top_hits":{
                    "size":1,
                    "_source":["dname","loc"]
                  }
                }
              }
            }
          }
        }
    return json.dumps(es.search(index="employee",body=body),ensure_ascii=False)
if __name__=="__main__":
    app.run()