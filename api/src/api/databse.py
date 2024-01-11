from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models.User import Base as UserBase
from api.models.Post import Base as PostBase

DATABASE_URI = 'postgresql://kairidev:l0ajmyo6qbDJ@ep-autumn-flower-96499455.us-east-2.aws.neon.tech/quarticle?sslmode=require'
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    UserBase.metadata.create_all(bind=engine)
    PostBase.metadata.create_all(bind=engine)
