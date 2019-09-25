# Market-Admin

market-admin 是一个使用[fastapi](https://fastapi.tiangolo.com/)搭建的商城后台管理系统.

## Contents

- [安装](#安装)
- [使用](#使用)
- [许可证](#许可证)

## 安装
1. 获取项目源代码
```bash
go -get https://github.com/Huangkai1008/market-admin
```

2. 确保你安装了[poetry](https://github.com/sdispater/poetry)
```bash
pip install poetry
```

## 使用

```bash
poetry install                  # Add the libs
poetry shell                    # Start the virtualenvs
uvicorn app.main:app --reload   # Start the uvicorn server
```

## 许可证
[MIT](https://www.mit-license.org/)

    
