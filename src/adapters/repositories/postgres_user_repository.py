from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.dtos.users.update_user_dto import UpdateUserDto
from domain.dtos.users.create_user_dto import CreateUserDto
from domain.dtos.users.find_user_dto import FindUserDto
from domain.dtos.users.user_dto import UserDto
from datetime import datetime
from typing import Optional
from uuid import uuid4
import psycopg2
import os


class PostgresUserRepository(IUserRepository):
    def __init__(self):
        database_url = os.getenv("DATABASE_URL")
        self.connection = psycopg2.connect(database_url)
        self.cursor = self.connection.cursor()

    def create(self, dto: CreateUserDto) -> UserDto:
        sql = """
        INSERT INTO users (id, name, email, password, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id, name, email, password, created_at, updated_at;
        """
        id = str(uuid4())
        created_at = datetime.now()
        updated_at = datetime.now()
        params = (id, dto.name, dto.email, dto.password, created_at, updated_at)
        self.cursor.execute(sql, params)
        row = self.cursor.fetchone()
        self.connection.commit()
        return UserDto(
            id=row[0],
            name=row[1],
            email=row[2],
            password=row[3],
            created_at=row[4],
            updated_at=row[5]
        )

    def find(self, dto: FindUserDto = FindUserDto()) -> list[UserDto]:
        sql = "SELECT * FROM users WHERE "
        filters = {}
        if dto.id is not None:
            sql += "id = %(id)s OR"
            filters['id'] = dto.id
        if dto.name is not None:
            sql += "name = %(name)s OR"
            filters['name'] = dto.name  
        if dto.email is not None:
            sql += "email = %(email)s OR"
            filters['email'] = dto.email
        if dto.created_at is not None:
            sql += "created_at = %(created_at)s OR"
            filters['created_at'] = dto.created_at
        if dto.updated_at is not None:
            sql += "updated_at = %(updated_at)s OR"
            filters['updated_at'] = dto.updated_at
        if sql.endswith(' OR'):
            sql = sql.removesuffix(' OR')
        if sql.endswith(' WHERE'):
            sql = sql.removesuffix(' WHERE')
        sql += ";"
        self.cursor.execute(sql, filters)
        rows = self.cursor.fetchall()
        return [
            UserDto(
                id=row[0],
                name=row[1],
                email=row[2],
                password=row[3],
                created_at=row[4],
                updated_at=row[5]
            ) for row in rows
        ]

    def update(self, id: str, dto: UpdateUserDto) -> Optional[UserDto]:
        sql = """
        UPDATE users
        SET name = COALESCE(%s, name),
            email = COALESCE(%s, email),
            password = COALESCE(%s, password),
            updated_at = NOW()
        WHERE id = %s
        RETURNING *;
        """
        params = (dto.name, dto.email, dto.password, id)
        self.cursor.execute(sql, params)
        row = self.cursor.fetchone()
        self.connection.commit()
        return UserDto(
            id=row[0],
            name=row[1],
            email=row[2],
            password=row[3],
            created_at=row[4],
            updated_at=row[5]
        ) if row else None
    
    def delete(self, id: str) -> None:
        sql = "DELETE FROM users WHERE id = %s;"
        self.cursor.execute(sql, (id,))
        self.connection.commit()
