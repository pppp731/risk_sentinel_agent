# config.py - 配置文件
# 这里存放项目的配置信息，包括 API 密钥和新闻源配置

# ==================== API 密钥配置 ====================

# NewsAPI 密钥
# 1. 访问 https://newsapi.org/ 注册免费账号
# 2. 获取 API Key（免费版 100 次/天）
NEWSAPI_KEY = "your_newsapi_key_here"

# GNews API 密钥（国内可访问）
# 1. 访问 https://gnews.io/ 注册免费账号
# 2. 获取 API Key（免费版 100 次/天）
GNEWS_API_KEY = "your_gnews_api_key_here"

# ==================== 搜索配置 ====================

# 目标公司名称（支持多个关键词，用 OR 连接）
# 当前针对"椰子水掺水掺糖"事件进行专项监控
COMPANY_KEYWORDS = "IF Coconut Water OR IF coconut OR coconut water adulteration OR coconut water sugar OR 椰子水 掺水 OR 椰子水 糖"

# 新闻语言 (en=英文, zh=中文)
LANGUAGE = "en"

# 每个新闻源获取的最大数量
MAX_RESULTS_PER_SOURCE = 20

# ==================== RSS 订阅源配置 ====================

# RSS 订阅源列表
# 优点：免费、稳定、无需 API Key
# 可以添加任意 RSS 源，格式：{"name": "显示名称", "url": "RSS地址"}
RSS_SOURCES = [
    # ==================== 通用搜索 RSS ====================
    # Google News RSS（通过搜索关键词生成）- 稳定可用
    {
        "name": "Google News",
        "url": "https://news.google.com/rss/search?q=coconut+water+industry+supply+chain"
    },
    # Bing News RSS
    {
        "name": "Bing News",
        "url": "https://www.bing.com/news/search?q=coconut+water&format=rss"
    },

    # ==================== 可靠商业新闻源 ====================
    # CNBC - 测试可用
    {
        "name": "CNBC Business",
        "url": "https://www.cnbc.com/id/10001147/device/rss/rss.html"
    },
    # MarketWatch - 稳定
    {
        "name": "MarketWatch",
        "url": "https://www.marketwatch.com/rss/topstories"
    },
    # Seeking Alpha - 投资分析
    {
        "name": "Seeking Alpha",
        "url": "https://seekingalpha.com/api/v3/feed.xml"
    },

    # ==================== 食品/饮料行业 - 已验证可用 ====================
    {
        "name": "Food Dive",
        "url": "https://www.fooddive.com/feeds/news/"
    },
    {
        "name": "Food Safety News",
        "url": "https://www.foodsafetynews.com/feed/"
    },
    {
        "name": "Grocery Dive",
        "url": "https://www.grocerydive.com/feeds/news/"
    },
    # BevNet - 饮料行业专业媒体
    {
        "name": "BevNet",
        "url": "https://www.bevnet.com/feed/"
    },

    # ==================== ESG/环境 - 已验证可用 ====================
    {
        "name": "ESG Today",
        "url": "https://www.esgtoday.com/feed/"
    },

    # ==================== 供应链 - 已验证可用 ====================
    {
        "name": "Supply Chain Dive",
        "url": "https://www.supplychaindive.com/feeds/news/"
    },

    # ==================== 劳工/法律 - 已验证可用 ====================
    {
        "name": "HR Dive",
        "url": "https://www.hrdive.com/feeds/news/"
    },

    # ==================== 国内财经RSS（国内可直接访问） ====================
    # 36氪 - 科技创业、消费零售（已验证可用）
    {
        "name": "36氪",
        "url": "https://36kr.com/feed"
    },
    # 食品商务网 - 食品行业新闻
    {
        "name": "食品商务网",
        "url": "https://www.21food.cn/rss.php"
    },
    # 中国食品报
    {
        "name": "中国食品报",
        "url": "http://www.cnfood.cn/rss/"
    },
    # 以下源在国内网络环境下可能不稳定，如需使用请取消注释：
    # {
    #     "name": "虎嗅",
    #     "url": "https://www.huxiu.com/rss"
    # },
    # {
    #     "name": "界面新闻",
    #     "url": "https://www.jiemian.com/rss"
    # },
    # {
    #     "name": "财新",
    #     "url": "http://www.caixin.com/rss/"
    # },
    # {
    #     "name": "新浪财经",
    #     "url": "https://rss.sina.com.cn/roll/finance/hot_roll.xml"
    # },
    # {
    #     "name": "网易财经",
    #     "url": "https://money.163.com/special/00252G8N/news_fund.xml"
    # },

    # ==================== 更多可选（按需启用） ====================
    # 以下源需要验证，如果遇到问题可以注释掉：

    # Reddit 特定话题（社交网络舆情）
    # {
    #     "name": "Reddit-Business",
    #     "url": "https://www.reddit.com/r/business/.rss"
    # },

    # 泰国相关新闻（椰子水主要产地）
    # {
    #     "name": "Thai PBS Business",
    #     "url": "https://www.thaipbs.or.th/rss/business"
    # },

    # Just Food - 食品行业
    # {
    #     "name": "Just Food",
    #     "url": "https://www.just-food.com/rss.xml"
    # },
]

# ==================== 风险关键词库 ====================

# 用于识别不同类型的风险
RISK_KEYWORDS = {
    "劳工风险": [
        "strike", "labor dispute", "worker protest", "union", "wage",
        "employee rights", "working conditions", "layoff", "firing",
        "discrimination", "harassment", "safety incident", "injury",
        "罢工", "劳资纠纷", "员工抗议", "工会", "工资", "裁员"
    ],
    "法律风险": [
        "lawsuit", "litigation", "fine", "penalty", "violation",
        "regulatory", "compliance", "court", "legal action", "settlement",
        "investigation", "sanction", "breach", "fraud", "诉讼", "罚款"
    ],
    "供应链风险": [
        "supply chain", "shortage", "recall", "contamination",
        "quality issue", "supplier", "raw material", "production halt",
        "factory closure", "inventory", "distribution", "物流", "召回",
        "adulterated", "watered down", "sugar added", "quality control",
        "掺水", "掺糖", "质量问题", "品控", "检测不合格"
    ],
    "财务风险": [
        "bankruptcy", "debt", "loss", "profit decline", "revenue drop",
        "stock plunge", "rating downgrade", "default", "financial crisis",
        "破产", "亏损", "股价下跌", "债务"
    ],
    "声誉风险": [
        "scandal", "boycott", "complaint", "negative review",
        "social media backlash", "PR crisis", "controversy", "criticism",
        "丑闻", "抵制", "负面评价", "公关危机",
        "adulteration", "fake", "fraud", "misleading", "debunk",
        "掺水", "掺糖", "造假", "虚假宣传", "辟谣", "澄清"
    ],
    "环境风险": [
        "pollution", "environmental", "climate", "sustainability",
        "carbon", "emission", "waste", "deforestation", "环保", "污染"
    ]
}

# ==================== 风险评分阈值 ====================

RISK_THRESHOLDS = {
    "low": 30,      # 0-30: 低风险
    "medium": 60,   # 31-60: 中风险
    "high": 80,     # 61-80: 高风险
    "critical": 100 # 81-100: 严重风险
}

# ==================== 新闻去重配置 ====================

# 去重相似度阈值（0-1，越高越严格）
# 0.8 表示标题相似度超过 80% 认为是重复新闻
DEDUPLICATION_THRESHOLD = 0.8

# 去重时考虑的字段权重
DEDUPLICATION_WEIGHTS = {
    "title": 0.6,      # 标题权重最高
    "content": 0.3,    # 内容摘要次之
    "source": 0.1      # 来源辅助判断
}
