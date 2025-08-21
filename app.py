import streamlit as st
import pandas as pd
import re

# --- Khởi tạo dữ liệu ---
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Mã hàng", "Tên hàng", "Tồn kho"])

if "nguyen_phu_lieu" not in st.session_state:
    # Lưu nguyên phụ liệu theo mã gốc (vd: AR01)
    st.session_state.nguyen_phu_lieu = {}

# Hàm lấy mã gốc (vd: "AR01 (215)" -> "AR01")
def get_base_code(code):
    match = re.match(r"([A-Za-z0-9]+)", code)
    return match.group(1) if match else code

# --- Sidebar Menu ---
menu = st.sidebar.radio("Chọn chức năng", [
    "Thêm mã hàng", "Cập nhật mã hàng", "Xóa mã hàng", 
    "Nhập/Xuất kho", "Nguyên phụ liệu", "Danh sách mã hàng"
])

# --- CREATE: Thêm mã hàng ---
if menu == "Thêm mã hàng":
    st.subheader("➕ Thêm mã hàng mới")
    ma_hang = st.text_input("Mã hàng (vd: AR01 (215))")
    ten_hang = st.text_input("Tên hàng")
    ton_kho = st.number_input("Số lượng nhập kho", min_value=0, step=1)

    if st.button("Thêm"):
        if ma_hang in st.session_state.data["Mã hàng"].values:
            st.error("❌ Mã hàng đã tồn tại!")
        else:
            new_row = pd.DataFrame([[ma_hang, ten_hang, ton_kho]], columns=st.session_state.data.columns)
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)

            # Kế thừa nguyên phụ liệu từ mã gốc
            base_code = get_base_code(ma_hang)
            if base_code in st.session_state.nguyen_phu_lieu:
                st.success(f"✅ Mã hàng {ma_hang} đã được thêm và kế thừa nguyên phụ liệu từ {base_code}")
            else:
                st.success("✅ Thêm thành công!")

# --- UPDATE: Cập nhật mã hàng ---
elif menu == "Cập nhật mã hàng":
    st.subheader("✏️ Cập nhật thông tin mã hàng")
    if not st.session_state.data.empty:
        ma_hang = st.selectbox("Chọn mã hàng cần sửa", st.session_state.data["Mã hàng"].unique())
        row = st.session_state.data[st.session_state.data["Mã hàng"] == ma_hang].iloc[0]
        new_ten_hang = st.text_input("Tên hàng", value=row["Tên hàng"])
        new_ton_kho = st.number_input("Tồn kho", min_value=0, step=1, value=int(row["Tồn kho"]))

        if st.button("Cập nhật"):
            st.session_state.data.loc[st.session_state.data["Mã hàng"] == ma_hang, ["Tên hàng", "Tồn kho"]] = [new_ten_hang, new_ton_kho]
            st.success("✅ Cập nhật thành công!")

# --- DELETE: Xóa mã hàng ---
elif menu == "Xóa mã hàng":
    st.subheader("🗑️ Xóa mã hàng")
    if not st.session_state.data.empty:
        ma_hang = st.selectbox("Chọn mã hàng cần xóa", st.session_state.data["Mã hàng"].unique())
        if st.button("Xóa"):
            st.session_state.data = st.session_state.data[st.session_state.data["Mã hàng"] != ma_hang]
            st.success("✅ Đã xóa thành công!")

# --- INVENTORY: Nhập/Xuất kho ---
elif menu == "Nhập/Xuất kho":
    st.subheader("📦 Nhập/Xuất kho")
    if not st.session_state.data.empty:
        ma_hang = st.selectbox("Chọn mã hàng", st.session_state.data["Mã hàng"].unique())
        so_luong = st.number_input("Số lượng", min_value=1, step=1)
        action = st.radio("Hành động", ["Nhập kho", "Xuất kho"])

        if st.button("Thực hiện"):
            if action == "Nhập kho":
                st.session_state.data.loc[st.session_state.data["Mã hàng"] == ma_hang, "Tồn kho"] += so_luong
                st.success(f"✅ Đã nhập thêm {so_luong} sản phẩm vào {ma_hang}")
            else:
                current = int(st.session_state.data.loc[st.session_state.data["Mã hàng"] == ma_hang, "Tồn kho"])
                if so_luong > current:
                    st.error("❌ Không đủ hàng để xuất!")
                else:
                    st.session_state.data.loc[st.session_state.data["Mã hàng"] == ma_hang, "Tồn kho"] -= so_luong
                    st.success(f"✅ Đã xuất {so_luong} sản phẩm từ {ma_hang}")

# --- MATERIALS: Nguyên phụ liệu ---
elif menu == "Nguyên phụ liệu":
    st.subheader("🧵 Quản lý nguyên phụ liệu")
    if not st.session_state.data.empty:
        ma_hang = st.selectbox("Chọn mã hàng", st.session_state.data["Mã hàng"].unique())
        base_code = get_base_code(ma_hang)

        # Hiển thị danh sách NPL
        st.write(f"**Nguyên phụ liệu của {base_code}:**")
        npl_list = st.session_state.nguyen_phu_lieu.get(base_code, [])
        st.table(pd.DataFrame(npl_list, columns=["Tên NPL", "Số lượng"])) if npl_list else st.info("Chưa có nguyên phụ liệu.")

        # Form nhập NPL
        ten_npl = st.text_input("Tên nguyên phụ liệu")
        so_luong_npl = st.number_input("Số lượng NPL", min_value=1, step=1)

        if st.button("Thêm NPL"):
            if base_code not in st.session_state.nguyen_phu_lieu:
                st.session_state.nguyen_phu_lieu[base_code] = []
            st.session_state.nguyen_phu_lieu[base_code].append([ten_npl, so_luong_npl])
            st.success(f"✅ Đã thêm nguyên phụ liệu cho {base_code}")

# --- READ: Danh sách ---
elif menu == "Danh sách mã hàng":
    st.subheader("📋 Danh sách mã hàng & tồn kho")
    st.dataframe(st.session_state.data, use_container_width=True)

    # Tìm kiếm
    keyword = st.text_input("🔍 Nhập mã hàng hoặc tên hàng cần tìm")
    if keyword:
        df_view = st.session_state.data[
            st.session_state.data.apply(lambda row: keyword.lower() in str(row.values).lower(), axis=1)
        ]
        st.dataframe(df_view, use_container_width=True)
