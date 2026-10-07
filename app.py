import streamlit as st
import base64
from openai import OpenAI
from PIL import Image

# ----------------- تنظیمات رابط کاربری تجاری -----------------
st.set_page_config(page_title="AI Conversion Analyzer", page_icon="🚀", layout="wide")

st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    h1 {color: #0f172a; font-weight: 900;}
    .stButton>button {background-color: #2563eb; color: white; border-radius: 8px; padding: 0.75rem 2rem; width: 100%; border: none;}
    .stButton>button:hover {background-color: #1d4ed8; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);}
    div[data-testid="stSidebar"] {background-color: #ffffff; border-right: 1px solid #e2e8f0;}
</style>
""", unsafe_allow_html=True)

# ----------------- توابع پردازشی -----------------
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# ----------------- معماری اصلی -----------------
def main():
    st.markdown("<h1>🚀 سیستم هوشمند تحلیل نرخ تبدیل (UX/UI Analyzer)</h1>", unsafe_allow_html=True)
    st.markdown("تصویر لندینگ‌پیج یا اپلیکیشن خود را آپلود کنید تا هوش مصنوعی در چند ثانیه خطاهای طراحی را پیدا کرده و راهکارهای افزایش فروش ارائه دهد.")
    st.markdown("---")

    with st.sidebar:
        st.header("⚙️ تنظیمات موتور AI")
        api_key = st.text_input("🔑 OpenAI API Key:", type="password")
        st.divider()
        uploaded_file = st.file_uploader("📸 آپلود اسکرین‌شات (PNG/JPG)", type=["png", "jpg", "jpeg"])
        st.caption("سیستم از مدل بینایی ماشین GPT-4o برای تحلیل استفاده می‌کند.")

    if uploaded_file and api_key:
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("تصویر ورودی")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True, caption="در حال پردازش توسط ماشین...")
            
        with col2:
            st.subheader("📊 گزارش تحلیل تخصصی (Actionable Insights)")
            
            # دکمه اجرای تحلیل
            if st.button("شروع اسکن هوشمند رابط کاربری"):
                with st.spinner("🤖 موتور Vision AI در حال تحلیل معماری بصری، رنگ‌ها و دکمه‌های CTA..."):
                    try:
                        client = OpenAI(api_key=api_key)
                        base64_image = encode_image(uploaded_file)
                        
                        # پرامپت مهندسی‌شده برای استخراج اطلاعات دقیق UI/UX
                        system_prompt = """
                        شما یک متخصص ارشد UX/UI و بهینه‌سازی نرخ تبدیل (CRO) هستید. تصویر ارسالی یک رابط کاربری است.
                        لطفاً با لحنی حرفه‌ای و تجاری، در ۳ بخش به زبان فارسی پاسخ دهید:
                        ۱. امتیاز تخمینی UX از ۱۰۰.
                        ۲. سه خطای اصلی در طراحی (مشکلات خوانایی، جایگذاری غلط، رنگ‌بندی و...).
                        ۳. سه راهکار عملی و فوری برای افزایش کلیک و تبدیل کاربر به مشتری.
                        از ساختار Markdown (بولد کردن و لیست‌ها) استفاده کنید.
                        """
                        
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {"type": "text", "text": system_prompt},
                                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                                    ]
                                }
                            ],
                            max_tokens=800,
                            temperature=0.3
                        )
                        
                        ai_report = response.choices[0].message.content
                        st.info(ai_report)
                        st.success("✅ تحلیل با موفقیت انجام شد. این اطلاعات مستقیماً باعث افزایش نرخ تبدیل می‌شود.")
                        
                    except Exception as e:
                        st.error(f"خطا در ارتباط با سرور هوش مصنوعی: {e}")
    else:
        st.info("👈 برای شروع، کلید API و یک تصویر از رابط کاربری را در پنل سمت راست وارد کنید.")

if __name__ == '__main__':
    main()