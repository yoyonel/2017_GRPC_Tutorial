"""
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://{PG_USER}:{PG_PASSWD}@{PG_HOST}:{PG_PORT}/{PG_DB}".format(
        PG_USER=os.environ.get("TUTORIAL_GRPC_PG_USER", 'docker'),
        PG_PASSWD=os.environ.get("TUTORIAL_GRPC_PG_PASSWD", 'docker'),
        PG_HOST=os.environ.get("TUTORIAL_GRPC_PG_HOST", 'localhost'),
        PG_PORT=int(os.getenv("TUTORIAL_GRPC_PG_PORT", "5432")),
        PG_DB=os.environ.get("TUTORIAL_GRPC_PG_DB", 'test'),
    ),
    echo=True
)

# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()
