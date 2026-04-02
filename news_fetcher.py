"""
news_fetcher.py - 新闻获取模块
支持多源聚合：NewsAPI + GNews + RSS订阅
包含智能去重机制
"""

import requests
import feedparser
import re
import json
import hashlib
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from difflib import SequenceMatcher
from dateutil import parser as date_parser

from config import (
    NEWSAPI_KEY, GNEWS_API_KEY, COMPANY_KEYWORDS, LANGUAGE,
    MAX_RESULTS_PER_SOURCE, RSS_SOURCES, DEDUPLICATION_THRESHOLD
)


# ==================== 抽象基类 ====================

class BaseNewsSource(ABC):
    """新闻源抽象基类"""

    def __init__(self, name: str):
        self.name = name
        self.enabled = True

    @abstractmethod
    def fetch(self, days_back: int = 30) -> List[Dict]:
        """获取新闻，返回统一格式的列表"""
        pass

    def _normalize_article(self, title: str, description: str = "",
                          content: str = "", url: str = "",
                          published_at: str = "", source: str = "") -> Dict:
        """统一文章格式"""
        return {
            "title": title.strip() if title else "",
            "description": description.strip() if description else "",
            "content": content.strip() if content else (description.strip() if description else ""),
            "url": url.strip() if url else "",
            "published_at": self._normalize_date(published_at),
            "source": source.strip() if source else self.name,
            "source_type": self.name,
            "fetched_at": datetime.now().isoformat()
        }

    def _normalize_date(self, date_str) -> str:
        """标准化日期格式为 ISO 8601"""
        if not date_str:
            return datetime.now().isoformat()

        try:
            if isinstance(date_str, datetime):
                return date_str.isoformat()
            # 尝试解析各种日期格式
            parsed = date_parser.parse(str(date_str))
            return parsed.isoformat()
        except Exception:
            return datetime.now().isoformat()


# ==================== NewsAPI 源 ====================

class NewsAPISource(BaseNewsSource):
    """NewsAPI 新闻源"""

    def __init__(self, api_key: str):
        super().__init__("NewsAPI")
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch(self, days_back: int = 30) -> List[Dict]:
        if self.api_key == "your_newsapi_key_here":
            print(f"[{self.name}] API 密钥未设置，跳过")
            return []

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        params = {
            "q": COMPANY_KEYWORDS,
            "language": LANGUAGE,
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "pageSize": MAX_RESULTS_PER_SOURCE,
            "sortBy": "relevancy",
            "apiKey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "ok":
                print(f"[{self.name}] API 错误: {data.get('message', '未知错误')}")
                return []

            articles = data.get("articles", [])
            print(f"[{self.name}] 成功获取 {len(articles)} 条新闻")

            return [self._normalize_article(
                title=a.get("title", ""),
                description=a.get("description", ""),
                content=a.get("content", ""),
                url=a.get("url", ""),
                published_at=a.get("publishedAt", ""),
                source=a.get("source", {}).get("name", "NewsAPI")
            ) for a in articles]

        except requests.exceptions.RequestException as e:
            print(f"[{self.name}] 请求失败: {e}")
            return []
        except Exception as e:
            print(f"[{self.name}] 解析失败: {e}")
            return []


# ==================== GNews 源 ====================

class GNewsSource(BaseNewsSource):
    """GNews API 新闻源（国内可访问）"""

    def __init__(self, api_key: str):
        super().__init__("GNews")
        self.api_key = api_key
        self.base_url = "https://gnews.io/api/v4/search"

    def fetch(self, days_back: int = 30) -> List[Dict]:
        if self.api_key == "your_gnews_api_key_here":
            print(f"[{self.name}] API 密钥未设置，跳过")
            return []

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        params = {
            "q": COMPANY_KEYWORDS,
            "lang": LANGUAGE,
            "from": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "to": end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "max": MAX_RESULTS_PER_SOURCE,
            "token": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            articles = data.get("articles", [])
            print(f"[{self.name}] 成功获取 {len(articles)} 条新闻")

            result = []
            for a in articles:
                source_name = a.get("source", {})
                if isinstance(source_name, dict):
                    source_name = source_name.get("name", "GNews")

                result.append(self._normalize_article(
                    title=a.get("title", ""),
                    description=a.get("description", ""),
                    content=a.get("content", ""),
                    url=a.get("url", ""),
                    published_at=a.get("publishedAt", ""),
                    source=source_name
                ))
            return result

        except requests.exceptions.RequestException as e:
            print(f"[{self.name}] 请求失败: {e}")
            return []
        except Exception as e:
            print(f"[{self.name}] 解析失败: {e}")
            return []


# ==================== RSS 订阅源 ====================

class RSSSource(BaseNewsSource):
    """RSS 订阅源"""

    def __init__(self, name: str, rss_url: str):
        super().__init__(f"RSS-{name}")
        self.rss_url = rss_url
        self.source_name = name

    def fetch(self, days_back: int = 30) -> List[Dict]:
        try:
            # 解析 RSS feed
            feed = feedparser.parse(self.rss_url)

            if feed.get("bozo"):
                print(f"[{self.name}] RSS 解析警告: {feed.get('bozo_exception', '未知问题')}")

            entries = feed.get("entries", [])
            cutoff_date = datetime.now() - timedelta(days=days_back)

            result = []
            for entry in entries:
                # 获取发布日期
                published = entry.get("published") or entry.get("updated") or ""

                # 过滤日期范围
                try:
                    if published:
                        pub_date = date_parser.parse(published)
                        if pub_date < cutoff_date:
                            continue
                except:
                    pass

                # 清理 HTML 标签
                description = self._clean_html(entry.get("summary", ""))
                content = self._clean_html(entry.get("description", ""))

                result.append(self._normalize_article(
                    title=entry.get("title", ""),
                    description=description,
                    content=content if content else description,
                    url=entry.get("link", ""),
                    published_at=published,
                    source=self.source_name
                ))

            print(f"[{self.name}] 成功获取 {len(result)} 条新闻")
            return result[:MAX_RESULTS_PER_SOURCE]

        except Exception as e:
            print(f"[{self.name}] 获取失败: {e}")
            return []

    def _clean_html(self, raw_html: str) -> str:
        """清理 HTML 标签"""
        if not raw_html:
            return ""
        clean = re.sub(r'<[^>]+>', '', raw_html)
        return clean.strip()


# ==================== 演示数据源 ====================

class DemoSource(BaseNewsSource):
    """演示数据源 - 模拟椰子水掺水掺糖舆情危机事件"""

    def __init__(self):
        super().__init__("舆情监控模拟")

    def fetch(self, days_back: int = 30) -> List[Dict]:
        print(f"[{self.name}] 生成'椰子水掺水掺糖'舆情事件模拟数据...")
        today = datetime.now()

        # 模拟"IF椰子水掺水掺糖"舆情事件的时间线
        demo_articles = [
            # ========== 负面曝光阶段（危机爆发）==========
            {
                "title": "曝IF椰子水涉嫌掺水掺糖！实测糖分超标",
                "description": "有消费者送检发现，热销品牌IF椰子水实际糖分含量远超标注，且检出添加糖浆成分，疑似并非100%纯椰子水。检测报告显示...",
                "published_at": (today - timedelta(days=2)).isoformat(),
                "source": "消费者报道",
                "url": "https://example.com/news/1"
            },
            {
                "title": "多家椰子水品牌被曝质量问题 IF也在列",
                "description": "媒体随机抽检10款椰子水产品，发现包括IF在内的多个品牌存在标签不实、添加剂超标等问题，引发消费者关注。",
                "published_at": (today - timedelta(days=2, hours=6)).isoformat(),
                "source": "食品安全网",
                "url": "https://example.com/news/2"
            },
            {
                "title": "网友实测：IF椰子水甜味不正常 疑加糖",
                "description": "多位网友在社交平台发文，表示IF椰子水口感过甜，与天然椰子水差异明显。有用户用血糖仪测试，发现饮用后血糖快速上升...",
                "published_at": (today - timedelta(days=2, hours=8)).isoformat(),
                "source": "微博热搜",
                "url": "https://example.com/news/3"
            },
            {
                "title": "椰子水行业乱象：掺水加糖成潜规则？",
                "description": "业内人士爆料，部分椰子水品牌为降低成本，采用浓缩还原加水加糖的方式生产，却标注100%纯椰子水，涉嫌虚假宣传。",
                "published_at": (today - timedelta(days=1, hours=12)).isoformat(),
                "source": "财经观察",
                "url": "https://example.com/news/4"
            },
            # ========== 舆论发酵阶段（危机扩散）==========
            {
                "title": "IF椰子水遭集体投诉 平台投诉量激增",
                "description": "各大电商平台数据显示，IF椰子水近一周投诉量环比增长300%，主要集中在'虚假宣传'、'质量问题'等方面。",
                "published_at": (today - timedelta(days=1)).isoformat(),
                "source": "电商观察",
                "url": "https://example.com/news/5"
            },
            {
                "title": "超市回应：已暂时下架IF椰子水相关产品",
                "description": "多家连锁超市表示，关注到相关舆情后，已暂时下架IF椰子水产品，等待品牌方和监管部门的进一步说明。",
                "published_at": (today - timedelta(days=1, hours=4)).isoformat(),
                "source": "零售资讯",
                "url": "https://example.com/news/6"
            },
            {
                "title": "专家解读：如何判断椰子水是否加糖",
                "description": "食品专家指出，可通过查看配料表、营养成分表等判断。纯椰子水碳水化合物含量应在4-5g/100ml左右，过高可能添加了糖。",
                "published_at": (today - timedelta(days=1, hours=6)).isoformat(),
                "source": "健康时报",
                "url": "https://example.com/news/7"
            },
            # ========== 企业回应阶段（危机应对）==========
            {
                "title": "IF官方声明：产品符合标准 保留追责权利",
                "description": "IF品牌发布官方声明，称所有产品均通过正规检测，符合食品安全标准。对于不实传言，公司将保留追究法律责任的权利。",
                "published_at": (today - timedelta(hours=18)).isoformat(),
                "source": "品牌官方",
                "url": "https://example.com/news/8"
            },
            {
                "title": "IF公布第三方检测报告 否认掺水掺糖指控",
                "description": "IF椰子水公布SGS检测报告，显示产品未检出添加糖，符合100%椰子水标准。公司表示网传检测方法不科学。",
                "published_at": (today - timedelta(hours=14)).isoformat(),
                "source": "品牌公告",
                "url": "https://example.com/news/9"
            },
            {
                "title": "IF负责人回应：竞争对手恶意抹黑",
                "description": "IF中国区负责人表示，此次舆情是有组织有计划的恶意攻击，公司已掌握证据，将通过法律手段维护品牌声誉。",
                "published_at": (today - timedelta(hours=10)).isoformat(),
                "source": "财经专访",
                "url": "https://example.com/news/10"
            },
            # ========== 舆论反转阶段（争议持续）==========
            {
                "title": "消费者不买账：IF回应避重就轻",
                "description": "尽管IF发布检测报告，但部分消费者仍不买账。有网友质疑报告真实性，称自己的检测结果与品牌方公布的不一致。",
                "published_at": (today - timedelta(hours=8)).isoformat(),
                "source": "社交媒体",
                "url": "https://example.com/news/11"
            },
            {
                "title": "市场监管部门介入调查IF椰子水",
                "description": "据了解，相关市场监管部门已介入调查，将对市场上销售的椰子水产品进行抽检，结果将及时向社会公布。",
                "published_at": (today - timedelta(hours=6)).isoformat(),
                "source": "市场监管报",
                "url": "https://example.com/news/12"
            },
            {
                "title": "椰子水行业迎来洗牌 质量将成为关键",
                "description": "此次事件或将加速椰子水行业规范化进程。专家表示，随着消费者健康意识提升，产品质量将成为品牌竞争的核心。",
                "published_at": (today - timedelta(hours=4)).isoformat(),
                "source": "产业分析",
                "url": "https://example.com/news/13"
            },
            {
                "title": "IF椰子水海外销售是否受影响？",
                "description": "作为泰国进口品牌，IF椰子水在海外的销售情况引发关注。目前海外电商平台评论中已出现质疑声音。",
                "published_at": (today - timedelta(hours=2)).isoformat(),
                "source": "跨境观察",
                "url": "https://example.com/news/14"
            },
            {
                "title": "如何选购真正的100%椰子水？选购指南",
                "description": "教你几招辨别真假椰子水：1.看配料表，纯椰子水应只有椰子水；2.看营养成分；3.选择知名品牌；4.注意口感...",
                "published_at": (today - timedelta(hours=1)).isoformat(),
                "source": "消费指南",
                "url": "https://example.com/news/15"
            }
        ]

        return [self._normalize_article(
            title=a["title"],
            description=a["description"],
            content=a["description"],
            url=a["url"],
            published_at=a["published_at"],
            source=a["source"]
        ) for a in demo_articles]


# ==================== 新闻聚合器 ====================

class NewsAggregator:
    """
    新闻聚合器 - 管理多个新闻源
    功能：
    1. 从多个源并行获取新闻
    2. 智能去重
    3. 统一输出格式
    """

    def __init__(self):
        self.sources: List[BaseNewsSource] = []
        self._init_sources()

    def _init_sources(self):
        """初始化所有新闻源"""
        # NewsAPI（国外，需要Key）
        self.sources.append(NewsAPISource(NEWSAPI_KEY))

        # GNews（国外，国内可访问）
        self.sources.append(GNewsSource(GNEWS_API_KEY))

        # RSS 订阅源（包含国内财经媒体）
        for rss_config in RSS_SOURCES:
            self.sources.append(RSSSource(
                name=rss_config["name"],
                rss_url=rss_config["url"]
            ))

    def fetch_all(self, days_back: int = 30, deduplicate: bool = True) -> List[Dict]:
        """
        从所有源获取新闻

        Args:
            days_back: 获取多少天内的新闻
            deduplicate: 是否进行去重

        Returns:
            统一格式的新闻列表
        """
        all_articles = []
        successful_sources = 0

        print(f"\n{'='*50}")
        print(f"开始从 {len(self.sources)} 个新闻源获取数据...")
        print(f"{'='*50}")

        for source in self.sources:
            try:
                articles = source.fetch(days_back)
                if articles:
                    all_articles.extend(articles)
                    successful_sources += 1
            except Exception as e:
                print(f"[{source.name}] 错误: {e}")

        print(f"\n{'='*50}")
        print(f"成功从 {successful_sources}/{len(self.sources)} 个源获取数据")
        print(f"原始新闻总数: {len(all_articles)}")
        print(f"{'='*50}\n")

        # 如果没有获取到任何数据，使用演示数据
        if not all_articles:
            print("[!] 所有源都失败，使用演示数据")
            demo = DemoSource()
            all_articles = demo.fetch(days_back)

        # 去重
        if deduplicate:
            all_articles = self._deduplicate(all_articles)

        # 按发布时间排序
        all_articles.sort(key=lambda x: x.get("published_at", ""), reverse=True)

        print(f"最终有效新闻数: {len(all_articles)}\n")
        return all_articles

    def _deduplicate(self, articles: List[Dict]) -> List[Dict]:
        """
        智能去重 - 基于标题相似度

        策略：
        1. 计算标题相似度
        2. URL 完全相同的直接去重
        3. 相似度超过阈值认为是重复新闻
        """
        if not articles:
            return []

        unique_articles = []
        seen_urls = set()

        for article in articles:
            url = article.get("url", "")
            title = article.get("title", "")

            # URL 完全相同的跳过
            if url and url in seen_urls:
                continue
            seen_urls.add(url)

            # 检查标题相似度
            is_duplicate = False
            for existing in unique_articles:
                similarity = self._calculate_similarity(
                    title,
                    existing.get("title", "")
                )
                if similarity > DEDUPLICATION_THRESHOLD:
                    is_duplicate = True
                    # 合并来源信息（保留更多信息）
                    if article.get("source") != existing.get("source"):
                        existing["source"] = f"{existing['source']}, {article['source']}"
                    break

            if not is_duplicate:
                unique_articles.append(article)

        removed_count = len(articles) - len(unique_articles)
        if removed_count > 0:
            print(f"[去重] 移除 {removed_count} 条重复新闻")

        return unique_articles

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算两段文本的相似度 (0-1)"""
        if not text1 or not text2:
            return 0.0

        # 预处理：小写、去除标点
        def clean(text):
            return re.sub(r'[^\w\s]', '', text.lower().strip())

        s1 = clean(text1)
        s2 = clean(text2)

        return SequenceMatcher(None, s1, s2).ratio()


# ==================== 兼容性接口 ====================

class NewsFetcher:
    """
    兼容旧接口的包装类
    保持与原有代码的兼容性
    """

    def __init__(self):
        self.aggregator = NewsAggregator()

    def fetch_news(self, days_back: int = 30) -> List[Dict]:
        """兼容旧接口"""
        return self.aggregator.fetch_all(days_back=days_back, deduplicate=True)


# ==================== 测试代码 ====================

if __name__ == "__main__":
    # 直接运行测试
    print("测试新闻获取模块...")

    fetcher = NewsFetcher()
    articles = fetcher.fetch_news(days_back=30)

    print(f"\n获取到 {len(articles)} 条新闻:")
    for i, article in enumerate(articles[:5], 1):
        print(f"\n{i}. {article['title']}")
        print(f"   来源: {article['source']} ({article['source_type']})")
        print(f"   时间: {article['published_at']}")
