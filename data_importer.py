"""
data_importer.py - 舆情数据导入分析模块
支持从各平台导出的Excel/CSV文件导入分析
"""

import pandas as pd
import json
from datetime import datetime
from typing import List, Dict
from social_analyzer import SocialMediaAnalyzer, SocialMediaReportGenerator


class DataImporter:
    """数据导入器"""

    def __init__(self):
        self.analyzer = SocialMediaAnalyzer()

    def import_from_excel(self, file_path: str, platform: str = "unknown") -> List[Dict]:
        """
        从Excel文件导入数据

        Args:
            file_path: Excel文件路径
            platform: 平台名称（weibo/xiaohongshu/douyin）

        Returns:
            标准化的帖子列表
        """
        try:
            df = pd.read_excel(file_path)
            print(f"成功读取Excel文件，共 {len(df)} 行数据")
            return self._process_dataframe(df, platform)
        except Exception as e:
            print(f"读取Excel失败: {e}")
            return []

    def import_from_csv(self, file_path: str, platform: str = "unknown") -> List[Dict]:
        """
        从CSV文件导入数据
        """
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            print(f"成功读取CSV文件，共 {len(df)} 行数据")
            return self._process_dataframe(df, platform)
        except Exception as e:
            print(f"读取CSV失败: {e}")
            return []

    def import_from_text(self, text_content: str, platform: str = "unknown") -> List[Dict]:
        """
        从纯文本导入（每行一条）
        """
        posts = []
        lines = text_content.strip().split('\n')

        for i, line in enumerate(lines):
            if line.strip():
                # 自动进行情感分析
                sentiment_result = self.analyzer.analyze_sentiment(line)

                posts.append({
                    'platform': platform,
                    'content': line.strip(),
                    'author': f'user_{i}',
                    'published_at': datetime.now().isoformat(),
                    'sentiment': sentiment_result['label'],
                    'sentiment_detail': sentiment_result,
                    'likes': 0,
                    'comments': 0,
                    'source': 'manual_import'
                })

        print(f"成功导入 {len(posts)} 条文本数据")
        return posts

    def _process_dataframe(self, df: pd.DataFrame, platform: str) -> List[Dict]:
        """处理DataFrame数据"""
        posts = []

        # 自动识别列名（适配不同平台的导出格式）
        content_cols = ['内容', '正文', 'content', 'text', '标题']
        author_cols = ['作者', '用户', 'author', 'username', '昵称']
        time_cols = ['发布时间', '时间', 'publish_time', 'created_at', '日期']
        likes_cols = ['点赞数', '点赞', 'likes', 'like_count']
        comments_cols = ['评论数', '评论', 'comments', 'comment_count']

        # 找到实际存在的列
        content_col = self._find_column(df, content_cols)
        author_col = self._find_column(df, author_cols)
        time_col = self._find_column(df, time_cols)
        likes_col = self._find_column(df, likes_cols)
        comments_col = self._find_column(df, comments_cols)

        for _, row in df.iterrows():
            content = str(row.get(content_col, '')) if content_col else ''

            if not content or content == 'nan':
                continue

            # 情感分析
            sentiment_result = self.analyzer.analyze_sentiment(content)

            post = {
                'platform': platform,
                'content': content,
                'title': content[:50] + '...' if len(content) > 50 else content,
                'author': str(row.get(author_col, 'unknown')) if author_col else 'unknown',
                'published_at': str(row.get(time_col, datetime.now().isoformat())) if time_col else datetime.now().isoformat(),
                'sentiment': sentiment_result['label'],
                'sentiment_detail': sentiment_result,
                'likes': int(row.get(likes_col, 0)) if likes_col and pd.notna(row.get(likes_col)) else 0,
                'comments': int(row.get(comments_col, 0)) if comments_col and pd.notna(row.get(comments_col)) else 0,
                'source': 'imported'
            }

            posts.append(post)

        return posts

    def _find_column(self, df: pd.DataFrame, possible_names: List[str]) -> str:
        """查找匹配的列名"""
        columns = [col for col in df.columns]

        for name in possible_names:
            if name in columns:
                return name

        # 模糊匹配
        for col in columns:
            for name in possible_names:
                if name in col or col in name:
                    return col

        return None

    def generate_report(self, posts: List[Dict], keyword: str = "IF椰子水") -> Dict:
        """
        生成舆情分析报告
        """
        report_gen = SocialMediaReportGenerator(self.analyzer)
        return report_gen.generate_report(posts, keyword)

    def save_to_json(self, posts: List[Dict], output_file: str = "social_media_data.json"):
        """保存为JSON文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {output_file}")


# 使用示例
def quick_import_example():
    """
    快速导入示例

    使用方法:
    1. 从清博指数/新榜导出Excel文件
    2. 运行: python data_importer.py
    3. 输入文件路径
    4. 自动生成分析报告
    """
    importer = DataImporter()

    print("=" * 60)
    print("舆情数据导入工具")
    print("=" * 60)
    print("\n支持的文件格式:")
    print("  - Excel (.xlsx)")
    print("  - CSV (.csv)")
    print("  - 纯文本 (.txt)")
    print("\n数据来源:")
    print("  - 清博指数 (qingbo_data.xlsx)")
    print("  - 新榜 (newrank_data.xlsx)")
    print("  - 手动复制粘贴 (paste.txt)")
    print("=" * 60)

    # 示例：从文本导入
    sample_text = """
IF椰子水真的很好喝，已经回购好几次了
买了IF椰子水，感觉甜得不太自然
客服说是纯椰子水，但我喝了血糖升高了
一直在喝IF，没什么问题啊
看到有人说掺糖，不知道真假
"""

    posts = importer.import_from_text(sample_text, "user_import")

    # 生成报告
    report = importer.generate_report(posts, "IF椰子水")

    # 打印报告
    print("\n" + "=" * 60)
    print("舆情分析报告")
    print("=" * 60)
    print(f"\n总帖子数: {report['summary']['total_posts']}")
    print(f"风险等级: {report['summary']['risk_level']} ({report['summary']['risk_color']})")
    print(f"负面比例: {report['summary']['negative_ratio']}%")

    print("\n情感分布:")
    for sentiment, count in report['sentiment_analysis']['distribution'].items():
        print(f"  {sentiment}: {count}")

    print("\n主要争议点:")
    for c in report['controversies'][:3]:
        print(f"  {c['category']}: {c['mentions']}次 (争议度: {c['controversy_level']})")

    print("\n建议:")
    for i, suggestion in enumerate(report['suggestions'][:3], 1):
        print(f"  {i}. {suggestion}")

    # 保存数据
    importer.save_to_json(posts, "imported_data.json")


if __name__ == "__main__":
    quick_import_example()
