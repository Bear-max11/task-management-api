# 使用 Python 3.12 作为基础镜像
FROM docker.m.daocloud.io/library/python:3.12-slim
# 设置容器内的工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露服务端口
EXPOSE 8000

# 启动 FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
