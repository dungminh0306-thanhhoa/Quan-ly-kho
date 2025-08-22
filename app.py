import streamlit as st
import pandas as pd
import os

DATA_FILE = "data.csv"

# Khởi tạo file nếu chưa có
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Mã hàng", "Màu sắc", "Số lượng", "Nguyên liệu"])
    df_init.to_csv(DATA_FILE, index=False)

# Load dữ liệu
def load_data():
    return pd.read_csv(DATA_FILE)

# Lưu dữ liệu
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# Menu
st.sidebar.title("📋 Menu")
menu = st.sidebar.radio("Chọn chức năng:", [
    "Xem danh sách mã hàng",
    "Thêm mã hàng mới",
    "Chỉnh sửa mã hàng",
    "Xóa mã hàng"
])

# ---------------------------
# Xem danh sách mã hàng
# ---------------------------
if menu == "Xem danh sách mã hàng":
    st.title("📑 Danh sách mã hàng")
    df = load_data()
    if df.empty:
        st.info("Chưa có dữ liệu.")
    else:
        st.dataframe(df)

# ---------------------------
# Thêm mã hàng mới
# ---------------------------
elif menu == "Thêm mã hàng mới":
    st.title("➕ Thêm mã hàng mới")
    df = load_data()

    ma_hang = st.text_input("Nhập mã hàng mới:")

    if ma_hang:
        so_dong = st.number_input("Chọn số dòng (số màu):", min_value=1, step=1, value=1)

        # Tạo bảng nhập dữ liệu
        new_data = []
        st.write("👉 Nhập thông tin chi tiết:")
        for i in range(so_dong):
            col1, col2, col3 = st.columns(3)
            with col1:
                mau = st.text_input(f"Màu sắc dòng {i+1}", key=f"mau_{i}")
            with col2:
                so_luong = st.number_input(f"Số lượng dòng {i+1}", min_value=0, step=1, key=f"soluong_{i}")
            with col3:
                nguyen_lieu = st.text_input(f"Nguyên liệu dòng {i+1}", key=f"nl_{i}")
            new_data.append([ma_hang, mau, so_luong, nguyen_lieu])

        if st.button("💾 Lưu mã hàng"):
            # Nếu mã hàng đã tồn tại, copy nguyên liệu
            if ma_hang in df["Mã hàng"].values:
                st.warning("Mã hàng đã tồn tại! Sẽ dùng nguyên liệu từ mã hàng trước.")
                old_df = df[df["Mã hàng"] == ma_hang]
                for row in new_data:
                    row[3] = old_df.iloc[0]["Nguyên liệu"]
            new_df = pd.DataFrame(new_data, columns=["Mã hàng", "Màu sắc", "Số lượng", "Nguyên liệu"])
            df = pd.concat([df, new_df], ignore_index=True)
            save_data(df)
            st.success(f"Đã thêm mã hàng {ma_hang} thành công!")

# ---------------------------
# Chỉnh sửa mã hàng
# ---------------------------
elif menu == "Chỉnh sửa mã hàng":
    st.title("✏️ Chỉnh sửa mã hàng")
    df = load_data()
    if df.empty:
        st.info("Chưa có dữ liệu.")
    else:
        ma_hang_list = df["Mã hàng"].unique().tolist()
        ma_hang = st.selectbox("Chọn mã hàng cần sửa:", ma_hang_list)
        df_edit = df[df["Mã hàng"] == ma_hang].copy()
        st.dataframe(df_edit)

        edited_df = st.data_editor(df_edit, num_rows="dynamic")

        if st.button("💾 Lưu chỉnh sửa"):
            df = df[df["Mã hàng"] != ma_hang]
            df = pd.concat([df, edited_df], ignore_index=True)
            save_data(df)
            st.success("Đã lưu chỉnh sửa.")

# ---------------------------
# Xóa mã hàng
# ---------------------------
elif menu == "Xóa mã hàng":
    st.title("🗑️ Xóa mã hàng")
    df = load_data()
    if df.empty:
        st.info("Chưa có dữ liệu.")
    else:
        ma_hang_list = df["Mã hàng"].unique().tolist()
        ma_hang = st.selectbox("Chọn mã hàng cần xóa:", ma_hang_list)

        if st.button("❌ Xóa"):
            df = df[df["Mã hàng"] != ma_hang]
            save_data(df)
            st.success(f"Đã xóa mã hàng {ma_hang}")
