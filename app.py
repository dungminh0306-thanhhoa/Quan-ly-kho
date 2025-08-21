import streamlit as st
import pandas as pd

# Khởi tạo dữ liệu
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Mã hàng", "Tên hàng", "Tồn kho"])

if "npl" not in st.session_state:
    st.session_state.npl = {}  # dict: {ma_hang: [ {Tên NPL, Đơn vị, Số lượng}, ... ] }

st.title("📦 Quản lý Mã hàng & Nguyên phụ liệu")

menu = st.sidebar.radio("Chọn chức năng", ["Thêm", "Sửa", "Xóa", "Danh sách", "Nguyên phụ liệu"])

# --- THÊM ---
if menu == "Thêm":
    st.subheader("➕ Thêm mã hàng")
    ma = st.text_input("Mã hàng")
    ten = st.text_input("Tên hàng")
    ton = st.number_input("Tồn kho", min_value=0, value=0, step=1)

    if st.button("Lưu"):
        if ma in st.session_state.data["Mã hàng"].values:
            st.error("⚠️ Mã hàng đã tồn tại!")
        else:
            new_row = pd.DataFrame([[ma, ten, ton]], columns=st.session_state.data.columns)
            st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
            st.session_state.npl[ma] = []  # khởi tạo list NPL rỗng cho mã hàng
            st.success("✅ Đã thêm mã hàng mới")

# --- SỬA ---
elif menu == "Sửa":
    st.subheader("✏️ Sửa mã hàng")
    if len(st.session_state.data) == 0:
        st.warning("⚠️ Chưa có mã hàng nào")
    else:
        ma = st.selectbox("Chọn mã hàng", st.session_state.data["Mã hàng"])
        row = st.session_state.data[st.session_state.data["Mã hàng"] == ma].iloc[0]

        ten = st.text_input("Tên hàng", value=row["Tên hàng"])
        ton = st.number_input("Tồn kho", min_value=0, value=int(row["Tồn kho"]), step=1)

        if st.button("Cập nhật"):
            st.session_state.data.loc[st.session_state.data["Mã hàng"] == ma, ["Tên hàng", "Tồn kho"]] = [ten, ton]
            st.success("✅ Đã cập nhật")

# --- XÓA ---
elif menu == "Xóa":
    st.subheader("🗑️ Xóa mã hàng")
    if len(st.session_state.data) == 0:
        st.warning("⚠️ Chưa có mã hàng nào")
    else:
        ma = st.selectbox("Chọn mã hàng", st.session_state.data["Mã hàng"])

        if st.button("Xóa"):
            st.session_state.data = st.session_state.data[st.session_state.data["Mã hàng"] != ma]
            if ma in st.session_state.npl:
                del st.session_state.npl[ma]  # xóa luôn nguyên phụ liệu liên quan
            st.success(f"✅ Đã xóa mã hàng {ma}")

# --- DANH SÁCH ---
elif menu == "Danh sách":
    st.subheader("📋 Danh sách mã hàng & tồn kho (toàn bộ)")
    st.dataframe(st.session_state.data, use_container_width=True)

    st.subheader("🔍 Kết quả tìm kiếm")
    keyword = st.text_input("Nhập mã hàng hoặc tên hàng cần tìm")

    if keyword:
        df_view = st.session_state.data[
            st.session_state.data.apply(lambda row: keyword.lower() in str(row.values).lower(), axis=1)
        ]
        st.dataframe(df_view, use_container_width=True)
    else:
        st.info("Nhập từ khóa để tìm kiếm (mã hàng hoặc tên hàng)")

# --- NGUYÊN PHỤ LIỆU ---
elif menu == "Nguyên phụ liệu":
    st.subheader("⚙️ Quản lý nguyên phụ liệu cho từng mã hàng")
    if len(st.session_state.data) == 0:
        st.warning("⚠️ Chưa có mã hàng nào, hãy thêm trước!")
    else:
        ma = st.selectbox("Chọn mã hàng", st.session_state.data["Mã hàng"])

        st.write(f"### 📦 Nguyên phụ liệu cho mã hàng **{ma}**")
        npl_list = st.session_state.npl.get(ma, [])

        # Hiển thị danh sách NPL
        if len(npl_list) > 0:
            for i, npl in enumerate(npl_list):
                with st.expander(f"🔹 {npl['Tên NPL']} ({npl['Số lượng']} {npl['Đơn vị']})"):
                    ten_edit = st.text_input("Tên NPL", value=npl["Tên NPL"], key=f"ten_{ma}_{i}")
                    donvi_edit = st.text_input("Đơn vị", value=npl["Đơn vị"], key=f"dv_{ma}_{i}")
                    soluong_edit = st.number_input("Số lượng", min_value=0, step=1,
                                                   value=int(npl["Số lượng"]), key=f"sl_{ma}_{i}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Lưu thay đổi", key=f"save_{ma}_{i}"):
                            st.session_state.npl[ma][i] = {
                                "Tên NPL": ten_edit,
                                "Đơn vị": donvi_edit,
                                "Số lượng": soluong_edit
                            }
                            st.success("✅ Đã cập nhật NPL")

                    with col2:
                        if st.button("🗑️ Xóa", key=f"delete_{ma}_{i}"):
                            st.session_state.npl[ma].pop(i)
                            st.success("✅ Đã xóa NPL")
                            st.experimental_rerun()
        else:
            st.info("❌ Chưa có nguyên phụ liệu nào cho mã hàng này")

        st.write("### ➕ Thêm nguyên phụ liệu")
        ten_npl = st.text_input("Tên nguyên phụ liệu")
        donvi = st.text_input("Đơn vị tính (m, cái, cuộn...)")
        soluong = st.number_input("Số lượng", min_value=0, step=1)

        if st.button("Thêm NPL"):
            new_npl = {"Tên NPL": ten_npl, "Đơn vị": donvi, "Số lượng": soluong}
            st.session_state.npl[ma].append(new_npl)
            st.success("✅ Đã thêm nguyên phụ liệu mới")


