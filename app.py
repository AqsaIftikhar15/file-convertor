from io import BytesIO
import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_icon = ":rocket:",
    page_title= "File covertor",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("File convertor and cleaner :mechanic:")
st.write("This is a simple file format transformer with Inbuilt data sanitization and embedded data visualization methods.")

files_upload = st.file_uploader("Upload your files(csv or xlsx) ", type=["csv", "xlsx"], accept_multiple_files=True)


if files_upload:
    for files in files_upload:
        file_ext = os.path.splitext(files.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(files)
            st.success("CSV file uploaded successfully") 
        elif file_ext == ".xlsx":
            df = pd.read_excel(files)
            st.success("Xlxs file uploaded successfully") 
        else:
            st.error(f"Error uploading file. Only csv and xlsx files are supported:{file_ext}")
            continue
#disply info about the fils
        st.write(f"**file Name:** {files.name}")
        st.write(f"**file Type:**", file_ext)
        st.write("**file size:**", f"{files.size:.2f} KB")
#showing data frame
        st.write("Preview the head of the data frame:")
        st.dataframe(df.head())
#data cleanig
        st.subheader("Data cleaning and sanitization options:")
        if st.checkbox(f"Clean data for {files.name}"):
            col1 , col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from{files.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success(f"Removed duplicates from {files.name}")
            with col2:
                if st.button(f"Fill missing values from {files.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success(f"Filled missing values from {files.name}")
#custom headers to clea or keep
        st.subheader("Choose columns to convert")
        columns = st.multiselect(f"choose from {files.name}", df.columns, default=df.columns)
        df = df[columns]
#visualization
        st.subheader("Data visualization📈")
        if st.button(f"Show data visualization for:{files.name}"):
            st.write("Here is the data visualization for the uploaded file")
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])

# file conversions
        st.subheader("File conversion options⚙️")
        conversion_types = st.radio(f"Convert {files.name} to:",["CSV","Excel"],key=files.name)
        if st.button(f"Convert:{files.name}"):
            buffer = BytesIO()
            if conversion_types == "CSV":
                df.to_csv(buffer,index=False)
                file_name = files.name.replace(file_ext,".csv")
                mime_type = "text/csv"
            elif conversion_types == "Excel":
                df.to_excel(buffer,index=False)
                file_name = files.name.replace(file_ext,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)
#downloads
            st.download_button(
                label=f"🔻Download {file_name} as {conversion_types}",
                data=buffer, 
                file_name=file_name,
                mime = mime_type)

    st.success("🎊All files successfully processed!")
            


st.write("---")  
st.write("Created by Aqsa Iftikhar")
