from typing import Optional
from urllib.request import Request
from fastapi import FastAPI,status
from pydantic import BaseModel, Field
from fastapi.responses import JSONResponse
from fastapi import Depends, Header, HTTPException
from .routers.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware
import time
from fastapi import BackgroundTasks

app = FastAPI(title='FastAPI',version='1.0')
app.include_router(user_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境不要写*，填写前端["https://xxx.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    print("服务启动，初始化数据库连接、加载大模型权重")


@app.on_event("shutdown")
async def shutdown():
    print("服务关闭，释放资源、关闭数据库")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)+'sss'
    return response

@app.get('/')
async def root():
    return {'msg':'hello fastapi'}

@app.post("/send")
async def send_msg(background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, "收到消息")  # ① 只是“登记”任务，不执行
    return {"msg": "任务已提交"}


@app.get('/hello/{user_id}')
async def hello(user_id:int):
    return {'msg':f'hello:{user_id}'}


@app.get("/search")
async def search(keyword: Optional[str] = None):
    return {"keyword": keyword}


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=20, description="用户名")
    password: str = Field(min_length=6)
    age: int | None = Field(default=None, ge=0, le=120)  # 可选，0~120


@app.post("/user/create")
async def create_user(user: UserCreate):
    # FastAPI自动把前端json解析成UserCreate对象，并自动校验
    return {"msg": "创建成功", "data": user.model_dump()}


@app.get("/item/{item_id}", status_code=status.HTTP_201_CREATED)
async def get_item(item_id: int):
    if item_id <= 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"msg": "id不能小于等于0"}
        )
    return {"item_id": item_id}


async def get_token(authorization: str | None = Header(default=None)):
    if not authorization or authorization != "Bearer test_token":
        raise HTTPException(status_code=401, detail="token无效")
    return authorization

@app.get('/user/info')
async def user_info(token:str = Depends(get_token)):
    return {'msg':'访问成功','token':token}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.status_code, "msg": exc.detail, "data": None},
    )


# 捕获非预期的服务器异常
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500, content={"code": 500, "msg": "服务器内部错误", "data": None}
    )


@app.get("/error")
async def test_error():
    raise HTTPException(status_code=400, detail="业务异常")
