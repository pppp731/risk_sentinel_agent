"""
Vercel 部署入口文件
将 Flask 应用适配为 Serverless 函数
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import json
from datetime import datetime

# 导入我们之前的模块
from news_fetcher import NewsFetcher
from risk_analyzer import PortfolioRiskAnalyzer
from data_importer import DataImporter

# 创建 Flask 应用
app = Flask(__name__,
    template_folder='../templates',
    static_folder='../static'
)
CORS(app)

# 初始化分析器
analyzer = PortfolioRiskAnalyzer()
fetcher = NewsFetcher()

@app.route('/')
def index():
    """主页 - 返回实时监控仪表盘"""
    return render_template('realtime_dashboard.html')

@app.route('/simple')
def simple():
    """简化版仪表盘（不需要WebSocket）"""
    return render_template('simple_dashboard.html')

@app.route('/api/analyze')
def api_analyze():
    """分析 API"""
    try:
        # 获取新闻
        articles = fetcher.fetch_news(days_back=3)

        if not articles:
            return jsonify({
                "success": False,
                "error": "未能获取到数据"
            }), 500

        # 分析
        report = analyzer.analyze_portfolio(articles)

        return jsonify({
            "success": True,
            "data": report,
            "timestamp": datetime.now().isoformat()
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/status')
def api_status():
    """系统状态"""
    return jsonify({
        "status": "ok",
        "message": "风险哨兵智能体运行正常",
        "version": "2.0",
        "features": [
            "实时舆情监控",
            "NLP情感分析",
            "风险识别预警",
            "数据可视化"
        ]
    })

# Vercel 需要的 handler
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('风险哨兵智能体已部署'.encode())

# 本地运行
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
