import streamlit as st
import pandas as pd

# --- Khởi tạo dữ liệu ban đầu ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Mã hàng": ["A01", "A02", "A03"],
        "Tên hàng": ["Áo phao", "Quần jean", "Áo sơ mi"],
        "Số lượng": [100, 200, 150]
    })

st.title("📦 Quản lý mã hàng (CRUD + Tìm kiếm)")

# --- SEARCH / FILTER ---
st.subheader("🔍 Tìm kiếm / Lọc")
keyword = st.text_input("Nhập mã hàng hoặc tên hàng cần tìm")

if keyword:
    df_view = st.session_state.data[
        st.session_state.data.apply(lambda row: keyword.lower() in str(row.values).lower(), axis=1)
    ]
else:
    df_view = st.session_state.data

# --- READ: Hiển thị bảng ---
st.subheader("📋 Danh sách mã hàng")
st.dataframe(df_view, use_container_width=True)

# --- CREATE: Thêm mã hàng mới ---
st.subheader("➕ Thêm mã hàng mới")
with st.form("add_form", clear_on_submit=True):
    new_code = st.text_input("Mã hàng")
    new_name = st.text_input("Tên hàng")
    new_qty = st.number_input("Số lượng", min_value=0, value=0)
    submitted = st.form_submit_button("Thêm")
    if submitted:
        if new_code in st.session_state.data["Mã hàng"].values:
            st.warning("⚠️ Mã hàng đã tồn tại!")
        else:
            st.session_state.data.loc[len(st.session_state.data)] = [new_code, new_name, new_qty]
            st.success(f"✅ Đã thêm {new_code} - {new_name}")

# --- UPDATE: Sửa mã hàng ---
st.subheader("✏️ Sửa mã hàng")
if len(st.session_state.data) > 0:
    selected = st.selectbox("Chọn mã hàng cần sửa", st.session_state.data["Mã hàng"])
    idx = st.session_state.data.index[st.session_state.data["Mã hàng"] == selected][0]

    edit_code = st.text_input("Mã hàng mới", value=st.session_state.data.at[idx, "Mã hàng"])
    edit_name = st.text_input("Tên hàng mới", value=st.session_state.data.at[idx, "Tên hàng"])
    edit_qty = st.number_input("Số lượng mới", min_value=0, value=int(st.session_state.data.at[idx, "Số lượng"]))

    if st.button("Cập nhật"):
        st.session_state.data.at[idx, "Mã hàng"] = edit_code
        st.session_state.data.at[idx, "Tên hàng"] = edit_name
        st.session_state.data.at[idx, "Số lượng"] = edit_qty
        st.success(f"✅ Đã cập nhật {selected} thành {edit_code}")

# --- DELETE: Xóa mã hàng ---
st.subheader("🗑️ Xóa mã hàng")
if len(st.session_state.data) > 0:
    del_selected = st.selectbox("Chọn mã hàng cần xóa", st.session_state.data["Mã hàng"], key="delete_select")
    if st.button("Xóa"):
        st.session_state.data = st.session_state.data[st.session_state.data["Mã hàng"] != del_selected].reset_index(drop=True)
        st.success(f"🗑️ Đã xóa {del_selected}")
