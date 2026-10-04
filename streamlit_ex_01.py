import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# データの読み込み
@st.cache_data
def load_data():
    return pd.read_csv('ad_expense_sales.csv')

df = load_data()

with st.sidebar:
    st.header('抽出条件')

    # 1. 製品カテゴリ選択 (複数選択可)
    prod_category_options = df['prod_category'].unique().tolist()
    selected_categories = st.multiselect(
        '製品カテゴリを選択してください（複数選択可）',
        options=prod_category_options,
        default=['air cleaner', 'hair dryer']
    )

    # 2. 広告媒体選択
    media_options = df['media'].unique().tolist()
    selected_media = st.selectbox(
        '広告媒体を選択してください',
        options=media_options,
        index=media_options.index('TV') if 'TV' in media_options else 0
    )

    # 3. 色分け設定
    st.header('色分け')

    # 分類選択（性別、年齢層、季節）
    color_group_map = {
        '性別': 'sex',
        '年齢層': 'age',
        '季節': 'season'
    }

    selected_group_label = st.selectbox(
        '分類を選択してください',
        options=list(color_group_map.keys()),
        index=0  # デフォルトで「性別」を選択
    )

selected_group_col = color_group_map[selected_group_label]

# --------------------------------------------------
# データの加工とマッピング
# --------------------------------------------------
# 英語表記値を日本語化するマッピング辞書
value_jp_map = {
    # 性別
    'male': '男性',
    'female': '女性',
    # 年齢層
    'young': '若年層',
    'middle': 'ミドル層',
    'senior': 'シニア層',
    # 季節
    'spring': '春',
    'summer': '夏',
    'fall': '秋',
    'winter': '冬'
}

# データの抽出・フィルタリング
filtered_df = df[
    (df['prod_category'].isin(selected_categories)) &
    (df['media'] == selected_media)
].copy()

# 色分け用列の値を日本語に変換
filtered_df['display_color'] = filtered_df[selected_group_col].map(value_jp_map).fillna(filtered_df[selected_group_col])

# --------------------------------------------------
# メイン画面表示
# --------------------------------------------------
st.title('広告費と売上')

if not filtered_df.empty:
    # Plotlyで散布図と回帰直線の作成
    fig = px.scatter(
        filtered_df,
        x='ad_expense',
        y='sales',
        color='display_color',
        trendline='ols',
        labels={
            'ad_expense': '広告費（万円）',
            'sales': '売上（万円）',
            'display_color': selected_group_label
        }
    )

    # グラフのレイアウト設定
    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            zeroline=True,
            zerolinecolor='#d0d0d0'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            zeroline=True,
            zerolinecolor='#d0d0d0'
        ),
        legend_title_text=selected_group_label
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning('該当するデータがありません。抽出条件を変更してください。')