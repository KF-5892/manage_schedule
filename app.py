import streamlit as st
import pandas as pd
from gspread_pandas import Spread, Client
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from datetime import datetime, time

# Googleスプレッドシートの設定
SPREADSHEET_ID = "https://docs.google.com/spreadsheets/d/1dgWwUnTNclHZBNyb6VEp97TpxrkjbTf2vjnmcTQorX0/edit?usp=sharing"
SHEET_NAME = "11月"

# 認証設定
# YOUR_CREDENTIAL_FILEPATH = 'streamlitkey.json'
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# credentials = Credentials.from_service_account_file(
#     YOUR_CREDENTIAL_FILEPATH,
#     scopes=scopes
# )
credentials = service_account.Credentials.from_service_account_info( st.secrets["gcp_service_account"], scopes=scopes)

gc = gspread.authorize(credentials)

# スプレッドシートからデータを読み込む関数
def load_data():
    spread = Spread(SPREADSHEET_ID, sheet=SHEET_NAME, creds=credentials)
    df = spread.sheet_to_df()
    df['時間'] = pd.to_datetime(df['時間'], format='%H:%M').dt.time  # 
    st.dataframe(df)
    return df

# データをスプレッドシートに保存する関数
def save_data(df):
    spread = Spread(SPREADSHEET_ID, sheet=SHEET_NAME, creds=credentials)
    spread.df_to_sheet(df, index=True, sheet=SHEET_NAME, start='A1', replace=True)

# メイン関数
def main():
    st.title("スケジュール")

    # データの読み込み
    if 'data' not in st.session_state:
        st.session_state.data = load_data()

    # データ編集用のフォーム
    with st.form("edit_form"):
        edited_df = st.data_editor(
            st.session_state.data,
            column_config={
                # "日付": st.column_config.DateColumn("日付", format="YYYY/MM/DD"),
                "時間": st.column_config.TimeColumn("時間", format="HH:mm",default=time(21, 00)),
                "タイトル": st.column_config.TextColumn("タイトル"),
                "種類": st.column_config.SelectboxColumn("種類", options=["レッスン", "本番", "リハーサル"]),
                "みなみ": st.column_config.CheckboxColumn("みなみ",default=False),
                "まあこ": st.column_config.CheckboxColumn("まあこ"),
                "るみ": st.column_config.CheckboxColumn("るみ"),
                "りく": st.column_config.CheckboxColumn("りく"),
                "たかみな": st.column_config.CheckboxColumn("たかみな"),
                "きょう": st.column_config.CheckboxColumn("きょう"),
                "備考": st.column_config.TextColumn("備考"),
            },
            num_rows="dynamic",
            use_container_width=True,
        )

        submitted = st.form_submit_button("保存")

    if submitted:
        save_data(edited_df)
        st.success("データが保存されました。")
        st.session_state.data = edited_df

if __name__ == "__main__":
    main()