# 舆情分析运行脚本 - 一键分析
import sys
import os

# 使用示例数据运行分析
sample_data = """
IF椰子水真的很好喝，回购好几次了！
买了IF椰子水，感觉甜得不太正常，怀疑加了糖
客服说是100%纯椰子水，但喝了血糖确实升高了
一直在喝IF，感觉还不错，希望不是假的
看到有人说掺糖，不知道该信谁了
官方发了检测报告，应该是真的吧
避雷！这个椰子水太甜了，不是纯的
孕妇慎喝，血糖会升高
性价比挺高的，比VitaCoco便宜
味道怪怪的，跟新鲜椰子不一样
"""

from data_importer import DataImporter
importer = DataImporter()
posts = importer.import_from_text(sample_data, "demo")

if posts:
    report = importer.generate_report(posts, "IF椰子水")

    # 打印报告
    print("="*60)
    print("舆情分析报告")
    print("="*60)
    print("\n[数据概况]")
    print("   总帖子数:", report['summary']['total_posts'], "条")
    print("   风险等级:", report['summary']['risk_level'], "(", report['summary']['risk_color'], ")")
    print("   负面比例:", report['summary']['negative_ratio'], "%")

    print("\n[情感分布]")
    for sentiment, count in report['sentiment_analysis']['distribution'].items():
        pct = report['sentiment_analysis']['percentages'].get(sentiment, 0)
        bar = '#' * int(pct / 5)
        print("  ", sentiment, ":", count, "条 (", pct, "%) ", bar)

    print("\n[争议热点]")
    for i, c in enumerate(report['controversies'][:5], 1):
        level_str = '[' + c['controversy_level'] + ']'
        print("  ", i, ".", level_str, c['category'], ":", c['mentions'], "次提及")

    print("\n[应对建议]")
    for i, suggestion in enumerate(report['suggestions'][:3], 1):
        print("  ", i, ".", suggestion)

    # 保存结果
    importer.save_to_json(posts, "analysis_result.json")

    print("\n" + "="*60)
    print("分析完成！数据已保存到 analysis_result.json")
    print("="*60)
else:
    print("没有可分析的数据")
