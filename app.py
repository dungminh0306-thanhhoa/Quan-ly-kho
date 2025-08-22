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

st.title("📦 Quản lý mã hàng & màu sắc")

# ------------------------
# 1. XEM DANH SÁCH
# ------------------------
st.subheader("📋 Danh sách hiện tại")
search = st.text_input("🔍 Tìm kiếm theo mã hàng hoặc nguyên liệu")
if search:
    df_filtered = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_string(), axis=1)]
else:
    df_filtered = df
st.dataframe(df_filtered, use_container_width=True)

# ------------------------
# 2. THÊM MÃ HÀNG
# ------------------------
st.subheader("➕ Thêm mã hàng mới")

if "new_rows" not in st.session_state:
    st.session_state["new_rows"] = 5

new_data = pd.DataFrame(
    {
        "Mã hàng": ["" for _ in range(st.session_state["new_rows"])],
        "Màu sắc": ["" for _ in range(st.session_state["new_rows"])],
        "Số lượng": [0 for _ in range(st.session_state["new_rows"])],
        "Nguyên liệu": ["" for _ in range(st.session_state["new_rows"])]
    }
)

edited_data = st.data_editor(new_data, num_rows="dynamic", use_container_width=True)

if st.button("➕ Thêm dòng trống"):
    st.session_state["new_rows"] += 1
    st.experimental_rerun()

if st.button("💾 Lưu mã hàng"):
    updated_rows = []
    for _, row in edited_data.iterrows():
        if row["Mã hàng"] == "" or row["Màu sắc"] == "":
            continue
        ma_hang = row["Mã hàng"]

        # Nếu mã hàng đã có thì lấy nguyên liệu cũ
        if ma_hang in df["Mã hàng"].values and row["Nguyên liệu"] == "":
            nguyen_lieu_cu = df[df["Mã hàng"] == ma_hang]["Nguyên liệu"].tolist()
            row["Nguyên liệu"] = nguyen_lieu_cu[len(updated_rows) % len(nguyen_lieu_cu)]

        updated_rows.append(row)

    if updated_rows:
        df = pd.concat([df, pd.DataFrame(updated_rows)], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("✅ Đã lưu thành công!")
        st.dataframe(df, use_container_width=True)

# ------------------------
# 3. CHỈNH SỬA MÃ HÀNG
# ------------------------
st.subheader("✏️ Chỉnh sửa mã hàng")

if not df.empty:
    ma_hang_edit = st.selectbox("Chọn mã hàng để chỉnh sửa", df["Mã hàng"].unique())
    df_edit = df[df["Mã hàng"] == ma_hang_edit].copy()

    df_edit_new = st.data_editor(df_edit, use_container_width=True)

    if st.button("💾 Lưu chỉnh sửa"):
        df = df[df["Mã hàng"] != ma_hang_edit]  # Xóa dữ liệu cũ
        df = pd.concat([df, df_edit_new], ignore_index=True)
        df.to_csv(FILE_PATH, index=False)
        st.success("✅ Đã cập nhật!")
        st.dataframe(df[df["Mã hàng"] == ma_hang_edit], use_container_width=True)

# ------------------------
# 4. XÓA MÃ HÀNG
# ------------------------
st.subheader("🗑️ Xóa mã hàng")

if not df.empty:
    ma_hang_delete = st.selectbox("Chọn mã hàng để xóa", [""] + list(df["Mã hàng"].unique()))
    if ma_hang_delete and st.button("❌ Xóa"):
        df = df[df["Mã hàng"] != ma_hang_delete]
        df.to_csv(FILE_PATH, index=False)
        st.success(f"✅ Đã xóa mã hàng {ma_hang_delete}")
        st.dataframe(df, use_container_width=True)
