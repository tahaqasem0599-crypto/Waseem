import streamlit as st
import pandas as pd

st.title("📊 نظام المبيعات")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["المنتج", "السعر"])

name = st.text_input("اسم المنتج:")
price = st.number_input("السعر:", min_value=1)

if st.button("إضافة"):
    if name:
        new_row = pd.DataFrame([{"المنتج": name, "السعر": price}])
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success("تم الحفظ!")

st.dataframe(st.session_state.df, use_container_width=True)
