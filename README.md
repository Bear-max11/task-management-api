# Task Management API —— 任务管理系统后端

一个基于 Python 和 FastAPI 开发的 RESTful 任务管理系统后端项目，实现了用户注册登录、JWT 身份认证、任务管理、用户数据隔离以及 Docker 容器化部署。

本项目主要用于学习和实践 Python 后端开发中的核心技术，包括 Web API 开发、数据库操作、身份认证、权限控制和容器化部署。

## 一、项目功能

- **用户注册**：支持用户注册，校验用户名和邮箱的唯一性。
- **用户登录**：基于 OAuth2 密码模式实现用户身份认证。
- **JWT 身份认证**：登录成功后生成 JWT Access Token，用于访问受保护的 API。
- **密码安全存储**：使用 Argon2 算法对用户密码进行哈希处理。
- **任务管理**：支持任务的创建、查询、修改、删除以及完成状态更新。
- **用户数据隔离**：每个用户只能访问和管理属于自己的任务。
- **数据库持久化**：使用 SQLite 和 SQLAlchemy ORM 存储用户及任务数据。
- **容器化部署**：使用 Docker 和 Docker Compose 运行项目。
- **API 在线文档**：通过 Swagger UI 自动生成接口文档，方便调试和测试。

## 二、技术栈

| 技术 | 用途 |
|---|---|
| Python 3.12 | 主要开发语言 |
| FastAPI | Web 后端框架 |
| Uvicorn | ASGI 服务器 |
| SQLAlchemy | ORM 数据库操作 |
| SQLite | 关系型数据库 |
| Pydantic | 数据校验 |
| PyJWT | JWT 身份认证 |
| pwdlib + Argon2 | 密码哈希 |
| Docker | 容器化 |
| Docker Compose | 容器编排 |
| Git | 版本控制 |

## 三、项目结构

```text
task-management-api/
├── main.py                 # 应用入口
├── config.py               # 配置管理
├── database.py             # 数据库连接与配置
├── dependencies.py         # 依赖注入及身份认证
├── security.py             # 密码哈希与 JWT 处理
├── migrate.py              # 数据库迁移脚本
├── models/                 # 数据库模型
│   ├── __init__.py
│   ├── user.py
│   └── task.py
├── schemas/                # Pydantic 数据模型
│   ├── __init__.py
│   ├── users.py
│   └── tasks.py
├── routers/                # API 路由
│   ├── users.py
│   └── tasks.py
├── Dockerfile              # Docker 镜像构建文件
├── docker-compose.yml      # Docker Compose 配置
├── requirements.txt        # 项目依赖
├── .env.example            # 环境变量示例
├── .gitignore
└── .dockerignore
```

## 四、API 接口

### 1. 用户认证接口

| 请求方式 | 接口路径 | 功能 | 是否需要认证 |
|---|---|---|---|
| POST | `/users/register` | 用户注册 | 否 |
| POST | `/users/login` | 用户登录，获取 JWT | 否 |

### 2. 任务管理接口

| 请求方式 | 接口路径 | 功能 | 是否需要认证 |
|---|---|---|---|
| POST | `/tasks/` | 创建任务 | 是 |
| GET | `/tasks/` | 获取当前用户的任务列表 | 是 |
| GET | `/tasks/{task_id}` | 根据 ID 获取任务 | 是 |
| PUT | `/tasks/{task_id}` | 更新任务信息 | 是 |
| DELETE | `/tasks/{task_id}` | 删除任务 | 是 |
| PATCH | `/tasks/{task_id}/status` | 修改任务完成状态 | 是 |

所有任务接口均基于当前登录用户进行权限校验，用户无法访问或修改其他用户的任务。

## 五、本地运行

### 1. 环境要求

- Python 3.12+
- pip
- Git

### 2. 克隆项目

```bash
git clone https://github.com/Bear-max11/task-management-api.git

cd task-management-api
```

### 3. 创建虚拟环境

```bash
python3 -m venv venv

source venv/bin/activate
```

### 4. 安装项目依赖

```bash
pip install -r requirements.txt
```

### 5. 配置环境变量

复制环境变量示例文件：

```bash
cp .env.example .env
```

生成随机密钥：

```bash
openssl rand -hex 32
```

将生成的密钥填入 `.env` 文件：

```env
SECRET_KEY=your_generated_secret_key
```

注意：不要将真实的 `.env` 文件或密钥上传到 GitHub。

### 6. 启动项目

```bash
uvicorn main:app --reload
```

项目启动后，可以通过以下地址访问：

```text
http://127.0.0.1:8000
```

## 六、Docker 部署

项目支持通过 Docker Compose 进行容器化运行。

### 1. 构建并启动容器

```bash
sudo docker compose up -d --build
```

### 2. 查看容器运行状态

```bash
sudo docker compose ps
```

### 3. 访问 API 文档

```text
http://localhost:8000/docs
```

### 4. 停止容器

```bash
sudo docker compose down
```

项目使用 Docker Named Volume 持久化 SQLite 数据库。停止容器不会自动删除数据库数据。

注意：如果需要保留数据，不要使用 `docker compose down -v`。

## 七、身份认证与权限控制

项目采用 JWT 实现用户身份认证，主要流程如下：

1. 用户通过注册接口创建账号。
2. 用户通过登录接口提交用户名和密码。
3. 后端验证密码，并生成 JWT Access Token。
4. 用户携带 Token 访问需要身份认证的接口。
5. 后端解析 Token，获取当前登录用户。
6. 根据当前用户 ID 过滤任务数据，实现用户之间的数据隔离。

在安全性方面：

- 使用 Argon2 对密码进行哈希处理。
- 使用 JWT 对用户身份进行认证。
- 通过环境变量管理 JWT 签名密钥。
- 对任务查询、修改和删除操作进行用户权限校验。

## 八、项目说明

本项目是一个 Python 后端实战学习项目，重点实践了 RESTful API 设计、模块化开发、ORM 数据库操作、JWT 身份认证、多用户权限隔离以及 Docker 容器化部署等后端开发基础能力。

当前项目使用 SQLite 作为数据库，并通过 Docker Compose 实现容器化运行，后续可以在此基础上继续学习和实践 PostgreSQL、Redis、自动化测试等技术。

## 九、作者

**GitHub：** [Bear-max11](https://github.com/Bear-max11)

**项目地址：** https://github.com/Bear-max11/task-management-api
