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
    "challenge": "58ef0241db9299a9917413157eaf640e1c0c88798a201ed53f1394f13ea28d27",
    "signature": "0x123456789"
  }'
```

## Opinion

### create
```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k" \
  -d '{
    "content": "区块链技术将改变世界, 它将带来新的机遇和挑战"
  }'
```

### get list
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/ranking" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k" \
```