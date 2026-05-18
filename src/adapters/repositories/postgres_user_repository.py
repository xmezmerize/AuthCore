from framework.helpers.exceptions import ConflictError, DatabaseError, NotFoundError
from domain.interfaces.repositories.i_user_repository import IUserRepository
from domain.dtos.users.update_user_dto import UpdateUserDto
from domain.dtos.users.create_user_dto import CreateUserDto
from domain.dtos.users.find_user_dto import FindUserDto
from framework.helpers.database_pool import get_conn
from domain.dtos.users.user_dto import UserDto
from datetime import datetime, timezone
from psycopg2 import errors
from typing import Optional
from uuid import uuid4


class PostgresUserRepository(IUserRepository):
    def create(self, dto: CreateUserDto) -> UserDto:
        sql = """
        INSERT INTO users (id, name, email, password, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
        """
        id = str(uuid4())
        created_at = datetime.now(timezone.utc)
        updated_at = datetime.now(timezone.utc)
        params = (id, dto.name, dto.email, dto.password, created_at, updated_at)
        try:
            with get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    row = cursor.fetchone()
                    conn.commit()
                    return UserDto(
                        id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3],
                        created_at=row[4],
                        updated_at=row[5]
                    )
        except errors.UniqueViolation:
            raise ConflictError(f"Erro interno: O email {dto.email} já está em uso.")
        except Exception as e:
            raise DatabaseError("Erro interno: Não foi possível processar a criação desse usuário no banco de dados.") from e

    def find(self, dto: FindUserDto = FindUserDto()) -> list[UserDto]:
        sql = "SELECT * FROM users"
        conditions = []
        filters = {}
        if dto.id:
            conditions.append("id = %(id)s")
            filters['id'] = dto.id
        if dto.created_at:
            conditions.append("created_at::date = %(created_at)s")
            filters['created_at'] = dto.created_at
        if dto.updated_at:
            conditions.append("updated_at::date = %(updated_at)s")
            filters['updated_at'] = dto.updated_at
        if dto.name:
            conditions.append("name ILIKE %(name)s")
            filters['name'] = f"%{dto.name}%"
        if dto.email:
            conditions.append("email ILIKE %(email)s")
            filters['email'] = f"%{dto.email}%"
        if conditions:
            sql += " WHERE " + " OR ".join(conditions)
        try:
            with get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, filters)
                    rows = cursor.fetchall()
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
        except Exception as e:
            raise DatabaseError("Erro interno: Não foi possível buscar usuários no banco.") from e

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
        try:
            with get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    row = cursor.fetchone()
                    conn.commit()
                    return UserDto(
                        id=row[0],
                        name=row[1],
                        email=row[2],
                        password=row[3],
                        created_at=row[4],
                        updated_at=row[5]
                    ) if row else None
        except errors.UniqueViolation:
            raise ConflictError(f"Erro interno: O email {dto.email} já está sendo utilizado por outro usuário.")
        except Exception as e:
            raise DatabaseError("Erro interno: Não foi possível atualizar os dados do usuário.") from e
    
    def delete(self, id: str) -> None:
        sql = "DELETE FROM users WHERE id = %s RETURNING id;"
        try:
            with get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (id,))
                    row = cursor.fetchone()
                    conn.commit()
                    if not row:
                        raise NotFoundError("Usuário", id)
                    return True
        except NotFoundError:
            raise
        except Exception as e:
            raise DatabaseError("Erro interno: Não foi possível excluir o usuário.") from e
