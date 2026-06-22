# Hệ Thống Quản Lý Thư Viện (Library Management System)

Đây là dự án quản lý thư viện được viết bằng ngôn ngữ Python, sử dụng giao diện đồ họa `tkinter`.

## Các tính năng chính

1. **Quản Lý Sách**
   - Thêm, sửa, xóa thông tin sách.
   - Nhập danh sách sách từ file (`.txt`).
   - Tìm kiếm sách theo mã sách, tên sách hoặc tác giả.
   - Quản lý số lượng tổng, số lượng khả dụng và lượt mượn của từng cuốn sách.

2. **Quản Lý Bạn Đọc (Sinh Viên)**
   - Thêm, sửa thông tin sinh viên (Mã SV, Họ tên, Khóa/Khoa, Ngành).
   - Nhập danh sách sinh viên từ file.
   - Theo dõi số lượng sách đang mượn và thanh toán phí nợ.

3. **Mượn / Trả Sách**
   - Tạo bản ghi mượn sách (cần mã sinh viên, mã sách, ngày mượn).
   - Trả sách theo mã bản ghi, tự động tính tiền phạt nếu trả quá hạn.
   - Cập nhật tự động trạng thái sách và giới hạn mượn của sinh viên.

4. **Báo Cáo - Thống Kê**
   - Danh sách các sách đang được mượn.
   - Danh sách các sách quá hạn chưa trả.
   - Danh sách Top 5 sách được mượn nhiều nhất.

## Hướng dẫn sử dụng

1. Đảm bảo máy tính đã cài đặt **Python 3.x**.
2. Mở terminal / command prompt tại thư mục của dự án.
3. Chạy lệnh sau để khởi động ứng dụng:
   ```bash
   python main.py
   ```

## Cấu trúc tệp tin

- `main.py`: Chứa mã nguồn giao diện người dùng (GUI) và vòng lặp ứng dụng.
- `library_manager.py`: Quản lý logic chính của hệ thống thư viện.
- `models.py`, `data_structures.py`: Định nghĩa các cấu trúc dữ liệu và mô hình hướng đối tượng của dự án.
- `database.py`, `file_io.py`, `algorithms.py`: Các module hỗ trợ xử lý dữ liệu và đọc/ghi file.
- `*.txt` (VD: `books.txt`, `readers.txt`, `records.txt`): Các file lưu trữ dữ liệu mẫu của chương trình.
