from flask import Flask, request
from flask_cors import CORS
from get_file_data import check
from embed import embed, make, query

app = Flask(__name__)
CORS(app, origins=["*"])
app.debug = True



@app.route("/process")
def process():
    f = request.args.get("f", None)
    make([f.strip()])
    return check()
    
@app.route("/embed")
def embed_file():
    f = request.args.get("f", None)
    model = request.args.get("model", None)
    embed(f, model)
    return check()

@app.route("/search")
def search():
    q = request.args.get("q", None)
    f = request.args.get("f", None)
    model = request.args.get("model", None)
    return query(f, q, model, 3)
    

@app.route("/metadata")
def index():
    file_metadata = check()
    return file_metadata

if __name__ == '__main__':
    app.run()
