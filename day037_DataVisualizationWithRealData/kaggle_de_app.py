# kaggle_de_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. ページの設定
st.set_page_config(page_title="学生就職データ分析", layout="wide")

# 2. タイトルと説明
st.title("Student Placement Analysis Dashboard")
st.markdown("学生の成績、スキル、インターン経験などが、**「就職(Placed)」**や**「年収(Salary)」**にどう影響するかを分析します。")

# 3. データの読み込み（キャッシュ機能を使って高速化）
@st.cache_data
def load_data():
    df = pd.read_csv("student_placement_prediction_dataset_2026.csv")
    return df

df = load_data()

# 4. サイドバーを作る
st.sidebar.header("Filter Options")

# 5. フィルターを作る
# 学部フィルタ
all_branches = df["branch"].unique()
selected_branches = st.sidebar.multiselect(
    "学部を選択",
    options=all_branches,
    default=all_branches
)

# 大学ランクフィルタ
all_tiers = df["college_tier"].unique()
selected_tiers = st.sidebar.multiselect(
    "大学ランク（Tier）を選択",
    options=all_tiers,
    default=all_tiers
)

# フィルタされたdf
filtered_df = df[
    (df['branch'].isin(selected_branches)) &
    (df["college_tier"].isin(selected_tiers))
]

# データがなかった場合
if filtered_df.empty:
    st.error("No data matched. Adjust the filter option(s).")
    st.stop()

st.divider()

# 6. KPIエリア
total_students = len(filtered_df)
placed_students = filtered_df[filtered_df["placement_status"] == "Placed"]
placement_rate = len(placed_students) / total_students * 100

# Salaryの平均
avg_salary = placed_students["salary_package_lpa"].mean() if not placed_students.empty else 0
max_salary = placed_students["salary_package_lpa"].max() if not placed_students.empty else 0

# 7. グラフを表示
col1, col2, col3, col4 = st.columns(4)
col1.metric("表示中の学生", f"{total_students}人")
col2.metric("就職率(Placement Rate)", f"{placement_rate:.1f}%")
col3.metric("平均年収(LPA)", f"₹{avg_salary:.2f}")
col4.metric("最高年収(LPA)", f"₹{max_salary:.2f}")

st.divider()

col_chart1, col_chart2 = st.columns(2)

# グラフ1: 学部ごとの就職状況（積み上げ棒グラフ）
with col_chart1:
    st.subheader("学部ごとの就職状況")
    branch_status = filtered_df.groupby(['branch', 'placement_status']).size().reset_index(name='count')

    fig1 = px.bar(
        branch_status,
        x='branch',
        y='count',
        color="placement_status",
        title='Branch vs Placement Status',
        text_auto=True,
        barmode='group'
    )
    st.plotly_chart(fig1, width='stretch')

# グラフ2: CGPAと年収の関係（散布図）
with col_chart2:
    st.subheader("成績（CGPA）と年収の関係")
    # 就職した人だけのデータを使う
    placed_only = filtered_df[filtered_df["placement_status"] == "Placed"]

    if not placed_only.empty:
        fig2 = px.scatter(
            placed_only,
            x="cgpa",
            y="salary_package_lpa",
            color="college_tier", #大学ランクで色分け
            size="coding_skill_score", #bubbleの大きさ=coding skill
            hover_data=["branch", "coding_skill_score"],
            title="CGPA vs Salary (Size = Coding Skill)"
        )
        st.plotly_chart(fig2, width='stretch')
    else:
        st.info("就職者データなし")

# グラフ3: スキルスコアの分布比較（箱ひげ図）
st.subheader("内定者 vs 未内定者：スキル比較")
st.markdown("就職できたできないで、スキルの点数に差はあるか？")

# 比較したいスコアを選択
target_score = st.selectbox(
    "比較するスキルを選択",
    ["coding_skill_score", "aptitude_score", "communication_skill_score", "logical_reasoning_score", "cgpa"]
)

fig3 = px.box(
    filtered_df,
    x="placement_status",
    y=target_score,
    color="placement_status",
    title=f"{target_score} Distribution by Placement Status",
    points="outliers" # データセットが膨大なため、外れ値だけを描画する！Allにすると、描画にフリーズしちゃうかも。
)
st.plotly_chart(fig3, width='stretch')

fig4 = px.treemap(
    filtered_df,
    path=['branch', 'placement_status'],
    color='placement_status',
    color_discrete_map={"Placed": "#00CC96", "Not Placed": "#EF553B"}
)
st.plotly_chart(fig4, width='stretch')

if st.checkbox("Raw Dataを表示"):
    st.dataframe(filtered_df)