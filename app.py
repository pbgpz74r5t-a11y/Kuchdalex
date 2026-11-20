import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="LexCheck AI", page_icon="⚖️", layout="wide")

st.title("⚖️ LexCheck AI: Huquqiy Tahlilchi")
st.write("O'quv qo'llanmangizni yuklang, tizim undagi barcha qonun moddalarini topib, tahlil qiladi.")

uploaded_file = st.file_uploader("PDF faylni tanlang", type="pdf")

if uploaded_file is not None:
    if st.button("Tahlilni boshlash", type="primary"):
        with st.spinner("Sun'iy intellekt 300 betlik kitobni skanerlamoqda..."):
            # O'zingizning Codespace havolangizni qo'ying
            url = "https://expert-space-invention-5v9v6pg5v9qpfvqx9-8000.app.github.dev/upload"
            
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            
            try:
                response = requests.post(url, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Natijalarni chiroyli ko'rsatish
                    col1, col2 = st.columns(2)
                    col1.metric("Fayl nomi", data['filename'])
                    col2.metric("Jami sahifalar", data['pages'])
                    
                    citations = data.get("citations", [])
                    
                    if citations:
                        st.success(f"Tahlil yakunlandi! Kitobdan {len(citations)} ta qonun moddasi topildi.")
                        
                        # Ma'lumotlarni jadvalga aylantirish
                        df = pd.DataFrame(citations)
                        df = df.rename(columns={
                            "raw": "Topilgan matn",
                            "code": "Kodeks",
                            "article": "Modda",
                            "page": "Sahifa"
                        })
                        
                        st.subheader("📋 Topilgan qonunlar ro'yxati:")
                        st.dataframe(df[["Sahifa", "Topilgan matn", "Kodeks", "Modda"]], use_container_width=True)
                        
                        # Sun'iy intellekt tahlili (Mock qismi)
                        st.subheader("🤖 AI Xulosasi va Ogohlantirishlar")
                        st.info("⚠️ Quyidagi moddalar Lex.uz bazasida o'zgarganligi aniqlandi (Demo):")
                        
                        # Taqdimot uchun bitta xatoni vizual ko'rsatish
                        with st.expander("🚨 MJTK 10-moddasi (6-sahifa) - O'zgartirilgan"):
                            st.error("**Kitobdagi matn:** MJTK 10-moddasi eski tahrirda berilgan.")
                            st.success("**Lex.uz dagi yangi tahrir:** Ushbu moddaga 2023-yil dekabr oyida o'zgartirish kiritilgan. Yangi jazo choralari qo'shilgan.")
                            st.button("Yangi tahrirni kitobga qo'shish")
                            
                else:
                    st.error(f"Backend xatolik qaytardi: {response.status_code}")
            except Exception as e:
                st.error(f"Ulanishda xatolik: {e}")
