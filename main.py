from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, opinion, nft
from app.database import create_tables, test_connection
import uvicorn


# 创建FastAPI应用实例
app = FastAPI(title="MoonCL Server API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 启动时测试数据库连接并创建表
@app.on_event("startup")
def startup_event():
    print("Starting MoonCL Server...")
    if test_connection():
        create_tables()
        print("Database tables created successfully!")
    else:
        print("Failed to connect to database!")


# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(opinion.router, prefix="/api/v1/opinions", tags=["opinions"])
app.include_router(nft.router, prefix="/api/v1/nfts", tags=["nfts"])


# 根路径
@app.get("/")
def root():
    return {"message": "MoonCL Server API"}


# 健康检查端点
@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
