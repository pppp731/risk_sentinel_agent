# 🤖 风险哨兵智能体

基于NLP技术的企业风险监测与预警系统 - 课程作业项目

## 📋 项目介绍

本项目是一个智能风险监测系统，通过自然语言处理(NLP)技术分析企业新闻，自动识别风险信号并生成预警。

### 核心功能

1. **新闻采集** - 自动从NewsAPI获取目标公司的最新新闻
2. **情感分析** - 使用TextBlob进行正面/负面情感判断
3. **风险识别** - 基于关键词匹配识别6大类风险
4. **风险评分** - 综合计算风险分数并分级
5. **可视化展示** - 网页界面展示分析结果

### 风险类型

- 🔴 **劳工风险** - 罢工、劳资纠纷、员工抗议等
- 🔴 **法律风险** - 诉讼、罚款、监管调查等
- 🔴 **供应链风险** - 原材料短缺、召回、生产中断等
- 🔴 **财务风险** - 亏损、债务、股价下跌等
- 🔴 **声誉风险** - 丑闻、抵制、公关危机等
- 🔴 **环境风险** - 污染、环保违规等

## 🚀 快速开始

### 步骤1: 安装Python

确保你的电脑已安装Python 3.7或更高版本。

在命令行中检查：
```bash
python --version
```

### 步骤2: 安装依赖

打开命令行，进入项目目录：

```bash
cd risk_sentinel
```

安装所需依赖：

```bash
pip install -r requirements.txt
```

> **国内用户加速**：如果安装慢，可以使用清华镜像：
> ```bash
> pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
> ```

### 步骤3: 配置API密钥

编辑 `config.py` 文件，设置你的NewsAPI密钥：

```python
NEWS_API_KEY = "your_newsapi_key_here"  # 替换为你的API Key
```

**获取API Key：**
1. 访问 https://newsapi.org/
2. 点击 "Get API Key" 注册免费账号
3. 复制API Key并粘贴到配置文件中

> 💡 **提示**：免费版每月100次请求，足够课程作业使用。
> 如果不想注册，代码会返回示例数据进行演示。

### 步骤4: 运行项目

```bash
python app.py
```

看到以下输出表示启动成功：
```
🤖 风险哨兵智能体启动中...
访问地址: http://localhost:5000
```

### 步骤5: 打开浏览器访问

在浏览器中打开：http://localhost:5000

点击 **"🔍 开始风险分析"** 按钮即可看到分析结果。

## 📁 文件结构说明

```
risk_sentinel/
├── app.py                 # 🚀 主程序入口，启动Web服务
├── config.py              # ⚙️ 配置文件（API密钥、风险关键词等）
├── news_fetcher.py        # 📰 新闻获取模块
├── risk_analyzer.py       # 🧠 风险分析核心模块
├── requirements.txt       # 📦 依赖包列表
├── README.md             # 📖 项目说明（本文件）
└── templates/
    └── index.html        # 🎨 网页界面模板
```

## 🔧 关键代码解析

### 1. 新闻获取 (news_fetcher.py)

```python
# 调用NewsAPI获取新闻
params = {
    "q": "if coconut water",    # 搜索关键词
    "language": "en",            # 语言
    "sortBy": "relevancy",       # 排序方式
    "pageSize": 20,              # 获取数量
    "apiKey": API_KEY
}
response = requests.get(url, params=params)
```

### 2. 情感分析 (risk_analyzer.py)

```python
# 使用TextBlob进行情感分析
from textblob import TextBlob

blob = TextBlob(text)
polarity = blob.sentiment.polarity  # -1(负面) 到 1(正面)
```

### 3. 风险识别 (risk_analyzer.py)

```python
# 基于关键词匹配识别风险
for risk_type, keywords in RISK_KEYWORDS.items():
    for keyword in keywords:
        if keyword in text:
            # 发现风险！
            identified_risks.append(risk_type)
```

### 4. 风险评分 (risk_analyzer.py)

```python
# 综合计算风险分数
total_score = (
    base_score(50) +
    sentiment_score(0-30) +      # 负面程度
    risk_type_score(0-60) +      # 风险类型数
    severity_score(0-20)         # 严重程度
)
```

## 🎯 作业扩展建议

如果你想进一步完善这个项目，可以考虑：

### 功能扩展
- [ ] 添加更多数据源（Twitter、财报等）
- [ ] 使用更高级的NLP模型（BERT、GPT）
- [ ] 添加风险预测功能
- [ ] 支持中文新闻分析
- [ ] 添加数据导出功能（Excel/PDF）

### 界面优化
- [ ] 添加数据图表（ECharts/D3.js）
- [ ] 支持切换监控公司
- [ ] 添加历史趋势对比
- [ ] 响应式设计适配手机

### 算法改进
- [ ] 使用机器学习训练风险分类模型
- [ ] 添加时间权重（新新闻权重更高）
- [ ] 实现风险相关性分析

## ❓ 常见问题

### Q: 安装依赖时报错？

**A:** 尝试升级pip后重新安装：
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q: 提示API密钥无效？

**A:** 
1. 确认已在config.py中正确设置API密钥
2. 确认密钥前后没有多余空格
3. 如果仍有问题，代码会自动使用示例数据运行

### Q: 如何更换监控的公司？

**A:** 修改 `config.py` 中的 `COMPANY_NAME`：
```python
COMPANY_NAME = "Apple"  # 改为你想监控的公司
```

### Q: 如何添加新的风险类型？

**A:** 在 `config.py` 的 `RISK_KEYWORDS` 中添加：
```python
RISK_KEYWORDS = {
    # 现有风险类型...
    "新风险类型": ["关键词1", "关键词2", "关键词3"]
}
```

## 📚 学习资源

- **Flask文档**: https://flask.palletsprojects.com/
- **TextBlob文档**: https://textblob.readthedocs.io/
- **NewsAPI文档**: https://newsapi.org/docs
- **情感分析原理**: https://en.wikipedia.org/wiki/Sentiment_analysis

## 📝 作业检查清单

提交前确认：

- [ ] 代码可以正常运行
- [ ] 包含了完整的项目文件
- [ ] config.py中的API密钥已设置或注释说明
- [ ] README.md说明了如何运行
- [ ] 有适当的代码注释
- [ ] 网页界面可以正常显示结果

## 👨‍💻 作者

课程作业项目 - 风险哨兵智能体

---

**祝你作业顺利！** 🎉
