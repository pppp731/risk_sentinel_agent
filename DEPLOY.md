# 风险哨兵智能体 - 部署指南

## 🎯 推荐方案：Render（免费 + 稳定）

**Render** 是一个免费的云托管平台，支持 Python Flask 应用，不需要信用卡。

### 部署步骤（15分钟）

#### 1. 准备代码

确保以下文件已创建：
```
risk_sentinel/
├── api/
│   └── index.py          # Vercel 入口
├── templates/
│   └── simple_dashboard.html  # 简化版仪表盘
├── news_fetcher.py       # 新闻获取
├── risk_analyzer.py      # 风险分析
├── app.py               # Flask 应用
├── requirements.txt     # 依赖
├── vercel.json          # Vercel 配置
└── DEPLOY.md           # 本文件
```

#### 2. 上传到 GitHub

```bash
# 初始化 git
git init

# 添加文件
git add .

# 提交
git commit -m "Initial commit"

# 创建 GitHub 仓库并推送
git remote add origin https://github.com/yourusername/risk-sentinel.git
git push -u origin main
```

#### 3. 部署到 Render

1. 访问 https://render.com/
2. 点击 **"Get Started for Free"**
3. 选择 **"Web Service"**
4. 连接你的 GitHub 账号，选择 `risk-sentinel` 仓库
5. 配置：
   - **Name**: `risk-sentinel`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. 点击 **"Create Web Service"**

#### 4. 获取网址

部署完成后，Render 会给你分配一个网址：
```
https://risk-sentinel.onrender.com
```

这个网址就是课堂展示时用的！

---

## 🚀 替代方案：Vercel（5分钟极速部署）

如果不想注册 Render，可以用 Vercel：

### 步骤

1. 访问 https://vercel.com/
2. 用 GitHub 账号登录
3. 点击 **"New Project"**
4. 导入 `risk-sentinel` 仓库
5. 点击 **"Deploy"**

网址格式：
```
https://risk-sentinel.vercel.app
```

---

## 🔥 最快方案：Ngrok（临时演示，2分钟）

如果只是想临时演示，不需要部署：

### 步骤

1. 下载 ngrok：https://ngrok.com/download
2. 注册免费账号，获取 authtoken
3. 配置 token：
   ```bash
   ngrok config add-authtoken YOUR_TOKEN
   ```
4. 启动你的本地服务：
   ```bash
   python app.py
   ```
5. 在另一个终端运行：
   ```bash
   ngrok http 5000
   ```

你会得到一个公网网址：
```
https://xxxx.ngrok-free.app
```

把这个网址发给同学或投影即可！

**注意**：Ngrok 网址每次重启都会变，适合临时演示。

---

## 📱 方案对比

| 方案 | 难度 | 费用 | 网址稳定性 | 推荐场景 |
|------|------|------|-----------|---------|
| **Render** | ⭐⭐ | 免费 | 永久固定 | 课堂展示首选 |
| **Vercel** | ⭐ | 免费 | 永久固定 | 快速部署 |
| **Ngrok** | ⭐ | 免费 | 临时 | 临时演示 |
| **腾讯云** | ⭐⭐⭐ | ~50元/月 | 永久固定 | 长期使用 |

---

## 💡 课堂展示建议

### 推荐流程

1. **提前 1 天部署到 Render**
2. **测试网址**是否正常访问
3. **课堂展示时直接打开网址**
4. **演示功能**：
   - 点击"刷新数据"查看最新分析
   - 展示风险评分和预警
   - 展示情感分布图表

### 备用方案

万一部署的网址打不开，准备 **Ngrok** 作为备用：
```bash
# 课前 5 分钟启动
python app.py
ngrok http 5000
```

---

## 🆘 常见问题

### Q: 部署后页面打不开？

A: 检查以下几点：
1. `requirements.txt` 是否包含所有依赖？
2. `app.py` 中 `debug=True` 是否改为 `debug=False`？
3. Render 的日志中是否有错误信息？

### Q: 数据加载很慢？

A: Render 免费版会休眠，首次访问需要 30 秒唤醒。可以：
- 课前先访问一次"预热"
- 或使用付费版（$7/月）不休眠

### Q: 可以自定义域名吗？

A: 可以！Render 和 Vercel 都支持绑定自己的域名（如 `risksentinel.yourschool.edu`）

---

## 📞 需要帮助？

部署过程中遇到问题：
1. 查看 Render 文档：https://render.com/docs
2. 或告诉我具体错误信息，我帮您解决

**推荐现在就试试 Render 部署，整个过程只需 15 分钟！** 🚀
