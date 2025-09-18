## Login
```shell
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "address":"0x566ebc2a42a92bbfea494fce84b6f3b3ce1feab284eab6a6f38435866c1e8338"
  }'
```

```shell
curl -X POST "http://localhost:8000/api/v1/auth/login_signature" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0x566ebc2a42a92bbfea494fce84b6f3b3ce1feab284eab6a6f38435866c1e8338",
    "challenge": "4a44f9731b5f4e6daedea0fdc74da38ffbfaecb562ad514c62e940e7b1fa524f",
    "signature": "0x123456789"
  }'
```

## Opinion

### create
```shell
curl -X POST "http://localhost:8000/api/v1/opinions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU4NjI5ODM3LCJpYXQiOjE3NTgwMjUwMzd9.o15kOQzbqdUDY4eLuKmucm2Cjoxf9QZqnd6zyWirIv4" \
  -d '{
    "content": "区块链技术将改变世界"
  }'
```

### get list
```shell
curl -X GET "http://localhost:8000/api/v1/opinions/ranking" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU4NjI5ODM3LCJpYXQiOjE3NTgwMjUwMzd9.o15kOQzbqdUDY4eLuKmucm2Cjoxf9QZqnd6zyWirIv4"
```