# 风险哨兵 // RISK SENTINEL v2.0

**编排式Agent架构的企业风险监控智能体** — 从舆情监控到智能风险决策

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green)](https://flask.palletsprojects.com/)
[![Lines](https://img.shields.io/badge/代码-12,000+行-orange)]()
[![Modules](https://img.shields.io/badge/模块-21个-purple)]()

---

## 项目简介

**风险哨兵**是一个基于编排式Agent架构的企业风险监控智能体，以IF椰子水（IFBH Limited, 6603.HK）为应用案例。系统通过"感知→推理→行动"的Agent闭环，将多源数据聚合、NLP情感分析、定量风险评估（EL/VaR）、多维应对策略生成和自动周报整合为一个可自动运行的Web平台。

与传统SaaS仪表盘只"展示数据"不同，Risk Sentinel能"理解风险"并"告诉你怎么做"。

### 核心数字

| 指标 | 数值 |
|------|------|
| Python模块 | 21个（7,089行） |
| 前端模板 | 5个（4,945行） |
| API端点 | 16个 |
| 监控维度 | 7个独立维度 |
| 应对策略库 | 5维（供应链/品牌/法律/市场/财务） |
| 外部数据源 | 10+（API/RSS/公开法规/股票） |

---

## Agent架构

```
感知层（7个数据源）→ 推理层（NLP+EL/VaR+情景）→ 行动层（5维策略库+优先级排序）
                         │
                   三阶段编排流水线
             初筛 → 条件深度分析 → 结构化报告
```

---

## 主要功能

### 1. 多源数据聚合
- **NewsAPI / GNews API** — 全球新闻搜索（多关键词轮询）
- **7个RSS源** — 饮料/食品行业垂直媒体（BevNet, Food Dive, 36氪等）
- **DemoSource** — 25条IF椰子水专项模拟数据（保底机制）
- **智能去重** — URL精确匹配 + 标题相似度模糊去重（阈值80%）
- **品牌过滤** — 四级分层过滤（品牌关键词→正则→品类→行业源）
- **缓存机制** — JSON文件缓存，4小时TTL

### 2. NLP情感分析与风险矩阵
- **多语言智能路由** — 中文→Baidu NLP→SnowNLP→TextBlob 三级回退
- **6大类风险识别** — 劳工/法律/供应链/财务/声誉/环境（中英双语关键词）
- **风险概率计算** — 来源权威性 + 关键词强度 + 时效性 三维加权
- **风险矩阵** — 可能性×影响度 → 3×3矩阵 → 高/中/低等级
- **风险评分** — 基础50+情感30+风险类型+严重程度 → 0-100分

### 3. 定量风险评估 ⭐
- **EL预期损失模型** — EL = PD × LGD × EAD（信用风险模型→舆情场景迁移）
- **财务比率调整因子** — 6维度加权评分 → 0.9-1.8×风险乘数
- **VaR风险价值** — 95%置信度百分位数法
- **压力测试** — 前3条负面新闻影响+50%情景
- **多情景分析** — 乐观(15%)/基准(50%)/悲观(25%)/极端(10%) 四情景概率加权

### 4. 智能体编排工作流 ⭐
- **三阶段流水线** — 初筛(全量NLP) → 条件深度分析(中高风险触发EL/VaR) → 结构化报告
- **动态预警** — 负面情感>0.6 + 预警关键词 → 实时控制台输出 + 存储
- **德尔菲分析** — 3轮专家共识评估（法律/市场/声誉三专家）

### 5. 五维风险应对引擎 ⭐
- **供应链应对** — 3个备选供应商 + 库存策略 + 合同调整建议
- **品牌危机公关** — 三级预警(黄/橙/红) + 四种声明模板 + 渠道策略
- **法律合规** — 标签整改 + 许可证管理 + 诉讼应对策略
- **市场保卫** — 定价策略 + 召回决策树 + 渠道拓展
- **财务对冲** — 准备金建议 + 产品召回险 + 现金流管理
- **行动优先级排序** — 紧急度×影响力×危机加权 → 三阶段执行时间线

### 6. 扩展监控维度 ⭐
| 模块 | 监控内容 | 数据源 |
|------|---------|--------|
| 🛒 电商监控 | 天猫/京东/小红书/抖音/微博 销量/评分/差评关键词 | 模拟数据 |
| 🏛️ 企业风险 | 天眼查/裁判文书/海关 行政处罚/诉讼/进口异常 | 公开+模拟 |
| 💰 财务监控 | IFBH(6603.HK) 实时股价/财务比率/6大反常信号 | yfinance+港交所 |
| 🚨 政策红线 | 8项适用法规/5个合规缺口/3项紧迫截止日 | 国家卫健委/海关/市监 |
| 🔗 卡脖子分析 | 100%单品种×单采购商×代工依赖/切换成本 | IFBH招股书 |
| 📋 自动周报 | 7模块聚合/红绿灯仪表盘/环比对比/TOP3风险 | 自动快照 |

### 7. 前端可视化
- **赛博朋克风格** — 深色背景 + 青蓝网络线 + 粉色点缀
- **10个异步面板** — 按数据依赖依次加载（1.0s-3.6s）
- **风险热图** — 3×3 CSS Grid矩阵（概率×影响度，绿→红渐变）
- **红绿灯仪表盘** — 7模块独立状态指示灯
- **定量分析面板** — EL/PD/LGD/VaR + 压力测试进度条
- **应对方案面板** — 危机等级 + TOP10行动排序表 + 三阶段时间线

---

## 快速开始

```bash
pip install -r requirements.txt
# 额外依赖: yfinance PyPDF2
pip install yfinance PyPDF2

python app.py
# 浏览器打开 http://localhost:5000
```

---

## 项目结构

```
risk_sentinel/
├── app.py                      # Flask主应用(733行) — 16个API端点 + 三阶段编排
├── config.py                   # 全局配置(API密钥/关键词库/RSS源/风险阈值)
│
├── news_fetcher.py             # 多源新闻聚合(894行) — 策略模式+缓存+品牌过滤
├── risk_analyzer.py            # NLP风险分析(498行) — 情感路由+风险矩阵+评分
├── baidu_nlp.py                # Baidu NLP+SnowNLP+TextBlob路由(275行)
├── quantitative_risk.py        # 定量风险(550行) — EL/VaR/压力/情景/财务调整
├── risk_response.py            # 风险应对引擎(792行) — 5维策略库+优先级排序
│
├── history_manager.py          # JSON历史记录管理(251行)
├── mcp_data_warehouse.py       # SQLite数据仓库(527行)
├── mcp_news_fetcher.py         # MCP优化新闻抓取(163行)
│
├── social_media_fetcher.py     # 社交媒体数据模拟(427行)
├── social_analyzer.py          # 社交媒体分析(183行)
├── data_importer.py            # 外部数据导入(216行)
│
├── realtime_monitor.py         # 实时监控调度框架(472行)
├── realtime_app.py             # WebSocket实时应用(237行)
│
├── data_sources/               # 扩展监控模块包
│   ├── ecommerce_monitor.py    #   电商平台监控(342行)
│   ├── enterprise_monitor.py   #   企业风险监控(397行)
│   ├── financial_monitor.py    #   IFBH股票+财务比率(318行)
│   ├── policy_monitor.py       #   政策红线预警(318行)
│   └── weekly_report.py        #   自动周报生成器(290行)
│
├── templates/
│   └── index.html              # 主仪表盘(1,842行) — 赛博朋克SPA
│
├── api/index.py                # Vercel Serverless部署入口
├── requirements.txt            # Python依赖
├── vercel.json                 # Vercel配置
└── .gitignore
```

---

## API端点（16个）

| 端点 | 方法 | 功能 |
|------|------|------|
| `/` | GET | 首页渲染 |
| `/api/analyze` | GET | 核心分析入口（三阶段编排工作流） |
| `/api/health` | GET | 健康检查 |
| `/api/history` | GET | 获取最近N条历史记录 |
| `/api/history/<id>` | GET | 获取单条记录详情 |
| `/api/history/save` | POST | 保存分析结果 |
| `/api/alerts` | GET | 获取活跃预警列表 |
| `/api/alerts/clear` | POST | 清除预警 |
| `/api/cache/clear` | POST | 强制清除新闻缓存 |
| `/api/ecommerce/monitor` | GET | 电商全平台监控数据 |
| `/api/enterprise/monitor` | GET | 企业风险监控数据 |
| `/api/financial/monitor` | GET | IFBH(6603.HK)财务风险报告 |
| `/api/policy/monitor` | GET | 政策红线预警 |
| `/api/response/plan` | GET | 综合风险应对方案生成 |
| `/api/report/weekly` | GET | 自动周报（7模块聚合+环比） |
| `/api/delphi-analyze` | GET | 德尔菲3轮专家共识评估 |

---

## 外部数据源

| 数据源 | 用途 | 限制 |
|--------|------|------|
| GNews API | 英文新闻搜索 | 100次/天免费 |
| Baidu NLP API | 中文情感分析 | 5万次/天免费 |
| Yahoo Finance (yfinance) | IFBH(6603.HK)实时股价 | 2000次/小时 |
| 港交所披露易 | 季度/年度财务数据 | 免费公开 |
| 国家卫健委/海关/市监 | GB标准+进口注册+标签规范 | 免费公开 |
| 7个RSS Feeds | 饮料/食品行业新闻背景 | 免费 |
| TextBlob / SnowNLP | 中英文情感分析离线兜底 | 无限制 |

---

## 技术栈

| 层级 | 技术 |
|------|------|
| Web框架 | Flask 3.0 |
| 前端 | Chart.js + CSS Grid + 原生JS（无框架） |
| NLP | TextBlob / SnowNLP / Baidu NLP API |
| 量化 | NumPy |
| 股价 | yfinance |
| RSS | feedparser |
| 存储 | JSON + SQLite |

---

## 开发阶段

| Phase | 核心能力 | 代码量 |
|-------|---------|--------|
| Phase 1 | 基础舆情检测（新闻抓取→情感→展示） | ~450行 |
| Phase 2 | 定量风险（EL/VaR/压力测试+中文NLP） | ~1,050行 |
| Phase 3 | Agent编排（三阶段+五维策略库+实时预警） | ~2,150行 |
| Phase 4 | 多维扩展（5个monitor+情景+周报） | ~7,050行 |

---

## 许可

本项目仅用于学术研究和教育目的。
