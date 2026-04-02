"""
realtime_app.py - 实时舆情监控Flask应用
集成WebSocket实现实时数据推送
"""

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, namespace
from flask_cors import CORS
import json
import threading
import time
from datetime import datetime

from realtime_monitor import RealtimeMonitor, RiskAlert
from news_fetcher import NewsFetcher
from risk_analyzer import PortfolioRiskAnalyzer

# 创建Flask应用
app = Flask(__name__)
app.config['SECRET_KEY'] = 'risk-sentinel-secret-key'

# 启用CORS
CORS(app)

# 创建SocketIO实例
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# 创建监控实例
monitor = RealtimeMonitor(socketio=socketio)

# 风险分析器
analyzer = PortfolioRiskAnalyzer()


# ========== HTTP路由 ==========

@app.route('/')
def index():
    """主页"""
    return render_template('realtime_dashboard.html')


@app.route('/api/monitor/start', methods=['POST'])
def start_monitoring():
    """启动监控"""
    data = request.json or {}
    keyword = data.get('keyword', 'IF椰子水')
    interval = data.get('interval_minutes', 30)

    task_id = monitor.start_monitoring(
        keyword=keyword,
        interval_minutes=interval
    )

    return jsonify({
        'success': True,
        'task_id': task_id,
        'message': f'监控已启动，关键词: {keyword}, 间隔: {interval}分钟'
    })


@app.route('/api/monitor/stop', methods=['POST'])
def stop_monitoring():
    """停止监控"""
    data = request.json or {}
    task_id = data.get('task_id')
    monitor.stop_monitoring(task_id)

    return jsonify({
        'success': True,
        'message': '监控已停止'
    })


@app.route('/api/monitor/status')
def get_monitor_status():
    """获取监控状态"""
    return jsonify({
        'success': True,
        'data': monitor.get_status()
    })


@app.route('/api/monitor/alerts')
def get_alerts():
    """获取预警列表"""
    level = request.args.get('level')
    limit = int(request.args.get('limit', 20))

    alerts = monitor.get_recent_alerts(level=level, limit=limit)

    return jsonify({
        'success': True,
        'data': alerts
    })


@app.route('/api/monitor/trend')
def get_trend():
    """获取趋势数据"""
    hours = int(request.args.get('hours', 24))
    trend_data = monitor.get_trend_data(hours=hours)

    return jsonify({
        'success': True,
        'data': trend_data
    })


@app.route('/api/analyze/realtime', methods=['POST'])
def analyze_realtime():
    """实时分析接口"""
    data = request.json or {}
    keyword = data.get('keyword', 'IF椰子水')

    # 获取最新数据
    fetcher = NewsFetcher()
    articles = fetcher.fetch_news(days_back=1)

    # 分析
    report = analyzer.analyze_portfolio(articles)

    return jsonify({
        'success': True,
        'data': report
    })


# ========== WebSocket事件 ==========

@socketio.on('connect', namespace='/monitor')
def handle_connect():
    """客户端连接"""
    print(f'[WebSocket] 客户端已连接: {request.sid}')
    emit('connected', {
        'message': '已连接到实时监控系统',
        'timestamp': datetime.now().isoformat()
    })


@socketio.on('disconnect', namespace='/monitor')
def handle_disconnect():
    """客户端断开"""
    print(f'[WebSocket] 客户端已断开: {request.sid}')


@socketio.on('start_monitoring', namespace='/monitor')
def handle_start_monitoring(data):
    """通过WebSocket启动监控"""
    keyword = data.get('keyword', 'IF椰子水')
    interval = data.get('interval_minutes', 30)

    task_id = monitor.start_monitoring(keyword, interval)

    emit('monitoring_started', {
        'task_id': task_id,
        'keyword': keyword,
        'interval_minutes': interval
    })


@socketio.on('stop_monitoring', namespace='/monitor')
def handle_stop_monitoring(data):
    """通过WebSocket停止监控"""
    task_id = data.get('task_id')
    monitor.stop_monitoring(task_id)

    emit('monitoring_stopped', {
        'task_id': task_id
    })


@socketio.on('request_status', namespace='/monitor')
def handle_request_status():
    """客户端请求状态"""
    status = monitor.get_status()
    emit('status_update', status)


@socketio.on('request_latest', namespace='/monitor')
def handle_request_latest():
    """客户端请求最新数据"""
    recent_posts = list(monitor.recent_posts)[-50:]  # 最近50条
    alerts = monitor.get_recent_alerts(limit=10)

    emit('latest_data', {
        'posts': recent_posts,
        'alerts': alerts,
        'timestamp': datetime.now().isoformat()
    })


# ========== 后台任务 ==========

def background_monitoring():
    """后台监控线程"""
    print("[后台线程] 监控服务启动")

    # 注册回调，当有新数据时通过WebSocket推送
    def on_new_data(posts, analysis):
        socketio.emit('data_update', {
            'type': 'new_data',
            'post_count': len(posts),
            'analysis': analysis,
            'timestamp': datetime.now().isoformat()
        }, namespace='/monitor')

    def on_alert(alert: RiskAlert):
        socketio.emit('new_alert', {
            'type': 'alert',
            'level': alert.level,
            'message': alert.message,
            'risk_score': alert.risk_score,
            'timestamp': alert.timestamp
        }, namespace='/monitor')

    monitor.on_new_data(on_new_data)
    monitor.on_alert(on_alert)


# ========== 主程序 ==========

if __name__ == '__main__':
    print("="*60)
    print("实时舆情监控系统启动")
    print("="*60)
    print("\n访问地址:")
    print("  Web界面: http://localhost:5000")
    print("  API文档: http://localhost:5000/api/docs")
    print("\n按 Ctrl+C 停止服务\n")

    # 启动后台监控线程
    monitoring_thread = threading.Thread(target=background_monitoring, daemon=True)
    monitoring_thread.start()

    # 启动SocketIO服务
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
