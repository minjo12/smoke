from flask import Flask
from charts import visual

app = Flask(__name__)


@app.route('/')
def visualize():
    return visual.show_smoking()


if __name__ == '__main__':
    app.run(debug=True)
