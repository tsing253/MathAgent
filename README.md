# Math Agent - 数学AI对话平台

## 项目概述
基于Django的数学AI对话平台，集成Coze AI服务，提供用户管理、对话记录和AI数学问题解答功能。

## 功能特点
- 用户认证与管理(学生/老师角色)
- 对话历史记录
- 与Coze AI的集成对话
- RESTful API接口
- 响应式前端界面

## 技术栈
- 后端: Django 5.2, Django REST framework
- 数据库: MySQL
- AI服务: Coze API
- 前端: HTML, JavaScript, CSS

## 安装指南

### 前提条件
- Python 3.8+
- MySQL 5.7+
- Node.js (可选，用于前端开发)

### 1. 克隆仓库
```bash
git clone [仓库地址]
cd myproject
```

### 2. 创建Python虚拟环境并安装依赖
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. 数据库设置
创建数据库`math_agent`

### 4. 环境变量配置
复制环境变量模板并填写实际值：
```bash
cp env.example .env
```

需要配置的环境变量包括：
- DB_PASSWORD: MySQL数据库密码
- COZE_API_TOKEN: Coze API访问令牌
- BOTID: Coze机器人ID

## 初始化与运行

### 初始化数据库
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py create_sample_data
```

### 运行开发服务器
```bash
python manage.py runserver
```

访问 http://localhost:8000 使用应用

## API文档

### 认证
使用Token认证，在请求头中添加：
```
Authorization: Token [your_token]
```

### 可用端点
- `GET /api/test/`: 测试接口
- `POST /api/save_conversation/`: 保存对话
- `POST /api/coze_proxy/`: Coze AI代理接口

## 贡献指南
欢迎提交Pull Request。请确保:
1. 遵循现有代码风格
2. 包含适当的测试
3. 更新相关文档

## 许可证
MIT License
