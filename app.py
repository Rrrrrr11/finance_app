import streamlit as st
import pandas as pd
import numpy as np

# 页面配置
st.set_page_config(
    page_title="数据集分析可视化工具",
    page_icon="📊",
    layout="wide"
)

# 标题
st.title("📊 数据集分析与可视化工具")
st.caption("支持CSV文件上传 | 自动统计分析 | 动态图表可视化")

# 1. 文件上传区域
st.subheader("📁 上传数据集")
uploaded_file = st.file_uploader("选择CSV文件", type="csv")

if uploaded_file is not None:
    # 解析CSV文件
    try:
        df = pd.read_csv(uploaded_file)
        st.success("文件上传并解析成功！")
        
        # 2. 数据预览区域
        st.subheader("👁️ 数据预览")
        st.dataframe(df.head(10), use_container_width=True)
        st.caption("仅展示前10行数据")
        
        # 3. 基础统计分析区域
        st.subheader("📈 基础统计分析")
        # 筛选数值型列
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if numeric_cols:
            stats_col1, stats_col2, stats_col3 = st.columns(3)
            for idx, col in enumerate(numeric_cols):
                values = df[col].dropna()
                count = len(values)
                mean = values.mean().round(2)
                median = values.median().round(2)
                min_val = values.min().round(2)
                max_val = values.max().round(2)
                std = values.std().round(2)
                
                # 按列展示统计卡片
                with [stats_col1, stats_col2, stats_col3][idx % 3]:
                    st.info(f"""
                    **{col}**  
                    数据总数：{count}  
                    平均值：{mean}  
                    中位数：{median}  
                    最小值：{min_val}  
                    最大值：{max_val}  
                    标准差：{std}
                    """)
        else:
            st.warning("数据集中无数值型列，无法生成统计分析")
        
        # 4. 数据可视化区域（改用Streamlit原生图表，无Plotly依赖）
        st.subheader("📊 数据可视化")
        if numeric_cols:
            selected_col = st.selectbox("选择要可视化的列", numeric_cols)
            chart_type = st.radio("选择图表类型", ["柱状图", "折线图"])
            
            # 准备可视化数据
            plot_data = df[selected_col].dropna()
            if len(plot_data) > 50:  # 限制数据量，避免卡顿
                plot_data = plot_data.head(50)
            
            # 生成原生图表
            if chart_type == "柱状图":
                st.bar_chart(plot_data, use_container_width=True)
            elif chart_type == "折线图":
                st.line_chart(plot_data, use_container_width=True)
        else:
            st.warning("数据集中无数值型列，无法生成可视化图表")
            
    except Exception as e:
        st.error(f"文件解析失败：{str(e)}")
else:
    st.info("⚠️ 仅支持CSV格式数据集，文件编码建议为UTF-8")

# 页脚
st.markdown("---")
st.caption("✅ 纯前端数据集分析工具 | 无需上传服务器 | 所有数据仅在本地处理")
