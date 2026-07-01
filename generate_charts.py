"""生成报告所需7张可视化图表"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('report_charts', exist_ok=True)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# ===== Chart 1: 四情景EL柱状图 =====
fig, ax = plt.subplots(figsize=(8, 4.5))
scenarios = ['乐观情景\n(15%)', '基准情景\n(50%)', '悲观情景\n(25%)', '极端情景\n(10%)']
el_values = [22.0, 44.0, 57.0, 57.0]
colors = ['#00c853', '#fee440', '#ff6b6b', '#ef233c']
bars = ax.bar(scenarios, el_values, color=colors, edgecolor='white', linewidth=0.8, width=0.55)
for bar, val in zip(bars, el_values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1.5, f'EL={val}',
            ha='center', fontsize=11, fontweight='bold')
ax.axhline(y=45.2, color='#00f5d4', linestyle='--', linewidth=1.5, label=f'加权EL=45.2')
ax.legend(fontsize=10, loc='upper left')
ax.set_ylabel('预期损失 (EL)', fontsize=11)
ax.set_title('多情景分析 —— 四情景预期损失分布', fontsize=13, fontweight='bold', pad=12)
ax.set_ylim(0, 70)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.2)
plt.tight_layout(); plt.savefig('report_charts/chart_scenarios.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 2: EL有/无财务调整对比 =====
fig, ax = plt.subplots(figsize=(7, 4.5))
labels = ['无财务调整\n(基准)', '融入IFBH财务\n(1.8x)', '财务健康假设\n(0.9x)']
el_vals = [12.67, 41.04, 10.21]
pd_vals = [0.20, 0.36, 0.18]
ead_vals = [100, 180, 90]
x = np.arange(len(labels)); w=0.25
b1=ax.bar(x-w, el_vals, w, color='#00f5d4', label='EL值')
ax_twin=ax.twinx()
b2=ax_twin.bar(x, pd_vals, w, color='#fee440', label='PD')
b3=ax_twin.bar(x+w, [v/2 for v in ead_vals], w, color='#ff006e', label='EAD/2')
ax.set_ylabel('EL值', fontsize=11, color='#00f5d4')
ax_twin.set_ylabel('PD / EAD', fontsize=11, color='#888')
ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=10)
for b,v in zip(b1,el_vals): ax.text(b.get_x()+b.get_width()/2, b.get_height()+1, str(v), ha='center', fontsize=10, fontweight='bold')
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_twin.get_legend_handles_labels()
ax.legend(lines1+lines2, labels1+labels2, fontsize=9, loc='upper left')
ax.set_title('EL模型：财务调整因子影响对比', fontsize=13, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False); ax_twin.spines['top'].set_visible(False)
ax.grid(axis='y', alpha=0.15)
plt.tight_layout(); plt.savefig('report_charts/chart_el_comparison.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 3: 四阶段代码增长 =====
fig, ax = plt.subplots(figsize=(8, 4.5))
phases = ['Phase 1\n基础舆情', 'Phase 2\n量化风险', 'Phase 3\nAgent编排', 'Phase 4\n多维扩展']
lines = [450, 1050, 2150, 7050]
modules = [4, 7, 11, 21]
ax.fill_between(range(len(phases)), 0, lines, alpha=0.15, color='#00f5d4')
ax.plot(range(len(phases)), lines, 'o-', color='#00f5d4', linewidth=2.5, markersize=12, markerfacecolor='white', markeredgewidth=2)
for i,(l,m) in enumerate(zip(lines, modules)):
    ax.annotate(f'{l}行\n{m}模块', (i,l), textcoords="offset points", xytext=(0,18), ha='center', fontsize=10, fontweight='bold', color='#333')
ax.set_xticks(range(len(phases))); ax.set_xticklabels(phases, fontsize=10)
ax.set_ylabel('代码行数', fontsize=11); ax.set_title('开发阶段演进 —— 代码量与模块增长', fontsize=13, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.15); ax.set_ylim(0, 8000)
plt.tight_layout(); plt.savefig('report_charts/chart_code_growth.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 4: 模块代码量分布 =====
fig, ax = plt.subplots(figsize=(8, 5))
modules_data = [
    ('news_fetcher', 894), ('risk_response', 791), ('app', 733),
    ('quantitative_risk', 550), ('mcp_data_warehouse', 527), ('risk_analyzer', 498),
    ('realtime_monitor', 472), ('social_media_fetcher', 427), ('enterprise_monitor', 397),
    ('ecommerce_monitor', 342), ('financial_monitor', 318), ('policy_monitor', 318),
    ('weekly_report', 290), ('baidu_nlp', 275), ('history_manager', 251),
]
modules_data.sort(key=lambda x: x[1])
names = [m[0] for m in modules_data]
vals = [m[1] for m in modules_data]
bars = ax.barh(names, vals, color=['#00f5d4' if v>500 else '#fee440' if v>300 else '#ccc' for v in vals], edgecolor='white', linewidth=0.5)
for bar, v in zip(bars, vals):
    ax.text(bar.get_width()+8, bar.get_y()+bar.get_height()/2, str(v), va='center', fontsize=8)
ax.set_xlabel('代码行数', fontsize=11)
ax.set_title('核心模块代码量分布 (Top 15)', fontsize=13, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='x', alpha=0.15)
plt.tight_layout(); plt.savefig('report_charts/chart_modules.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 5: 七模块红绿灯仪表盘 =====
fig, ax = plt.subplots(figsize=(8, 3.5))
modules_tl = ['新闻舆情', '定量风险', '电商监控', '企业风险', '财务健康', '政策红线', '卡脖子风险']
signals = ['yellow', 'red', 'yellow', 'yellow', 'red', 'red', 'red']
values = [72, 41.0, 4.5, 59, 92, 90, 81]
colors_tl = ['#fee440' if s=='yellow' else '#ef233c' for s in signals]
x_pos = range(len(modules_tl))
ax.scatter(x_pos, [1]*len(modules_tl), s=[v*5+100 for v in values], c=colors_tl, alpha=0.8, edgecolors='white', linewidth=1.5)
for i,(name,sig,val) in enumerate(zip(modules_tl, signals, values)):
    label_text = 'HIGH' if sig=='red' else 'MID'
    ax.annotate(f'{label_text}\n{val}', (i,1), textcoords="offset points", xytext=(0, -35), ha='center', fontsize=9, fontweight='bold', color=colors_tl[i])
ax.set_xticks(x_pos); ax.set_xticklabels(modules_tl, fontsize=9, rotation=15)
ax.set_ylim(0.5, 1.5); ax.set_yticks([])
ax.set_title('七模块风险红绿灯仪表盘', fontsize=13, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['left'].set_visible(False)
plt.tight_layout(); plt.savefig('report_charts/chart_traffic_light.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 6: 五维策略库概览 =====
fig, ax = plt.subplots(figsize=(8, 4.5))
dims = ['供应链\n应对', '品牌\n公关', '法律\n合规', '市场\n保卫', '财务\n对冲']
action_counts = [4, 4, 3, 3, 3]
costs = [700, 11, 20, 7, 220]  # 万元
x=np.arange(len(dims)); w=0.35
b1=ax.bar(x-w/2, action_counts, w, color='#00f5d4', label='行动项数量')
ax_twin2=ax.twinx()
b2=ax_twin2.bar(x+w/2, costs, w, color='#ff006e', alpha=0.7, label='预估成本(万元)')
ax.set_ylabel('行动项数量', fontsize=11)
ax_twin2.set_ylabel('预估成本(万元)', fontsize=11, color='#ff006e')
for b,v in zip(b1,action_counts): ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.15, str(v), ha='center', fontweight='bold')
for b,v in zip(b2,costs): ax_twin2.text(b.get_x()+b.get_width()/2, b.get_height()+5, str(v), ha='center', fontsize=9, color='#ff006e')
ax.set_xticks(x); ax.set_xticklabels(dims, fontsize=10)
lines1,l1=ax.get_legend_handles_labels(); lines2,l2=ax_twin2.get_legend_handles_labels()
ax.legend(lines1+lines2,l1+l2,fontsize=9,loc='upper right')
ax.set_title('五维风险应对策略库 —— 行动项与成本概览', fontsize=13, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False); ax_twin2.spines['top'].set_visible(False)
plt.tight_layout(); plt.savefig('report_charts/chart_strategy.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 7: 新闻管道数据流 =====
fig, ax = plt.subplots(figsize=(8, 3))
stages = ['原始获取\n(10源)', '去重后', '品牌过滤后', '+Demo\n(25条)', '最终\n分析管道']
counts = [109, 86, 49, 74, 71]
colors_flow = ['#888', '#fee440', '#ff6b6b', '#00f5d4', '#00c853']
bars = ax.bar(range(len(stages)), counts, color=colors_flow, edgecolor='white', linewidth=1, width=0.6)
for bar,v in zip(bars, counts):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+2, str(v), ha='center', fontsize=11, fontweight='bold')
ax.set_xticks(range(len(stages))); ax.set_xticklabels(stages, fontsize=10)
ax.set_ylabel('新闻数量', fontsize=11)
ax.set_title('新闻抓取管道 —— 从原始数据到分析输入', fontsize=13, fontweight='bold', pad=12)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(axis='y', alpha=0.15); ax.set_ylim(0, 130)
plt.tight_layout(); plt.savefig('report_charts/chart_news_pipeline.png', dpi=200, bbox_inches='tight'); plt.close()

print('7 charts generated in report_charts/')
