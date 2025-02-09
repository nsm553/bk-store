from fastapi import FastAPI
from strawberry.asgi import GraphQL
import know_your_business
import uvicorn

app = FastAPI()
graphql_app = GraphQL(know_your_business.schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

