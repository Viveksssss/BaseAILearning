from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from contextlib import asynccontextmanager

# SQLAlchemy 异步相关导入
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, func, select

# ------------------------------
# 1. 远程 MySQL 数据库配置
# ------------------------------
# 格式：mysql+aiomysql://用户名:密码@主机:端口/数据库名?字符集
DATABASE_URL = "mysql+aiomysql://root:38324@127.0.0.1/test_db?charset=utf8mb4"

# 创建异步引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # 开发环境开启：打印SQL日志；生产环境关闭
    pool_pre_ping=True,  # 自动检测断开的连接，避免长连接失效
    pool_size=5,  # 连接池核心大小
    max_overflow=10,  # 连接池最大溢出数
)

# 异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,  # 提交后不失效对象，避免重复查询
    class_=AsyncSession,
)

# ORM 模型基类
Base = declarative_base()


# ------------------------------
# 2. ORM 数据模型（用户表）
# ------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


# ------------------------------
# 3. Pydantic 响应模型（接口格式规范）
# ------------------------------
class UserResp(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # 支持 ORM 对象直接转 Pydantic


# ------------------------------
# 4. 应用生命周期：启动自动建表
# ------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时：创建所有数据表
    async with engine.begin() as conn:
        # 同步建表方法放到异步线程执行
        await conn.run_sync(Base.metadata.create_all)
    yield
    # 关闭时：释放数据库连接池
    await engine.dispose()


app = FastAPI(title="异步MySQL集成示例", lifespan=lifespan)


# ------------------------------
# 5. 数据库会话依赖（每个请求一个独立会话）
# ------------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# ------------------------------
# 6. 全异步 CRUD 数据库操作
# ------------------------------
async def create_user(db: AsyncSession, username: str, email: str) -> User:
    """创建用户"""
    user = User(username=username, email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)  # 刷新获取数据库生成的ID和时间
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    """根据ID查用户"""
    return await db.get(User, user_id)


async def get_user_by_name(db: AsyncSession, username: str) -> User | None:
    """根据用户名查用户"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession, skip: int = 0, limit: int = 10) -> list[User]:
    """分页查询用户列表"""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user_email(
    db: AsyncSession, user_id: int, new_email: str
) -> User | None:
    """更新用户邮箱"""
    user = await get_user_by_id(db, user_id)
    if not user:
        return None
    user.email = new_email
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> bool:
    """删除用户"""
    user = await get_user_by_id(db, user_id)
    if not user:
        return False
    await db.delete(user)
    await db.commit()
    return True


# ------------------------------
# 7. FastAPI 接口层
# ------------------------------
@app.post("/users/", response_model=UserResp, summary="创建用户")
async def create_user_api(
    username: str, email: str, db: AsyncSession = Depends(get_db)
):
    # 用户名唯一性校验
    if await get_user_by_name(db, username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    return await create_user(db, username, email)


@app.get("/users/{user_id}", response_model=UserResp, summary="根据ID查询用户")
async def get_user_api(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@app.get("/users/", summary="查询用户列表")
async def list_users_api(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    users = await list_users(db, skip, limit)
    return {"code": 200, "data": users}


@app.put("/users/{user_id}", response_model=UserResp, summary="更新用户邮箱")
async def update_user_api(user_id: int, email: str, db: AsyncSession = Depends(get_db)):
    user = await update_user_email(db, user_id, email)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@app.delete("/users/{user_id}", summary="删除用户")
async def delete_user_api(user_id: int, db: AsyncSession = Depends(get_db)):
    if not await delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 200, "message": "删除成功"}


# ------------------------------
# 启动入口
# ------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=10086, reload=True)
