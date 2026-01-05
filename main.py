import streamlit as st
import yfinance as yf
import pandas as pd

# 1. 網頁頁面設定
st.set_page_config(page_title="台股即時監控", layout="wide")
st.title("📈 台股即時自動化分析儀表板")

# 2. 搜尋欄位
user_input = st.text_input("輸入台股代號 (例如: 2330, 2454, 0050)", value="2330").strip()

# 自動補足 .TW 邏輯
stock_id = user_input + ".TW" if user_input.isdigit() else user_input

# 3. 抓取數據
stock = yf.Ticker(stock_id)

try:
    # 抓取歷史股價與公司資訊
    hist = stock.history(period="3mo")  # 抓三個月的資料
    info = stock.info

    if hist.empty:
        st.error("找不到該股票資料，請檢查代號是否正確。")
    else:
        # 計算漲跌
        current_price = hist['Close'].iloc[-1]
        prev_price = hist['Close'].iloc[-2]
        delta = current_price - prev_price

        # 4. 顯示大標題與指標
        display_name = info.get('shortName') or info.get('longName') or "未知公司"
        st.header(f"{display_name} ({stock_id})")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("目前股價", f"{current_price:.2f} 元", f"{delta:.2f}")
        col2.metric("本益比 (PE)", f"{info.get('trailingPE', 'N/A')}")

        # 殖利率處理
        dy = info.get('dividendYield') or info.get('yield')
        dy_display = f"{dy * 100:.2f}%" if dy else "暫無資料"
        col3.metric("現金殖利率", dy_display)
        col4.metric("今日最高價", f"{hist['High'].iloc[-1]:.2f}")

        # 5. 繪製互動式股價走勢圖
        st.subheader("📊 三個月股價走勢圖")
        st.line_chart(hist['Close'])

        # 6. 顯示公司詳細財務數據
        with st.expander("查看詳細財務數據"):
            st.write(f"**市值:** {info.get('marketCap', 0):,}")
            st.write(f"**52週最高:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
            st.write(f"**52週最低:** {info.get('fiftyTwoWeekLow', 'N/A')}")
            st.write(f"**公司簡介:** {info.get('longBusinessSummary', '暫無簡介')}")

except Exception as e:
    st.error(f"系統發生錯誤: {e}")