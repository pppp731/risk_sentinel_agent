"""
social_analyzer.py - 社交媒体舆情分析模块
"""

from textblob import TextBlob
from collections import Counter, defaultdict
from typing import List, Dict
from datetime import datetime


class SocialMediaAnalyzer:
    """社交媒体分析器"""

    def __init__(self):
        self.positive_words = {
            '好喝', '不错', '喜欢', '推荐', '满意', '正品', '值得信赖',
            'good', 'great', 'love', 'like', 'recommend', 'excellent',
            '良心', '性价比', '值得', '回购', '好评', '支持'
        }

        self.negative_words = {
            '难喝', '踩雷', '失望', '假货', '骗人', '垃圾', '恶心',
            'bad', 'terrible', 'hate', 'disappointed', 'fake', 'fraud',
            '避雷', '投诉', '退货', '欺骗', '虚假宣传', '有问题',
            '掺水', '掺糖', '造假', '不合格', '超标'
        }

        self.controversy_keywords = {
            '质量': ['质量问题', '品控', '不合格', '假货', '掺水', '掺糖'],
            '口感': ['太甜', '不新鲜', '难喝', '味道怪', '跟椰子不一样'],
            '健康': ['血糖', '糖尿病', '孕妇', '添加剂', '防腐剂'],
            '价格': ['贵', '不值', '涨价', '性价比'],
            '真假': ['真假', '正品', '假货', '山寨', '仿冒']
        }

    def analyze_sentiment(self, text: str) -> Dict:
        """情感分析"""
        if not text:
            return {"label": "中性", "score": 0, "confidence": 0}

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        text_lower = text.lower()
        pos_count = sum(1 for word in self.positive_words if word in text_lower)
        neg_count = sum(1 for word in self.negative_words if word in text_lower)

        keyword_score = (pos_count - neg_count) * 0.3
        final_score = polarity + keyword_score

        if final_score > 0.1 or pos_count > neg_count:
            label = "正面"
        elif final_score < -0.1 or neg_count > pos_count:
            label = "负面"
        else:
            label = "中性"

        confidence = min(abs(final_score) + abs(pos_count - neg_count) * 0.1, 1.0)

        return {
            "label": label,
            "score": round(final_score, 3),
            "confidence": round(confidence, 3)
        }

    def identify_controversies(self, posts: List[Dict]) -> List[Dict]:
        """识别争议点"""
        controversy_stats = defaultdict(lambda: {
            "mentions": 0, "正面": 0, "负面": 0, "中性": 0, "examples": []
        })

        for post in posts:
            content = post.get("content", "") + post.get("title", "")
            sentiment = post.get("sentiment", "中性")

            for category, keywords in self.controversy_keywords.items():
                for keyword in keywords:
                    if keyword in content:
                        controversy_stats[category]["mentions"] += 1
                        controversy_stats[category][sentiment] += 1

                        if len(controversy_stats[category]["examples"]) < 3:
                            controversy_stats[category]["examples"].append({
                                "text": content[:100] + "..." if len(content) > 100 else content,
                                "sentiment": sentiment
                            })
                        break

        controversies = []
        for category, stats in controversy_stats.items():
            if stats["mentions"] > 0:
                total = stats["正面"] + stats["负面"] + stats["中性"]
                negative_ratio = stats["负面"] / total if total > 0 else 0

                controversies.append({
                    "category": category,
                    "mentions": stats["mentions"],
                    "sentiment_distribution": {
                        "正面": stats["正面"],
                        "负面": stats["负面"],
                        "中性": stats["中性"]
                    },
                    "negative_ratio": round(negative_ratio, 2),
                    "controversy_level": "高" if negative_ratio > 0.6 else "中" if negative_ratio > 0.3 else "低",
                    "examples": stats["examples"]
                })

        controversies.sort(key=lambda x: x["mentions"], reverse=True)
        return controversies


class SocialMediaReportGenerator:
    """报告生成器"""

    def __init__(self, analyzer: SocialMediaAnalyzer):
        self.analyzer = analyzer

    def generate_report(self, posts: List[Dict], keyword: str = "IF椰子水") -> Dict:
        """生成报告"""
        sentiment_stats = Counter(post.get("sentiment", "中性") for post in posts)
        total = sum(sentiment_stats.values())

        controversies = self.analyzer.identify_controversies(posts)

        negative_ratio = sentiment_stats.get("负面", 0) / total if total > 0 else 0
        high_controversy = sum(1 for c in controversies if c["controversy_level"] == "高")

        if negative_ratio > 0.4 or high_controversy >= 2:
            risk_level = "严重"
            risk_color = "红色"
        elif negative_ratio > 0.25 or high_controversy >= 1:
            risk_level = "高"
            risk_color = "橙色"
        elif negative_ratio > 0.15:
            risk_level = "中"
            risk_color = "黄色"
        else:
            risk_level = "低"
            risk_color = "绿色"

        suggestions = self._generate_suggestions(sentiment_stats, controversies, negative_ratio)

        return {
            "report_title": f"{keyword} 社交媒体舆情分析报告",
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_posts": total,
                "risk_level": risk_level,
                "risk_color": risk_color,
                "negative_ratio": round(negative_ratio * 100, 1),
                "main_controversies": [c["category"] for c in controversies[:3]]
            },
            "sentiment_analysis": {
                "distribution": dict(sentiment_stats),
                "percentages": {k: round(v / total * 100, 1) for k, v in sentiment_stats.items()} if total > 0 else {}
            },
            "controversies": controversies,
            "suggestions": suggestions
        }

    def _generate_suggestions(self, sentiment_stats: Counter, controversies: List[Dict], negative_ratio: float) -> List[str]:
        """生成建议"""
        suggestions = []

        if negative_ratio > 0.4:
            suggestions.append("负面舆情占比较高，建议立即启动危机公关预案")
        elif negative_ratio > 0.25:
            suggestions.append("负面舆情有所上升，建议加强舆情监控频率")

        for controversy in controversies:
            if controversy["controversy_level"] == "高":
                category = controversy["category"]
                if category == "质量":
                    suggestions.append("产品质量争议突出，建议尽快发布权威检测报告")
                elif category == "健康":
                    suggestions.append("健康安全问题受关注，建议邀请第三方机构进行安全评估")

        if not suggestions:
            suggestions.append("整体舆情可控，建议持续监控并积累正面口碑")

        suggestions.append("建议定期发布产品质量报告，增强消费者信任")

        return suggestions
