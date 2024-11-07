from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# docker run --name contacts_rest_app -p 5432:5432 -e POSTGRES_PASSWORD=567234 -d postgres
# docker exec -it contacts_rest_app psql -U postgres -c "CREATE DATABASE contacts_rest_app;"
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:567234@localhost:5432/contacts_rest_app"
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


async def get_db():      
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()