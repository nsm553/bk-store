from typing import List

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import uvicorn

# @app.get('/')
# async def read_root():
#     return {"Hello": "World"}


@strawberry.type
class User:
    id: int
    name: str
    age: int

Users: List[User] = [User(id=1, name="John", age=30)]

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        for user in Users:
            if user.id == id:
                return user
        raise ValueError(f"User with id {id} is not found")

@strawberry.type
class AddUser:
    user: User


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name: str, age: int) -> AddUser:
        user = User(id=len(Users) + 1, name=name, age=age)
        Users.append(user)
        print(f"Added User: {user}")
        return AddUser(user=user)   


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

# app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



## Test case 1
# query($id: Int!) {
#     user(id: $id) {
#         id
#         name
#     }
# }

# Test Case 2
# mutation($name: String!, $age: Int!) {
#     addUser(name: $name, age: $age) {
#         user {
    id
#             name
#             age
#         }
#     }
# }