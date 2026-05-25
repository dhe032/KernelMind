import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="KernelMind",
    page_icon="💻",
    layout="wide"
)

# 제목
st.markdown("""
<h1 style='text-align:center;
color:#00FFD1;
font-size:60px;'>
💻 KernelMind
</h1>
""", unsafe_allow_html=True)

st.markdown("""
<h3 style='text-align:center; color:gray;'>
AI Kernel Panic & Linux Log Analyzer
</h3>
""", unsafe_allow_html=True)

st.subheader("AI Kernel Panic & OS Log Explainer")

# 사이드바
st.sidebar.title("About")
st.sidebar.write("""
KernelMind analyzes Linux kernel and system logs
using AI and explains OS-level issues.
""")

# API 연결
client = OpenAI(
    api_key="여기에_API_KEY",
    base_url="https://api.upstage.ai/v1"
)

# 파일 업로드
uploaded_file = st.file_uploader(
    "Upload log file (.txt)",
    type=["txt"]
)

log_input = ""

# 샘플 로그 버튼
if st.button("Load Sample Kernel Panic"):

    log_input = """
kernel panic - not syncing:
Fatal exception
CPU overload
memory corruption detected
"""

    st.text_area(
        "Sample Log",
        log_input,
        height=200
    )

# 업로드 파일 읽기
if uploaded_file is not None:
    log_input = uploaded_file.read().decode("utf-8")

    st.text_area(
        "Uploaded Log",
        log_input,
        height=200
    )

# 직접 입력창
manual_input = st.text_area(
    "Or paste your log here",
    height=200
)

if manual_input:
    log_input = manual_input

# 분석 버튼
if st.button("Analyze Log"):

    if log_input == "":
        st.warning("Please upload or paste a log.")

    else:

        error_type = "Unknown"
        severity = "Low"

        log_lower = log_input.lower()

        # 로그 분류
        if "kernel panic" in log_lower:
            error_type = "Kernel Panic"
            severity = "Critical"

        elif "segmentation fault" in log_lower:
            error_type = "Segmentation Fault"
            severity = "High"

        elif "deadlock" in log_lower:
            error_type = "Deadlock"
            severity = "High"

        elif "out of memory" in log_lower:
            error_type = "Memory Issue"
            severity = "High"

        # 결과 표시
        st.subheader("Analysis Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Error Type", error_type)

        with col2:
            st.metric("Severity", severity)

        # 위험도 표시
        if severity == "Critical":
            st.error("Critical System Issue Detected")

        elif severity == "High":
            st.warning("High Severity Issue")

        else:
            st.success("Low Severity")

        # AI 프롬프트
        prompt = f"""
Analyze this Linux OS log.

Log:
{log_input}

Explain:
1. What happened
2. Possible causes
3. Suggested solutions

Make the explanation beginner-friendly.
"""

        # AI 로딩
        with st.spinner("Analyzing system logs..."):

            # AI 호출
            response = client.chat.completions.create(
                model="solar-pro2",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            ai_result = response.choices[0].message.content

        # AI 결과 출력
        st.subheader("AI Explanation")

        st.write(ai_result)