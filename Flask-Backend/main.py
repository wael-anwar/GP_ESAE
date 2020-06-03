import flask

app=flask.Flask("__main__")

@app.route("/",methods=["POST","GET"])
def my_index():
    if flask.request =="POST":
        pass
    else:
        return flask.render_template("index.html",answer="Hello Flask+React (GP ESAE)")

app.run(debug=True)