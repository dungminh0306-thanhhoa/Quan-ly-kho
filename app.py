import streamlit as st
import pandas as pd

# Khởi tạo session state
if "products" not in st.session_state:
    st.session_state.products = {}  # {mã_hàng: {"colors": [], "materials": []}}

# ------------------ HÀM XỬ LÝ ------------------

def add_product(ma_hang):
    if ma_hang not in st.session_state.products:
        st.session_state.products[ma_hang] = {"colors": [], "materials": []}

def delete_product(ma_hang):
    if ma_hang in st.session_state.products:
        del st.session_state.products[ma_hang]

def edit_product(old_ma, new_ma):
    if old_ma in st.session_state.products:
        st.session_state.products[new_ma] = st.session_state.products.pop(old_ma)

def add_color(ma_hang, color, quantity):
    if ma_hang in st.session_state.products:
        st.session_state.products[ma_hang]["colors"].append({"color": color, "quantity": quantity})

def add_material(ma_hang, color, material, material_qty):
    if ma_hang in st.session_state.products:
        st.session_state.products[ma_hang]["materials"].append(
            {"color": color, "material": material, "material_qty": material_qty}
        )

# ------------------ GIAO DIỆN ------------------

st.title("📦 Quản lý Mã Hàng & Nguyên Phụ Liệu")

menu = st.sidebar.radio("Chức năng", ["Thêm mã hàng", "Chỉnh sửa mã hàng", "Xóa mã hàng", "Quản lý màu sắc", "Quản lý nguyên phụ liệu", "Xem dữ liệu"])

# --- Thêm mã hàng ---
if menu == "Thêm mã hàng":
    ma_hang = st.text_input("Nhập mã hàng mới:")
    if st.button("Thêm mã hàng"):
        if ma_hang:
            add_product(ma_hang)
            st.success(f"Đã thêm mã hàng: {ma_hang}")
        else:
            st.warning("Vui lòng nhập mã hàng.")

# --- Chỉnh sửa mã hàng ---
elif menu == "Chỉnh sửa mã hàng":
    if st.session_state.products:
        ma_cu = st.selectbox("Chọn mã hàng cần sửa:", list(st.session_state.products.keys()))
        ma_moi = st.text_input("Nhập mã hàng mới:")
        if st.button("Cập nhật"):
            if ma_moi:
                edit_product(ma_cu, ma_moi)
                st.success(f"Đã đổi {ma_cu} thành {ma_moi}")
    else:
        st.info("Chưa có mã hàng nào.")

# --- Xóa mã hàng ---
elif menu == "Xóa mã hàng":
    if st.session_state.products:
        ma_xoa = st.selectbox("Chọn mã hàng cần xóa:", list(st.session_state.products.keys()))
        if st.button("Xóa"):
            delete_product(ma_xoa)
            st.success(f"Đã xóa mã hàng {ma_xoa}")
    else:
        st.info("Chưa có mã hàng nào.")

# --- Quản lý màu sắc ---
elif menu == "Quản lý màu sắc":
    if st.session_state.products:
        ma_hang = st.selectbox("Chọn mã hàng:", list(st.session_state.products.keys()))
        color = st.text_input("Tên màu:")
        qty = st.number_input("Số lượng sản phẩm:", min_value=1, step=1)
        if st.button("Thêm màu"):
            add_color(ma_hang, color, qty)
            st.success(f"Đã thêm màu {color} ({qty}) cho {ma_hang}")
    else:
        st.info("Chưa có mã hàng nào.")

# --- Quản lý nguyên phụ liệu ---
elif menu == "Quản lý nguyên phụ liệu":
    if st.session_state.products:
        ma_hang = st.selectbox("Chọn mã hàng:", list(st.session_state.products.keys()))
        if st.session_state.products[ma_hang]["colors"]:
            color = st.selectbox("Chọn màu:", [c["color"] for c in st.session_state.products[ma_hang]["colors"]])
            material = st.text_input("Nguyên phụ liệu:")
            material_qty = st.text_input("Số lượng nguyên phụ liệu:")
            if st.button("Thêm nguyên phụ liệu"):
                add_material(ma_hang, color, material, material_qty)
                st.success(f"Đã thêm NPL {material} ({material_qty}) cho {ma_hang} - {color}")
        else:
            st.warning("Mã hàng này chưa có màu nào, hãy thêm màu trước.")
    else:
        st.info("Chưa có mã hàng nào.")

# --- Xem dữ liệu ---
elif menu == "Xem dữ liệu":
    if st.session_state.products:
        for ma, data in st.session_state.products.items():
            st.subheader(f"📌 Mã hàng: {ma}")

            # Bảng màu sắc
            if data["colors"]:
                df_colors = pd.DataFrame(data["colors"])
                st.markdown("### 🎨 Bảng màu sắc")
                st.table(df_colors)
            else:
                st.write("Chưa có màu sắc.")

            # Bảng nguyên phụ liệu
            if data["materials"]:
                df_materials = pd.DataFrame(data["materials"])
                st.markdown("### 🧵 Bảng nguyên phụ liệu")
                st.table(df_materials)
            else:
                st.write("Chưa có nguyên phụ liệu.")
    else:
        st.info("Chưa có dữ liệu để hiển thị.")
