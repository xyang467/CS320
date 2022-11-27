# project: p4
# submitter: xyang467
# partner: none
# hours: 10
import pandas as pd
import re
from flask import Flask, request, jsonify, Response
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from io import StringIO
import time

app = Flask(__name__)
df = pd.read_csv("main.csv")
# main.csv are retrieved from https://www.kaggle.com/datasets/fernandomatheus/genshin-impact-dataset
visit = 0
@app.route('/')
def home():
    global visit
    visit +=1
    with open("index.html") as f:
        html_A = f.read()
        html_change_color = re.sub('red','green',html_A)
        html_B = re.sub("A","B",html_change_color)
    if visit<=10:
        if visit % 2 ==1:
            return html_A
        else:
            return html_B
    else:
        if donate_from_A > donate_from_B:
            return html_A
        else: 
            return html_B

@app.route('/browse.html')
def browse():
    return "<html>{}</html>".format("<h1>Browse</h1>"+ df.to_html())

IPs = {}
@app.route('/browse.json')
def browse_json():
    global IPs
    data = df.to_dict('index')
    ip = request.remote_addr
    if ip not in IPs.keys():
        IPs[ip] = time.time()
        return jsonify(data)
    else:
        if time.time() - IPs[ip] >60:
            IPs[ip] = time.time()
            return jsonify(data)
        else:
            html = "Please come back later one minute later"
            return Response(html, status=429, headers={"Retry-After": 60}) 

                              
num_subscribed = 0
@app.route('/email', methods=["POST"])
def email():
    global num_subscribed
    email = str(request.data, "utf-8")
    if re.match(r"^[^@\.]+@[^@\.]+\.[^@\.]+$", email): # 1
        num_subscribed += 1
        with open("emails.txt", "a") as f: # open file in append mode
            f.write(email + "\n") # 2
        return jsonify(f"thanks, you're subscriber number {num_subscribed}!")
    return jsonify("You have entered an invalid email address! Please enter a valid email address!") # 3

donate_from_A = 0
donate_from_B = 0 
@app.route('/donate.html')
def donate():
    global donate_from_A,donate_from_B
    args = dict(request.args)
    if args.get("from") == "A":
        donate_from_A+=1
    elif args.get("from") == "B":
        donate_from_B+=1
    return """<html><body>
              <h1>Donations</h1>
              Please help us by making some donations. Thank you so much!
              <body></html>"""

@app.route("/dashboard_1.svg")
def svg_1():
    fig, ax = plt.subplots()
    col = dict(request.args)
    var = col.get("cmap")
    if col:
        m = ax.scatter(df.ATK, df.DEF, c=df[var],alpha=0.7)
        cbar = plt.colorbar(m)
        cbar.ax.set_ylabel(var)
    else:
        ax.scatter(df.ATK,df.DEF,alpha=0.7)
    ax.set_ylabel("DEF")
    ax.set_xlabel("ATK")
    ax.set_title("Scatter plot of ATK vs. DEF")
        
    f = StringIO()
    plt.tight_layout()
    fig.savefig(f, format="svg")
    plt.close()
    
    png = f.getvalue()
    
    hdr = {"Content-Type": "image/svg+xml"}
    return Response(png, headers=hdr)

@app.route("/dashboard_2.svg")
def svg_2():
    fig, ax = plt.subplots()
    df.ATK.hist(ax=ax, bins=100)
    ax.set_xlabel("ATK")
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram of ATK")
    
    f = StringIO() 
    plt.tight_layout()
    fig.savefig(f, format="svg")
    plt.close()
    
    png = f.getvalue()
    
    hdr = {"Content-Type": "image/svg+xml"}
    return Response(png, headers=hdr)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False) # don't change this line!
