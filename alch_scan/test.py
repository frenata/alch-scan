import flask
import flask_sqlalchemy
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base


app = flask.Flask(__name__)
db = flask_sqlalchemy.SQLAlchemy(session_options=dict(expire_on_commit=False))
Base = declarative_base()


class Foo(Base):
    __tablename__ = "foo"
    id = sa.Column(sa.Integer, primary_key=True)
    val = sa.Column(sa.Text)

    def __repr__(self):
        return f"Foo: {self.val}"


app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "{driver}://{user}:{passwd}@{host}:{port}/{dbname}".format(
    driver="postgresql",
    user="test",
    passwd="test",
    host="localhost",
    port="5432",
    dbname="test",
)
db.init_app(app)


@app.route("/ping")
def ping():
    return "pong"


@app.route("/debug")
def debug():
    breakpoint()
    return ""


@app.route("/vuln", methods=("GET", "POST"))
def vuln():
    v = flask.request.json.get("v")
    res = db.session.query(Foo).filter(Foo.val.ilike(v)).all()
    return flask.jsonify([r.val for r in res])
