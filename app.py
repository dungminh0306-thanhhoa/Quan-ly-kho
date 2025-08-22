import streamlit as st
import pandas as pd
import os

FILE_PATH = "data.csv"

# Khởi tạo file CSV nếu chưa có
if not os.path.exists(FILE_PATH):
    df_init = pd.DataFrame(columns=["Mã hàng", "Màu sắc", "Số lượng", "Nguyên liệu"])
    df_init.to_csv(FILE_PATH, index=False)

# Load dữ liệu
df = pd.read_csv(FILE_PATH)

st.title("Quản lý mã hàng & màu sắc")

# Hiển thị dữ liệu hiện có
st.subheader("📋 Danh sách hiện tại")
st.dataframe(df)

st.subheader("➕ Thêm mã hàng mới")

# Số dòng mặc định nhập liệu
if "new_rows" not in st.session_state:
    st.session_state["new_rows"] = 5

# Tạo bảng nhập liệu rỗng
new_data = pd.DataFrame(
    {
        "Mã hàng": ["" for _ in range(st.session_state["new_rows"])],
        "Màu sắc": ["" for _ in range(st.session_state["new_rows"])],
        "Số lượng": [0 for _ in range(st.session_state["new_rows"])],
        "Nguyên liệu": ["" for _ in range(st.session_state["new_rows"])]
    }
)

edited_data = st.data_editor(new_data, num_rows="dynamic", use_container_width=True)

# Nút thêm dòng
if st.button("➕ Thêm dòng trống"):
    st.session_state["new_rows"] += 1
    st.experimental_rerun()

# Xử lý lưu
if st.button("💾 Lưu mã hàng"):
    updated_rows = []

    for _, row in edited_data.iterrows():
        if row["Mã hàng"] == "" or row["Màu sắc"] == "":
            continue  # bỏ qua dòng trống

        ma_hang = row["Mã hàng"]

        # Nếu mã hàng đã có, lấy nguyên phụ liệu cũ
        if ma_hang in df["Mã hàng"].values:
            nguyen_lieu_cu = df[df["Mã hàng"] == ma_hang]["Nguyên liệu"].tolist()
            # Nếu cột "Nguyên liệu" chưa nhập thì tự điền từ dữ liệu cũ (theo thứ tự vòng lặp)
            if row["Nguyên liệu"] == "":
                row["Nguyên liệu"] = nguyen_lieu_cu[len(updated_rows) % len(nguyen_lieu_cu)]
        
        updated_rows.append(row)

    if updated_rows:
        df = pd.concat([df, pd.DataFrame(updated_rows)], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("Đã lưu thành công!")
        st.dataframe(df)
