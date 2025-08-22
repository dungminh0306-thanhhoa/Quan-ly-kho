import streamlit as st
import pandas as pd

# --- Khởi tạo session state ---
if "products" not in st.session_state:
    st.session_state.products = {}  # {ma_hang: [{"Màu sắc":..., "Số lượng":..., "Nguyên liệu":...}, ...]}

if "edit_ma_hang" not in st.session_state:
    st.session_state.edit_ma_hang = None


# --- MENU ---
menu = st.sidebar.radio("Chọn chức năng", ["Thêm mã hàng", "Xem danh sách", "Sửa mã hàng", "Xóa mã hàng"])


# --- THÊM MÃ HÀNG ---
if menu == "Thêm mã hàng":
    st.header("Thêm mã hàng mới")

    ma_hang = st.text_input("Nhập mã hàng")
    so_dong = st.number_input("Số dòng màu sắc muốn nhập", min_value=1, step=1, value=1)

    if ma_hang:
        if ma_hang not in st.session_state.products:
            st.session_state.products[ma_hang] = []

        with st.form(key=f"form_add_{ma_hang}"):
            temp_data = []
            for i in range(so_dong):
                col1, col2, col3 = st.columns(3)
                with col1:
                    mau = st.text_input(f"Màu sắc {i+1}", key=f"mau_{ma_hang}_{i}")
                with col2:
                    so_luong = st.number_input(f"Số lượng {i+1}", min_value=0, key=f"sl_{ma_hang}_{i}")
                with col3:
                    nguyen_lieu = st.text_input(f"Nguyên liệu {i+1}", key=f"nl_{ma_hang}_{i}")

                if mau:  # chỉ lưu khi có màu
                    temp_data.append({"Màu sắc": mau, "Số lượng": so_luong, "Nguyên liệu": nguyen_lieu})

            submit = st.form_submit_button("Lưu màu sắc")

            if submit and temp_data:
                st.session_state.products[ma_hang].extend(temp_data)
                st.success("Đã thêm màu sắc vào mã hàng!")

    # Hiển thị dữ liệu của mã hàng vừa nhập
    if ma_hang and st.session_state.products[ma_hang]:
        st.subheader(f"Bảng dữ liệu của mã hàng: {ma_hang}")
        df = pd.DataFrame(st.session_state.products[ma_hang])
        st.dataframe(df)


# --- XEM DANH SÁCH (có tìm kiếm) ---
elif menu == "Xem danh sách":
    st.header("Danh sách tất cả mã hàng")

    if not st.session_state.products:
        st.info("Chưa có dữ liệu.")
    else:
        keyword = st.text_input("Tìm kiếm mã hàng")
        filtered = {mh: data for mh, data in st.session_state.products.items() if keyword.lower() in mh.lower()}

        if not filtered:
            st.warning("Không tìm thấy mã hàng phù hợp.")
        else:
            for mh, data in filtered.items():
                st.subheader(f"Mã hàng: {mh}")
                df = pd.DataFrame(data)
                st.dataframe(df)


# --- SỬA MÃ HÀNG ---
elif menu == "Sửa mã hàng":
    st.header("Sửa mã hàng")

    if not st.session_state.products:
        st.info("Chưa có dữ liệu để sửa.")
    else:
        ma_hang_chon = st.selectbox("Chọn mã hàng cần sửa", list(st.session_state.products.keys()))

        if ma_hang_chon:
            df = pd.DataFrame(st.session_state.products[ma_hang_chon])
            st.write("Dữ liệu hiện tại:")
            st.dataframe(df)

            st.write("Chỉnh sửa dữ liệu:")
            new_data = []
            with st.form(key=f"form_edit_{ma_hang_chon}"):
                for i, row in enumerate(st.session_state.products[ma_hang_chon]):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        mau = st.text_input(f"Màu sắc {i+1}", value=row["Màu sắc"], key=f"edit_mau_{ma_hang_chon}_{i}")
                    with col2:
                        so_luong = st.number_input(f"Số lượng {i+1}", value=row["Số lượng"], min_value=0, key=f"edit_sl_{ma_hang_chon}_{i}")
                    with col3:
                        nguyen_lieu = st.text_input(f"Nguyên liệu {i+1}", value=row["Nguyên liệu"], key=f"edit_nl_{ma_hang_chon}_{i}")
                    new_data.append({"Màu sắc": mau, "Số lượng": so_luong, "Nguyên liệu": nguyen_lieu})

                save = st.form_submit_button("Lưu thay đổi")

                if save:
                    st.session_state.products[ma_hang_chon] = new_data
                    st.success(f"Đã cập nhật dữ liệu cho mã hàng {ma_hang_chon}")


# --- XÓA MÃ HÀNG ---
elif menu == "Xóa mã hàng":
    st.header("Xóa mã hàng")

    if not st.session_state.products:
        st.info("Chưa có dữ liệu để xóa.")
    else:
        ma_hang_xoa = st.selectbox("Chọn mã hàng cần xóa", list(st.session_state.products.keys()))
        if st.button("Xóa"):
            del st.session_state.products[ma_hang_xoa]
            st.success(f"Đã xóa mã hàng {ma_hang_xoa}")
