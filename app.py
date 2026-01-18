import streamlit as st
import requests
import base64
from pdf2image import convert_from_bytes
from io import BytesIO

# 設定網頁標題與風格
st.set_page_config(page_title="PDF 轉 Google 簡報工具", layout="centered")
st.title("📄 PDF 一鍵轉 Google 簡報")
st.write("上傳 NotebookLM PDF，系統會自動在您的雲端硬碟生成分頁簡報。")

# --- 關鍵：您的 GAS 接收網址 ---
GAS_URL = "https://script.google.com/macros/s/AKfycbx6s5EHaHBEg_wLEHyFJpwgppcyQQA3SPpKywTohHPPcIBUr7gx8tL1xVp2RMxuRfGPmQ/exec"

uploaded_file = st.file_uploader("請選擇 PDF 檔案", type="pdf")

if uploaded_file and st.button("🚀 開始轉換並存入 Google Drive"):
    with st.spinner('正在渲染高清分頁並傳送至 Google 雲端... 請稍候'):
        try:
            # 1. 使用 Python 強大的 poppler 引擎渲染 PDF
            # dpi=150 是畫質與速度的最佳平衡點
            images = convert_from_bytes(uploaded_file.read(), dpi=300)
            
            base64_images = []
            for img in images:
                buffered = BytesIO()
                img.save(buffered, format="JPEG", quality=85)
                # 將圖片轉為 Base64 字串，以便傳送給 GAS
                img_str = base64.b64encode(buffered.getvalue()).decode()
                base64_images.append(img_str)
            
            # 2. 封裝數據並傳送給您的 GAS 網址
            payload = {
                "fileName": uploaded_file.name,
                "images": base64_images
            }
            
            # 使用 POST 方法將資料推送到 Google 
            response = requests.post(GAS_URL, json=payload)
            
            if response.status_code == 200:
                # GAS 回傳的是新簡報的 URL
                presentation_url = response.text
                st.success("🎉 轉換成功！簡報已存入您的 Google Drive。")
                st.balloons() # 慶祝動畫
                st.markdown(f"### 👉 [點此開啟您的 Google 簡報]({presentation_url})")
            else:
                st.error(f"連線失敗，Google 伺服器回傳狀態碼: {response.status_code}")
                
        except Exception as e:
            st.error(f"轉換過程中發生錯誤: {str(e)}")
            st.info("提示：請確認 GitHub 中是否有 packages.txt 並包含 poppler-utils")

st.divider()
st.caption("本工具由 Python (Streamlit) 與 Google Apps Script 聯手驅動。")
