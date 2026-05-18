"""
EPTA Services - Visualization Scripts
Shepherd University Transit Data Analysis
----------------------------------------------
Requirements: pandas, matplotlib, numpy
Install: pip install pandas matplotlib numpy

Each function reads from the CSV files in the same directory
and saves a PNG. Call main() to generate all charts at once.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

# ── Shared style ─────────────────────────────────────────────────────────────
BLUE    = '#3266ad'
TEAL    = '#1D9E75'
CORAL   = '#D85A30'
AMBER   = '#BA7517'
GRAY    = '#888780'
LIGHT   = '#3266ad44'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.dpi': 150,
})

DATA_DIR = os.path.dirname(os.path.abspath(__file__))


# ── 1. Annual ridership history ───────────────────────────────────────────────
def chart_annual_ridership():
    df = pd.read_csv(os.path.join(DATA_DIR, '01_annual_ridership_enrollment.csv'))
    df_plot = df[df['anomaly_flag'] == 0].copy()

    fig, ax = plt.subplots(figsize=(12, 5))
    colors = [BLUE if fy == 'FY25-26' else '#3266ad88' for fy in df_plot['fiscal_year']]
    bars = ax.bar(df_plot['fiscal_year'], df_plot['annual_riders'], color=colors, width=0.7)

    # Highlight FY25-26
    ax.bar(df_plot[df_plot['fiscal_year'] == 'FY25-26']['fiscal_year'],
           df_plot[df_plot['fiscal_year'] == 'FY25-26']['annual_riders'],
           color=BLUE, width=0.7, label='FY25-26 (partial)')

    ax.set_title('EPTA Annual Ridership — Shepherd University', pad=12)
    ax.set_ylabel('Annual riders')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.set_xticks(range(len(df_plot))); ax.set_xticklabels(df_plot["fiscal_year"], rotation=45, ha='right')
    ax.annotate('FY12-13 excluded\n(anomaly: 82,006)',
                xy=(0.01, 0.97), xycoords='axes fraction',
                fontsize=9, color=GRAY, va='top')
    ax.annotate('* partial year', xy=(0.99, 0.97), xycoords='axes fraction',
                fontsize=9, color=GRAY, va='top', ha='right')

    # Value labels on bars
    for bar in bars:
        h = bar.get_height()
        if h > 0:
            ax.text(bar.get_x() + bar.get_width()/2, h + 200,
                    f'{int(h):,}', ha='center', va='bottom', fontsize=8, color='#444')

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_01_annual_ridership.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 2. Enrollment vs. ridership dual-axis ────────────────────────────────────
def chart_enrollment_vs_ridership():
    df = pd.read_csv(os.path.join(DATA_DIR, '01_annual_ridership_enrollment.csv'))
    df = df[df['anomaly_flag'] == 0].copy()

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()

    x = np.arange(len(df))
    ax1.bar(x, df['fall_enrollment'], color=BLUE + '44', width=0.6, label='Fall enrollment')
    ax1.set_ylabel('Fall enrollment (headcount)', color=BLUE)
    ax1.tick_params(axis='y', labelcolor=BLUE)
    ax1.set_ylim(2000, 5200)

    ax2.plot(x, df['annual_riders'], color=CORAL, linewidth=2.5,
             marker='o', markersize=5, label='Annual riders', linestyle='--')
    ax2.set_ylabel('Annual riders', color=CORAL)
    ax2.tick_params(axis='y', labelcolor=CORAL)
    ax2.set_ylim(10000, 42000)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v/1000)}k'))

    ax1.set_xticks(x)
    ax1.set_xticklabels(df['fiscal_year'], rotation=45, ha='right')
    ax1.set_title('Enrollment vs. EPTA Ridership — Shepherd University', pad=12)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right', fontsize=9)

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_02_enrollment_vs_ridership.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 3. Riders per 100 students ───────────────────────────────────────────────
def chart_riders_per_100():
    df = pd.read_csv(os.path.join(DATA_DIR, '01_annual_ridership_enrollment.csv'))
    df = df[df['anomaly_flag'] == 0].copy()

    fig, ax = plt.subplots(figsize=(12, 4))
    colors = [BLUE if fy == 'FY25-26' else BLUE + '99' for fy in df['fiscal_year']]
    ax.bar(df['fiscal_year'], df['riders_per_100_students'], color=colors, width=0.7)

    ax.set_title('EPTA Riders per 100 Enrolled Students', pad=12)
    ax.set_ylabel('Riders per 100 students')
    ax.set_xticklabels(df['fiscal_year'], rotation=45, ha='right')

    for i, (fy, val) in enumerate(zip(df['fiscal_year'], df['riders_per_100_students'])):
        ax.text(i, val + 0.1, f'{val:.1f}', ha='center', va='bottom', fontsize=8, color='#444')

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_03_riders_per_100.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 4. Monthly ridership FY24-25 stacked bar ─────────────────────────────────
def chart_monthly_fy2425():
    df = pd.read_csv(os.path.join(DATA_DIR, '02_monthly_ridership_fy2425.csv'))

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    w = 0.6
    ax.bar(x, df['rf1_am'],  width=w, label='Ram Force One AM', color=BLUE)
    ax.bar(x, df['express'], width=w, bottom=df['rf1_am'], label='Ram Express', color=TEAL)
    ax.bar(x, df['rf1_pm'],  width=w, bottom=df['rf1_am']+df['express'], label='Ram Force One PM', color=CORAL)

    ax.set_xticks(x)
    ax.set_xticklabels(df['month'], rotation=30, ha='right')
    ax.set_title('Monthly Ridership by Route — FY2024-25', pad=12)
    ax.set_ylabel('Riders')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
    ax.legend(fontsize=9)

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_04_monthly_fy2425.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 5. FY25-26 monthly comparison ────────────────────────────────────────────
def chart_monthly_fy2526_comparison():
    df = pd.read_csv(os.path.join(DATA_DIR, '03_monthly_ridership_fy2526.csv'))
    df = df[df['month'] != 'May-26'].copy()  # exclude partial May

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df))
    w = 0.35
    ax.bar(x - w/2, df['total'], width=w, label='FY25-26', color=BLUE)
    ax.bar(x + w/2, df['prior_year_total'], width=w, label='FY24-25', color=BLUE + '55')

    ax.set_xticks(x)
    ax.set_xticklabels(df['month'], rotation=30, ha='right')
    ax.set_title('Monthly Ridership — FY25-26 vs. FY24-25', pad=12)
    ax.set_ylabel('Riders')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
    ax.legend(fontsize=9)

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_05_monthly_fy2526_comparison.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 6. YoY % change FY25-26 ──────────────────────────────────────────────────
def chart_yoy_change():
    df = pd.read_csv(os.path.join(DATA_DIR, '03_monthly_ridership_fy2526.csv'))
    df = df[df['month'] != 'May-26'].copy()

    fig, ax = plt.subplots(figsize=(10, 4))
    colors = [TEAL if v >= 0 else CORAL for v in df['yoy_pct_change']]
    ax.bar(df['month'], df['yoy_pct_change'], color=colors, width=0.6)
    ax.axhline(0, color='#aaa', linewidth=0.8)
    ax.set_title('Year-over-Year Ridership Change — FY25-26 vs. FY24-25', pad=12)
    ax.set_ylabel('% change')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.set_xticklabels(df['month'], rotation=30, ha='right')

    for i, (m, v) in enumerate(zip(df['month'], df['yoy_pct_change'])):
        ax.text(i, v + 0.5 if v >= 0 else v - 1.5,
                f'+{v:.0f}%' if v >= 0 else f'{v:.0f}%',
                ha='center', va='bottom', fontsize=9, color='#444')

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_06_yoy_change.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 7. Survey: ride frequency ─────────────────────────────────────────────────
def chart_survey_frequency():
    df = pd.read_csv(os.path.join(DATA_DIR, '04_survey_frequency_results.csv'))
    q2 = df[df['question'] == 'Q2 Ride frequency'].copy()

    fig, ax = plt.subplots(figsize=(9, 4))
    colors = [BLUE, BLUE, BLUE, TEAL, TEAL, GRAY]
    ax.barh(q2['response'][::-1], q2['count'][::-1], color=colors[::-1], height=0.6)
    ax.set_title('How often do you ride the EPTA buses? (n=445)', pad=12)
    ax.set_xlabel('Number of students')

    for i, (v, c) in enumerate(zip(q2['count'][::-1], q2['pct'][::-1])):
        ax.text(v + 1, i, f'{v} ({c:.1f}%)', va='center', fontsize=9)

    ax.set_xlim(0, 230)
    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_07_survey_frequency.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 8. Survey: reasons for riding ────────────────────────────────────────────
def chart_survey_reasons():
    df = pd.read_csv(os.path.join(DATA_DIR, '04_survey_frequency_results.csv'))
    q3 = df[df['question'] == 'Q3 Reasons for riding'].sort_values('count').copy()

    fig, ax = plt.subplots(figsize=(9, 5))
    bar_colors = [CORAL if r in ['Injury','Accessibility','Personal safety'] else BLUE
                  for r in q3['response']]
    ax.barh(q3['response'], q3['respondent_pct'], color=bar_colors, height=0.6)
    ax.set_title('Why do students ride? (% of 360 riders, multi-select)', pad=12)
    ax.set_xlabel('% of riders selecting this reason')
    ax.set_xlim(0, 110)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))

    for i, (v, c) in enumerate(zip(q3['respondent_pct'], q3['count'])):
        ax.text(v + 1, i, f'{v:.0f}%  (n={c})', va='center', fontsize=9)

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_08_survey_reasons.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 9. Survey: importance & time slots ───────────────────────────────────────
def chart_survey_importance():
    df = pd.read_csv(os.path.join(DATA_DIR, '04_survey_frequency_results.csv'))

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    q6 = df[df['question'] == 'Q6 Importance'].copy()
    colors6 = [BLUE, BLUE, AMBER, CORAL]
    axes[0].barh(q6['response'][::-1], q6['pct'][::-1], color=colors6[::-1], height=0.6)
    axes[0].set_title('How important is campus bus service?\n(n=420)', pad=8)
    axes[0].set_xlabel('% of respondents')
    axes[0].xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    for i, (v, p) in enumerate(zip(q6['count'][::-1], q6['pct'][::-1])):
        axes[0].text(p + 0.5, i, f'{p:.1f}%', va='center', fontsize=9)

    q7 = df[df['question'] == 'Q7 Critical time slots'].copy()
    colors7 = [BLUE, BLUE, TEAL, TEAL, GRAY]
    axes[1].bar(q7['response'], q7['respondent_pct'], color=colors7, width=0.6)
    axes[1].set_title('When is service most critical?\n(n=420, multi-select)', pad=8)
    axes[1].set_ylabel('% of respondents')
    axes[1].set_xticklabels(q7['response'], rotation=20, ha='right')
    axes[1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    for i, v in enumerate(q7['respondent_pct']):
        axes[1].text(i, v + 0.5, f'{v:.0f}%', ha='center', fontsize=9)

    plt.suptitle('EPTA Service Importance — Student Survey 2025', y=1.02, fontsize=13)
    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_09_survey_importance.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 10. Survey: Likert agreement ─────────────────────────────────────────────
def chart_survey_likert():
    df = pd.read_csv(os.path.join(DATA_DIR, '05_survey_likert_results.csv'))

    labels = [q.replace('Q9 ','').replace('Q10 ','').replace('Q11 ','').replace('Q12 ','')
              for q in df['question']]
    sa  = df['strongly_agree_pct'].values
    a   = df['agree_pct'].values
    d   = df['disagree_pct'].values
    sd  = df['strongly_disagree_pct'].values

    fig, ax = plt.subplots(figsize=(10, 4))
    y = np.arange(len(df))
    ax.barh(y, sa,  height=0.5, color='#185FA5', label='Strongly agree')
    ax.barh(y, a,   height=0.5, left=sa, color='#85B7EB', label='Agree')
    ax.barh(y, d,   height=0.5, left=sa+a, color='#F0997B', label='Disagree')
    ax.barh(y, sd,  height=0.5, left=sa+a+d, color='#D85A30', label='Strongly disagree')

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel('% of respondents')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:.0f}%'))
    ax.set_title('Student Agreement — Service Quality Statements (n≈413)', pad=12)
    ax.legend(loc='lower right', fontsize=9, ncol=2)

    for i, row in df.iterrows():
        total_pos = row['strongly_agree_pct'] + row['agree_pct']
        ax.text(101, i, f'{total_pos:.0f}% agree', va='center', fontsize=9, color='#444')

    ax.set_xlim(0, 115)
    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_10_survey_likert.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 11. Hourly ridership pattern FY24-25 ─────────────────────────────────────
def chart_hourly():
    df = pd.read_csv(os.path.join(DATA_DIR, '06_hourly_ridership_fy2425.csv'))

    hour_order = ['7-8','8-9','9-10','10-11','11-12','12-1','1-2','2-3',
                  '3-4','4-5','5-6','6-7','7-8p','8-9p','9-10p']
    route_colors = {'RF1_AM': BLUE, 'Express': TEAL, 'RF1_PM': CORAL}
    route_labels = {'RF1_AM': 'Ram Force One AM', 'Express': 'Ram Express', 'RF1_PM': 'Ram Force One PM'}

    fig, ax = plt.subplots(figsize=(13, 5))
    x_positions = {}
    offset = {'RF1_AM': -0.25, 'Express': 0, 'RF1_PM': 0.25}
    w = 0.22

    all_hours = df['hour_slot'].unique()
    x_map = {h: i for i, h in enumerate(hour_order) if h in all_hours}

    for route in ['RF1_AM', 'Express', 'RF1_PM']:
        sub = df[df['route'] == route]
        xs = [x_map.get(h, None) for h in sub['hour_slot']]
        xs = [x + offset[route] for x in xs if x is not None]
        ys = sub['total_riders'].values
        ax.bar(xs, ys, width=w, color=route_colors[route], label=route_labels[route], alpha=0.9)

    ax.set_xticks(range(len(all_hours)))
    ax.set_xticklabels([h for h in hour_order if h in all_hours], rotation=30, ha='right')
    ax.set_title('Ridership by Hour of Day — FY2024-25 (all months combined)', pad=12)
    ax.set_ylabel('Total riders (all months)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{int(v):,}'))
    ax.legend(fontsize=9)

    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_11_hourly_ridership.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── 12. Fee support and survey composition ────────────────────────────────────
def chart_survey_summary():
    df = pd.read_csv(os.path.join(DATA_DIR, '04_survey_frequency_results.csv'))

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    q1 = df[df['question'] == 'Q1 Student type']
    axes[0].pie(q1['count'], labels=q1['response'],
                colors=[BLUE, TEAL, GRAY],
                autopct='%1.0f%%', startangle=90,
                textprops={'fontsize': 10})
    axes[0].set_title('Survey respondents by student type\n(n=445)', pad=8)

    q8 = df[df['question'] == 'Q8 Fee support']
    axes[1].pie(q8['count'], labels=q8['response'],
                colors=[TEAL, CORAL],
                autopct='%1.1f%%', startangle=90,
                textprops={'fontsize': 10})
    axes[1].set_title('Would support a small fee to\nmaintain service? (n=420)', pad=8)

    plt.suptitle('EPTA Student Survey 2025 — Key Breakdowns', y=1.02, fontsize=13)
    plt.tight_layout()
    path = os.path.join(DATA_DIR, 'chart_12_survey_summary.png')
    plt.savefig(path, bbox_inches='tight')
    plt.close()
    print(f'Saved: {path}')


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("Generating all EPTA charts...\n")
    chart_annual_ridership()
    chart_enrollment_vs_ridership()
    chart_riders_per_100()
    chart_monthly_fy2425()
    chart_monthly_fy2526_comparison()
    chart_yoy_change()
    chart_survey_frequency()
    chart_survey_reasons()
    chart_survey_importance()
    chart_survey_likert()
    chart_hourly()
    chart_survey_summary()
    print("\nDone. 12 charts saved.")


if __name__ == '__main__':
    main()
