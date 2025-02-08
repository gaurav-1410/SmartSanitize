# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import seaborn as sns
# import matplotlib.pyplot as plt

# class VisualizationPage:
#     def __init__(self):
#         pass

#     def display_visualization_options(self, df):
#         """Displays EDA and visualization options."""
#         # st.subheader("📊 Explore Data with Visualizations")

#         if df is None or df.empty:
#             st.warning("⚠️ No data available. Please upload a file first.")
#             return

#         # Select column for visualization
#         column = st.selectbox("Select a column to visualize:", df.columns)

#         # Choose plot type
#         plot_type = st.radio("Choose Plot Type", ["Histogram", "Boxplot", "Scatter", "Correlation Heatmap"])

#         if plot_type == "Histogram":
#             fig = px.histogram(df, x=column, title=f"Distribution of {column}", nbins=30)
#             st.plotly_chart(fig)

#         elif plot_type == "Boxplot":
#             fig = px.box(df, y=column, title=f"Boxplot of {column}")
#             st.plotly_chart(fig)

#         elif plot_type == "Scatter":
#             num_cols = df.select_dtypes(include=["number"]).columns
#             if len(num_cols) < 2:
#                 st.error("⚠️ Scatter plot requires at least two numeric columns.")
#             else:
#                 col2 = st.selectbox("Select another column for scatter plot:", num_cols)
#                 fig = px.scatter(df, x=column, y=col2, title=f"Scatter Plot: {column} vs {col2}")
#                 st.plotly_chart(fig)

#         elif plot_type == "Correlation Heatmap":
#             num_cols = df.select_dtypes(include=["number"])
#             if num_cols.shape[1] < 2:
#                 st.error("⚠️ Not enough numerical columns for correlation heatmap.")
#             else:
#                 fig, ax = plt.subplots(figsize=(8, 6))
#                 sns.heatmap(num_cols.corr(), annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
#                 st.pyplot(fig)

import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import io

class VisualizationPage:
    def __init__(self):
        pass

    def display_visualization_options(self, df):
        """Enhanced EDA and Visualization with optional filtering."""
        # st.subheader("📊 Explore Your Data")

        if df is None or df.empty:
            st.warning("⚠️ No data available. Please upload a file first.")
            return

        ## **✨ Auto-Detect Numerical and Categorical Columns**
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        ## **📑 Data Summary Before Visualization**
        if st.checkbox("🔍 Show Data Summary"):
            st.write(df.describe(include="all"))

        ## **🔽 Optional Advanced Filtering**
        apply_filter = st.checkbox("⚙️ Enable Advanced Filtering")  # Checkbox to enable filtering

        if apply_filter:
            with st.expander("🔽 Advanced Filtering Options"):
                filter_column = st.selectbox("📂 Select column to filter:", df.columns)
                unique_values = df[filter_column].unique()
                selected_values = st.multiselect(f"🎯 Filter {filter_column}:", unique_values, default=unique_values[:5])
                df_filtered = df[df[filter_column].isin(selected_values)]
        else:
            df_filtered = df.copy()  # Keep original data if filtering is not applied

        ## **📈 Select Column(s) for Visualization**
        col_selection = st.multiselect("🎯 Select columns for visualization:", num_cols + cat_cols, default=[num_cols[0]] if num_cols else [])

        ## **📊 Choose Visualization Type**
        plot_type = st.radio("📌 Choose a Plot Type", ["Histogram", "Boxplot", "Scatter", "Line Chart", "Correlation Heatmap", "Bar Chart"])

        ## **📌 Handling Different Chart Types**
        if plot_type == "Histogram":
            fig = px.histogram(df_filtered, x=col_selection[0], title=f"📊 Distribution of {col_selection[0]}", nbins=30, color_discrete_sequence=["#636EFA"])
            fig.update_layout(bargap=0.2)  # Adds spacing between bars
            st.plotly_chart(fig)

        elif plot_type == "Boxplot":
            fig = px.box(df_filtered, y=col_selection[0], title=f"📦 Boxplot of {col_selection[0]}", color_discrete_sequence=["#EF553B"])
            st.plotly_chart(fig)

        elif plot_type == "Scatter":
            if len(col_selection) < 2:
                st.error("⚠️ Scatter plot requires at least two numeric columns.")
            else:
                fig = px.scatter(df_filtered, x=col_selection[0], y=col_selection[1], title=f"📍 Scatter Plot: {col_selection[0]} vs {col_selection[1]}", color_discrete_sequence=["#00CC96"])
                fig.update_traces(marker=dict(size=8, opacity=0.7))  # Improve marker visibility
                st.plotly_chart(fig)

        elif plot_type == "Line Chart":
            time_col = st.selectbox("⏳ Select a time column (if applicable):", df_filtered.columns)
            fig = px.line(df_filtered, x=time_col, y=col_selection[0], title=f"📈 Line Chart of {col_selection[0]} Over Time")
            st.plotly_chart(fig)

        elif plot_type == "Correlation Heatmap":
            if len(num_cols) < 2:
                st.error("⚠️ Not enough numerical columns for correlation heatmap.")
            else:
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.heatmap(df_filtered[num_cols].corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
                st.pyplot(fig)

        elif plot_type == "Bar Chart":
            fig = px.bar(df_filtered, x=col_selection[0], y=col_selection[1] if len(col_selection) > 1 else None, title=f"📊 Bar Chart of {col_selection[0]}")
            st.plotly_chart(fig)

        ## **📥 Download Chart Option**
        # st.markdown("### 💾 Download Chart as PNG")
        # buf = io.BytesIO()
        # fig.write_image(buf, format="png")
        # st.download_button(label="📥 Download Image", data=buf, file_name="visualization.png", mime="image/png")
