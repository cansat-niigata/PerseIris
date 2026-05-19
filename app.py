import streamlit as st
import math

# ページの基本設定
st.set_page_config(page_title="POLARiS 落下分散シミュレータ", layout="centered")

st.title("PerseIris 落下分散シミュレータ 🛰️")
st.markdown("投下高度の安全評価ツールです made by nakahen")
st.markdown("---")

# サイドバーまたはメイン画面にパラメータ入力欄を作成
st.header("パラメータ入力")
col1, col2 = st.columns(2)

with col1:
    field_size = st.number_input("フィールドの一辺の長さ [m]", min_value=20.0, max_value=100.0, value=60.0, step=10.0)
    wind_speed = st.number_input("想定限界風速 [m/s]", min_value=1.0, max_value=15.0, value=5.0, step=0.5)

with col2:
    vt = st.number_input("実測した終端速度 [m/s]", min_value=3.0, max_value=20.0, value=10.0, step=0.5)
    margin = st.slider("安全マージン [%]", min_value=50, max_value=100, value=80, step=5, 
                       help="計算上の最大高度に対して、どの程度の余裕を持たせるか（突風などを考慮）")

# 物理定数
g = 9.80665

# 計算処理
# 1. フィールド外に流されるまでの限界落下時間
t_max = (field_size / 2) / wind_speed

# 2. 安全な最大投下高度の計算
# 式: x = (vt^2 / g) * ln(cosh(g * t_max / vt))
max_height = (vt**2 / g) * math.log(math.cosh(g * t_max / vt))

# 安全マージンを考慮した運用上の上限高度
operational_height = max_height * (margin / 100)

st.markdown("---")
st.header("シミュレーション結果")

# 結果のハイライト表示
st.success(f"**運用上の上限投下高度 (マージン{margin}%): {operational_height:.1f} m**")

col3, col4 = st.columns(2)
col3.metric(label="計算上の限界最大高度", value=f"{max_height:.1f} m")
col4.metric(label="限界落下時間 (場外に出るまで)", value=f"{t_max:.2f} 秒")

# 審査向けの説明・数式表示
st.markdown("---")
st.subheader("📝 審査資料用：計算モデル")
st.markdown("本シミュレータは、パラシュートの空気抵抗を慣性抵抗として扱い、以下の式に基づき算出しています。")
st.latex(r"x = \frac{{v_{\infty}}^{2}}{g}\log\left(\cosh\left(\frac{g \cdot t_{max}}{v_{\infty}}\right)\right)")
st.caption("※ $x$: 投下高度, $v_{\infty}$: 終端速度, $g$: 重力加速度, $t_{max}$: フィールド半径 / 想定風速")