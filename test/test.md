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
    "challenge": "ab39b26fa59e68aaf0596abe4844c95b9f28c5e38d9951b03eba24f851ec7802",
    "signature": "0x123456789"
  }'
```

## Opinion

### create
```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxOTIzLCJpYXQiOjE3NTkwNjcxMjN9.0pMz4WKHtjp55kCqwvgflyeL0_udHCvwkRCaRBHnOQA" \
  -d '{
    "content": "区块链技术将改变世界, 它将带来新的机遇和挑战"
  }'
```

### get ranking list
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/ranking" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```

### get ranking list with parameters
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/ranking?sort_by=price&limit=20&offset=0" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```

### get user opinions
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/user/0x566ebc2a42a92bbfea494fce84b6f3b3ce1feab284eab6a6f38435866c1e8338" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```

### get opinion detail
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/detail/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```

### get opinion price
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/opinions/detail/1/price" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE7NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```

## NFT

### mint NFT
```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/nfts/mint" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxOTIzLCJpYXQiOjE3NTkwNjcxMjN9.0pMz4WKHtjp55kCqwvgflyeL0_udHCvwkRCaRBHnOQA" \
  -d '{
    "opinion_id": 1
  }'
```

### get mint estimate
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/nfts/mint/estimate?opinion_id=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```

### get purchase estimate
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/nfts/purchase/estimate?nft_id=1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```

### purchase NFT
```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/nfts/purchase" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxOTIzLCJpYXQiOjE3NTkwNjcxMjN9.0pMz4WKHtjp55kCqwvgflyeL0_udHCvwkRCaRBHnOQA" \
  -d '{
    "nft_id": 1
  }'
```

### transfer NFT
```shell
curl -X POST "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/nfts/transfer" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxOTIzLCJpYXQiOjE3NTkwNjcxMjN9.0pMz4WKHtjp55kCqwvgflyeL0_udHCvwkRCaRBHnOQA" \
  -d '{
    "nft_id": 1,
    "to_address": "0x742d35Cc6634C0532925a3b8D4C9db96590c6C87"
  }'
```

### get user NFTs
```shell
curl -X GET "https://distributor-professionals-same-speakers.trycloudflare.com/api/v1/nfts/user/0x566ebc2a42a92bbfea494fce84b6f3b3ce1feab284eab6a6f38435866c1e8338" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHg1NjZlYmMyYTQyYTkyYmJmZWE0OTRmY2U4NGI2ZjNiM2NlMWZlYWIyODRlYWI2YTZmMzg0MzU4NjZjMWU4MzM4IiwiZXhwIjoxNzU5NjcxMjQwLCJpYXQiOjE3NTkwNjY0NDB9.mxsq25CourgmFHh-Kt3QMbQXRLh0ox1AN3MgKvOiy3k"
```


0xe8bf99e698afe4b880e4b8aae6b58be8af95e8a782e782b9e58685e5aeb9efbc8ce794a8e4ba8ee9aa8ce8af81e59ca82043656c6f20e7bd91e7bb9ce4b88ae79a84204e465420e993b8e980a0e58a9fe883bd

data:application/json;base64,eyJuYW1lIjogIk9waW5pb24gIzk5OSIsICJkZXNjcmlwdGlvbiI6ICLljLrlnZfpk77mioDmnK/lsIbmlLnlj5jkuJbnlYwsIOWug+WwhuW4puadpeaWsOeahOacuumBh+WSjOaMkeaImCIsICJhdHRyaWJ1dGVzIjogW3sidHJhaXRfdHlwZSI6ICJPcGluaW9uIElEIiwgInZhbHVlIjogOTk5fSwgeyJ0cmFpdF90eXBlIjogIkNyZWF0b3IiLCAidmFsdWUiOiAiMHhkMjhGNDhBNTk3NzFFMTdmQ0Q5Y0RhRDkzRDA4OGZiOTYzZGFjNTU0In0sIHsidHJhaXRfdHlwZSI6ICJDb250ZW50IExlbmd0aCIsICJ2YWx1ZSI6IDIzfSwgeyJ0cmFpdF90eXBlIjogIkNyZWF0ZWQgRGF0ZSIsICJ2YWx1ZSI6ICIyMDI1LTA5LTI5In0sIHsidHJhaXRfdHlwZSI6ICJDaGFpbiBJRCIsICJ2YWx1ZSI6IDExMTQyMjIwfV0sICJjb250ZW50IjogIuWMuuWdl+mTvuaKgOacr+WwhuaUueWPmOS4lueVjCwg5a6D5bCG5bim5p2l5paw55qE5py66YGH5ZKM5oyR5oiYIn0=