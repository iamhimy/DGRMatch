import pandas as pd
import os
from flask import Flask,render_template,request, redirect, url_for
from werkzeug.utils import secure_filename
app=Flask("DGRApp")
name=""
def irravg():
    irravg=sum(df['IrrActual'])/n
    return irravg
def neteavg():
    netbavg=sum(df['NetExpActual'])/n
    return netbavg
def search(x,y):
    i=0
    for plant in df['Plant']:
        if x==plant:
            return str(df[y][i])
        else :
            i+=1
@app.route("/")
def Home():
    return render_template("index.html")
@app.route('/upload', methods=['GET','POST'])
def upload():
    if request.method =='POST':
        f=request.files["file"]
        n =  f.filename
        f.save(f.filename)
        r=n+" uploaded successfully."
        return render_template("index.html", name=r)
df=pd.read_excel("./DGR.xlsx")
n=df['Plant'].size

@app.route("/result",methods=["GET"])
def result():
    plant=request.args.get("plant")
    query=request.args.get("resultype")
    if query=='IrrActualAverage':
        r=irravg()
        htmlcode=render_template("index.html",result=r)
        return htmlcode
    elif query=='NetExpAverage':
        r=neteavg()
        htmlcode=render_template("index.html",result=r)
        return htmlcode
    elif "Match" in query:
        var=query[:len(query)-5]
        x=float(search(plant,f"{var}Actual"))
        y=float(search(plant,f"{var}Budget"))
        r=str((y*100)/x)+"%"
        htmlcode=render_template("index.html",result=r)
        return htmlcode
    else:
        r=search(plant,query)
        htmlcode=render_template("index.html",result=r)
        return htmlcode
app.run(port=1111,host='0.0.0.0')
