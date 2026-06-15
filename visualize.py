import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ================================
# 0. 한글 폰트 설정
# ================================
sns.set(style='whitegrid')
plt.rcParams['font.sans-serif'] = ['AppleGothic', 'Malgun Gothic', 'NanumGothic', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# ================================
# 전처리 데이터 로드
# ================================
PROCESSED_DIR = 'processed'
if not os.path.exists(f'{PROCESSED_DIR}/산업데이터.pkl'):
    raise FileNotFoundError(
        "'processed' 폴더에 전처리 데이터가 없습니다.\n"
        "먼저 preprocess.py를 실행하세요:\n"
        "  python preprocess.py"
    )

산업데이터 = pd.read_pickle(f'{PROCESSED_DIR}/산업데이터.pkl')
직무데이터 = pd.read_pickle(f'{PROCESSED_DIR}/직무데이터.pkl')
통합데이터 = pd.read_pickle(f'{PROCESSED_DIR}/통합데이터.pkl')

print("[데이터 로드 완료]")
print(f"  - 산업데이터: {산업데이터.shape[0]:,}행 × {산업데이터.shape[1]}열")
print(f"  - 직무데이터: {직무데이터.shape[0]:,}행 × {직무데이터.shape[1]}열")
print(f"  - 통합데이터: {통합데이터.shape[0]:,}행 × {통합데이터.shape[1]}열")

# ================================
# 시각화 출력 폴더 생성
# ================================
os.makedirs('plots', exist_ok=True)
print("\n[시각화 시작] 'plots' 폴더에 고해상도 PNG로 저장합니다...\n")

# ================================
# 12-1 산업별 평균 대체율 상위 10개
# ================================
if {'산업명', '산업인력대체율'}.issubset(산업데이터.columns):
    산업대체율 = (
        산업데이터.groupby('산업명')['산업인력대체율']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    plt.figure(figsize=(10, 6))
    ax = sns.barplot(
        x=산업대체율.values,
        y=산업대체율.index,
        palette='crest_r',
        hue=산업대체율.index,
        legend=False
    )
    sns.despine(left=True, bottom=True)

    for p in ax.patches:
        width = p.get_width()
        if width > 0:
            ax.text(
                width + 0.3,
                p.get_y() + p.get_height() / 2,
                f"{width:.1f}%",
                ha="left", va="center",
                fontsize=10, fontweight='bold', color='#2c3e50'
            )

    plt.xlabel('평균 인력 대체율 (%)', fontsize=11, fontweight='bold', labelpad=10)
    plt.ylabel('산업군', fontsize=11, fontweight='bold', labelpad=10)
    plt.title('산업별 평균 AI 대체율 상위 10개', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('plots/01_industry_avg_replacement.png', dpi=300)
    plt.show()

# ================================
# 12-2 평균 대체율 및 순인력변화율 추이
# ================================
if {'날짜', '산업인력대체율', '순인력변화율'}.issubset(산업데이터.columns):
    시계열 = (
        산업데이터.sort_values('날짜')
        .groupby('날짜')[['산업인력대체율', '순인력변화율']]
        .mean()
    )

    plt.figure(figsize=(12, 6))
    plt.plot(시계열.index, 시계열['산업인력대체율'], label='대체율 (%)', color='#e74c3c', linewidth=2.5, marker='o', markersize=5)
    plt.plot(시계열.index, 시계열['순인력변화율'], label='순일자리 변화율 (%)', color='#3498db', linewidth=2.5, marker='s', markersize=5)
    plt.axhline(0, color='#7f8c8d', linewidth=1.2, linestyle='--')
    plt.fill_between(시계열.index, 시계열['산업인력대체율'], alpha=0.08, color='#e74c3c')
    plt.fill_between(시계열.index, 시계열['순인력변화율'], alpha=0.08, color='#3498db')
    plt.xlabel('연도 및 분기', fontsize=11, fontweight='bold', labelpad=10)
    plt.ylabel('비율 (%)', fontsize=11, fontweight='bold', labelpad=10)
    plt.title('전 세계 평균 AI 대체율 및 순일자리변화율 추이 (2020–2026)', fontsize=14, fontweight='bold', pad=15)
    plt.legend(frameon=True, facecolor='white', edgecolor='none', fontsize=10)
    sns.despine()
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('plots/02_global_trend_over_time.png', dpi=300)
    plt.show()

# ================================
# 12-3 산업 수준 상관 히트맵
# ================================
상관열 = [열 for 열 in [
    '산업자동화위험점수', '산업인력대체율',
    '순인력변화율', '1인당GDP(달러)', '재교육프로그램수', 'AI도입지수'
] if 열 in 산업데이터.columns]

if len(상관열) >= 2:
    상관행렬 = 산업데이터[상관열].corr()
    mask = np.triu(np.ones_like(상관행렬, dtype=bool))

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        상관행렬, mask=mask, annot=True, fmt='.2f',
        cmap='coolwarm', vmin=-1, vmax=1, center=0,
        square=True, linewidths=0.8, linecolor='white',
        cbar_kws={"shrink": .8}
    )
    plt.title('산업 수준 주요 변수 상관관계 (상관계수)', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig('plots/03_industry_correlation.png', dpi=300)
    plt.show()

# ================================
# 12-5 자동화 위험등급별 연봉 변화 (그룹화 분포)
# ================================
if {'자동화위험등급', '연봉변화율(%)'}.issubset(직무데이터.columns):
    직무위험도순서 = ['Low', 'Medium', 'High']
    plt.figure(figsize=(9, 6))
    sns.boxplot(
        data=직무데이터,
        x='자동화위험등급', y='연봉변화율(%)',
        order=직무위험도순서,
        palette='Pastel1', width=0.4,
        hue='자동화위험등급', legend=False
    )
    plt.xlabel('자동화 위험 카테고리', fontsize=11, fontweight='bold', labelpad=10)
    plt.ylabel('연봉 변화율 (%)', fontsize=11, fontweight='bold', labelpad=10)
    plt.title('자동화 위험 등급별 연봉 변화율 분포', fontsize=14, fontweight='bold', pad=15)
    sns.despine()
    plt.grid(True, axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('plots/05_salary_change_by_risk_category.png', dpi=300)
    plt.show()

# ================================
# 12-7 국가 × 산업별 평균 대체율 히트맵
# ================================
if {'국가명', '산업명', '산업인력대체율'}.issubset(산업데이터.columns):
    상위국가 = (
        산업데이터.groupby('국가명')['산업인력대체율']
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .index
    )
    # 국가별 산업별 평균 대체율 계산
    국가산업평균 = (
        산업데이터[산업데이터['국가명'].isin(상위국가)]
        .groupby(['국가명', '산업명'])['산업인력대체율']
        .mean()
        .unstack('산업명')
    )
    # 전체(글로벌) 산업별 평균 대체율 계산
    전체산업평균 = 산업데이터.groupby('산업명')['산업인력대체율'].mean()
    # 글로벌 평균 대비 각 국가의 상대적 편차 계산 (가짜 데이터의 편차 소멸 보완)
    히트맵피벗 = 국가산업평균.sub(전체산업평균, axis='columns')

    plt.figure(figsize=(12, 8))
    sns.heatmap(
        히트맵피벗, cmap='RdBu_r', center=0,
        linewidths=0.8, linecolor='white',
        annot=True, fmt='.2f',
        annot_kws={"size": 10, "weight": "bold"},
        cbar_kws={'label': '평균 대체율 편차 (%p)'}
    )
    plt.title('국가 × 산업별 평균 AI 대체율 편차 (글로벌 평균 대비, 상위 10개 국가)', fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('산업군', fontsize=11, fontweight='bold', labelpad=10)
    plt.ylabel('국가명', fontsize=11, fontweight='bold', labelpad=10)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig('plots/07_country_industry_heatmap.png', dpi=300)
    plt.show()

print("\n[시각화 완료] 모든 시각화 결과가 'plots' 폴더에 고해상도 PNG로 저장되었습니다!")
