# 使用官方 Python 作为基础镜像
FROM python:3.9-alpine

# 设置工作目录
WORKDIR /app

# 复制项目文件到容器中
COPY . .

# 安装项目依赖
RUN apk add --no-cache bash \
    && pip install --no-cache-dir -r requirements.txt

# 设置环境变量（可选）
ENV TZ=Asia/Shanghai

# 指定容器启动时运行的命令
CMD ["python", "sample.py"]