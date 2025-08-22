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

st.set_page_config(page_title="Quản lý mã hàng", layout="wide")
st.title("👕 Quản lý mã hàng & nguyên phụ liệu")

# Thanh menu lựa chọn
menu = st.sidebar.radio(
    "Chọn chức năng:",
    ["📋 Xem danh sách", "➕ Thêm mã hàng", "✏️ Chỉnh sửa mã hàng", "🗑️ Xóa mã hàng", "📦 Xuất dữ liệu"]
)

# ============= 1. XEM DANH SÁCH ==================
if menu == "📋 Xem danh sách":
    st.subheader("📋 Danh sách mã hàng hiện tại")
    search = st.text_input("🔍 Tìm kiếm theo mã hàng hoặc màu sắc:")
    if search:
        df_show = df[df.apply(lambda row: search.lower() in row.astype(str).str.lower().to_list(), axis=1)]
    else:
        df_show = df
    st.dataframe(df_show, use_container_width=True)

# ============= 2. THÊM MÃ HÀNG ==================
elif menu == "➕ Thêm mã hàng":
    st.subheader("➕ Thêm mã hàng mới")

    if "new_rows" not in st.session_state:
        st.session_state["new_rows"] = 5

    # Tạo bảng nhập liệu
    new_data = pd.DataFrame({
        "Mã hàng": ["" for _ in range(st.session_state["new_rows"])],
        "Màu sắc": ["" for _ in range(st.session_state["new_rows"])],
        "Số lượng": [0 for _ in range(st.session_state["new_rows"])],
        "Nguyên liệu": ["" for _ in range(st.session_state["new_rows"])]
    })

    edited_data = st.data_editor(new_data, num_rows="dynamic", use_container_width=True)

    if st.button("💾 Lưu dữ liệu"):
        updated_rows = []

        for _, row in edited_data.iterrows():
            if row["Mã hàng"] == "" or row["Màu sắc"] == "":
                continue

            ma_hang = row["Mã hàng"]

            # Nếu mã hàng đã có, lấy nguyên phụ liệu cũ
            if ma_hang in df["Mã hàng"].values and row["Nguyên liệu"] == "":
                nguyen_lieu_cu = df[df["Mã hàng"] == ma_hang]["Nguyên liệu"].tolist()
                if nguyen_lieu_cu:
                    row["Nguyên liệu"] = nguyen_lieu_cu[len(updated_rows) % len(nguyen_lieu_cu)]

            updated_rows.append(row)

        if updated_rows:
            df = pd.concat([df, pd.DataFrame(updated_rows)], ignore_index=True)
            df.to_csv(FILE_PATH, index=False)
            st.success("✅ Đã thêm thành công!")

# ============= 3. CHỈNH SỬA MÃ HÀNG ==================
elif menu == "✏️ Chỉnh sửa mã hàng":
    st.subheader("✏️ Chỉnh sửa mã hàng")

    ma_list = df["Mã hàng"].unique().tolist()
    if ma_list:
        ma_chon = st.selectbox("Chọn mã hàng cần chỉnh sửa:", ma_list)
        df_edit = df[df["Mã hàng"] == ma_chon].copy()
        edited = st.data_editor(df_edit, use_container_width=True)

        if st.button("💾 Lưu chỉnh sửa"):
            df = df[df["Mã hàng"] != ma_chon]
            df = pd.concat([df, edited], ignore_index=True)
            df.to_csv(FILE_PATH, index=False)
            st.success("✅ Đã lưu chỉnh sửa!")

# ============= 4. XÓA MÃ HÀNG ==================
elif menu == "🗑️ Xóa mã hàng":
    st.subheader("🗑️ Xóa mã hàng")

    ma_list = df["Mã hàng"].unique().tolist()
    if ma_list:
        ma_chon = st.selectbox("Chọn mã hàng cần xóa:", ma_list)
        if st.button("❌ Xóa toàn bộ mã hàng này"):
            df = df[df["Mã hàng"] != ma_chon]
            df.to_csv(FILE_PATH, index=False)
            st.success(f"✅ Đã xóa mã hàng {ma_chon}")

# ============= 5. XUẤT FILE ==================
elif menu == "📦 Xuất dữ liệu":
    st.subheader("📦 Xuất dữ liệu")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Tải về CSV", data=csv, file_name="ma_hang.csv", mime="text/csv")
