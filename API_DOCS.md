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

## 2. 观点模块 (Opinions) - 5个接口
- `POST /api/v1/opinions/` - 创建观点
- `GET /api/v1/opinions/{opinion_id}` - 获取观点详情
- `GET /api/v1/opinions/user/{user_address}` - 获取用户观点列表
- `GET /api/v1/opinions/ranking` - 获取观点排行榜
- `GET /api/v1/opinions/{opinion_id}/price` - 获取观点价格

### 2.1 创建观点

**接口**: `POST /api/v1/opinions/`

**描述**: 创建新的观点内容

**认证**: 需要JWT Token

**请求参数**:
```json
{
  "content": "string"
}
```

**响应**:
```json
{
  "id": 1,
  "address": "string",
  "content": "string",
  "is_minted": false,
  "evaluate_price": 0.01,
  "created_at": "string",
  "updated_at": null
}
```

**状态码**:
- `200`: 创建成功
- `401`: 未认证
- `500`: 服务器内部错误

---

### 2.2 获取观点详情

**接口**: `GET /api/v1/opinions/detail/{opinion_id}`

**描述**: 根据ID获取观点详细信息

**路径参数**:
- `opinion_id` (integer): 观点ID

**响应**:
```json
{
  "id": 1,
  "address": "string",
  "content": "string",
  "is_minted": false,
  "evaluate_price": 0.01,
  "created_at": "string",
  "updated_at": null
}
```

**状态码**:
- `200`: 获取成功
- `404`: 观点不存在

---


### 2.3 获取用户观点列表

**接口**: `GET /api/v1/opinions/user/{user_address}`

**描述**: 获取指定用户的所有观点

**路径参数**:
- `user_address` (string)

**响应**:
```json
[
  {
    "id": 1,
    "title": "string",
    "content": "string",
    "address": "string",
    "created_at": "string",
    "likes": 0,
    "is_minted": false,
    "nft_id": null
  }
]
```

**状态码**:
- `200`: 获取成功
- `500`: 服务器内部错误

---

### 2.4 获取观点排行榜

**接口**: `GET /api/v1/opinions/ranking`

**描述**: 获取观点排行榜，支持多种排序方式

**查询参数**:
- `sort_by` (string, 可选): 排序方式，默认"price"
  - `price` - 按价格排序
  - `recent` - 按创建时间排序
- `limit` (integer, 可选): 返回数量限制，默认10，最大100
- `offset` (integer, 可选): 偏移量，用于分页，默认0

**响应**:
```json
[
  {
    "id": 1,
    "address": "string",
    "content": "string",
    "is_minted": true,
    "evaluate_price": 0.5,
    "created_at": "string",
    "updated_at": null
  }
]
```

**状态码**:
- `200`: 获取成功
- `400`: 请求参数错误
- `500`: 服务器内部错误

---

### 2.5 获取观点价格

**接口**: `GET /api/v1/opinions/detail/{opinion_id}/price`

**描述**: 获取指定观点的当前价格信息

**路径参数**:
- `opinion_id` (integer): 观点ID

**响应**:
```json
{
  "opinion_id": 1,
  "price": 0.01,
}
```

**状态码**:
- `200`: 获取成功
- `404`: 观点不存在
- `500`: 服务器内部错误

---


## 3. NFT模块 (6个接口)
- `POST /api/v1/nfts/mint` - 铸造NFT
- `GET /api/v1/nfts/mint/estimate` - 获取NFT铸造估价
- `GET /api/v1/nfts/purchase/estimate` - 获取NFT购买估价
- `POST /api/v1/nfts/purchase` - 购买NFT
- `POST /api/v1/nfts/transfer` - 转移NFT
- `GET /api/v1/nfts/user/{user_address}` - 获取用户NFT列表

### 3.1 铸造NFT

**接口**: `POST /api/v1/nfts/mint`

**描述**: 将观点铸造为NFT

**认证**: 需要JWT Token

**请求参数**:
```json
{
  "opinion_id": 1  
}
```

**响应**:
```json
{
  "success": true,
  "nft_id": 1,
  "token_id": "string",
  "transaction_hash": "string",
  "error": null
}
```

**状态码**:
- `200`: 铸造成功
- `400`: 请求参数错误或业务逻辑错误
- `401`: 未认证
- `500`: 服务器内部错误

---

### 3.2 获取NFT铸造估价

**接口**: `GET /api/v1/nfts/mint/estimate`

**描述**: 获取NFT铸造所需的Gas费用估价

**查询参数**:
- `opinion_id` (integer): 观点ID

**响应**:
```json
{
  "success": true,
  "opinion_id": 1,
  "estimated_fee": 0.001,
  "error": null
}
```

**状态码**:
- `200`: 获取成功
- `400`: 观点ID无效或已铸造
- `500`: 服务器内部错误

---

### 3.3 获取NFT购买估价

**接口**: `GET /api/v1/nfts/purchase/estimate`

**描述**: 获取购买NFT的费用估价（包含交易费用）

**查询参数**:
- `nft_id` (integer): NFT ID

**响应**:
```json
{
  "success": true,
  "nft_id": 1,
  "estimated_price": 0.5,
  "currency": "ETH",
  "error": null
}
```

**状态码**:
- `200`: 获取成功
- `400`: NFT不存在或不在售
- `500`: 服务器内部错误

---

### 3.4 购买NFT

**接口**: `POST /api/v1/nfts/purchase`

**描述**: 购买指定的NFT（交易NFT）

**认证**: 需要JWT Token

**请求参数**:
```json
{
  "nft_id": 1
}
```

**响应**:
```json
{
  "success": true,
  "nft_id": 1,
  "buyer": "string",
  "seller": "string",
  "price": 0.5,
  "currency": "ETH",
  "transaction_hash": "string",
  "error": null
}
```

**状态码**:
- `200`: 购买成功
- `400`: 请求参数错误、NFT不在售或价格不匹配
- `401`: 未认证
- `403`: 不能购买自己的NFT
- `500`: 服务器内部错误

---

### 3.5 转移NFT

**接口**: `POST /api/v1/nfts/transfer`

**描述**: 免费转移NFT所有权（非交易转移）

**认证**: 需要JWT Token

**请求参数**:
```json
{
  "nft_id": 1,
  "to_address": "string"
}
```

**响应**:
```json
{
  "success": true,
  "nft_id": 1,
  "from_address": "string",
  "to_address": "string",
  "transaction_hash": "string",
  "error": null
}
```

**状态码**:
- `200`: 转移成功
- `400`: 请求参数错误或业务逻辑错误
- `401`: 未认证
- `500`: 服务器内部错误

---

### 3.6 获取用户NFT列表

**接口**: `GET /api/v1/nfts/user/{user_address}`

**描述**: 获取用户拥有的所有NFT

**路径参数**:
- `user_address` (string): 用户区块链地址

**响应**:
```json
[
  {
    "id": 1,
    "token_id": "string",
    "owner_address": "string",
    "mint_price": 0.01,
    "current_price": 0.5,
    "is_for_sale": true,
    "created_at": "string",
    "opinion_content": "string"
  }
]
```

**状态码**:
- `200`: 获取成功
- `500`: 服务器内部错误

---

## 4. 系统接口

### 4.1 根路径

**接口**: `GET /`

**描述**: API根路径，返回基本信息

**响应**:
```json
{
  "message": "MoonCL Server API"
}
```

---

### 4.2 健康检查

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



## 注意事项

1. **认证Token有效期**: JWT Token有效期为7天
2. **CORS配置**: API支持跨域请求
3. **数据库**: 使用MySQL存储数据
4. **区块链集成**: 基于Sui区块链进行身份验证和NFT操作
5. **错误处理**: 所有接口都包含适当的错误处理和状态码返回