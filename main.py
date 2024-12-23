from fastapi import FastAPI
from app.database import engine, SessionLocal, engine_237
from app.routes import users, genapi, db_api
from app.models import Base, ServerMetadata, ServerMetadataLogs
from dotenv import load_dotenv
import uvicorn 
from fastapi.middleware.cors import CORSMiddleware


origins = [
    "*",
]


load_dotenv()


app = FastAPI(docs_url="/dbgen-api/", title="DB Gen API", redoc_url="/dbgen-api/redoc")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(posts.router)
app.include_router(users.router)
app.include_router(genapi.router)
app.include_router(db_api.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    ServerMetadataLogs.__table__.create(bind=engine_237)
    # Base.metadata.create_all(bind=engine_linkedin_237)
    # Base.metadata.create_all(bind=engine_43_playwright)

if __name__ == "__main__":
    # init_db()  # Initialize database tables
    uvicorn.run("main:app", host="0.0.0.0", port=8020, reload=True)
