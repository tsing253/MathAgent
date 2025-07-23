创建数据库`math_agent`

创建环境变量：
- `cp env.example .env`
创建后需要填写环境变量

初始化数据库：
- `python manage.py makemigrations`
- `python manage.py migrate`
- `python manage.py create_sample_data`

运行：
- `python manage.py runserver`