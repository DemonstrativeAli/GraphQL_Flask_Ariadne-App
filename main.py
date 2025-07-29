from flask import Flask, request, jsonify
from ariadne import graphql_sync, make_executable_schema, load_schema_from_path
from ariadne.explorer import ExplorerGraphiQL
from app.schema import schema

app = Flask(__name__)

@app.route("/graphql", methods=["GET"])
def grapql_playground():
    return ExplorerGraphiQL().html(None), 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code

@app.route("/")
def index():
    return "<h2>🚀 Welcome to the Ariadne GraphQL + SQLite App</h2><p>Go to <a href='/graphql'>/graphql</a> to explore GraphQL.</p>"

if __name__ == "__main__":
    app.run(debug=True)