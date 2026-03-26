from folder1.kis_auth import get_access_token

token1 = get_access_token()
token2 = get_access_token()

print(token1[:20])
print(token2[:20])

if token1 == token2:
    print("같은 토큰 재사용 성공")
else:
    print("토큰이 새로 발급됨")