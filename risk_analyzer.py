"""
risk_analyzer.py - 风险分析模块
核心功能：情感分析 + 风险识别 + 风险评分
"""

from textblob import TextBlob
from config import RISK_KEYWORDS, RISK_THRESHOLDS
import re


class RiskAnalyzer:
    """风险分析器类 - 分析单条新闻的风险"""

    def __init__(self):
        """初始化分析器"""
        self.risk_keywords = RISK_KEYWORDS

    def analyze_sentiment(self, text):
        """
        情感分析 - 判断文本是正面还是负面

        参数:
            text: 要分析的文本

        返回:
            dict: 包含极性(polarity)和主观性(subjectivity)的字典
                - polarity: -1(负面) 到 1(正面)
                - subjectivity: 0(客观) 到 1(主观)
        """
        if not text:
            return {"polarity": 0, "subjectivity": 0}

        # 使用TextBlob进行情感分析
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity

        return {
            "polarity": round(polarity, 3),
            "subjectivity": round(subjectivity, 3),
            "sentiment_label": self._get_sentiment_label(polarity)
        }

    def _get_sentiment_label(self, polarity):
        """
        根据极性值返回情感标签

        参数:
            polarity: 极性值 (-1 到 1)

        返回:
            str: 正面/负面/中性
        """
        if polarity > 0.1:
            return "正面"
        elif polarity < -0.1:
            return "负面"
        else:
            return "中性"

    def identify_risks(self, text):
        """
        风险识别 - 识别文本中包含的风险类型

        参数:
            text: 要分析的文本

        返回:
            list: 风险类型列表，每项包含风险类型、关键词、证据
        """
        if not text:
            return []

        text_lower = text.lower()
        identified_risks = []

        # 遍历所有风险类型和关键词
        for risk_type, keywords in self.risk_keywords.items():
            matched_keywords = []
            evidence = []

            for keyword in keywords:
                # 使用正则表达式匹配关键词（忽略大小写）
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    matched_keywords.append(keyword)
                    # 提取关键词周围的上下文作为证据
                    evidence.append(self._extract_context(text, keyword))

            # 如果匹配到关键词，记录该风险
            if matched_keywords:
                identified_risks.append({
                    "risk_type": risk_type,
                    "keywords_found": matched_keywords,
                    "evidence": list(set(evidence))[:2],  # 最多2条证据
                    "severity": len(matched_keywords)  # 匹配越多，严重程度越高
                })

        return identified_risks

    def _extract_context(self, text, keyword, window=50):
        """
        提取关键词周围的上下文

        参数:
            text: 原文本
            keyword: 关键词
            window: 前后提取的字符数

        返回:
            str: 包含关键词的上下文
        """
        text_lower = text.lower()
        keyword_lower = keyword.lower()

        # 找到关键词位置
        pos = text_lower.find(keyword_lower)
        if pos == -1:
            return ""

        # 提取上下文
        start = max(0, pos - window)
        end = min(len(text), pos + len(keyword) + window)

        context = text[start:end]

        # 添加省略号表示截取
        if start > 0:
            context = "..." + context
        if end < len(text):
            context = context + "..."

        return context

    def calculate_risk_score(self, sentiment, risks):
        """
        计算风险评分

        评分规则:
        - 基础分: 50分
        - 负面情感加分 (0-30分)
        - 风险类型加分 (每个风险类型10-20分)
        - 风险严重程度加分 (0-20分)

        参数:
            sentiment: 情感分析结果
            risks: 识别的风险列表

        返回:
            dict: 包含总评分和评分详情
        """
        score_details = {
            "base_score": 50,
            "sentiment_score": 0,
            "risk_type_score": 0,
            "severity_score": 0,
            "total_score": 50
        }

        # 负面情感增加风险分数
        polarity = sentiment.get("polarity", 0)
        if polarity < -0.1:
            # 越负面分数越高
            sentiment_score = abs(polarity) * 30
            score_details["sentiment_score"] = round(sentiment_score, 1)

        # 风险类型数量增加分数
        if risks:
            risk_type_score = len(risks) * 10
            score_details["risk_type_score"] = risk_type_score

            # 风险严重程度
            total_severity = sum(r.get("severity", 0) for r in risks)
            severity_score = min(total_severity * 3, 20)  # 最高20分
            score_details["severity_score"] = severity_score

        # 计算总分
        total = sum([
            score_details["base_score"],
            score_details["sentiment_score"],
            score_details["risk_type_score"],
            score_details["severity_score"]
        ])
        score_details["total_score"] = min(round(total), 100)

        # 确定风险等级
        score_details["risk_level"] = self._get_risk_level(score_details["total_score"])

        return score_details

    def _get_risk_level(self, score):
        """
        根据分数确定风险等级

        参数:
            score: 风险分数 (0-100)

        返回:
            str: 风险等级
        """
        if score >= RISK_THRESHOLDS["high"]:
            return "严重风险"
        elif score >= RISK_THRESHOLDS["medium"]:
            return "高风险"
        elif score >= RISK_THRESHOLDS["low"]:
            return "中风险"
        else:
            return "低风险"

    def analyze_article(self, article):
        """
        分析单条新闻 - 主入口函数

        参数:
            article: 新闻字典，包含title, description等字段

        返回:
            dict: 完整的分析结果
        """
        # 合并标题和描述进行分析
        full_text = f"{article.get('title', '')} {article.get('description', '')}"

        # 1. 情感分析
        sentiment = self.analyze_sentiment(full_text)

        # 2. 风险识别
        risks = self.identify_risks(full_text)

        # 3. 风险评分
        score = self.calculate_risk_score(sentiment, risks)

        return {
            "article": article,
            "sentiment": sentiment,
            "risks": risks,
            "score": score,
            "has_risk": len(risks) > 0 or sentiment.get("polarity", 0) < -0.1
        }


class PortfolioRiskAnalyzer:
    """组合风险分析器 - 分析多条新闻的综合风险"""

    def __init__(self):
        self.analyzer = RiskAnalyzer()

    def analyze_portfolio(self, articles):
        """
        分析一组新闻，生成综合报告

        参数:
            articles: 新闻列表

        返回:
            dict: 综合分析报告
        """
        if not articles:
            return {"error": "没有可分析的新闻"}

        # 分析每条新闻
        analyzed_articles = []
        all_risk_types = {}
        total_score = 0
        risk_count = 0
        sentiment_distribution = {"正面": 0, "负面": 0, "中性": 0}

        for article in articles:
            result = self.analyzer.analyze_article(article)
            analyzed_articles.append(result)

            # 统计情感分布
            sentiment_label = result["sentiment"].get("sentiment_label", "中性")
            sentiment_distribution[sentiment_label] += 1

            # 统计风险类型
            for risk in result["risks"]:
                risk_type = risk["risk_type"]
                if risk_type not in all_risk_types:
                    all_risk_types[risk_type] = {"count": 0, "articles": []}
                all_risk_types[risk_type]["count"] += 1
                all_risk_types[risk_type]["articles"].append(article.get("title", ""))

            # 累计风险分数
            if result["has_risk"]:
                total_score += result["score"]["total_score"]
                risk_count += 1

        # 计算平均风险分数
        avg_score = total_score / risk_count if risk_count > 0 else 0

        # 生成预警建议
        warnings = self._generate_warnings(all_risk_types, avg_score, sentiment_distribution)

        return {
            "total_articles": len(articles),
            "risky_articles": risk_count,
            "average_risk_score": round(avg_score, 1),
            "overall_risk_level": self._get_overall_risk_level(avg_score),
            "sentiment_distribution": sentiment_distribution,
            "risk_type_summary": all_risk_types,
            "analyzed_articles": analyzed_articles,
            "warnings": warnings
        }

    def _generate_warnings(self, risk_types, avg_score, sentiment_dist):
        """
        生成风险预警建议

        参数:
            risk_types: 风险类型统计
            avg_score: 平均风险分数
            sentiment_dist: 情感分布

        返回:
            list: 预警建议列表
        """
        warnings = []

        # 根据平均分数预警
        if avg_score >= 80:
            warnings.append({
                "level": "严重",
                "message": "检测到严重风险信号，建议立即采取应对措施！"
            })
        elif avg_score >= 60:
            warnings.append({
                "level": "高",
                "message": "存在较高风险，需要密切关注并准备应对预案。"
            })
        elif avg_score >= 40:
            warnings.append({
                "level": "中",
                "message": "存在一定风险，建议定期监控。"
            })

        # 根据负面新闻比例预警
        total = sum(sentiment_dist.values())
        if total > 0:
            negative_ratio = sentiment_dist["负面"] / total
            if negative_ratio > 0.5:
                warnings.append({
                    "level": "高",
                    "message": f"负面新闻占比高达{negative_ratio*100:.1f}%，需特别关注舆情变化。"
                })

        # 根据风险类型预警
        for risk_type, data in risk_types.items():
            if data["count"] >= 3:
                warnings.append({
                    "level": "中",
                    "message": f"检测到多次{risk_type}相关报道（{data['count']}次），建议专项调查。"
                })

        if not warnings:
            warnings.append({
                "level": "低",
                "message": "整体风险可控，继续保持监控即可。"
            })

        return warnings

    def _get_overall_risk_level(self, score):
        """获取整体风险等级"""
        if score >= 80:
            return "严重风险"
        elif score >= 60:
            return "高风险"
        elif score >= 40:
            return "中风险"
        elif score > 0:
            return "低风险"
        else:
            return "无风险"
