# fixtures 用于初始化数据库

# 导出数据
python manage.py dumpdata courese --indent=2 --output=fixtures\initial_data.json

# 导入数据
python manage.py  loaddata fixtures\initial_data.json