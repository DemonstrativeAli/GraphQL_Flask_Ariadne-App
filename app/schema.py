from ariadne import QueryType, MutationType, make_executable_schema
from .resolvers import (
    resolve_users,
    resolve_create_user,
    resolve_update_user,
    resolve_delete_user,
    resolve_get_user_by_email,
    resolve_login_user,
    resolve_me
)

type_defs = """
    type User {
        id: ID!
        name: String!
        email: String!
    }
    type Query {
        users: [User!]!
        getUserByEmail(email: String!): User
        me: User!
    }
    type Mutation {
        createUser(name: String!, email: String!, password: String!): User!
        updateUser(id: ID!, name: String, email: String): User
        deleteUser(id: ID!): Boolean
        login(email: String!, password: String!): String!
    }

"""

query = QueryType()
mutation = MutationType()
query.set_field("users", resolve_users)
query.set_field("getUserByEmail", resolve_get_user_by_email)
query.set_field("me", resolve_me)

mutation.set_field("createUser", resolve_create_user)
mutation.set_field("updateUser", resolve_update_user)
mutation.set_field("deleteUser", resolve_delete_user)
mutation.set_field("login", resolve_login_user)

schema = make_executable_schema(type_defs, [query, mutation])