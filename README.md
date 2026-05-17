# Project GUIDE

init:
```sh
poetry new .
```

install:
```sh
poetry add fastapi python-multipart jinja2 uvicorn python-dotenv psycopg2 pydantic duckdi pyjwt argon2-cffi
```

.env-example:
```sh
export DATABASE_URL="postgresql://[user[:password]@][host][:port][/dbname][?paramspec]"
export JWT_SECRET="your_generated_random_hex_string_here"
export BRAZILIAN_DATE_FORMAT="%d/%m/%Y %H:%M:%S"
export INJECTIONS_PATH="$PWD/injections.toml"
export JWT_EXPIRES_IN=1
export HOST="127.0.0.1"
export PORT="8000"
```

tables-example:
```sql
CREATE TABLE users(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE refresh_token (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    token_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    revoked_at TIMESTAMP
);
```

to run:
```sh
direnv allow
make run
```
