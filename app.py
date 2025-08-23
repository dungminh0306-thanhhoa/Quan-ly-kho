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

# ----------------- HÀM THÊM NHIỀU MÀU SẮC -----------------
def add_colors():
    st.subheader("🎨 Thêm nhiều màu sắc cho mã hàng")
    if not st.session_state.products:
        st.info("Chưa có mã hàng nào. Vui lòng thêm mã hàng trước.")
        return
    
    code = st.selectbox("Chọn mã hàng", list(st.session_state.products.keys()))

    st.markdown("Nhập danh sách màu và số lượng (có thể nhập nhiều dòng).")
    example_df = pd.DataFrame({
        "Tên màu": ["Đỏ", "Xanh", "Đen"],
        "Số lượng": [100, 200, 150]
    })

    edited_df = st.data_editor(example_df, num_rows="dynamic", use_container_width=True)

    if st.button("Lưu các màu vào mã hàng"):
        for _, row in edited_df.iterrows():
            color = str(row["Tên màu"]).strip()
            qty = int(row["Số lượng"]) if not pd.isna(row["Số lượng"]) else 0
            if color != "":
                if color not in st.session_state.products[code]["colors"]:
                    st.session_state.products[code]["colors"][color] = {"qty": qty, "materials": []}
                else:
                    # Nếu màu đã có thì chỉ cập nhật số lượng
                    st.session_state.products[code]["colors"][color]["qty"] = qty
        st.success(f"Đã thêm/cập nhật {len(edited_df)} màu cho mã hàng {code}")

# ----------------- HÀM THÊM NHIỀU NGUYÊN PHỤ LIỆU -----------------
def add_materials():
    st.subheader("🧵 Thêm nhiều nguyên phụ liệu cho màu sắc")
    if not st.session_state.products:
        st.info("Chưa có mã hàng nào. Vui lòng thêm mã hàng trước.")
        return
    
    code = st.selectbox("Chọn mã hàng", list(st.session_state.products.keys()))
    colors = list(st.session_state.products[code]["colors"].keys())
    
    if not colors:
        st.info("Mã hàng này chưa có màu sắc. Vui lòng thêm màu trước.")
        return
    
    color = st.selectbox("Chọn màu sắc", colors)
    
    st.markdown("Nhập danh sách nguyên phụ liệu (có thể nhập nhiều dòng).")
    example_df = pd.DataFrame({
        "Tên nguyên phụ liệu": ["Thun Nylon", "Dây kéo 17cm"],
        "Lượng hàng": [100, 200],
        "Đã có trong kho": [100, 150]
    })

    edited_df = st.data_editor(example_df, num_rows="dynamic", use_container_width=True)

    if st.button("Lưu nguyên phụ liệu"):
        materials = []
        for _, row in edited_df.iterrows():
            name = str(row["Tên nguyên phụ liệu"]).strip()
            qty = int(row["Lượng hàng"]) if not pd.isna(row["Lượng hàng"]) else 0
            stock = int(row["Đã có trong kho"]) if not pd.isna(row["Đã có trong kho"]) else 0
            if name != "":
                status = "ĐỦ" if stock >= qty else "THIẾU"
                materials.append([name, qty, stock, status])
        
        if materials:
            st.session_state.products[code]["colors"][color]["materials"].extend(materials)
            st.success(f"Đã thêm {len(materials)} nguyên phụ liệu cho màu {color} của mã {code}")

# ----------------- HÀM HIỂN THỊ -----------------
def display_data():
    if not st.session_state.products:
        st.info("Chưa có mã hàng nào.")
        return
    
    for code, data in st.session_state.products.items():
        st.subheader(f"📦 Mã hàng: {code}")
        for color, color_data in data.get("colors", {}).items():
            st.markdown(f"🎨 **Màu sắc: {color}** | Số lượng: {color_data.get('qty', 0)}")
            materials = color_data.get("materials", [])
            if materials:
                df = pd.DataFrame(materials, columns=["Tên nguyên phụ liệu", "Lượng hàng", "Đã có trong kho", "Trạng thái"])
                st.dataframe(df, use_container_width=True)
            else:
                st.caption("⚠️ Chưa có nguyên phụ liệu nào cho màu này.")

# ----------------- MAIN APP -----------------
st.title("📋 Quản lý mã hàng, màu sắc & nguyên phụ liệu")

menu = ["Thêm mã hàng", "Thêm nhiều màu sắc", "Thêm nhiều nguyên phụ liệu", "Xem dữ liệu"]
choice = st.sidebar.radio("Chọn chức năng", menu)

if choice == "Thêm mã hàng":
    add_product()
elif choice == "Thêm nhiều màu sắc":
    add_colors()
elif choice == "Thêm nhiều nguyên phụ liệu":
    add_materials()
elif choice == "Xem dữ liệu":
    display_data()
