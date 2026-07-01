"""为IFBH主报告生成5张图表"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

os.makedirs('report_charts', exist_ok=True)
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
FIGSIZE = (7.5, 4.5)

# ===== Chart 1: 营收与净利润趋势 (放于2.2营收结构) =====
fig, ax1 = plt.subplots(figsize=(7, 4.2))
years = ['2023', '2024', '2025']
revenue = [118, 158, 176]
profit = [25, 33.3, 22.8]
margin = [21.2, 21.1, 13.0]
bar1 = ax1.bar(years, revenue, 0.5, color='#00f5d4', alpha=0.7, label='营业收入(百万美元)')
ax1.set_ylabel('营业收入 (百万美元)', fontsize=10, color='#00a88a')
ax2 = ax1.twinx()
line1, = ax2.plot(years, profit, 'o-', color='#ef233c', linewidth=2.5, markersize=10, label='净利润(百万美元)')
for i, (r, p) in enumerate(zip(revenue, profit)):
    ax1.text(i, r+5, f'${r}M', ha='center', fontsize=9, color='#00a88a')
    ax2.text(i, p+1, f'${p}M', ha='center', fontsize=9, color='#ef233c')
ax2.set_ylabel('净利润 (百万美元)', fontsize=10, color='#ef233c')
ax1.set_xticks(range(len(years))); ax1.set_xticklabels(years, fontsize=11)
ax1.set_title('IFBH 营业收入与净利润趋势 (2023-2025)', fontsize=13, fontweight='bold', pad=10)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend([bar1, line1], ['营业收入', '净利润'], fontsize=9, loc='upper left')
ax1.spines['top'].set_visible(False); ax2.spines['top'].set_visible(False)
ax1.grid(axis='y', alpha=0.12)
plt.tight_layout(); plt.savefig('report_charts/chart_revenue.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 2: 风险矩阵气泡图 (放于4.2风险矩阵评估) =====
fig, ax = plt.subplots(figsize=(7.5, 5))
risks = [
    ('R1 供应链集中', 4, 5, 20, '#ef233c'),
    ('R2 品牌声誉', 4, 5, 20, '#ef233c'),
    ('R3 单一市场依赖', 5, 4, 20, '#ef233c'),
    ('R4 财务恶化', 4, 4, 16, '#ff6b6b'),
    ('R5 法律合规', 4, 3, 12, '#fee440'),
    ('R6 代工品控', 3, 4, 12, '#fee440'),
    ('R7 汇率波动', 4, 2, 8, '#00c853'),
    ('R8 关键人才', 2, 5, 10, '#fee440'),
]
for name, prob, impact, score, color in risks:
    ax.scatter(prob, impact, s=score*40, c=color, alpha=0.7, edgecolors='white', linewidth=1.5, zorder=5)
    ax.annotate(name, (prob, impact), textcoords="offset points", xytext=(8, 8), fontsize=8, fontweight='bold', color='#333')
# Zone lines
ax.axhline(y=3, xmin=0, xmax=0.6, color='#ccc', linestyle='--', linewidth=0.8)
ax.axvline(x=3, ymin=0, ymax=0.6, color='#ccc', linestyle='--', linewidth=0.8)
ax.fill_between([0,5], [0,0], [2.9,2.9], alpha=0.03, color='green')
ax.fill_between([0,5], [3.1,3.1], [5,5], alpha=0.03, color='red')
ax.fill_between([0,2.9], [0,0], [5,5], alpha=0.02, color='green')
ax.fill_between([3.1,5], [0,0], [5,5], alpha=0.02, color='red')
ax.text(1.5, 1.5, '低风险区', fontsize=8, color='#888', ha='center')
ax.text(4, 4.5, '重大风险区', fontsize=8, color='#888', ha='center')
ax.set_xlabel('可能性 (1-5)', fontsize=11); ax.set_ylabel('影响程度 (1-5)', fontsize=11)
ax.set_xlim(0.5, 5.5); ax.set_ylim(0.5, 5.5)
ax.set_title('IFBH 风险矩阵 — 可能性 × 影响程度', fontsize=13, fontweight='bold', pad=10)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
ax.grid(alpha=0.1)
plt.tight_layout(); plt.savefig('report_charts/chart_risk_matrix.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 3: 股权结构简图 (放于1.1基本信息) =====
fig, ax = plt.subplots(figsize=(7.5, 3.8))
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis('off')
# Boxes
boxes = [
    (3, 4.2, 4, 0.6, 'Pongsakorn Pongsak (创始人/CEO)', '#f0f0f0'),
    (3, 3.0, 4, 0.6, 'General Beverage Co., Ltd. (控股股东/核心供应商)', '#d4e6f1'),
    (1, 1.5, 3, 0.6, '公众股东 (~34.5%)', '#e8e8e8'),
    (6, 1.5, 3, 0.6, '其他机构投资者', '#e8e8e8'),
    (3, 0.5, 4, 0.6, 'IFBH Limited (6603.HK)', '#00f5d4'),
]
for x, y, w, h, text, color in boxes:
    rect = mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1", facecolor=color, edgecolor='#999', linewidth=1.2)
    ax.add_patch(rect)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center', fontsize=9, fontweight='bold' if 'IFBH' in text else 'normal')
# Arrows
ax.annotate('', xy=(5, 3.65), xytext=(5, 3.8), arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))
ax.text(5.1, 3.55, '持股100%', fontsize=7, color='#666')
ax.annotate('', xy=(3.5, 2.15), xytext=(4.5, 2.85), arrowprops=dict(arrowstyle='->', color='#666', lw=1.5))
ax.text(4.9, 2.5, '控股\n65.51%', fontsize=7, color='#666')
ax.annotate('', xy=(2.5, 2.15), xytext=(2.5, 2.8), arrowprops=dict(arrowstyle='->', color='#999', lw=1.2))
ax.annotate('', xy=(7.5, 2.15), xytext=(7.5, 2.8), arrowprops=dict(arrowstyle='->', color='#999', lw=1.2))
ax.set_title('IFBH 股权结构简图', fontsize=13, fontweight='bold', pad=8)
plt.tight_layout(); plt.savefig('report_charts/chart_ownership.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 4: 毛利率与费用率变化 (放于2.2营收结构后) =====
fig, ax = plt.subplots(figsize=(7, 4.2))
years_24_25 = ['2024', '2025']
gm = [36.7, 32.9]
mkt_ratio = [4.7, 7.4]
x = np.arange(len(years_24_25)); w = 0.3
b1 = ax.bar(x-w/2, gm, w, color='#00f5d4', alpha=0.8, label='毛利率(%)')
ax_t = ax.twinx()
b2 = ax_t.bar(x+w/2, mkt_ratio, w, color='#ef233c', alpha=0.6, label='营销费用率(%)')
for i, v in enumerate(gm): ax.text(i-w/2, v+0.5, f'{v}%', ha='center', fontsize=9, fontweight='bold')
for i, v in enumerate(mkt_ratio): ax_t.text(i+w/2, v+0.3, f'{v}%', ha='center', fontsize=9, fontweight='bold')
ax.set_xticks(x); ax.set_xticklabels(years_24_25, fontsize=11)
ax.set_ylabel('毛利率 (%)', fontsize=10, color='#00a88a')
ax_t.set_ylabel('营销费用率 (%)', fontsize=10, color='#ef233c')
ax.set_title('IFBH 毛利率 vs 营销费用率 (2024-2025)', fontsize=13, fontweight='bold', pad=10)
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax_t.get_legend_handles_labels()
ax.legend(lines1+lines2, labels1+labels2, fontsize=9, loc='upper right')
ax.spines['top'].set_visible(False); ax_t.spines['top'].set_visible(False)
ax.grid(axis='y', alpha=0.1)
plt.tight_layout(); plt.savefig('report_charts/chart_margin.png', dpi=200, bbox_inches='tight'); plt.close()

# ===== Chart 5: 营收结构饼图 (放于2.2) =====
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.8))
# 产品结构
products = ['椰子水 (if)', '电解质水 (Innococo)', '其他']
prod_vals = [94.5, 3.3, 2.2]
colors_p = ['#00f5d4', '#fee440', '#ccc']
ax1.pie(prod_vals, labels=products, autopct='%1.1f%%', colors=colors_p, startangle=90,
        textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
ax1.set_title('按产品 (2025)', fontsize=11, fontweight='bold')
# 区域结构
regions = ['中国内地', '其他地区']
reg_vals = [90.4, 9.6]
colors_r = ['#ff6b6b', '#ccc']
ax2.pie(reg_vals, labels=regions, autopct='%1.1f%%', colors=colors_r, startangle=90,
        textprops={'fontsize': 9}, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
ax2.set_title('按区域 (2025)', fontsize=11, fontweight='bold')
fig.suptitle('IFBH 收入结构分布', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout(); plt.savefig('report_charts/chart_revenue_struct.png', dpi=200, bbox_inches='tight'); plt.close()

print('5 charts generated in report_charts/')
