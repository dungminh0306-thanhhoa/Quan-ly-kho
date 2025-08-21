import streamlit as st
import pandas as pd

# --- Khởi tạo dữ liệu ban đầu ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame({
        "Mã hàng": ["A01", "A02", "A03"],
        "Tên hàng": ["Áo phao", "Quần jean", "Áo sơ mi"],
        "Tồn kho": [100, 200, 150]
    })

st.title("📦 Quản lý mã hàng (CRUD + Tìm kiếm + Tồn kho)")

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
st.subheader("📋 Danh sách mã hàng & tồn kho")
st.dataframe(df_view, use_container_width=True)

# --- CREATE: Thêm mã hàng mới ---
st.subheader("➕ Thêm mã hàng mới")
with st.form("add_form", clear_on_submit=True):
    new_code = st.text_input("Mã hàng")
    new_name = st.text_input("Tên hàng")
    new_qty = st.number_input("Tồn kho ban đầu", min_value=0, value=0)
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
    edit_qty = st.number_input("Số lượng tồn mới", min_value=0, value=int(st.session_state.data.at[idx, "Tồn kho"]))

    if st.button("Cập nhật"):
        st.session_state.data.at[idx, "Mã hàng"] = edit_code
        st.session_state.data.at[idx, "Tên hàng"] = edit_name
        st.session_state.data.at[idx, "Tồn kho"] = edit_qty
        st.success(f"✅ Đã cập nhật {selected} thành {edit_code}")

# --- DELETE: Xóa mã hàng ---
st.subheader("🗑️ Xóa mã hàng")
if len(st.session_state.data) > 0:
    del_selected = st.selectbox("Chọn mã hàng cần xóa", st.session_state.data["Mã hàng"], key="delete_select")
    if st.button("Xóa"):
        st.session_state.data = st.session_state.data[st.session_state.data["Mã hàng"] != del_selected].reset_index(drop=True)
        st.success(f"🗑️ Đã xóa {del_selected}")

# --- STOCK MANAGEMENT: Nhập / Xuất kho ---
st.subheader("📊 Quản lý tồn kho")
if len(st.session_state.data) > 0:
    stock_selected = st.selectbox("Chọn mã hàng để nhập/xuất kho", st.session_state.data["Mã hàng"], key="stock_select")
    stock_idx = st.session_state.data.index[st.session_state.data["Mã hàng"] == stock_selected][0]

    col1, col2 = st.columns(2)

    with col1:
        nhap_sl = st.number_input("Số lượng nhập kho", min_value=0, value=0, key="nhap")
        if st.button("Nhập kho"):
            st.session_state.data.at[stock_idx, "Tồn kho"] += nhap_sl
            st.success(f"✅ Đã nhập {nhap_sl} vào {stock_selected}")

    with col2:
        xuat_sl = st.number_input("Số lượng xuất kho", min_value=0, value=0, key="xuat")
        if st.button("Xuất kho"):
            if st.session_state.data.at[stock_idx, "Tồn kho"] >= xuat_sl:
                st.session_state.data.at[stock_idx, "Tồn kho"] -= xuat_sl
                st.success(f"✅ Đã xuất {xuat_sl} từ {stock_selected}")
            else:
                st.error("⚠️ Không đủ tồn kho để xuất!")


