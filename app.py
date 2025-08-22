import streamlit as st
import pandas as pd
import os

# =========================
# CẤU HÌNH CƠ BẢN
# =========================
st.set_page_config(page_title="Quản lý Mã hàng & Nguyên phụ liệu", layout="wide")
DATA_FILE = "data.csv"

# =========================
# TIỆN ÍCH LƯU / ĐỌC
# =========================
def ensure_store():
    if not os.path.exists(DATA_FILE):
        pd.DataFrame(columns=["Mã hàng", "Màu sắc", "Số lượng", "Nguyên liệu"]).to_csv(DATA_FILE, index=False)

def load_data() -> pd.DataFrame:
    ensure_store()
    try:
        df = pd.read_csv(DATA_FILE)
    except Exception:
        df = pd.DataFrame(columns=["Mã hàng", "Màu sắc", "Số lượng", "Nguyên liệu"])
    # Chuẩn hóa cột & kiểu dữ liệu
    for col in ["Mã hàng", "Màu sắc", "Nguyên liệu"]:
        if col in df.columns:
            df[col] = df[col].astype(str)
    if "Số lượng" in df.columns:
        # ép kiểu số; lỗi thì đưa về 0
        df["Số lượng"] = pd.to_numeric(df["Số lượng"], errors="coerce").fillna(0).astype(int)
    return df

def save_data(df: pd.DataFrame):
    # Đảm bảo cột đầy đủ & thứ tự
    base_cols = ["Mã hàng", "Màu sắc", "Số lượng", "Nguyên liệu"]
    for c in base_cols:
        if c not in df.columns:
            df[c] = ""
    df = df[base_cols]
    df.to_csv(DATA_FILE, index=False)

def collapse_ma_hang_once(df: pd.DataFrame) -> pd.DataFrame:
    """Ẩn giá trị 'Mã hàng' ở các dòng sau trong cùng nhóm (hiển thị như gộp ô)."""
    if df.empty:
        return df.copy()
    out = df.copy()
    for ma, idx in out.groupby("Mã hàng", sort=False).groups.items():
        # idx là Index của các dòng trong nhóm
        if len(idx) > 1:
            out.loc[idx[1:], "Mã hàng"] = ""
    return out

# =========================
# KHỞI TẠO SESSION
# =========================
if "add_table" not in st.session_state:
    st.session_state.add_table = None   # DataFrame nhập liệu tạm thời
if "add_ma" not in st.session_state:
    st.session_state.add_ma = ""        # Mã hàng đang nhập

# =========================
# GIAO DIỆN MENU
# =========================
st.sidebar.title("📋 Menu")
menu = st.sidebar.radio(
    "Chọn chức năng:",
    [
        "📑 Xem danh sách",
        "➕ Thêm mã hàng mới",
        "✏️ Chỉnh sửa mã hàng",
        "🗑️ Xóa mã hàng"
    ]
)

# =========================
# 1) XEM DANH SÁCH
# =========================
if menu == "📑 Xem danh sách":
    st.title("📑 Danh sách mã hàng")
    df = load_data()

    col_a, col_b = st.columns([2, 1])
    with col_a:
        search = st.text_input("🔍 Tìm kiếm (theo Mã hàng / Màu sắc / Nguyên liệu):", "")
    with col_b:
        only_ma = st.checkbox("Ẩn lặp 'Mã hàng' (mã xuất hiện 1 lần)", value=True)

    if search.strip():
        s = search.lower()
        mask = (
            df["Mã hàng"].str.lower().str.contains(s)
            | df["Màu sắc"].str.lower().str.contains(s)
            | df["Nguyên liệu"].str.lower().str.contains(s)
        )
        df_view = df[mask].copy()
    else:
        df_view = df.copy()

    if only_ma:
        df_view = collapse_ma_hang_once(df_view)

    st.dataframe(df_view, use_container_width=True)

# =========================
# 2) THÊM MÃ HÀNG MỚI
# =========================
elif menu == "➕ Thêm mã hàng mới":
    st.title("➕ Thêm mã hàng mới (nhập theo bảng)")

    df = load_data()

    # Bước 1: nhập mã hàng & số dòng
    with st.form("setup_new_ma", clear_on_submit=False):
        col1, col2 = st.columns([2, 1])
        with col1:
            ma_input = st.text_input("Mã hàng:", value=st.session_state.add_ma)
        with col2:
            so_dong = st.number_input("Số dòng (số màu):", min_value=1, max_value=200, value=5, step=1)
        create_clicked = st.form_submit_button("Tạo bảng nhập")

    # Khi tạo bảng: khởi tạo bảng trống với số dòng mong muốn
    if create_clicked:
        st.session_state.add_ma = ma_input.strip()
        rows = int(so_dong)
        st.session_state.add_table = pd.DataFrame({
            "Màu sắc": ["" for _ in range(rows)],
            "Số lượng": [0 for _ in range(rows)],
            "Nguyên liệu": ["" for _ in range(rows)]
        })

    # Bước 2: hiển thị bảng nhập trực tiếp
    if st.session_state.add_ma and isinstance(st.session_state.add_table, pd.DataFrame):
        st.markdown(f"**Mã hàng:** `{st.session_state.add_ma}`")
        st.caption("Nhập trực tiếp vào bảng bên dưới. Bạn có thể thêm/bớt dòng.")

        edited = st.data_editor(
            st.session_state.add_table,
            num_rows="dynamic",
            use_container_width=True,
            key="add_editor"
        )

        # Lưu lại bảng đã chỉnh vào session
        st.session_state.add_table = edited

        # Nút Lưu
        if st.button("💾 Lưu mã hàng này"):
            ma_hang = st.session_state.add_ma
            temp = st.session_state.add_table.copy()

            # Loại bỏ các dòng trống (không có màu sắc)
            temp = temp[ temp["Màu sắc"].astype(str).str.strip() != "" ].copy()
            # Ép kiểu số lượng
            temp["Số lượng"] = pd.to_numeric(temp["Số lượng"], errors="coerce").fillna(0).astype(int)

            if temp.empty:
                st.warning("Chưa có dòng hợp lệ để lưu.")
            else:
                # Auto kế thừa nguyên phụ liệu nếu mã hàng đã tồn tại & ô Nguyên liệu đang trống
                if ma_hang in df["Mã hàng"].values:
                    existing_nl = df.loc[df["Mã hàng"] == ma_hang, "Nguyên liệu"]
                    inherited = existing_nl.iloc[0] if not existing_nl.empty else ""
                    temp.loc[temp["Nguyên liệu"].astype(str).str.strip() == "", "Nguyên liệu"] = inherited

                # Ghép với Mã hàng để lưu
                temp.insert(0, "Mã hàng", ma_hang)

                # Ghi thêm (không ghi đè)
                df_out = pd.concat([df, temp], ignore_index=True)
                save_data(df_out)

                st.success(f"✅ Đã lưu {len(temp)} dòng cho mã hàng `{ma_hang}`.")
                # Hiển thị lại phần vừa lưu (ẩn lặp mã hàng)
                st.subheader("Bảng vừa lưu")
                st.dataframe(collapse_ma_hang_once(temp), use_container_width=True)

                # Reset bảng nhập (giữ lại mã hàng cho lần nhập tiếp theo nếu muốn)
                st.session_state.add_table = None

# =========================
# 3) CHỈNH SỬA MÃ HÀNG
# =========================
elif menu == "✏️ Chỉnh sửa mã hàng":
    st.title("✏️ Chỉnh sửa mã hàng")
    df = load_data()

    if df.empty:
        st.info("Chưa có dữ liệu để chỉnh sửa.")
    else:
        ma_list = df["Mã hàng"].unique().tolist()
        ma_pick = st.selectbox("Chọn mã hàng:", ma_list)

        sub = df[df["Mã hàng"] == ma_pick].copy()
        st.caption("Sửa trực tiếp rồi bấm Lưu thay đổi.")
        edited = st.data_editor(sub, num_rows="dynamic", use_container_width=True, key="edit_editor")

        colL, colR = st.columns([1, 1])
        with colL:
            if st.button("💾 Lưu thay đổi"):
                # Ghi đè nhóm mã hàng này bằng edited
                remain = df[df["Mã hàng"] != ma_pick]
                df_new = pd.concat([remain, edited], ignore_index=True)
                # Chuẩn hóa kiểu dữ liệu
                if "Số lượng" in df_new.columns:
                    df_new["Số lượng"] = pd.to_numeric(df_new["Số lượng"], errors="coerce").fillna(0).astype(int)
                save_data(df_new)
                st.success("✅ Đã lưu thay đổi.")
        with colR:
            # Xóa dòng theo index trong nhóm đang xem
            if not edited.empty:
                idx_to_del = st.number_input("Xóa dòng (STT trong bảng đang xem)", min_value=0, max_value=len(edited)-1, step=1, value=0)
                if st.button("❌ Xóa dòng đã chọn"):
                    edited2 = edited.drop(edited.index[idx_to_del]).reset_index(drop=True)
                    remain = df[df["Mã hàng"] != ma_pick]
                    df_new = pd.concat([remain, edited2], ignore_index=True)
                    if "Số lượng" in df_new.columns:
                        df_new["Số lượng"] = pd.to_numeric(df_new["Số lượng"], errors="coerce").fillna(0).astype(int)
                    save_data(df_new)
                    st.success("✅ Đã xóa dòng trong nhóm.")

# =========================
# 4) XÓA MÃ HÀNG
# =========================
elif menu == "🗑️ Xóa mã hàng":
    st.title("🗑️ Xóa mã hàng")
    df = load_data()

    if df.empty:
        st.info("Chưa có dữ liệu.")
    else:
        ma_list = df["Mã hàng"].unique().tolist()
        ma_pick = st.selectbox("Chọn mã hàng cần xóa:", ma_list)
        if st.button("❌ Xóa toàn bộ mã hàng này"):
            df_new = df[df["Mã hàng"] != ma_pick].copy()
            save_data(df_new)
            st.success(f"✅ Đã xóa toàn bộ mã hàng `{ma_pick}`.")
