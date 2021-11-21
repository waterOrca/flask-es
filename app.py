from flask import Flask
from flask import render_template 
from flask import request
import time
from datetime import datetime
from elasticsearch import Elasticsearch
import pandas as pd

app=Flask(
    __name__,
    static_folder="static", #靜態資料夾
    static_url_path="/" #靜態檔案路徑
    )
es = Elasticsearch()

@app.route("/")
def index():
    index_ip =  request.remote_addr
    print(index_ip)
    index_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    print(index_date)
    return render_template("index.html") 

@app.route("/es_meta_in")
def es_meta_in():
    ip_meta =  request.remote_addr
    date_meta = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    return render_template("es_meta_in.html")

@app.route("/es_meta_res", methods=["GET", "POST"])
def es_meta_res():
    searchMeta = request.args.get('searchMeta', "")
    print(searchMeta)
    size = 50
    resMeta = es.search(index="srda_0307", 
                    body={'min_score': 1, #最小評分
                        "query": {
                        "simple_query_string": {
                        "query": searchMeta,
                        "fields": ["title_c^10","all"],
                        "default_operator": "or",
                        "auto_generate_synonyms_phrase_query": True}}},
                    size=size)
    print("Got %d Hits:" % resMeta['hits']['total']['value'])
    gotHits = str(resMeta['hits']['total']['value'])
    return render_template("es_Meta_res.html", resMeta=resMeta, searchMeta=searchMeta)

@app.route("/es_ques_in")
def es_ques_in():
    ip_ques =  request.remote_addr
    date_ques = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    return render_template("es_ques_in.html")

@app.route("/es_ques_res", methods=["GET", "POST"])
def es_ques_res():
    titele = "ques"
    searchQues = request.args.get('searchQues', "")
    print(searchQues)
    size = 50
    resQues = es.search(index="srda_que", 
                    body={'min_score': 1, #最小評分
                        "query": {
                        "simple_query_string": {
                        "query": searchQues,
                        "fields": ["all_text"],
                        "default_operator": "or"}}},
                    size=size)
    print("Got %d Hits:" % resQues['hits']['total']['value'])
    gotHits = str(resQues['hits']['total']['value'])
    return render_template("es_Ques_res.html", resQues=resQues, searchQues=searchQues)

@app.route("/es_tscs_que_in")
def es_tscs_que_in():
    es_que_ip =  request.remote_addr
    es_que_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    return render_template("es_tscs_que_in.html")

@app.route("/es_tscs_que_res", methods=["GET", "POST"])
def es_tscs_que_res():
    searchTSCS = request.args.get('searchTSCS', "")
    print(searchTSCS)
    size = 50
    res = es.search(index="tscs_sc", 
                    body={'min_score': 1, #最小評分
                        "query": {
                        "query_string": {
                        "query": searchTSCS,
                        "fields": ["all_text"],
                        "default_operator": "or"}}},
                    size=size)
    print("Got %d Hits:" % res['hits']['total']['value'])
    gotHits = str(res['hits']['total']['value'])
    outRes = [] 
    for hit in res['hits']['hits']:
        temOut = hit["_source"]
        outRes.append(temOut)
        print("%(id)s  %(per)s  %(var)s" % hit["_source"])
    #df = pd.DataFrame(outRes)
    return render_template("es_tscs_que_res.html", res=res, searchTSCS=searchTSCS)



#app.debug = True
#app.run(port=3000)
app.run(host='140.109.171.208', port=3000)