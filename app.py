"""
app.py - 主程序入口
Flask Web应用，提供网页界面和API接口
"""

from flask import Flask, render_template, jsonify
from news_fetcher import NewsFetcher
from risk_analyzer import PortfolioRiskAnalyzer

# 创建Flask应用实例
app = Flask(__name__)


@app.route('/')
def index():
    """
    首页路由
    返回主页面
    """
    return render_template('index.html')


@app.route('/api/analyze')
def analyze():
    """
    分析API接口
    获取新闻并进行风险分析，返回JSON格式的分析结果

    访问地址: http://localhost:5000/api/analyze
    """
    try:
        # 第1步：获取新闻
        print("正在获取新闻...")
        fetcher = NewsFetcher()
        articles = fetcher.fetch_news(days_back=30)

        if not articles:
            return jsonify({
                "success": False,
                "error": "未能获取到新闻数据"
            }), 500

        # 第2步：分析风险
        print("正在分析风险...")
        analyzer = PortfolioRiskAnalyzer()
        report = analyzer.analyze_portfolio(articles)

        # 返回分析结果
        return jsonify({
            "success": True,
            "data": report
        })

    except Exception as e:
        print(f"分析过程出错: {e}")
        return jsonify({
            "success": False,
            "error": f"分析失败: {str(e)}"
        }), 500


@app.route('/api/health')
def health_check():
    """
    健康检查接口
    用于确认服务是否正常运行
    """
    return jsonify({
        "status": "ok",
        "message": "风险哨兵智能体运行正常"
    })


# 主程序入口
if __name__ == '__main__':
    print("=" * 50)
    print("[ROBOT] 风险哨兵智能体启动中...")
    print("=" * 50)
    print("访问地址: http://localhost:5000")
    print("API地址: http://localhost:5000/api/analyze")
    print("=" * 50)

    # 启动Flask服务器
    # debug=True: 开启调试模式，代码修改后自动重启
    # host='0.0.0.0': 允许外部访问
    # port=5000: 端口号
    app.run(debug=True, host='0.0.0.0', port=5000)
