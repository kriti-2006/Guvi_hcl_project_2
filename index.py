import streamlit as st
import pandas as pd

st.title("Missing Data Cleaner")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Original Dataset")
    st.dataframe(df)

    st.subheader("Missing Values per Column")
    missing_counts = df.isnull().sum()
    st.write(missing_counts)

    method = st.selectbox(
        "Choose a method to fill missing values (numeric columns only):",
        ["Mean", "Median", "Mode"]
    )

    if st.button("Clean Missing Data"):
        numeric_cols = df.select_dtypes(include=['number']).columns

        if method == "Mean":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif method == "Median":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif method == "Mode":
            for col in numeric_cols:
                mode_value = df[col].mode()
                if not mode_value.empty:
                    df[col].fillna(mode_value[0], inplace=True)

        st.success("Missing values have been filled successfully!")

        st.subheader("Cleaned Dataset")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Cleaned CSV",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )
