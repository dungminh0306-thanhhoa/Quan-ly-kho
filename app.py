import streamlit as st
import pandas as pd

# File lưu dữ liệu
data_file = "data.xlsx"

# Hàm load dữ liệu
def load_data():
    try:
        return pd.read_excel(data_file)
    except:
        return pd.DataFrame(columns=["Mã hàng", "Nguyên phụ liệu", "Màu sắc"])

# Hàm lưu dữ liệu
def save_data(df):
    df.to_excel(data_file, index=False)

# Giao diện chính
def main():
    st.title("📦 Quản lý nguyên phụ liệu theo mã hàng")

    df = load_data()

    menu = ["Xem dữ liệu", "Thêm mã hàng", "Chỉnh sửa mã hàng"]
    choice = st.sidebar.selectbox("Chức năng", menu)

    if choice == "Xem dữ liệu":
        st.subheader("📋 Danh sách mã hàng")
        st.dataframe(df)

    elif choice == "Thêm mã hàng":
        st.subheader("➕ Thêm mã hàng mới")
        ma_hang = st.text_input("Nhập mã hàng")
        npl = st.text_area("Nguyên phụ liệu")
        mau = st.text_input("Màu sắc (cách nhau bằng dấu phẩy)")

        if st.button("Thêm"):
            if ma_hang:
                # Nếu mã hàng đã tồn tại thì lấy lại dữ liệu cũ
                if ma_hang in df["Mã hàng"].values:
                    old_row = df[df["Mã hàng"] == ma_hang].iloc[0]
                    new_mau = str(old_row["Màu sắc"]) + ", " + mau if mau else old_row["Màu sắc"]
                    new_npl = npl if npl else old_row["Nguyên phụ liệu"]
                    df.loc[df["Mã hàng"] == ma_hang, ["Nguyên phụ liệu", "Màu sắc"]] = [new_npl, new_mau]
                else:
                    new_row = pd.DataFrame({
                        "Mã hàng": [ma_hang],
                        "Nguyên phụ liệu": [npl],
                        "Màu sắc": [mau]
                    })
                    df = pd.concat([df, new_row], ignore_index=True)

                save_data(df)
                st.success("Đã thêm/cập nhật mã hàng thành công!")
            else:
                st.warning("Vui lòng nhập mã hàng")

    elif choice == "Chỉnh sửa mã hàng":
        st.subheader("✏️ Chỉnh sửa thông tin")
        if len(df) > 0:
            ma_chon = st.selectbox("Chọn mã hàng", df["Mã hàng"].unique())
            row = df[df["Mã hàng"] == ma_chon].iloc[0]

            new_ma = st.text_input("Mã hàng", row["Mã hàng"])
            new_npl = st.text_area("Nguyên phụ liệu", row["Nguyên phụ liệu"])
            new_mau = st.text_input("Màu sắc", row["Màu sắc"])

            if st.button("Cập nhật"):
                df.loc[df["Mã hàng"] == ma_chon, ["Mã hàng", "Nguyên phụ liệu", "Màu sắc"]] = [new_ma, new_npl, new_mau]
                save_data(df)
                st.success("Đã cập nhật thành công!")
        else:
            st.info("Chưa có dữ liệu để chỉnh sửa")

if __name__ == "__main__":
    main()
