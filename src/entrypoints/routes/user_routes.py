from entrypoints.controllers.create_user_controller import CreateUserController
from entrypoints.controllers.delete_user_controller import DeleteUserController
from entrypoints.controllers.update_user_controller import UpdateUserController
from entrypoints.controllers.login_user_controller import LoginUserController
from entrypoints.controllers.find_user_controller import FindUserController
from entrypoints.requests.update_user_request import UpdateUserRequest
from entrypoints.requests.create_user_request import CreateUserRequest
from entrypoints.requests.login_user_request import LoginUserRequest
from framework.helpers.handler_jwt import HandlerJwt
from fastapi import APIRouter, Request, status


route = APIRouter(tags=["users"])

@route.post("/create", status_code=status.HTTP_201_CREATED)
async def create(request: CreateUserRequest):
    return CreateUserController().create(request)

@route.post("/login", status_code=status.HTTP_202_ACCEPTED)
async def login(request: LoginUserRequest):
    return LoginUserController().login(request)

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
