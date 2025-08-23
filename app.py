import streamlit as st
import pandas as pd

# =====================
# Khởi tạo dữ liệu
# =====================
if "products" not in st.session_state:
    st.session_state.products = {}

if "new_colors" not in st.session_state:
    st.session_state.new_colors = []

if "new_materials" not in st.session_state:
    st.session_state.new_materials = []


# =====================
# Hàm hiển thị bảng nhập liệu màu sắc
# =====================
def color_table():
    st.subheader("Bảng màu sắc")
    df = pd.DataFrame(st.session_state.new_colors, columns=["Màu sắc", "Số lượng"])
    st.dataframe(df, use_container_width=True)

    with st.form("add_color_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            color = st.text_input("Nhập màu sắc")
        with col2:
            qty = st.number_input("Số lượng", min_value=0, step=1)

        submitted = st.form_submit_button("➕ Thêm màu sắc")
        if submitted and color:
            st.session_state.new_colors.append([color, qty])


# =====================
# Hàm hiển thị bảng nhập liệu nguyên phụ liệu
# =====================
def material_table():
    st.subheader("Bảng nguyên phụ liệu")
    df = pd.DataFrame(
        st.session_state.new_materials,
        columns=["Màu sắc", "Tên nguyên phụ liệu", "Lượng hàng", "Đã có trong kho", "Trạng thái"],
    )
    st.dataframe(df, use_container_width=True)

    with st.form("add_material_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            color = st.selectbox("Chọn màu", [c[0] for c in st.session_state.new_colors] or ["(Chưa có màu)"])
        with col2:
            material = st.text_input("Tên nguyên phụ liệu")

        col3, col4, col5 = st.columns(3)
        with col3:
            qty = st.number_input("Lượng hàng", min_value=0, step=1)
        with col4:
            stock = st.number_input("Đã có trong kho", min_value=0, step=1)
        with col5:
            status = st.selectbox("Trạng thái", ["ĐỦ", "THIẾU"])

        submitted = st.form_submit_button("➕ Thêm nguyên phụ liệu")
        if submitted and material:
            st.session_state.new_materials.append([color, material, qty, stock, status])


# =====================
# Menu chức năng
# =====================
menu = st.sidebar.radio("Chức năng", ["Xem danh sách", "Thêm mã hàng", "Chỉnh sửa mã hàng", "Xóa mã hàng"])

# =====================
# Xem danh sách
# =====================
if menu == "Xem danh sách":
    st.title("📋 Danh sách mã hàng")

    if not st.session_state.products:
        st.info("Chưa có mã hàng nào.")
    else:
        for code, data in st.session_state.products.items():
            st.subheader(f"➡️ {code} - {data['name']}")

            st.markdown("**Màu sắc:**")
            st.dataframe(pd.DataFrame(data["colors"], columns=["Màu sắc", "Số lượng"]), use_container_width=True)

            st.markdown("**Nguyên phụ liệu:**")
            st.dataframe(
                pd.DataFrame(
                    data["materials"],
                    columns=["Màu sắc", "Tên nguyên phụ liệu", "Lượng hàng", "Đã có trong kho", "Trạng thái"],
                ),
                use_container_width=True,
            )

# =====================
# Thêm mã hàng
# =====================
elif menu == "Thêm mã hàng":
    st.title("➕ Thêm mã hàng mới")

    code = st.text_input("Mã hàng")
    name = st.text_input("Tên sản phẩm")

    # Hiển thị bảng nhập
    color_table()
    material_table()

    if st.button("💾 Lưu mã hàng"):
        if code:
            st.session_state.products[code] = {
                "name": name,
                "colors": st.session_state.new_colors.copy(),
                "materials": st.session_state.new_materials.copy(),
            }
            st.success(f"Đã lưu mã hàng {code}")
            st.session_state.new_colors = []
            st.session_state.new_materials = []
        else:
            st.error("Vui lòng nhập Mã hàng.")

# =====================
# Chỉnh sửa mã hàng
# =====================
elif menu == "Chỉnh sửa mã hàng":
    st.title("✏️ Chỉnh sửa mã hàng")
    if not st.session_state.products:
        st.info("Chưa có mã hàng để chỉnh sửa.")
    else:
        code_to_edit = st.selectbox("Chọn mã hàng để chỉnh sửa", list(st.session_state.products.keys()))

        product = st.session_state.products[code_to_edit]

        name = st.text_input("Tên sản phẩm", value=product["name"])

        # Nếu lần đầu chỉnh sửa thì load dữ liệu vào new_colors/new_materials
        if not st.session_state.new_colors and not st.session_state.new_materials:
            st.session_state.new_colors = product["colors"].copy()
            st.session_state.new_materials = product["materials"].copy()

        # Hiển thị bảng nhập
        color_table()
        material_table()

        if st.button("💾 Lưu chỉnh sửa"):
            st.session_state.products[code_to_edit] = {
                "name": name,
                "colors": st.session_state.new_colors.copy(),
                "materials": st.session_state.new_materials.copy(),
            }
            st.success(f"Đã cập nhật mã hàng {code_to_edit}")
            st.session_state.new_colors = []
            st.session_state.new_materials = []

# =====================
# Xóa mã hàng
# =====================
elif menu == "Xóa mã hàng":
    st.title("🗑️ Xóa mã hàng")
    if not st.session_state.products:
        st.info("Chưa có mã hàng để xóa.")
    else:
        code_to_delete = st.selectbox("Chọn mã hàng để xóa", list(st.session_state.products.keys()))
        if st.button("Xóa"):
            del st.session_state.products[code_to_delete]
            st.success(f"Đã xóa mã hàng {code_to_delete}")
