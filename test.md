## Login
```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "address":"0x566ebc2a42a92bbfea494fce84b6f3b3ce1feab284eab6a6f38435866c1e8338"
  }'
```

```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/auth/login_signature" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0x566ebc2a42a92bbfea494fce84b6f3b3ce1feab284eab6a6f38435866c1e8338",
    "challenge": "b524976c60ad27e927962bdc7e8c8e7155bc11acaed7d4fd1bf2c863162ec55f",
    "signature": "0x123456789"
  }'
```

## Opinion

### create
```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU4OTQxMjgyLCJpYXQiOjE3NTgzMzY0ODJ9.rpfVaiibKBWUU0wR8ZEzzJsZYsNOX-CYPheRK1VyHWw" \
  -d '{
    "content": "区块链技术将改变世界"
  }'
```

### get list
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/ranking" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU4OTQxMjgyLCJpYXQiOjE3NTgzMzY0ODJ9.rpfVaiibKBWUU0wR8ZEzzJsZYsNOX-CYPheRK1VyHWw" \
```