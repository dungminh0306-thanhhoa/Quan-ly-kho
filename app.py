import streamlit as st
import pandas as pd

# File lưu dữ liệu (đổi sang CSV để không cần openpyxl)
data_file = "data.csv"

# Hàm load dữ liệu
def load_data():
    try:
        return pd.read_csv(data_file)
    except:
        return pd.DataFrame(columns=["Mã hàng", "Nguyên phụ liệu", "Màu sắc", "Số lượng"])

# Hàm lưu dữ liệu
def save_data(df):
    df.to_csv(data_file, index=False)

# Giao diện chính
def main():
    st.title("📦 Quản lý nguyên phụ liệu theo mã hàng và màu sắc")

    df = load_data()

    menu = ["Xem dữ liệu", "Thêm mã hàng", "Chỉnh sửa thông tin", "Xem gộp theo mã hàng"]
    choice = st.sidebar.selectbox("Chức năng", menu)

    if choice == "Xem dữ liệu":
        st.subheader("📋 Danh sách chi tiết")
        st.dataframe(df)

    elif choice == "Thêm mã hàng":
        st.subheader("➕ Thêm mã hàng mới")
        ma_hang = st.text_input("Nhập mã hàng")

        # Nếu mã hàng đã có thì lấy NPL cũ, nếu chưa có thì cho nhập mới
        if ma_hang and ma_hang in df["Mã hàng"].values:
            npl = df[df["Mã hàng"] == ma_hang].iloc[0]["Nguyên phụ liệu"]
            st.info(f"Mã hàng này đã có, dùng chung nguyên phụ liệu: {npl}")
        else:
            npl = st.text_area("Nguyên phụ liệu")

        mau = st.text_input("Màu sắc")
        so_luong = st.number_input("Số lượng", min_value=0, step=1)

        if st.button("Thêm"):
            if ma_hang and mau:
                new_row = pd.DataFrame({
                    "Mã hàng": [ma_hang],
                    "Nguyên phụ liệu": [npl],
                    "Màu sắc": [mau],
                    "Số lượng": [so_luong]
                })
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)
                st.success("Đã thêm thành công!")
            else:
                st.warning("Vui lòng nhập đầy đủ Mã hàng và Màu sắc")

    elif choice == "Chỉnh sửa thông tin":
        st.subheader("✏️ Chỉnh sửa thông tin mã hàng")
        if len(df) > 0:
            idx = st.number_input("Nhập số thứ tự dòng cần sửa (0 → n)", min_value=0, max_value=len(df)-1, step=1)
            row = df.iloc[idx]

            new_ma = st.text_input("Mã hàng", row["Mã hàng"])
            # Không cho sửa NPL ở đây nếu đã có mã hàng khác giống
            if new_ma in df["Mã hàng"].values:
                new_npl = df[df["Mã hàng"] == new_ma].iloc[0]["Nguyên phụ liệu"]
                st.info(f"Nguyên phụ liệu giữ nguyên: {new_npl}")
            else:
                new_npl = st.text_area("Nguyên phụ liệu", row["Nguyên phụ liệu"])

            new_mau = st.text_input("Màu sắc", row["Màu sắc"])
            new_sl = st.number_input("Số lượng", min_value=0, step=1, value=int(row["Số lượng"]))

            if st.button("Cập nhật"):
                df.loc[idx, ["Mã hàng", "Nguyên phụ liệu", "Màu sắc", "Số lượng"]] = [new_ma, new_npl, new_mau, new_sl]
                save_data(df)
                st.success("Đã cập nhật thành công!")
        else:
            st.info("Chưa có dữ liệu để chỉnh sửa")

    elif choice == "Xem gộp theo mã hàng":
        st.subheader("📊 Danh sách gộp theo mã hàng")
        if len(df) > 0:
            grouped = df.groupby(["Mã hàng", "Nguyên phụ liệu", "Màu sắc"]).agg({
                "Số lượng": "sum"
            }).reset_index()
            st.dataframe(grouped)
        else:
            st.info("Chưa có dữ liệu để xem gộp")

if __name__ == "__main__":
    main()
