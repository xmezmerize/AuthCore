from entrypoints.controllers.users.create_user_controller import CreateUserController
from entrypoints.controllers.users.update_user_controller import UpdateUserController
from entrypoints.controllers.users.delete_user_controller import DeleteUserController
from entrypoints.controllers.users.login_user_controller import LoginUserController
from entrypoints.controllers.users.find_user_controller import FindUserController
from entrypoints.requests.users.create_user_request import CreateUserRequest
from entrypoints.requests.users.update_user_request import UpdateUserRequest
from entrypoints.requests.users.login_user_request import LoginUserRequest
from fastapi import APIRouter, Request, Response, status
from framework.helpers.handler_jwt import HandlerJwt


route = APIRouter()

@route.post("/create", status_code=status.HTTP_201_CREATED)
async def create(request: CreateUserRequest):
    return CreateUserController().create(request)

@route.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(request: LoginUserRequest, response: Response):
    return LoginUserController().login(request, response)

@route.get("/find", status_code=status.HTTP_200_OK)
async def find(data: Request):
    authorization = HandlerJwt().get_jwt_from_request(data)
    search = data.query_params.get("search")
    return FindUserController().find(authorization, search)

@route.put("/{id}", status_code=status.HTTP_200_OK)
async def update(id: str, request: UpdateUserRequest, data: Request):
    authorization = HandlerJwt().get_jwt_from_request(data)
    return UpdateUserController().update(id, request, authorization)

@route.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete(id: str, data: Request):
    authorization = HandlerJwt().get_jwt_from_request(data)
    return DeleteUserController().delete(id, authorization)
