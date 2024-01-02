#!/usr/bin/python3
"""Create a flask app"""


from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def teardown_appcontext(error=None):
    # if error is not None:
    #     with open("error.l", w) as file_error:
    #         file_error.write(error)
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states_list():
    result = storage.all(State)
    sorted_res = dict(sorted(result.items(), key=lambda item: item[1].name))
    return render_template("7-states_list.html", states=sorted_res)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)