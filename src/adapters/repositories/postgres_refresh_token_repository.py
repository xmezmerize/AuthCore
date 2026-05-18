from domain.interfaces.repositories.i_refresh_token_repository import IRefreshTokenRepository
from domain.dtos.refresh_token.refresh_token_dto import RefreshTokenDto
from framework.helpers.exceptions import DatabaseError
from framework.helpers.database_pool import get_conn
from datetime import datetime
from typing import Optional


class PostgresRefreshTokenRepository(IRefreshTokenRepository):
    def create(self, user_fk: str, token: str, expires_at: datetime) -> None:
        sql = """
        INSERT INTO refresh_token (user_fk, token, expires_at, is_revoked)
        VALUES (%s, %s, %s, %s);
        """
        params = (user_fk, token, expires_at, False)
        try:
            with get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params)
                    conn.commit()
        except Exception as e:
            raise DatabaseError("Erro interno: Não foi possível persistir o refresh token no banco.") from e

    def find(self, token: str) -> Optional[RefreshTokenDto]:
        sql = "SELECT id, user_fk, token, expires_at, is_revoked FROM refresh_token WHERE token = %s LIMIT 1;"
        try:
            with get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (token,))
                    row = cursor.fetchone()
                
                    if not row:
                        return None
                
                    return RefreshTokenDto(
                        id=str(row[0]),
                        user_fk=str(row[1]),
                        token=row[2],
                        expires_at=row[3],
                        is_revoked=row[4]
                    )
        except Exception as e:
            raise DatabaseError("Erro interno: Não foi possível consultar o refresh token.") from e

    def update(self, token: str) -> None:
        sql = "UPDATE refresh_token SET is_revoked = TRUE WHERE token = %s;"
        try:
            with get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql, (token,))
                    conn.commit()
        except Exception as e:
            raise DatabaseError("Erro interno: Não foi possível revogar o token no banco.") from e
