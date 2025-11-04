import streamlit as st
import pandas as pd
import numpy as np
import io 
import matplotlib.pyplot as mb

# set page (title and text)
st.set_page_config(page_title='SharKlean',layout='wide',page_icon='🦈')
st.title('🦈SharKlean')
st.write('Upload your CSV files SharKlean will help to find missing values.')


# for uploading data
upload_file=st.file_uploader('📂 Upload CSV file',type=['csv'])

if upload_file is not None:
    try:
        df=pd.read_csv(upload_file)
        # converting bool column as str
        bool_col=df.select_dtypes(include=['bool']).columns
        df[bool_col]=df[bool_col].astype(str)
    except Exception as e:
        st.error('Could Not Read The Csv.Please Check The File Format')
        st.exception(e)
        st.stop()
    st.success('📩 File Uploaded Successfully!')
    st.write('### 📃 Preview of Data')
    st.dataframe(df.head())

    st.subheader('ℹ️ Summary')
    st.write(f'**Shape : ** {df.shape[0]} rows x {df.shape[1]} columns')
    st.write('**Column Info : **')
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    st.text(s)
     
     # add missing searcher
    st.write('**Missing Values Per Column :**')
    st.write(df.isnull().sum())
    st.write(f"**Total Missing Values:** {df.isnull().sum().sum()}")
    #records duplication
    st.write(f"**Duplicate Records:** {df.duplicated().sum()}")

     # if no missing values  
    total_missing = df.isnull().sum().sum()
    total_duplicates = df.duplicated().sum()

    if total_missing == 0:
        st.info("🎉 Your data doesn’t have any missing values!")
    else:
        st.warning(f"⚠️ Your data has {total_missing} missing values.")
        
    # Data cleaning
    st.subheader('💼 Data Cleaning')
    def convert_df_to_csv(download_df):
        return download_df.to_csv(index=False).encode('utf-8')
    if st.button("🚫 Remove Missing Values"):
        cleaned_df = df.dropna()
        st.success(f"Removed missing values! Rows left: {cleaned_df.shape[0]}")
        csv = convert_df_to_csv(cleaned_df)
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv,
            file_name="cleaned_remove_missing.csv",
            mime="text/csv"
        )
   