import streamlit as st
import pandas as pd

# ==============================
# Khởi tạo dữ liệu
# ==============================
if "data" not in st.session_state:
    st.session_state.data = {}  # Lưu dữ liệu theo mã hàng
if "nguyen_lieu" not in st.session_state:
    st.session_state.nguyen_lieu = {}  # Lưu nguyên phụ liệu riêng

# ==============================
# Hàm lưu dữ liệu
# ==============================
def save_data(ma_hang, colors, materials):
    if ma_hang in st.session_state.data:
        # Nếu mã hàng đã có -> chỉ cập nhật thêm màu, giữ nguyên nguyên liệu cũ
        st.session_state.data[ma_hang].extend(colors)
        if ma_hang not in st.session_state.nguyen_lieu:
            st.session_state.nguyen_lieu[ma_hang] = materials
    else:
        st.session_state.data[ma_hang] = colors
        st.session_state.nguyen_lieu[ma_hang] = materials

# ==============================
# Giao diện thêm mã hàng
# ==============================
st.header("Thêm mã hàng mới")

ma_hang = st.text_input("Nhập mã hàng")
so_dong = st.number_input("Số dòng muốn nhập", min_value=1, value=3)

st.subheader("Bảng 1: Màu sắc + Số lượng")
colors = []
for i in range(int(so_dong)):
    col1, col2 = st.columns(2)
    with col1:
        mau = st.text_input(f"Màu sắc {i+1}", key=f"mau_{i}")
    with col2:
        sl = st.number_input(f"Số lượng {i+1}", min_value=0, value=0, key=f"sl_{i}")
    if mau:  # chỉ thêm khi có nhập màu
        colors.append({"Màu sắc": mau, "Số lượng": sl})

st.subheader("Bảng 2: Nguyên phụ liệu")
materials = []
for i in range(int(so_dong)):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        npl = st.text_input(f"Nguyên liệu {i+1}", key=f"npl_{i}")
    with col2:
        donvi = st.text_input(f"Đơn vị {i+1}", key=f"dv_{i}")
    with col3:
        dinhmuc = st.number_input(f"Định mức {i+1}", min_value=0.0, value=0.0, key=f"dm_{i}")
    with col4:
        ncc = st.text_input(f"Nhà cung cấp {i+1}", key=f"ncc_{i}")
    if npl:  # chỉ thêm khi có nhập nguyên liệu
        materials.append({
            "Nguyên liệu": npl,
            "Đơn vị": donvi,
            "Định mức": dinhmuc,
            "Nhà cung cấp": ncc
        })

if st.button("Lưu dữ liệu"):
    if ma_hang.strip() != "":
        save_data(ma_hang, colors, materials)
        st.success(f"Đã lưu mã hàng {ma_hang}")
    else:
        st.warning("Vui lòng nhập mã hàng!")

# ==============================
# Hiển thị dữ liệu đã lưu
# ==============================
st.header("Danh sách mã hàng đã lưu")

for ma, colors in st.session_state.data.items():
    st.write(f"### Mã hàng: {ma}")
    
    st.write("**Màu sắc (chỉnh sửa được):**")
    edited_colors = st.data_editor(
        pd.DataFrame(colors),
        num_rows="dynamic",
        key=f"edit_colors_{ma}"
    )

    if st.button(f"Cập nhật màu sắc {ma}"):
        st.session_state.data[ma] = edited_colors.to_dict("records")
        st.success(f"Đã cập nhật màu sắc cho {ma}")

    if ma in st.session_state.nguyen_lieu:
        st.write("**Nguyên phụ liệu (chỉnh sửa được):**")
        
        edited_materials = st.data_editor(
            pd.DataFrame(st.session_state.nguyen_lieu[ma]),
            num_rows="dynamic",
            key=f"edit_materials_{ma}"
        )

        if st.button(f"Cập nhật nguyên phụ liệu {ma}"):
            st.session_state.nguyen_lieu[ma] = edited_materials.to_dict("records")
            st.success(f"Đã cập nhật nguyên phụ liệu cho {ma}")
