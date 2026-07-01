from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from .config import settings

# Base class that all models will inherit from.
# SQLAlchemy uses it to collect metadata for migrations.
class Base(DeclarativeBase):
  pass

# Create the database engine.
# The engine manages connections to PostgreSQL.
# It does NOT connect immediately—it creates connections only when needed.
engine = create_async_engine(
  settings.DATABASE_URL,
  # Print all generated SQL statements to the console.
  # Useful for development and debugging.
  # Set to False in production.
  echo=True
)

# Create a session factory.
# This is NOT a database session yet.
# Think of it as a blueprint for creating new sessions.
#
# Each HTTP request should get its own session.
AsyncSessionLocal = async_sessionmaker(
  engine,
  # After calling session.commit(), SQLAlchemy normally expires
  # all loaded objects and reloads them from the database when accessed.
  #
  # Setting this to False keeps objects in memory after commit,
  # avoiding unnecessary database queries.
  expire_on_commit=False
)

# Dependency function for FastAPI.
#
# Every time an endpoint depends on get_db():
#
#   1. Create a new database session
#   2. Give that session to the endpoint
#   3. Automatically close the session when the request finishes
#
# This ensures every request has its own isolated session.
async def get_db():
  # Create a new database session
  async with AsyncSessionLocal() as session:
    # Pass the session to the endpoint
    yield session

    # When the endpoint finishes, execution resumes here.
    # The "async with" block automatically closes the session,
    # even if an exception occurred.
    # @see `async_with_and_yield.md` for details explain