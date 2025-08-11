# 使用官方Python镜像作为基础
FROM python:3.11-slim

# 设置容器内工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个项目代码（注意.dockerignore配置）
COPY . .

# 设置环境变量
ENV PYTHONUNBUFFERED 1

# 暴露端口（与Django runserver默认端口一致）
EXPOSE 8000

# 启动命令（确保manage.py在/app目录下）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
