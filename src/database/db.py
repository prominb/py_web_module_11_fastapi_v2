# from os import getenv

# from dotenv import load_dotenv  #, find_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# load_dotenv()  # NOT WORK
# load_dotenv(find_dotenv())  # NOT WORK
# load_dotenv(find_dotenv('.env'))  # NOT WORK
# load_dotenv('/home/usrone/Documents/git_repos/py_web_module_11_fastapi_v2/.env')  # NOT WORK
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://db1_usr:password@host:port/db1"  # WORK
# SQLALCHEMY_DATABASE_URL = getenv("DATABASE_URL")  # NOT WORK
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
