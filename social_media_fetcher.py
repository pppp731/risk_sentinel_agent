"""
social_media_fetcher.py - 社交媒体数据获取模块
支持：小红书、微博、抖音等平台的舆情数据获取
"""

import requests
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict


class SocialMediaSource:
    """社交媒体数据源基类"""

    def __init__(self, name: str):
        self.name = name

    def fetch(self, keyword: str, days_back: int = 7) -> List[Dict]:
        """获取社交媒体数据"""
        pass


class XiaohongshuSource(SocialMediaSource):
    """
    小红书数据源
    注：小红书有严格的反爬机制，这里使用模拟数据展示功能
    实际使用时需要：
    1. 申请小红书开放平台API
    2. 或使用第三方数据服务（如新榜、飞瓜）
    """

    def __init__(self):
        super().__init__("小红书")

    def fetch(self, keyword: str = "IF椰子水", days_back: int = 7) -> List[Dict]:
        """
        模拟获取小红书笔记数据
        基于真实的舆情场景构建
        """
        print(f"[{self.name}] 正在搜索相关笔记...")

        # 模拟小红书笔记数据（基于真实的消费者讨论）
        mock_notes = [
            # ========== 负面评价 ==========
            {
                "title": "IF椰子水踩雷！甜得不对劲",
                "content": "姐妹们避雷！新买的IF椰子水甜得发腻，跟新鲜椰子完全不一样。看了配料表写的是100%椰子水，但口感明显加了糖。喝完之后口干，不像天然椰子水那么清爽。",
                "author": "健康生活小美",
                "likes": 2341,
                "comments": 456,
                "sentiment": "负面",
                "tags": ["椰子水测评", "IF椰子水", "避雷"],
                "published_at": (datetime.now() - timedelta(days=2)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "测评笔记"
            },
            {
                "title": "实测IF椰子水，血糖飙升",
                "content": "作为一个妊娠糖妈妈，本来想买椰子水补羊水。结果喝了IF之后血糖直接飙升！这根本不是纯椰子水，肯定加了糖！大家千万别被骗了！",
                "author": "准妈妈日记",
                "likes": 1892,
                "comments": 323,
                "sentiment": "负面",
                "tags": ["妊娠糖尿病", "椰子水", "血糖"],
                "published_at": (datetime.now() - timedelta(days=3)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "经验分享"
            },
            {
                "title": "椰子水行业揭秘",
                "content": "在饮料行业工作5年了，说点内幕。市面上很多椰子水都是浓缩还原的，还要加水加糖调味。真正的纯椰子水成本很高，卖这个价根本赚不到钱。",
                "author": "业内人士",
                "likes": 5678,
                "comments": 892,
                "sentiment": "负面",
                "tags": ["行业内幕", "椰子水", "食品安全"],
                "published_at": (datetime.now() - timedelta(days=4)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "科普揭秘"
            },
            {
                "title": "IF椰子水维权成功！",
                "content": "之前买了IF椰子水，发现味道不对就去投诉了。客服一开始不承认，我提供了对比测评之后终于退款了。姐妹们遇到质量问题一定要维权！",
                "author": "消费者维权日记",
                "likes": 1234,
                "comments": 234,
                "sentiment": "负面",
                "tags": ["维权", "消费者权益", "IF椰子水"],
                "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "维权分享"
            },

            # ========== 正面评价 ==========
            {
                "title": "IF椰子水还是很好喝的",
                "content": "喝了好几年了，一直很喜欢。口感清甜，比 Vitacoco 好喝。看到最近有人说掺糖，我专门看了配料表，只有椰子水一个成分啊。",
                "author": "椰子水爱好者",
                "likes": 892,
                "comments": 156,
                "sentiment": "正面",
                "tags": ["椰子水", "IF", "好物分享"],
                "published_at": (datetime.now() - timedelta(days=2, hours=6)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "好物分享"
            },
            {
                "title": "官方辟谣来了！IF检测报告",
                "content": "看到IF官方发的检测报告了，SGS认证的，确实是100%椰子水。那些说加糖的可能是喝不惯这个味道？我反正觉得挺好的。",
                "author": "理性消费者",
                "likes": 1567,
                "comments": 298,
                "sentiment": "正面",
                "tags": ["辟谣", "IF椰子水", "检测报告"],
                "published_at": (datetime.now() - timedelta(hours=18)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "辟谣笔记"
            },
            {
                "title": "孕期椰子水推荐",
                "content": "孕中期一直在喝椰子水补羊水，IF的性价比最高。买了好几箱了，清测血糖正常。建议大家买正规渠道的，不要买假货。",
                "author": "二胎妈妈",
                "likes": 2345,
                "comments": 412,
                "sentiment": "正面",
                "tags": ["孕期", "椰子水", "补羊水"],
                "published_at": (datetime.now() - timedelta(days=1, hours=8)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "孕期分享"
            },

            # ========== 中性/讨论 ==========
            {
                "title": "IF椰子水真的有问题吗？",
                "content": "最近看到很多关于IF椰子水的争议，有人说掺糖有人说没事。作为普通消费者到底该信谁？有没有懂行的姐妹来说说？",
                "author": "困惑的消费者",
                "likes": 3456,
                "comments": 678,
                "sentiment": "中性",
                "tags": ["椰子水", "争议", "讨论"],
                "published_at": (datetime.now() - timedelta(days=1, hours=12)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "讨论帖"
            },
            {
                "title": "不同品牌椰子水对比测评",
                "content": "买了市面上5个品牌的椰子水做对比。IF的口感偏甜，VitaCoco偏酸，三麟的比较淡。各有利弊吧，看个人口味。",
                "author": "测评博主小王",
                "likes": 4567,
                "comments": 789,
                "sentiment": "中性",
                "tags": ["测评", "椰子水对比", "饮品"],
                "published_at": (datetime.now() - timedelta(days=3, hours=6)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "测评笔记"
            },
            {
                "title": "椰子水选购指南",
                "content": "教大家怎么选椰子水：1.看配料表，纯椰子水应该只有一个成分；2.看产地，泰国、越南的比较好；3.看保质期，越短越新鲜。",
                "author": "营养师小李",
                "likes": 8901,
                "comments": 1234,
                "sentiment": "中性",
                "tags": ["选购指南", "椰子水", "科普"],
                "published_at": (datetime.now() - timedelta(days=2, hours=12)).isoformat(),
                "platform": "xiaohongshu",
                "note_type": "科普笔记"
            }
        ]

        print(f"[{self.name}] 成功获取 {len(mock_notes)} 条笔记")
        return mock_notes


class WeiboSource(SocialMediaSource):
    """
    微博数据源
    注：微博数据需要通过官方API或第三方服务获取
    """

    def __init__(self):
        super().__init__("微博")

    def fetch(self, keyword: str = "IF椰子水", days_back: int = 7) -> List[Dict]:
        """模拟获取微博数据"""
        print(f"[{self.name}] 正在搜索相关微博...")

        mock_weibos = [
            # ========== 热搜/话题 ==========
            {
                "content": "#IF椰子水掺糖# 刚买了几箱就看到这个热搜，整个人都不好了。已经申请退款了，希望官方能给个说法。",
                "author": "消费者张三",
                "followers": 5234,
                "reposts": 567,
                "comments": 890,
                "likes": 1234,
                "sentiment": "负面",
                "is_hot": True,
                "topic": "#IF椰子水掺糖#",
                "published_at": (datetime.now() - timedelta(days=2)).isoformat(),
                "platform": "weibo"
            },
            {
                "content": "#IF椰子水辟谣# 官方晒检测报告了！SGS认证的100%椰子水。那些说加糖的麻烦拿证据好吗？别造谣了。",
                "author": "品牌守护者",
                "followers": 12345,
                "reposts": 2345,
                "comments": 1567,
                "likes": 8901,
                "sentiment": "正面",
                "is_hot": True,
                "topic": "#IF椰子水辟谣#",
                "published_at": (datetime.now() - timedelta(hours=20)).isoformat(),
                "platform": "weibo"
            },
            {
                "content": "#市场监管介入调查椰子水# 看来事情闹大了，监管部门都介入了。等一个官方调查结果。",
                "author": "财经观察员",
                "followers": 45678,
                "reposts": 3456,
                "comments": 2345,
                "likes": 6789,
                "sentiment": "中性",
                "is_hot": True,
                "topic": "#市场监管介入调查椰子水#",
                "published_at": (datetime.now() - timedelta(hours=8)).isoformat(),
                "platform": "weibo"
            },

            # ========== 普通用户评论 ==========
            {
                "content": "喝了一年的IF椰子水，说实话挺好喝的。比VitaCoco便宜，味道也不错。希望这次事件不要影响到产品质量。",
                "author": "忠实用户",
                "followers": 234,
                "reposts": 12,
                "comments": 45,
                "likes": 89,
                "sentiment": "正面",
                "is_hot": False,
                "topic": "",
                "published_at": (datetime.now() - timedelta(days=1)).isoformat(),
                "platform": "weibo"
            },
            {
                "content": "我买的IF椰子水确实甜得不对劲，跟新鲜椰子完全不一样。如果是纯椰子水怎么可能这么甜？",
                "author": "质疑者",
                "followers": 567,
                "reposts": 89,
                "comments": 234,
                "likes": 456,
                "sentiment": "负面",
                "is_hot": False,
                "topic": "",
                "published_at": (datetime.now() - timedelta(days=3)).isoformat(),
                "platform": "weibo"
            },
            {
                "content": "作为食品行业从业者，说几句公道话。椰子水的甜度跟产地、季节、椰子品种都有关系，不能单纯凭口感判断是否加糖。还是等官方检测结果吧。",
                "author": "食品工程师",
                "followers": 12345,
                "reposts": 567,
                "comments": 456,
                "likes": 1234,
                "sentiment": "中性",
                "is_hot": False,
                "topic": "",
                "published_at": (datetime.now() - timedelta(days=2, hours=8)).isoformat(),
                "platform": "weibo"
            },
            {
                "content": "超市已经下架IF椰子水了，这波操作够快的。不管真假，食品安全确实不能马虎。",
                "author": "超市观察者",
                "followers": 890,
                "reposts": 234,
                "comments": 345,
                "likes": 567,
                "sentiment": "负面",
                "is_hot": False,
                "topic": "",
                "published_at": (datetime.now() - timedelta(days=1, hours=6)).isoformat(),
                "platform": "weibo"
            },
            {
                "content": "看到有人说孕妇喝IF椰子水血糖飙升，我也是一个孕妇，喝了几个月IF血糖一直正常啊。个体差异吧？",
                "author": "二胎准妈妈",
                "followers": 3456,
                "reposts": 123,
                "comments": 567,
                "likes": 890,
                "sentiment": "中性",
                "is_hot": False,
                "topic": "",
                "published_at": (datetime.now() - timedelta(days=2, hours=4)).isoformat(),
                "platform": "weibo"
            }
        ]

        print(f"[{self.name}] 成功获取 {len(mock_weibos)} 条微博")
        return mock_weibos


class DouyinSource(SocialMediaSource):
    """
    抖音数据源
    注：抖音数据需要通过官方API或第三方服务获取
    """

    def __init__(self):
        super().__init__("抖音")

    def fetch(self, keyword: str = "IF椰子水", days_back: int = 7) -> List[Dict]:
        """模拟获取抖音视频数据"""
        print(f"[{self.name}] 正在搜索相关视频...")

        mock_videos = [
            {
                "title": "IF椰子水真假测评",
                "description": "今天来测评一下最近很火的IF椰子水，看看是不是真的100%纯椰子水",
                "author": "测评达人",
                "views": 1234567,
                "likes": 45678,
                "comments": 3456,
                "shares": 2345,
                "sentiment": "中性",
                "published_at": (datetime.now() - timedelta(days=2)).isoformat(),
                "platform": "douyin"
            },
            {
                "title": "椰子水踩雷！姐妹们避雷",
                "description": "千万不要买这个牌子的椰子水，真的太甜了，根本不是纯椰子水",
                "author": "避雷小能手",
                "views": 2345678,
                "likes": 67890,
                "comments": 5678,
                "shares": 3456,
                "sentiment": "负面",
                "published_at": (datetime.now() - timedelta(days=3)).isoformat(),
                "platform": "douyin"
            },
            {
                "title": "官方辟谣！IF椰子水没问题",
                "description": "看了官方的检测报告，IF椰子水确实是100%纯椰子水，大家放心喝",
                "author": "真相揭秘",
                "views": 890123,
                "likes": 34567,
                "comments": 2345,
                "shares": 1234,
                "sentiment": "正面",
                "published_at": (datetime.now() - timedelta(hours=16)).isoformat(),
                "platform": "douyin"
            }
        ]

        print(f"[{self.name}] 成功获取 {len(mock_videos)} 条视频")
        return mock_videos


class SocialMediaAggregator:
    """社交媒体数据聚合器"""

    def __init__(self):
        self.sources = [
            XiaohongshuSource(),
            WeiboSource(),
            DouyinSource()
        ]

    def fetch_all(self, keyword: str = "IF椰子水", days_back: int = 7) -> Dict:
        """
        从所有平台获取数据并汇总

        Returns:
            {
                "total_count": 总数量,
                "platforms": {
                    "小红书": [...],
                    "微博": [...],
                    "抖音": [...]
                },
                "all_posts": [...]  # 合并后的列表
            }
        """
        result = {
            "total_count": 0,
            "platforms": {},
            "all_posts": []
        }

        print(f"\n{'='*60}")
        print(f"开始从社交媒体平台获取数据...")
        print(f"关键词: {keyword}")
        print(f"{'='*60}\n")

        for source in self.sources:
            try:
                posts = source.fetch(keyword, days_back)
                result["platforms"][source.name] = posts
                result["all_posts"].extend(posts)
                result["total_count"] += len(posts)
            except Exception as e:
                print(f"[{source.name}] 获取失败: {e}")

        # 按时间排序
        result["all_posts"].sort(
            key=lambda x: x.get("published_at", ""),
            reverse=True
        )

        print(f"\n{'='*60}")
        print(f"社交媒体数据采集完成")
        print(f"总计: {result['total_count']} 条")
        print(f"{'='*60}\n")

        return result


# 测试代码
if __name__ == "__main__":
    aggregator = SocialMediaAggregator()
    data = aggregator.fetch_all("IF椰子水")

    print("\n数据示例:")
    for platform, posts in data["platforms"].items():
        print(f"\n{platform}: {len(posts)} 条")
        if posts:
            print(f"  最新: {posts[0]['title'] if 'title' in posts[0] else posts[0]['content'][:50]}...")
