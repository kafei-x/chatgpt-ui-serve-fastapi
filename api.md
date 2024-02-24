fastapi
tortoise-orm[aiosqlite, aiomysql]
# 获取Form参数需要用到
python-multipart
PyJWT
# 用于安全生成和验证令牌和签名的 Python 库
itsdangerous
uvicorn[standard]
# 添加命令行功能
typer[all]
python-dotenv
# 迁移数据库，依赖tortoise-orm    
# aerich
langchain


-i https://pypi.tuna.tsinghua.edu.cn/simple








/api/chat/settings/

配置

```
[
    {
        "name": "open_frugal_mode_control",
        "value": "True"
    },
    {
        "name": "open_registration",	# 开启注册
        "value": "True"
    },
    {
        "name": "open_web_search",		# 开启web搜索
        "value": "False"
    },
    {
        "name": "open_api_key_setting",	# 开启openapi_key设置
        "value": "False"
    }
]
```



/api/chat/conversation

```
get

res
[
    {
        "id": 6,
        "topic": "快速API",
        "created_at": "2024-02-22T07:24:27.290204Z"
    },
    {
        "id": 5,
        "topic": "你好。",
        "created_at": "2024-02-22T07:10:19.363980Z"
    },
    {
        "id": 4,
        "topic": "Hello",
        "created_at": "2024-02-22T05:28:01.637666Z"
    },
    {
        "id": 3,
        "topic": "无法生成标题，因为内容太过简单。",
        "created_at": "2024-02-21T13:52:26.318745Z"
    }
]
```











/api/account/registration/

```
{"username":"user2","email":"1332189825@qq.com","password1":"kafei2222","password2":"kafei2222","code":""}


success response
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NTgwMzkzLCJpYXQiOjE3MDg0OTM5OTMsImp0aSI6IjMxOWZhYjYzN2I5ZjRiYWNhN2M1YTc1NDJiYmJmMWU5IiwidXNlcl9pZCI6M30.gEyo_eowu7OCo_0OmpUoTobQn7WJIIsmdK8AOElFRzQ",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwODU4MDM5MywiaWF0IjoxNzA4NDkzOTkzLCJqdGkiOiJlNWI1NDQ1Yjg3ZTc0Y2NhYjU3MjkyYzBlNTdlNTk0YyIsInVzZXJfaWQiOjN9.gKGWmg2wcpML071gcw245uaktAuYBDxfqlZp5anKtwo",
    "user": {
        "username": "use2",
        "email": "1332189826@qq.com",
        "first_name": "",
        "last_name": ""
    },
    "email_verification_required": "none"
}

error response
{
    "username": [
        "A user with that username already exists."
    ],
    "email": [
        "A user is already registered with this e-mail address."
    ]
}


```



/api/account/login/

```
POST
{"username":"user","password":"kafei22222"}

res
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NTk3MDM5LCJpYXQiOjE3MDg1MTA2MzksImp0aSI6IjI0M2JkMzc3MGNjNzQzMzFhYTcyMmVkMWY3OGYyZTE3IiwidXNlcl9pZCI6M30.hnnEAPRfbuXbhHPYfTVLy10ww1YJtoWueYcG3i4zXs4",
    "refresh_token": "",
    "user": {
        "username": "use2",
        "email": "1332189826@qq.com",
        "first_name": "",
        "last_name": ""
    }
}

err res
{"non_field_errors":["Unable to log in with provided credentials."]}
```



```
Request URL:
http://127.0.0.1:3002/api/account/login/
Request Method:
POST
Status Code:
200 OK
Remote Address:
127.0.0.1:3002
Referrer Policy:
strict-origin-when-cross-origin
Access-Control-Allow-Origin:
*
Allow:
POST, OPTIONS
Connection:
close
Content-Length:
352
Content-Type:
application/json
Cross-Origin-Opener-Policy:
same-origin
Date:
Wed, 21 Feb 2024 10:17:19 GMT
Referrer-Policy:
same-origin
Server:
WSGIServer/0.2 CPython/3.10.13
Set-Cookie:
auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA4NTk3MDM5LCJpYXQiOjE3MDg1MTA2MzksImp0aSI6IjI0M2JkMzc3MGNjNzQzMzFhYTcyMmVkMWY3OGYyZTE3IiwidXNlcl9pZCI6M30.hnnEAPRfbuXbhHPYfTVLy10ww1YJtoWueYcG3i4zXs4; expires=Thu, 22 Feb 2024 10:17:19 GMT; HttpOnly; Max-Age=86400; Path=/; SameSite=Lax
```





/api/conversation/

```
{"name":"gpt-3.5-turbo","frequency_penalty":0,"presence_penalty":0,"total_tokens":4096,"max_tokens":1000,"temperature":0.7,"top_p":1,"openaiApiKey":null,"message":[{"content":"fastapi","tool":"chat","message_type":0}],"conversationId":null,"frugalMode":true}
```

no res





/api/gen_title/

```

{"conversationId":6,"prompt":"为以下内容生成一个不超过10个字的简短标题。 \n\n内容: ","openaiApiKey":null}


response
{"title":"快速API"}

```







