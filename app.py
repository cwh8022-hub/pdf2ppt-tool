import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes
from io import BytesIO

st.title("🚀 PDF 轉 Google 簡報 - 一鍵直達版")

# 這裡填入你剛剛在 GAS 取得的網址
GAS_URL = "你的_GAS_網頁應用程式網址"

uploaded_file = st.file_uploader("選擇 PDF 檔案", type="pdf")

if uploaded_file and st.button("開始轉檔並存入 Google 簡報"):
    with st.spinner('正在渲染分頁...請稍候'):
        # 1. Python 負責最難的分頁轉圖
        images = convert_from_bytes(uploaded_file.read(), dpi=150)
        
        base64_images = []
        for img in images:
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            base64_images.append(base64.b64encode(buffered.getvalue()).decode())
        
        # 2. 把圖傳給 GAS，讓 GAS 幫你生簡報
        payload = {
            "fileName": uploaded_file.name,
            "images": base64_images
        }
        
        response = requests.post(GAS_URL, json=payload)
        
        if response.status_code == 200:
            st.success("🎉 轉換成功！簡報已存入您的 Google Drive")
            st.write(f"👉 [點此開啟簡報]({response.text})")
        else:
            st.error("連線到 Google 失敗，請檢查 GAS 部署設定。")
