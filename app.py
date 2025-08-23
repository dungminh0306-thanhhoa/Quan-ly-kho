import streamlit as st
import pandas as pd

# ----------------- KHỞI TẠO -----------------
if "products" not in st.session_state:
    st.session_state.products = {}

# ----------------- HÀM THÊM MÃ HÀNG -----------------
def add_product():
    st.subheader("➕ Thêm mã hàng mới")
    code = st.text_input("Nhập mã hàng")
    if st.button("Thêm mã hàng"):
        if code.strip() == "":
            st.warning("Mã hàng không được để trống.")
        elif code in st.session_state.products:
            st.warning("Mã hàng đã tồn tại.")
        else:
            st.session_state.products[code] = {"colors": {}}
            st.success(f"Đã thêm mã hàng: {code}")

# ----------------- HÀM THÊM MÀU SẮC -----------------
def add_color():
    st.subheader("🎨 Thêm màu sắc cho mã hàng")
    if not st.session_state.products:
        st.info("Chưa có mã hàng nào. Vui lòng thêm mã hàng trước.")
        return
    
    code = st.selectbox("Chọn mã hàng", list(st.session_state.products.keys()))
    color = st.text_input("Nhập màu sắc")
    if st.button("Thêm màu"):
        if color.strip() == "":
            st.warning("Tên màu không được để trống.")
        else:
            if color not in st.session_state.products[code]["colors"]:
                st.session_state.products[code]["colors"][color] = []
                st.success(f"Đã thêm màu {color} cho mã hàng {code}")
            else:
                st.warning("Màu này đã tồn tại trong mã hàng.")

# ----------------- HÀM THÊM NGUYÊN PHỤ LIỆU -----------------
def add_material():
    st.subheader("🧵 Thêm nguyên phụ liệu cho màu sắc")
    if not st.session_state.products:
        st.info("Chưa có mã hàng nào. Vui lòng thêm mã hàng trước.")
        return
    
    code = st.selectbox("Chọn mã hàng", list(st.session_state.products.keys()))
    colors = list(st.session_state.products[code]["colors"].keys())
    
    if not colors:
        st.info("Mã hàng này chưa có màu sắc. Vui lòng thêm màu trước.")
        return
    
    color = st.selectbox("Chọn màu sắc", colors)
    
    with st.form(key="add_material_form"):
        name = st.text_input("Tên nguyên phụ liệu")
        qty = st.number_input("Lượng hàng", min_value=0, step=1)
        stock = st.number_input("Đã có trong kho", min_value=0, step=1)
        
        submitted = st.form_submit_button("Thêm nguyên phụ liệu")
        if submitted:
            if name.strip() == "":
                st.warning("Tên nguyên phụ liệu không được để trống.")
            else:
                status = "ĐỦ" if stock >= qty else "THIẾU"
                st.session_state.products[code]["colors"][color].append(
                    [name, qty, stock, status]
                )
                st.success(f"Đã thêm {name} cho màu {color} của mã {code}")

# ----------------- HÀM HIỂN THỊ -----------------
def display_data():
    if not st.session_state.products:
        st.info("Chưa có mã hàng nào.")
        return
    
    for code, data in st.session_state.products.items():
        st.subheader(f"📦 Mã hàng: {code}")
        for color, materials in data.get("colors", {}).items():
            st.markdown(f"🎨 **Màu sắc: {color}**")
            if materials:
                df = pd.DataFrame(materials, columns=["Tên nguyên phụ liệu", "Lượng hàng", "Đã có trong kho", "Trạng thái"])
                st.dataframe(df, use_container_width=True)
            else:
                st.caption("⚠️ Chưa có nguyên phụ liệu nào cho màu này.")

# ----------------- HÀM XÓA -----------------
def delete_data():
    st.subheader("🗑️ Xóa dữ liệu")

    if not st.session_state.products:
        st.info("Chưa có dữ liệu để xóa.")
        return

    options = ["Xóa mã hàng", "Xóa màu sắc trong mã hàng", "Xóa nguyên phụ liệu trong màu"]
    action = st.radio("Chọn loại xóa", options)

    # XÓA MÃ HÀNG
    if action == "Xóa mã hàng":
        code = st.selectbox("Chọn mã hàng cần xóa", list(st.session_state.products.keys()))
        if st.button("Xóa mã hàng"):
            del st.session_state.products[code]
            st.success(f"Đã xóa mã hàng {code}")

    # XÓA MÀU
    elif action == "Xóa màu sắc trong mã hàng":
        code = st.selectbox("Chọn mã hàng", list(st.session_state.products.keys()))
        colors = list(st.session_state.products[code]["colors"].keys())
        if not colors:
            st.info("Mã hàng này chưa có màu sắc nào.")
            return
        color = st.selectbox("Chọn màu sắc cần xóa", colors)
        if st.button("Xóa màu sắc"):
            del st.session_state.products[code]["colors"][color]
            st.success(f"Đã xóa màu {color} trong mã hàng {code}")

    # XÓA NGUYÊN PHỤ LIỆU
    elif action == "Xóa nguyên phụ liệu trong màu":
        code = st.selectbox("Chọn mã hàng", list(st.session_state.products.keys()))
        colors = list(st.session_state.products[code]["colors"].keys())
        if not colors:
            st.info("Mã hàng này chưa có màu sắc nào.")
            return
        color = st.selectbox("Chọn màu sắc", colors)
        materials = st.session_state.products[code]["colors"][color]
        if not materials:
            st.info("Màu này chưa có nguyên phụ liệu nào.")
            return
        material_names = [m[0] for m in materials]
        selected_material = st.selectbox("Chọn nguyên phụ liệu cần xóa", material_names)
        if st.button("Xóa nguyên phụ liệu"):
            st.session_state.products[code]["colors"][color] = [m for m in materials if m[0] != selected_material]
            st.success(f"Đã xóa nguyên phụ liệu {selected_material} trong màu {color} của mã {code}")

# ----------------- MAIN APP -----------------
st.title("📋 Quản lý mã hàng, màu sắc & nguyên phụ liệu")

menu = ["Thêm mã hàng", "Thêm màu sắc", "Thêm nguyên phụ liệu", "Xem dữ liệu", "Xóa dữ liệu"]
choice = st.sidebar.radio("Chọn chức năng", menu)

if choice == "Thêm mã hàng":
    add_product()
elif choice == "Thêm màu sắc":
    add_color()
elif choice == "Thêm nguyên phụ liệu":
    add_material()
elif choice == "Xem dữ liệu":
    display_data()
elif choice == "Xóa dữ liệu":
    delete_data()
