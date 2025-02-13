from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from app.services.books import schema

import uvicorn

app = FastAPI()
graphql_app = GraphQLRouter(schema)

app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

# # Database setup
# Base.metadata.create_all(bind=database)
# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

