import streamlit as st
import pandas as pd

# --- Khởi tạo session state ---
if "products_colors" not in st.session_state:
    st.session_state.products_colors = {}   # {ma_hang: [{"Màu sắc":..., "Số lượng":...}, ...]}

if "products_materials" not in st.session_state:
    st.session_state.products_materials = {}  # {ma_hang: [{"Nguyên liệu":...}, ...]}


# --- MENU ---
menu = st.sidebar.radio("Chọn chức năng", ["Thêm mã hàng", "Xem danh sách", "Sửa mã hàng", "Xóa mã hàng"])


# --- THÊM MÃ HÀNG ---
if menu == "Thêm mã hàng":
    st.header("Thêm mã hàng mới")

    ma_hang = st.text_input("Nhập mã hàng")
    so_dong = st.number_input("Số dòng muốn nhập", min_value=1, step=1, value=1)

    if ma_hang:
        if ma_hang not in st.session_state.products_colors:
            st.session_state.products_colors[ma_hang] = []
        if ma_hang not in st.session_state.products_materials:
            st.session_state.products_materials[ma_hang] = []

        with st.form(key=f"form_add_{ma_hang}"):
            temp_colors = []
            temp_materials = []

            for i in range(so_dong):
                col1, col2, col3 = st.columns(3)
                with col1:
                    mau = st.text_input(f"Màu sắc {i+1}", key=f"mau_{ma_hang}_{i}")
                with col2:
                    so_luong = st.number_input(f"Số lượng {i+1}", min_value=0, key=f"sl_{ma_hang}_{i}")
                with col3:
                    nguyen_lieu = st.text_input(f"Nguyên liệu {i+1}", key=f"nl_{ma_hang}_{i}")

                if mau:
                    temp_colors.append({"Màu sắc": mau, "Số lượng": so_luong})
                if nguyen_lieu:
                    temp_materials.append({"Nguyên liệu": nguyen_lieu})

            submit = st.form_submit_button("Lưu dữ liệu")

            if submit:
                st.session_state.products_colors[ma_hang].extend(temp_colors)
                st.session_state.products_materials[ma_hang].extend(temp_materials)
                st.success("Đã thêm dữ liệu cho mã hàng!")

    # Hiển thị dữ liệu của mã hàng vừa nhập
    if ma_hang and (st.session_state.products_colors[ma_hang] or st.session_state.products_materials[ma_hang]):
        st.subheader(f"Mã hàng: {ma_hang}")

        if st.session_state.products_colors[ma_hang]:
            st.write("Bảng màu sắc & số lượng:")
            df1 = pd.DataFrame(st.session_state.products_colors[ma_hang])
            st.dataframe(df1)

        if st.session_state.products_materials[ma_hang]:
            st.write("Bảng nguyên liệu:")
            df2 = pd.DataFrame(st.session_state.products_materials[ma_hang])
            st.dataframe(df2)


# --- XEM DANH SÁCH ---
elif menu == "Xem danh sách":
    st.header("Danh sách tất cả mã hàng")

    if not st.session_state.products_colors and not st.session_state.products_materials:
        st.info("Chưa có dữ liệu.")
    else:
        keyword = st.text_input("Tìm kiếm mã hàng")
        filtered = {mh: True for mh in set(st.session_state.products_colors.keys()) | set(st.session_state.products_materials.keys()) if keyword.lower() in mh.lower()}

        if not filtered:
            st.warning("Không tìm thấy mã hàng phù hợp.")
        else:
            for mh in filtered:
                st.subheader(f"Mã hàng: {mh}")

                if mh in st.session_state.products_colors and st.session_state.products_colors[mh]:
                    st.write("Bảng màu sắc & số lượng:")
                    df1 = pd.DataFrame(st.session_state.products_colors[mh])
                    st.dataframe(df1)

                if mh in st.session_state.products_materials and st.session_state.products_materials[mh]:
                    st.write("Bảng nguyên liệu:")
                    df2 = pd.DataFrame(st.session_state.products_materials[mh])
                    st.dataframe(df2)


# --- SỬA MÃ HÀNG ---
elif menu == "Sửa mã hàng":
    st.header("Sửa mã hàng")

    all_keys = list(set(st.session_state.products_colors.keys()) | set(st.session_state.products_materials.keys()))
    if not all_keys:
        st.info("Chưa có dữ liệu để sửa.")
    else:
        ma_hang_chon = st.selectbox("Chọn mã hàng cần sửa", all_keys)

        st.write("Dữ liệu hiện tại:")

        if ma_hang_chon in st.session_state.products_colors:
            df1 = pd.DataFrame(st.session_state.products_colors[ma_hang_chon])
            st.write("Bảng màu sắc & số lượng:")
            st.dataframe(df1)

        if ma_hang_chon in st.session_state.products_materials:
            df2 = pd.DataFrame(st.session_state.products_materials[ma_hang_chon])
            st.write("Bảng nguyên liệu:")
            st.dataframe(df2)

        # Chỉnh sửa
        st.write("Chỉnh sửa dữ liệu:")
        new_colors = []
        new_materials = []
        with st.form(key=f"form_edit_{ma_hang_chon}"):
            # sửa màu sắc
            if ma_hang_chon in st.session_state.products_colors:
                for i, row in enumerate(st.session_state.products_colors[ma_hang_chon]):
                    col1, col2 = st.columns(2)
                    with col1:
                        mau = st.text_input(f"Màu sắc {i+1}", value=row["Màu sắc"], key=f"edit_mau_{ma_hang_chon}_{i}")
                    with col2:
                        so_luong = st.number_input(f"Số lượng {i+1}", value=row["Số lượng"], min_value=0, key=f"edit_sl_{ma_hang_chon}_{i}")
                    new_colors.append({"Màu sắc": mau, "Số lượng": so_luong})

            # sửa nguyên liệu
            if ma_hang_chon in st.session_state.products_materials:
                for i, row in enumerate(st.session_state.products_materials[ma_hang_chon]):
                    nguyen_lieu = st.text_input(f"Nguyên liệu {i+1}", value=row["Nguyên liệu"], key=f"edit_nl_{ma_hang_chon}_{i}")
                    new_materials.append({"Nguyên liệu": nguyen_lieu})

            save = st.form_submit_button("Lưu thay đổi")

            if save:
                st.session_state.products_colors[ma_hang_chon] = new_colors
                st.session_state.products_materials[ma_hang_chon] = new_materials
                st.success(f"Đã cập nhật dữ liệu cho mã hàng {ma_hang_chon}")


# --- XÓA MÃ HÀNG ---
elif menu == "Xóa mã hàng":
    st.header("Xóa mã hàng")

    all_keys = list(set(st.session_state.products_colors.keys()) | set(st.session_state.products_materials.keys()))
    if not all_keys:
        st.info("Chưa có dữ liệu để xóa.")
    else:
        ma_hang_xoa = st.selectbox("Chọn mã hàng cần xóa", all_keys)
        if st.button("Xóa"):
            if ma_hang_xoa in st.session_state.products_colors:
                del st.session_state.products_colors[ma_hang_xoa]
            if ma_hang_xoa in st.session_state.products_materials:
                del st.session_state.products_materials[ma_hang_xoa]
            st.success(f"Đã xóa mã hàng {ma_hang_xoa}")
