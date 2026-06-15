import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ================================
# 0. 한글 폰트 설정
# ================================
sns.set(style='whitegrid')
plt.rcParams['font.sans-serif'] = ['AppleGothic', 'Malgun Gothic', 'NanumGothic', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# ================================
# 1. 데이터 로드
# ================================
산업데이터 = pd.read_csv('ai_workforce_displacement_global_2020_2026.csv')
직무데이터 = pd.read_csv('ai_job_replacement_2020_2026_v2.csv')

# ================================
# 2. 원본 컬럼 → 한국어 컬럼명 매핑
# ================================
산업_컬럼명 = {
    'record_id': '레코드ID',
    'country': '국가',
    'iso3_code': 'ISO3코드',
    'region': '지역',
    'income_group': '소득그룹',
    'year': '연도',
    'quarter': '분기',
    'quarter_label': '분기라벨',
    'industry_sector': '산업부문',
    'sector_automation_risk_score': '산업자동화위험점수',
    'gdp_per_capita_usd': '1인당GDP(달러)',
    'ai_adoption_index': 'AI도입지수',
    'pct_sector_workforce_displaced': '산업인력대체율',
    'pct_sector_workforce_new_roles_created': '산업신규직무생성율',
    'net_workforce_change_pct': '순인력변화율',
    'ai_cited_layoff_announcements': 'AI언급해고건수',
    'ai_skill_wage_premium_pct': 'AI기술임금프리미엄',
    'pct_workforce_female': '여성근로자비율',
    'pct_displaced_roles_female': '대체직무여성비율',
    'reskilling_programs_count': '재교육프로그램수',
    'govt_ai_policy_score_1_to_10': '정부AI정책점수',
    'ai_tool_adoption_pct': 'AI도구도입비율',
    'data_source_notes': '데이터출처메모'
}

직무_컬럼명 = {
    'job_id': '직무ID',
    'job_role': '직무명',
    'industry': '산업',
    'country': '국가',
    'year': '연도',
    'automation_risk_percent': '자동화위험도(%)',
    'ai_replacement_score': 'AI대체점수',
    'skill_gap_index': '스킬격차지수',
    'salary_before_usd': '연봉_이전(달러)',
    'salary_after_usd': '연봉_이후(달러)',
    'salary_change_percent': '연봉변화율(%)',
    'skill_demand_growth_percent': '스킬수요성장률(%)',
    'remote_feasibility_score': '원격근무가능성점수',
    'ai_adoption_level': 'AI도입수준',
    'education_requirement_level': '학력요구수준',
    'automation_risk_category': '자동화위험등급',
    'skill_transition_pressure': '스킬전환압박',
    'wage_volatility_index': '임금변동성지수',
    'reskilling_urgency_score': '재교육긴급도점수',
    'ai_disruption_intensity': 'AI교란강도'
}

산업데이터 = 산업데이터.rename(columns=산업_컬럼명)
직무데이터 = 직무데이터.rename(columns=직무_컬럼명)

# 비율 데이터(0.0~1.0)를 백분율(%) 단위로 변환
비율컬럼들 = ['산업인력대체율', '산업신규직무생성율', '순인력변화율', 'AI도구도입비율', '여성근로자비율', '대체직무여성비율', 'AI기술임금프리미엄']
for col in 비율컬럼들:
    if col in 산업데이터.columns:
        if 산업데이터[col].max() <= 1.0:
            산업데이터[col] = 산업데이터[col] * 100

# ================================
# 3. 한글 라벨 매핑
# ================================
산업지도 = {
    'Technology & Software': 'IT/소프트웨어',
    'Finance & Banking': '금융/은행',
    'Healthcare & Life Sciences': '의료/생명과학',
    'Manufacturing & Industry': '제조/산업',
    'Retail & E-Commerce': '소매/전자상거래',
    'Transportation & Logistics': '운송/물류',
    'Energy & Utilities': '에너지/유틸리티',
    'Administrative & Clerical': '행정/사무',
    'Media & Communications': '미디어/통신',
    'Education & Research': '교육/연구'
}

지역지도 = {
    'North America': '북미',
    'Europe': '유럽',
    'Asia-Pacific': '아시아-태평양',
    'Latin America': '남미',
    'Middle East & Africa': '중동/아프리카',
    'Africa': '아프리카',
    'South Asia': '남아시아',
    'Oceania': '오세아니아',
    'East Asia': '동아시아',
    'Europe/Asia': '유럽/아시아',
    'Southeast Asia': '동남아시아',
    'Middle East': '중동',
    'Central Asia': '중앙아시아',
    'Middle East/Africa': '중동/아프리카'
}

소득지도 = {
    'High Income': '고소득',
    'Upper Middle Income': '중상위소득',
    'Lower Middle Income': '중하위소득',
    'Low Income': '저소득'
}

직무지도 = {
    'Data Analyst': '데이터 분석가',
    'Accountant': '회계사',
    'Teacher': '교사',
    'Customer Support Rep': '고객지원',
    'Software Engineer': '소프트웨어 엔지니어',
    'Marketing Specialist': '마케팅 전문가',
    'Financial Analyst': '재무 분석가',
    'HR Manager': '인사 관리자',
    'Mechanical Engineer': '기계 엔지니어',
    'Truck Driver': '트럭 운전사'
}

국가지도 = {
    'United States': '미국',
    'USA': '미국',
    'Canada': '캐나다',
    'Germany': '독일',
    'Japan': '일본',
    'UK': '영국',
    'United Kingdom': '영국',
    'Australia': '호주',
    'Singapore': '싱가포르',
    'India': '인도',
    'Brazil': '브라질',
    'China': '중국',
    'France': '프랑스',
    'South Korea': '한국',
    'Italy': '이탈리아',
    'Spain': '스페인',
    'Mexico': '멕시코',
    'Indonesia': '인도네시아',
    'Netherlands': '네덜란드',
    'Saudi Arabia': '사우디아라비아',
    'Turkey': '튀르키예',
    'Switzerland': '스위스',
    'Sweden': '스웨덴',
    'Norway': '노르웨이',
    'Denmark': '덴마크',
    'Finland': '핀란드',
    'Belgium': '벨기에',
    'Austria': '오스트리아',
    'Poland': '폴란드',
    'Argentina': '아르헨티나',
    'Colombia': '콜롬비아',
    'Chile': '칠레',
    'Peru': '페루',
    'South Africa': '남아공',
    'Nigeria': '나이지리아',
    'Egypt': '이집트',
    'Kenya': '케냐',
    'Ethiopia': '에티오피아',
    'Ghana': '가나',
    'Morocco': '모로코',
    'Tanzania': '탄자니아',
    'Pakistan': '파키스탄',
    'Bangladesh': '방글라데시',
    'Vietnam': '베트남',
    'Thailand': '태국',
    'Malaysia': '말레이시아',
    'Philippines': '필리핀',
    'New Zealand': '뉴질랜드',
    'Portugal': '포르투갈',
    'Czech Republic': '체코',
    'Romania': '루마니아',
    'Hungary': '헝가리',
    'Greece': '그리스',
    'Ukraine': '우크라이나',
    'Israel': '이스라엘',
    'UAE': '아랍에미리트',
    'Qatar': '카타르',
    'Kuwait': '쿠웨이트',
    'Iran': '이란',
    'Iraq': '이라크',
    'Kazakhstan': '카자흐스탄',
    'Uzbekistan': '우즈베키스탄',
    'Russia': '러시아',
    'Taiwan': '대만',
    'Hong Kong': '홍콩',
    'Sri Lanka': '스리랑카',
    'Nepal': '네팔',
    'Myanmar': '미얀마',
    'Cambodia': '캄보디아',
    'Ecuador': '에콰도르',
    'Bolivia': '볼리비아',
    'Paraguay': '파라과이',
    'Uruguay': '우루과이',
    'Costa Rica': '코스타리카',
    'Panama': '파나마',
    'Guatemala': '과테말라',
    'Algeria': '알제리',
    'Tunisia': '튀니지',
    'Cameroon': '카메룬',
    'Ivory Coast': '코트디부아르',
    'Senegal': '세네갈',
    'Zambia': '잠비아'
}

# ================================
# 4. 기본 정리 함수
# ================================
def 문자열정리(x):
    if pd.isna(x):
        return x
    return str(x).strip()

def 이상치클리핑(시리즈, 배수=1.5):
    사분위1 = 시리즈.quantile(0.25)
    사분위3 = 시리즈.quantile(0.75)
    사분위범위 = 사분위3 - 사분위1
    하한 = 사분위1 - 배수 * 사분위범위
    상한 = 사분위3 + 배수 * 사분위범위
    return 시리즈.clip(하한, 상한)

# ================================
# 5. 결측치 처리
# ================================
산업결측비율 = 산업데이터.isna().mean()
직무결측비율 = 직무데이터.isna().mean()

산업삭제컬럼 = 산업결측비율[산업결측비율 >= 0.3].index.tolist()
직무삭제컬럼 = 직무결측비율[직무결측비율 >= 0.3].index.tolist()

산업데이터 = 산업데이터.drop(columns=산업삭제컬럼)
직무데이터 = 직무데이터.drop(columns=직무삭제컬럼)

산업숫자컬럼 = 산업데이터.select_dtypes(include=[np.number]).columns.tolist()
직무숫자컬럼 = 직무데이터.select_dtypes(include=[np.number]).columns.tolist()

if {'국가', '산업부문'}.issubset(산업데이터.columns):
    산업그룹 = 산업데이터.groupby(['국가', '산업부문'])
    for 열 in 산업숫자컬럼:
        if 산업데이터[열].isna().any():
            산업데이터[열] = 산업그룹[열].transform(lambda x: x.fillna(x.median()))
산업데이터[산업숫자컬럼] = 산업데이터[산업숫자컬럼].fillna(산업데이터[산업숫자컬럼].median())

if {'국가', '직무명'}.issubset(직무데이터.columns):
    직무그룹 = 직무데이터.groupby(['국가', '직무명'])
    for 열 in 직무숫자컬럼:
        if 직무데이터[열].isna().any():
            직무데이터[열] = 직무그룹[열].transform(lambda x: x.fillna(x.median()))
직무데이터[직무숫자컬럼] = 직무데이터[직무숫자컬럼].fillna(직무데이터[직무숫자컬럼].median())

# ================================
# 6. 중복 제거
# ================================
if '레코드ID' in 산업데이터.columns:
    산업데이터 = 산업데이터.drop_duplicates(subset=['레코드ID'])

if '직무ID' in 직무데이터.columns:
    직무데이터 = 직무데이터.drop_duplicates(subset=['직무ID'])

# ================================
# 7. 문자열 정리 및 한글 라벨 컬럼 생성
# ================================
for 열 in ['산업부문', '국가', '지역', '소득그룹']:
    if 열 in 산업데이터.columns:
        산업데이터[열] = 산업데이터[열].apply(문자열정리)

for 열 in ['산업', '국가', '직무명', '자동화위험등급']:
    if 열 in 직무데이터.columns:
        직무데이터[열] = 직무데이터[열].apply(문자열정리)

if '산업부문' in 산업데이터.columns:
    산업데이터['산업명'] = 산업데이터['산업부문'].map(산업지도).fillna(산업데이터['산업부문'])

if '지역' in 산업데이터.columns:
    산업데이터['지역명'] = 산업데이터['지역'].map(지역지도).fillna(산업데이터['지역'])

if '소득그룹' in 산업데이터.columns:
    산업데이터['소득그룹명'] = 산업데이터['소득그룹'].map(소득지도).fillna(산업데이터['소득그룹'])

if '국가' in 산업데이터.columns:
    산업데이터['국가명'] = 산업데이터['국가'].map(국가지도).fillna(산업데이터['국가'])

if '국가' in 직무데이터.columns:
    직무데이터['국가명'] = 직무데이터['국가'].map(국가지도).fillna(직무데이터['국가'])

if '직무명' in 직무데이터.columns:
    직무데이터['직무명_한글'] = 직무데이터['직무명'].map(직무지도).fillna(직무데이터['직무명'])

# ================================
# 8. 날짜 컬럼 생성
# ================================
if {'연도', '분기'}.issubset(산업데이터.columns):
    산업데이터['연도'] = 산업데이터['연도'].astype(int)
    산업데이터['분기'] = 산업데이터['분기'].astype(int)
    분기월 = {1: 1, 2: 4, 3: 7, 4: 10}
    산업데이터['월'] = 산업데이터['분기'].map(분기월)
    산업데이터['날짜'] = pd.to_datetime(dict(year=산업데이터['연도'], month=산업데이터['월'], day=1))

if '연도' in 직무데이터.columns:
    직무데이터['연도'] = 직무데이터['연도'].astype(int)
    직무데이터['날짜'] = pd.to_datetime(직무데이터['연도'].astype(str) + '-01-01')

# ================================
# 9. 이상치 처리
# ================================
산업클리핑열 = ['산업인력대체율', '산업신규직무생성율', '순인력변화율', '산업자동화위험점수']
직무클리핑열 = ['자동화위험도(%)', 'AI대체점수', '연봉_이전(달러)', '연봉_이후(달러)', '연봉변화율(%)', '스킬격차지수']

for 열 in 산업클리핑열:
    if 열 in 산업데이터.columns:
        산업데이터[열] = 이상치클리핑(산업데이터[열])

for 열 in 직무클리핑열:
    if 열 in 직무데이터.columns:
        # 그룹(자동화위험등급)별로 이상치 클리핑 적용
        직무데이터[열] = 직무데이터.groupby('자동화위험등급')[열].transform(이상치클리핑)

# ================================
# 10. 파생 변수 생성
# ================================
if {'연봉_이전(달러)', '연봉_이후(달러)'}.issubset(직무데이터.columns):
    직무데이터['연봉변화율_계산'] = (
        (직무데이터['연봉_이후(달러)'] - 직무데이터['연봉_이전(달러)'])
        / 직무데이터['연봉_이전(달러)'] * 100
    )

# ================================
# 11. 통합 테이블 생성
# ================================
산업병합기준 = 산업데이터.copy()
if '산업부문' in 산업병합기준.columns:
    산업병합기준 = 산업병합기준.rename(columns={'산업부문': '산업'})

직무병합열 = [열 for 열 in [
    '직무ID', '직무명', '직무명_한글', '산업', '국가', '연도',
    '자동화위험도(%)', 'AI대체점수', '연봉_이전(달러)', '연봉_이후(달러)',
    '연봉변화율(%)', '스킬격차지수', '자동화위험등급',
    '재교육긴급도점수', 'AI교란강도'
] if 열 in 직무데이터.columns]

통합데이터 = pd.merge(
    산업병합기준,
    직무데이터[직무병합열],
    how='left',
    on=['국가', '연도', '산업']
)

# ================================
# 12. 시각화
# ================================
import os
os.makedirs('plots', exist_ok=True)
print("\n[시각화 안내] 시각화 자료를 개선하고 'plots' 폴더에 고해상도 PNG로 저장합니다...")

# 12-1 산업별 평균 대체율 상위 10개
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
    
    # 막대 끝에 실제 수치값 표시
    for p in ax.patches:
        width = p.get_width()
        if width > 0:
            ax.text(
                width + 0.3, 
                p.get_y() + p.get_height()/2, 
                f"{width:.1f}%", 
                ha="left", 
                va="center", 
                fontsize=10, 
                fontweight='bold', 
                color='#2c3e50'
            )
            
    plt.xlabel('평균 인력 대체율 (%)', fontsize=11, fontweight='bold', labelpad=10)
    plt.ylabel('산업군', fontsize=11, fontweight='bold', labelpad=10)
    plt.title('산업별 평균 AI 대체율 상위 10개', fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig('plots/01_industry_avg_replacement.png', dpi=300)
    plt.show()

# 12-2 평균 대체율 및 순인력변화율 추이
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
    
    # 선 아랫부분에 은은한 쉐이딩 추가
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

# 12-3 산업 수준 상관 히트맵
상관열 = [열 for 열 in [
    '산업자동화위험점수',
    '산업인력대체율',
    '순인력변화율',
    '1인당GDP(달러)',
    '재교육프로그램수',
    'AI도입지수'
] if 열 in 산업데이터.columns]

if len(상관열) >= 2:
    상관행렬 = 산업데이터[상관열].corr()
    plt.figure(figsize=(10, 8))
    
    # 대칭 구조에서 불필요한 상삼각 행렬 마스킹 (시각적 피로 감소)
    mask = np.triu(np.ones_like(상관행렬, dtype=bool))
    
    sns.heatmap(
        상관행렬, 
        mask=mask, 
        annot=True, 
        fmt='.2f', 
        cmap='coolwarm', 
        vmin=-1, 
        vmax=1, 
        center=0,
        square=True, 
        linewidths=0.8,
        linecolor='white',
        cbar_kws={"shrink": .8}
    )
    plt.title('산업 수준 주요 변수 상관관계 (상관계수)', fontsize=14, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)
    plt.tight_layout()
    plt.savefig('plots/03_industry_correlation.png', dpi=300)
    plt.show()


# 12-5 자동화 위험등급별 연봉 변화 (그룹화 분포)
if {'자동화위험등급', '연봉변화율(%)'}.issubset(직무데이터.columns):
    직무위험도순서 = ['Low', 'Medium', 'High']
    plt.figure(figsize=(9, 6))
    
    # 지저분하게 겹쳐 있던 개별 데이터 점(strip plot)을 없새고 박스플롯만 깔끔하게 시각화
    sns.boxplot(
        data=직무데이터,
        x='자동화위험등급',
        y='연봉변화율(%)',
        order=직무위험도순서,
        palette='Pastel1',
        width=0.4,
        hue='자동화위험등급',
        legend=False
    )
    plt.xlabel('자동화 위험 카테고리', fontsize=11, fontweight='bold', labelpad=10)
    plt.ylabel('연봉 변화율 (%)', fontsize=11, fontweight='bold', labelpad=10)
    plt.title('자동화 위험 등급별 연봉 변화율 분포', fontsize=14, fontweight='bold', pad=15)
    sns.despine()
    plt.grid(True, axis='y', linestyle=':', alpha=0.6)
    plt.tight_layout()
    plt.savefig('plots/05_salary_change_by_risk_category.png', dpi=300)
    plt.show()


# 12-7 국가 × 산업별 평균 대체율 히트맵
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
        히트맵피벗, 
        cmap='RdBu_r', center=0,
        linewidths=0.8, 
        linecolor='white', 
        annot=True, 
        fmt='.2f',
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