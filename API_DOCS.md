# MoonCL Server API 接口文档

## 基本信息

- **服务名称**: MoonCL Server API
- **版本**: 1.0.0
- **基础URL**: `https://distributor-professionals-same-speakers.trycloudflare.com`
- **协议**: HTTP/HTTPS

## 认证方式

基于签名的JWT认证机制。需要认证的接口需要在请求头中包含：

```
Authorization: Bearer <JWT_TOKEN>
```


---

## 1. 认证模块 (Authentication)

### 1.1 发起登录挑战

**接口**: `POST /api/v1/auth/login`

**描述**: 生成登录挑战，用户需要使用私钥对挑战进行签名

**请求参数**:
```json
{
  "address": "string"  
}
```

**响应**:
```json
{
  "success": true,
  "challenge": "string",  
  "token": null,
  "reason": null
}
```

**状态码**:
- `200`: 成功
- `400`: 地址参数缺失

---

### 1.2 验证签名并获取Token

**接口**: `POST /api/v1/auth/login_signature`

**描述**: 验证用户对挑战的签名，成功后返回JWT Token

**请求参数**:
```json
{
  "address": "string",    
  "signature": "string",  
  "challenge": "string"   
}
```

**响应**:
```json
{
  "success": true,
  "challenge": null,
  "token": "string",  
  "reason": null
}
```

**状态码**:
- `200`: 验证成功
- `400`: 参数错误或签名验证失败

---


## 2. NFT模块 (3个接口)
- `GET /api/v1/nfts/ranking` - 获取NFT排行榜
- `GET /api/v1/nfts/detail/{token_id}` - 获取NFT详情
- `GET /api/v1/nfts/user/{user_address}` - 获取用户NFT列表

### 2.1 获取NFT排行榜

**接口**: `GET /api/v1/nfts/ranking`

**描述**: 获取NFT排行榜，按价格排序

**查询参数**:
- `limit` (integer, 可选): 返回数量限制，默认20

**响应**:
```json
[
  {
    "token_id": 1,
    "owner_address": "string",
    "content": "string",
    "evaluate_price": 0.01,
    "current_price": 0.5,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

**状态码**:
- `200`: 获取成功
- `500`: 服务器内部错误

---

### 2.2 获取NFT详情

**接口**: `GET /api/v1/nfts/detail/{token_id}`

**描述**: 根据token_id获取NFT详细信息

**路径参数**:
- `token_id` (integer): NFT的token ID

**响应**:
```json
{
  "token_id": 1,
  "owner_address": "string",
  "content": "string",
  "evaluate_price": 0.01,
  "current_price": 0.5,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

**状态码**:
- `200`: 获取成功
- `404`: NFT不存在

---

### 2.3 获取用户NFT列表

**接口**: `GET /api/v1/nfts/user/{user_address}`

**描述**: 获取指定用户拥有的所有NFT

**路径参数**:
- `user_address` (string): 用户区块链地址

**响应**:
```json
[
  {
    "token_id": 1,
    "owner_address": "string",
    "content": "string",
    "evaluate_price": 0.01,
    "current_price": 0.5,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

**状态码**:
- `200`: 获取成功
- `500`: 服务器内部错误

---

## 3. 系统接口

### 3.1 根路径

**接口**: `GET /`

**描述**: API根路径，返回基本信息

**响应**:
```json
{
  "message": "MoonCL Server API"
}
```

---

### 3.2 健康检查

**接口**: `GET /health`

**描述**: 服务健康状态检查

**响应**:
```json
{
  "status": "healthy"
}
```

---

## 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "detail": "错误描述信息"
}
```

## 常见状态码

- `200`: 请求成功
- `400`: 请求参数错误
- `401`: 未认证或认证失败
- `404`: 资源不存在
- `500`: 服务器内部错误
