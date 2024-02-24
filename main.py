from typing import Union, Optional
from fastapi import FastAPI, Request, Cookie
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
from api import api_router
from core import Events
from config import settings
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


app = FastAPI()


# 设置路由
app.include_router(api_router)


# 事件监听
app.add_event_handler("startup", Events.startup(app))
app.add_event_handler("shutdown", Events.stopping(app))



# 添加core中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)





@app.get("/")
def read_root(request: Request, auth: Optional[str] = Cookie(None)):
    
    cookie = auth
    session = request.session.get("session")

    data = {
        "cookie": cookie,
        "session": session,
    }

    return data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
