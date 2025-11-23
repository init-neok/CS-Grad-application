# 快速开始指南

## 1. 初始化数据库

如果要重新生成带有500+真实数据的数据库：

```bash
python init_db.py
```

**输出示例：**
```
Starting data initialization...
...
Database initialization complete!
Created 100 users with 565 total applications

Statistics:
  Total Applications: 565
  Accepts: 133 (23.5%)
  Rejects: 145 (25.7%)
  Waitlists: 287 (50.8%)
  Unique Universities: 39
  Unique Programs: 14
```

## 2. 启动应用

```bash
python app.py
```

默认运行在 `http://localhost:5000`

## 3. 数据库结构

### 核心表

| 表名 | 行数 | 说明 |
|------|------|------|
| users | 100 | 申请者账户 |
| profiles | 100 | 申请者基本信息 |
| application_records | 565 | 申请记录 |
| educations | 100 | 学历记录 |
| test_scores | 143 | 考试成绩（GRE/TOEFL/IELTS） |
| experiences | 207 | 工作/实习/研究经验 |
| publications | 86 | 发表论文 |
| recommendation_letters | 258 | 推荐信 |

### 关键数据分布

**申请结果：**
- Accept: 23.5%
- Reject: 25.7%
- Waitlist: 50.8%

**学位类型：**
- Master: 51.3%
- PhD: 48.7%

**地理分布：**
- 美国: 20所大学
- 加拿大: 5所
- 英国: 5所
- 欧洲: 2所
- 亚洲: 7所

## 4. API 端点概览

### 认证
```
POST   /api/register        - 用户注册
POST   /api/login           - 用户登录
POST   /api/logout          - 用户登出
```

### 个人信息
```
GET    /api/profile         - 获取个人信息
PUT    /api/profile         - 更新个人信息
```

### 教育
```
GET    /api/education       - 获取所有学历
POST   /api/education       - 添加学历
PUT    /api/education/<id>  - 更新学历
DELETE /api/education/<id>  - 删除学历
```

### 考试成绩
```
GET    /api/scores          - 获取所有成绩
POST   /api/scores          - 添加成绩
PUT    /api/scores/<id>     - 更新成绩
DELETE /api/scores/<id>     - 删除成绩
```

### 工作经验
```
GET    /api/experiences     - 获取所有经验
POST   /api/experiences     - 添加经验
PUT    /api/experiences/<id> - 更新经验
DELETE /api/experiences/<id> - 删除经验
```

### 出版物
```
GET    /api/publications    - 获取所有论文
POST   /api/publications    - 添加论文
PUT    /api/publications/<id> - 更新论文
DELETE /api/publications/<id> - 删除论文
```

### 推荐信 (新增)
```
GET    /api/recommendation-letters     - 获取所有推荐信
POST   /api/recommendation-letters     - 添加推荐信
PUT    /api/recommendation-letters/<id> - 更新推荐信
DELETE /api/recommendation-letters/<id> - 删除推荐信
```

### 申请
```
GET    /api/applications/my          - 获取我的申请
POST   /api/applications             - 创建申请
PUT    /api/applications/<id>        - 更新申请
DELETE /api/applications/<id>        - 删除申请
```

### 公共查询
```
GET    /api/search/applications      - 搜索申请
GET    /api/analytics/universities   - 大学分布
GET    /api/analytics/programs       - 项目分布
GET    /api/analytics/regional       - 区域分布
GET    /api/match/suggestions        - 匹配建议
```

## 5. 示例查询

### 查看申请记录

```bash
# 搜索 Stanford 的申请
curl "http://localhost:5000/api/search/applications?university=Stanford"

# 按结果过滤
curl "http://localhost:5000/api/search/applications?result=Accept"

# 特定国家
curl "http://localhost:5000/api/search/applications?country=USA"
```

### 分析数据

```bash
# 大学统计
curl "http://localhost:5000/api/analytics/universities"

# 项目统计
curl "http://localhost:5000/api/analytics/programs"

# 区域统计
curl "http://localhost:5000/api/analytics/regional"
```

## 6. 数据特点

### 大学列表 (39所)
```
Stanford University, MIT, Carnegie Mellon, UC Berkeley,
University of Washington, UT Austin, UIUC, Cornell,
Princeton, Harvard, UC San Diego, Wisconsin, Georgia Tech,
UPenn, Northwestern, Columbia, Yale, Michigan, UC Irvine,
Purdue, Toronto, UBC, McGill, Waterloo, McMaster,
Cambridge, Oxford, Imperial College London, UCL, Edinburgh,
Manchester, ETH Zurich, TU Munich, Delft, NUS, NTU,
Tokyo, Seoul National, HKUST
```

### 项目列表 (14个)
```
Computer Science, Machine Learning, Artificial Intelligence,
Data Science, Software Engineering, Computer Engineering,
Cybersecurity, Human-Computer Interaction, Computer Networks,
Computer Vision, Natural Language Processing, Distributed Systems,
Database Systems, Cloud Computing
```

## 7. 数据清理

### 完全重置数据库
```python
from app import create_app, db

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
```

### 仅删除应用记录
```python
from app import create_app, db, ApplicationRecord

app = create_app()
with app.app_context():
    ApplicationRecord.query.delete()
    db.session.commit()
```

## 8. 验证数据

运行验证脚本查看所有统计信息：

```bash
python3 << 'EOF'
from app import create_app, db, ApplicationRecord

app = create_app()
with app.app_context():
    total = ApplicationRecord.query.count()
    accepts = ApplicationRecord.query.filter_by(result="Accept").count()
    rejects = ApplicationRecord.query.filter_by(result="Reject").count()

    print(f"Total: {total}")
    print(f"Accept: {accepts} ({accepts/total*100:.1f}%)")
    print(f"Reject: {rejects} ({rejects/total*100:.1f}%)")
EOF
```

## 9. 文件位置

```
/Users/neok/Documents/CS-Grad-application/
├── app.py                       # Flask应用和模型定义
├── init_db.py                   # 数据初始化脚本
├── CSGradApplication.sql        # 原始设计规范
├── DATABASE_IMPROVEMENTS.md     # 详细改进说明
├── QUICK_START_GUIDE.md        # 本文件
├── templates/                   # HTML模板
├── static/                      # 静态资源
└── instance/
    └── app.db                   # SQLite数据库文件
```

## 10. 常见问题

### Q: 如何添加更多数据？
修改 `init_db.py` 中的 `num_users` 变量：
```python
num_users = 200  # 改为200个用户
```

### Q: 如何修改申请结果分布？
编辑 `init_db.py` 中的 `generate_admission_result()` 函数

### Q: 数据库在哪里？
SQLite数据库：`instance/app.db`

### Q: 如何备份数据？
```bash
cp instance/app.db instance/app.db.backup
```

---

有任何问题，请查看 `DATABASE_IMPROVEMENTS.md` 了解更详细信息。
