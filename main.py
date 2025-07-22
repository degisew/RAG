from fastapi import FastAPI
from backend.core.exceptions import register_global_exceptions
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.router import router as auth_router
from backend.router import router as rag_router
from backend.account.router import router as account_router


app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(rag_router)
app.include_router(account_router)


register_global_exceptions(app)
