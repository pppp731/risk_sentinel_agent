"""
realtime_monitor.py - 实时舆情监控系统
功能：
1. 定时抓取最新舆情数据
2. 增量更新，避免重复
3. 风险阈值预警
4. 趋势分析和存储
5. 实时推送通知
"""

import json
import os
import time
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict
from collections import deque
import threading

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from flask_socketio import SocketIO, emit

from news_fetcher import NewsFetcher
from social_media_fetcher import SocialMediaAggregator
from risk_analyzer import PortfolioRiskAnalyzer


@dataclass
class RiskAlert:
    """风险预警数据类"""
    timestamp: str
    level: str  # critical, high, medium, low
    message: str
    risk_score: float
    source: str
    details: Dict


@dataclass
class MonitoringTask:
    """监控任务数据类"""
    task_id: str
    keyword: str
    interval_minutes: int
    last_run: Optional[str]
    status: str  # running, paused, stopped
    total_runs: int
    data_count: int


class RealtimeMonitor:
    """
    实时舆情监控核心类

    功能：
    - 定时执行舆情抓取任务
    - 检测新增内容
    - 风险阈值监控
    - 历史数据存储
    - 趋势分析
    """

    def __init__(self, socketio: Optional[SocketIO] = None):
        self.scheduler = BackgroundScheduler()
        self.socketio = socketio
        self.news_fetcher = NewsFetcher()
        self.social_fetcher = SocialMediaAggregator()
        self.risk_analyzer = PortfolioRiskAnalyzer()

        # 数据存储
        self.data_dir = "monitoring_data"
        self._ensure_data_dir()

        # 内存缓存（最近1000条）
        self.recent_posts = deque(maxlen=1000)
        self.alerts_history = deque(maxlen=500)

        # 已处理内容的指纹集合（用于去重）
        self.processed_fingerprints = set()

        # 监控任务状态
        self.tasks = {}
        self.monitoring = False

        # 回调函数（用于外部通知）
        self.alert_callbacks: List[Callable] = []
        self.data_callbacks: List[Callable] = []

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _get_fingerprint(self, post: Dict) -> str:
        """生成内容指纹用于去重"""
        content = post.get('content', '') or post.get('title', '')
        source = post.get('source', 'unknown')
        # 使用内容前50字符+来源作为指纹
        return f"{source}:{content[:50]}"

    def _is_new_post(self, post: Dict) -> bool:
        """检查是否为新增内容"""
        fingerprint = self._get_fingerprint(post)
        if fingerprint in self.processed_fingerprints:
            return False
        self.processed_fingerprints.add(fingerprint)
        return True

    def _analyze_sentiment_trend(self, posts: List[Dict]) -> Dict:
        """分析情感趋势"""
        if not posts:
            return {}

        # 按小时分组统计
        hourly_stats = {}
        for post in posts:
            time_str = post.get('published_at', '')
            if time_str:
                hour = time_str[:13]  # 精确到小时
                if hour not in hourly_stats:
                    hourly_stats[hour] = {'positive': 0, 'negative': 0, 'neutral': 0}

                sentiment = post.get('sentiment', '中性')
                if sentiment == '正面':
                    hourly_stats[hour]['positive'] += 1
                elif sentiment == '负面':
                    hourly_stats[hour]['negative'] += 1
                else:
                    hourly_stats[hour]['neutral'] += 1

        return hourly_stats

    def _check_risk_thresholds(self, analysis_result: Dict) -> List[RiskAlert]:
        """检查风险阈值并生成预警"""
        alerts = []

        # 检查1：整体风险评分
        avg_score = analysis_result.get('average_risk_score', 0)
        if avg_score >= 80:
            alerts.append(RiskAlert(
                timestamp=datetime.now().isoformat(),
                level='critical',
                message='风险评分超过80分，达到严重级别！',
                risk_score=avg_score,
                source='risk_score_monitor',
                details={'score': avg_score, 'threshold': 80}
            ))
        elif avg_score >= 60:
            alerts.append(RiskAlert(
                timestamp=datetime.now().isoformat(),
                level='high',
                message='风险评分超过60分，需要密切关注！',
                risk_score=avg_score,
                source='risk_score_monitor',
                details={'score': avg_score, 'threshold': 60}
            ))

        # 检查2：负面情感比例
        sentiment_dist = analysis_result.get('sentiment_distribution', {})
        total = sum(sentiment_dist.values())
        if total > 0:
            negative_ratio = sentiment_dist.get('负面', 0) / total
            if negative_ratio >= 0.5:
                alerts.append(RiskAlert(
                    timestamp=datetime.now().isoformat(),
                    level='high',
                    message=f'负面舆情占比高达{negative_ratio*100:.1f}%，存在声誉风险！',
                    risk_score=negative_ratio * 100,
                    source='sentiment_monitor',
                    details={'negative_ratio': negative_ratio}
                ))

        # 检查3：特定风险类型
        risk_types = analysis_result.get('risk_type_summary', {})
        for risk_type, data in risk_types.items():
            if data['count'] >= 5:  # 某类风险提及超过5次
                alerts.append(RiskAlert(
                    timestamp=datetime.now().isoformat(),
                    level='medium',
                    message=f'{risk_type}相关讨论激增（{data["count"]}次），建议关注',
                    risk_score=min(data['count'] * 10, 100),
                    source='risk_type_monitor',
                    details={'risk_type': risk_type, 'count': data['count']}
                ))

        # 保存预警历史
        self.alerts_history.extend(alerts)

        return alerts

    def _save_monitoring_data(self, posts: List[Dict], analysis: Dict, alerts: List[RiskAlert]):
        """保存监控数据到文件"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # 保存原始数据
        data_file = os.path.join(self.data_dir, f'data_{timestamp}.json')
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'posts': posts,
                'post_count': len(posts)
            }, f, ensure_ascii=False, indent=2)

        # 保存分析结果
        analysis_file = os.path.join(self.data_dir, f'analysis_{timestamp}.json')
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump({
                'timestamp': timestamp,
                'analysis': analysis
            }, f, ensure_ascii=False, indent=2)

        # 保存预警
        if alerts:
            alerts_file = os.path.join(self.data_dir, f'alerts_{timestamp}.json')
            with open(alerts_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'timestamp': timestamp,
                    'alerts': [asdict(alert) for alert in alerts]
                }, f, ensure_ascii=False, indent=2)

    def _execute_monitoring_job(self, keyword: str, sources: List[str] = None):
        """执行监控任务"""
        print(f"\n[{datetime.now()}] 执行监控任务: {keyword}")

        try:
            # 1. 获取最新数据
            all_new_posts = []

            if sources is None or 'news' in sources:
                # 获取新闻数据
                news_data = self.news_fetcher.fetch_news(days_back=1)
                for article in news_data:
                    if self._is_new_post(article):
                        all_new_posts.append(article)

            if sources is None or 'social' in sources:
                # 获取社交媒体数据
                social_data = self.social_fetcher.fetch_all(keyword, days_back=1)
                for post in social_data.get('all_posts', []):
                    if self._is_new_post(post):
                        all_new_posts.append(post)

            if not all_new_posts:
                print(f"  未发现新内容")
                return

            print(f"  发现 {len(all_new_posts)} 条新内容")

            # 2. 添加到内存缓存
            self.recent_posts.extend(all_new_posts)

            # 3. 风险分析
            analysis = self.risk_analyzer.analyze_portfolio(all_new_posts)

            # 4. 检查风险阈值
            alerts = self._check_risk_thresholds(analysis)

            if alerts:
                print(f"  ⚠️  触发 {len(alerts)} 个预警")
                for alert in alerts:
                    print(f"     [{alert.level.upper()}] {alert.message}")

            # 5. 保存数据
            self._save_monitoring_data(all_new_posts, analysis, alerts)

            # 6. 通过WebSocket推送实时更新
            if self.socketio:
                self.socketio.emit('new_data', {
                    'timestamp': datetime.now().isoformat(),
                    'new_posts_count': len(all_new_posts),
                    'analysis': analysis,
                    'alerts': [asdict(alert) for alert in alerts]
                }, namespace='/monitor')

            # 7. 执行回调
            for callback in self.data_callbacks:
                callback(all_new_posts, analysis)

            for callback in self.alert_callbacks:
                for alert in alerts:
                    callback(alert)

            # 8. 更新任务状态
            task_id = f"monitor_{keyword}"
            if task_id in self.tasks:
                self.tasks[task_id].total_runs += 1
                self.tasks[task_id].data_count += len(all_new_posts)
                self.tasks[task_id].last_run = datetime.now().isoformat()

        except Exception as e:
            print(f"  监控任务执行失败: {e}")
            import traceback
            traceback.print_exc()

    def start_monitoring(self, keyword: str = "IF椰子水",
                        interval_minutes: int = 30,
                        sources: List[str] = None) -> str:
        """
        启动实时监控

        Args:
            keyword: 监控关键词
            interval_minutes: 抓取间隔（分钟）
            sources: 数据源列表 ['news', 'social']

        Returns:
            任务ID
        """
        task_id = f"monitor_{keyword}"

        if task_id in self.tasks and self.tasks[task_id].status == 'running':
            print(f"监控任务 '{keyword}' 已在运行中")
            return task_id

        # 创建任务
        task = MonitoringTask(
            task_id=task_id,
            keyword=keyword,
            interval_minutes=interval_minutes,
            last_run=None,
            status='running',
            total_runs=0,
            data_count=0
        )
        self.tasks[task_id] = task

        # 添加定时任务
        self.scheduler.add_job(
            func=self._execute_monitoring_job,
            trigger=IntervalTrigger(minutes=interval_minutes),
            id=task_id,
            args=[keyword, sources],
            replace_existing=True
        )

        # 启动调度器
        if not self.scheduler.running:
            self.scheduler.start()
            self.monitoring = True
            print(f"\n✅ 实时监控系统已启动")
            print(f"   关键词: {keyword}")
            print(f"   监控间隔: {interval_minutes} 分钟")
            print(f"   任务ID: {task_id}\n")

        # 立即执行一次
        self._execute_monitoring_job(keyword, sources)

        return task_id

    def stop_monitoring(self, task_id: str = None):
        """停止监控"""
        if task_id and task_id in self.tasks:
            self.scheduler.remove_job(task_id)
            self.tasks[task_id].status = 'stopped'
            print(f"监控任务 '{task_id}' 已停止")
        else:
            self.scheduler.shutdown()
            self.monitoring = False
            print("所有监控任务已停止")

    def pause_monitoring(self, task_id: str):
        """暂停监控"""
        if task_id in self.tasks:
            self.scheduler.pause_job(task_id)
            self.tasks[task_id].status = 'paused'
            print(f"监控任务 '{task_id}' 已暂停")

    def resume_monitoring(self, task_id: str):
        """恢复监控"""
        if task_id in self.tasks:
            self.scheduler.resume_job(task_id)
            self.tasks[task_id].status = 'running'
            print(f"监控任务 '{task_id}' 已恢复")

    def get_status(self) -> Dict:
        """获取监控状态"""
        return {
            'is_monitoring': self.monitoring,
            'active_tasks': [
                {
                    'task_id': task.task_id,
                    'keyword': task.keyword,
                    'interval_minutes': task.interval_minutes,
                    'status': task.status,
                    'total_runs': task.total_runs,
                    'data_count': task.data_count,
                    'last_run': task.last_run
                }
                for task in self.tasks.values()
            ],
            'recent_posts_count': len(self.recent_posts),
            'alerts_count': len(self.alerts_history),
            'processed_count': len(self.processed_fingerprints)
        }

    def get_recent_alerts(self, level: str = None, limit: int = 20) -> List[Dict]:
        """获取最近的预警"""
        alerts = list(self.alerts_history)
        if level:
            alerts = [a for a in alerts if a.level == level]
        return [asdict(a) for a in alerts[-limit:]]

    def get_trend_data(self, hours: int = 24) -> Dict:
        """获取趋势数据"""
        posts = list(self.recent_posts)

        # 过滤最近N小时的数据
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_posts = [
            p for p in posts
            if datetime.fromisoformat(p.get('published_at', '2000-01-01')) > cutoff_time
        ]

        return {
            'total_posts': len(recent_posts),
            'hourly_trend': self._analyze_sentiment_trend(recent_posts),
            'risk_distribution': self._analyze_risk_distribution(recent_posts)
        }

    def _analyze_risk_distribution(self, posts: List[Dict]) -> Dict:
        """分析风险分布"""
        risk_counts = {}
        for post in posts:
            risks = post.get('risks', [])
            for risk in risks:
                risk_type = risk.get('risk_type', '其他')
                risk_counts[risk_type] = risk_counts.get(risk_type, 0) + 1
        return risk_counts

    def on_alert(self, callback: Callable):
        """注册预警回调函数"""
        self.alert_callbacks.append(callback)

    def on_new_data(self, callback: Callable):
        """注册新数据回调函数"""
        self.data_callbacks.append(callback)


# 使用示例
if __name__ == "__main__":
    print("实时舆情监控系统")
    print("=" * 60)

    # 创建监控实例
    monitor = RealtimeMonitor()

    # 注册预警回调
    def on_alert(alert: RiskAlert):
        print(f"\n🚨 新预警: [{alert.level.upper()}] {alert.message}")

    def on_data(posts, analysis):
        print(f"\n📊 新数据: {len(posts)} 条帖子，风险评分: {analysis.get('average_risk_score', 0)}")

    monitor.on_alert(on_alert)
    monitor.on_new_data(on_data)

    # 启动监控（每5分钟执行一次，测试用）
    task_id = monitor.start_monitoring(
        keyword="IF椰子水",
        interval_minutes=5,
        sources=['news', 'social']
    )

    print("\n监控运行中，按 Ctrl+C 停止...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n停止监控...")
        monitor.stop_monitoring()
        print("已退出")
