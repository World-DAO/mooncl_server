# MoonCL Server

一个基于FastAPI的区块链观点NFT化平台后端服务。

## 功能特性

- 🔐 用户认证系统
- 💭 观点发布与管理
- 🎨 观点NFT化（铸造、转移、交易）
- 💰 价格评估与交易
- 🗄️ MySQL数据库存储

## 技术栈

- **框架**: FastAPI 0.104.1
- **数据库**: MySQL (通过SQLAlchemy ORM)
- **认证**: JWT
- **服务器**: Uvicorn
- **其他**: Pydantic, PyMySQL

## 快速开始

### 环境要求

- Python 3.8+
- MySQL 数据库

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行服务

```bash
python main.py
```

服务将在 `http://localhost:8000` 启动。

## API 接口

### 认证 (Authentication)
- `POST /api/v1/auth/login` - 用户登录

### 观点 (Opinions)
- `POST /api/v1/opinions` - 发布观点
- `GET /api/v1/opinions` - 获取观点列表
- `GET /api/v1/opinions/{id}` - 获取单个观点
- `GET /api/v1/opinions/{id}/price` - 获取观点价格评估

### NFT
- `POST /api/v1/nfts/mint` - 铸造NFT
- `GET /api/v1/nfts` - 获取NFT列表
- `POST /api/v1/nfts/transfer` - 转移NFT
- `POST /api/v1/nfts/purchase` - 购买NFT
- `GET /api/v1/nfts/mint-estimate` - 铸造费用估算
- `GET /api/v1/nfts/purchase-estimate` - 购买价格估算

### 系统
- `GET /` - 根路径
- `GET /health` - 健康检查

## 数据库模型

### Opinions 表
- 存储用户发布的观点内容
- 包含地址、内容、铸造状态、评估价格等字段

### NFT 表
- 存储NFT相关信息
- 包含token_id、所有者地址、价格、销售状态等字段

## 开发说明

项目采用模块化结构：
- `main.py` - 应用入口和配置
- `app/models.py` - 数据模型定义
- `app/routers/` - API路由模块
- `app/database.py` - 数据库配置

## API 文档

启动服务后，可访问以下地址查看API文档：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
