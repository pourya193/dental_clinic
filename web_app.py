
import streamlit as st
import json
import pandas as pd
import os

DATA_FILE = "patients.json"

def load_patients():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = f.read().strip()
        if not data:
            return []
        return json.loads(data)

def save_patients(patients):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(patients, f, ensure_ascii=False, indent=4)

st.set_page_config(page_title="مدیریت مطب تحت وب", layout="centered")
st.title("🦷 مدیریت مطب دندان‌پزشکی (نسخه وب)")

menu = st.sidebar.radio("منو", ["📋 لیست بیماران", "➕ افزودن بیمار جدید"])

patients = load_patients()

if menu == "📋 لیست بیماران":
    if patients:
        df = pd.DataFrame(patients)
        st.dataframe(df)
    else:
        st.info("هیچ بیماری ثبت نشده است.")

if menu == "➕ افزودن بیمار جدید":
    with st.form("patient_form"):
        col1, col2 = st.columns(2)
        with col1:
            fname = st.text_input("نام")
            phone = st.text_input("شماره تلفن")
            national_id = st.text_input("کد ملی")
        with col2:
            lname = st.text_input("نام خانوادگی")
            insurance = st.selectbox("نوع بیمه", ["تأمین اجتماعی", "سلامت", "خدمات درمانی", "آزاد", "سایر"])
            service = st.text_input("نوع خدمت")

        submitted = st.form_submit_button("ثبت بیمار")
        if submitted:
            new_patient = {
                "شماره پرونده": str(100 + len(patients)),
                "نام": fname,
                "نام خانوادگی": lname,
                "کد ملی": national_id,
                "شماره تلفن": phone,
                "شماره بیمه": "",
                "نوع بیمه": insurance,
                "نوع خدمت": service,
                "خدمات درمانی": {}
            }
            patients.append(new_patient)
            save_patients(patients)
            st.success("✅ بیمار جدید ثبت شد.")
