from framework.factories.adapters.postgres_repository_factory import PostgresRepositoryFactory
from adapters.providers.argon2_password_provider import Argon2PasswordProvider
from adapters.providers.jwt_token_provider import JwtTokenProvider

from duckdi import register


register(PostgresRepositoryFactory, label="postgres", is_singleton=True)
register(JwtTokenProvider, label="jwt", is_singleton=True)
register(Argon2PasswordProvider, label="argon2", is_singleton=True)
