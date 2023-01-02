from flask import Flask, request, redirect
from search import load_data, query

app = Flask(__name__)
app.debug = True
df = load_data()

@app.route("/")
def index():
    return "Hello World"

@app.route("/search")
def search():
    q = request.args.get("q", "")
    if q == "":
        return redirect("/")
    try:
        result = query(df, q)
        return {
            "status": "success",
            "data": result
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == '__main__':
    app.run()
