import uuid
from datetime import datetime, timedelta
from data_structures import LinkedList
from algorithms import merge_sort
from models import Book, Reader, BorrowRecord
from database import Database

class LibraryManager:
    def __init__(self, db_folder="."):
        self.db = Database(db_folder)
        self.books = self.db.load_list("books.txt", Book.from_string)
        self.readers = self.db.load_list("readers.txt", Reader.from_string)
        self.records = self.db.load_list("records.txt", BorrowRecord.from_string)
        
        # Cấu hình luật mượn
        self.borrow_limit = 3
        self.borrow_days = 14
        self.fine_per_day = 5000 # VND/ngày

    def save_all(self):
        self.db.save_list("books.txt", self.books)
        self.db.save_list("readers.txt", self.readers)
        self.db.save_list("records.txt", self.records)

    # 1. QUẢN LÝ SÁCH
    def add_book(self, book_id, title, author, genre, total_quantity):
        existing = self.books.find(lambda b: b.book_id == book_id)
        if existing:
            return False, "Mã sách đã tồn tại."
        new_book = Book(book_id, title, author, genre, total_quantity, total_quantity, 0)
        self.books.append(new_book)
        self.save_all()
        return True, "Thêm sách thành công."

    def delete_book(self, book_id):
        book = self.books.find(lambda b: b.book_id == book_id)
        if not book:
            return False, "Không tìm thấy sách."
        if book.total_quantity != book.available_quantity:
            return False, "Không thể xóa sách đang có người mượn."
            
        success = self.books.remove(lambda b: b.book_id == book_id)
        if success:
            self.save_all()
            return True, "Xóa sách thành công."
        return False, "Lỗi khi xóa sách."
        
    def edit_book(self, book_id, title, author, genre, total_quantity):
        book = self.books.find(lambda b: b.book_id == book_id)
        if not book:
            return False, "Không tìm thấy sách."
            
        diff = int(total_quantity) - book.total_quantity
        if book.available_quantity + diff < 0:
            return False, "Số lượng tổng mới không hợp lệ (nhỏ hơn số sách đang được mượn)."
            
        book.title = title
        book.author = author
        book.genre = genre
        book.total_quantity = int(total_quantity)
        book.available_quantity += diff
        self.save_all()
        return True, "Cập nhật sách thành công."

    def search_books(self, keyword):
        keyword = keyword.lower()
        return self.books.find_all(lambda b: 
            keyword in b.title.lower() or 
            keyword in b.author.lower() or 
            keyword in b.genre.lower() or
            keyword in b.book_id.lower()
        )

    def import_books(self, filepath):
        import file_io
        success, msg = file_io.import_books_from_file(filepath, self.books)
        if success:
            self.save_all()
        return success, msg

    # 2. QUẢN LÝ BẠN ĐỌC
    def add_reader(self, reader_id, name, khoa, nganh):
        if len(reader_id) != 9 or not reader_id.startswith("202") or not reader_id.isdigit():
            return False, "Mã sinh viên phải có 9 chữ số và bắt đầu bằng '202'."
            
        existing = self.readers.find(lambda r: r.reader_id == reader_id)
        if existing:
            return False, "Mã sinh viên đã tồn tại."
        new_reader = Reader(reader_id, name, khoa, nganh)
        self.readers.append(new_reader)
        self.save_all()
        return True, "Thêm sinh viên thành công."

    def edit_reader(self, reader_id, name, khoa, nganh):
        reader = self.readers.find(lambda r: r.reader_id == reader_id)
        if not reader:
            return False, "Không tìm thấy sinh viên."
            
        reader.name = name
        reader.khoa = khoa
        reader.nganh = nganh
        self.save_all()
        return True, "Cập nhật sinh viên thành công."

    def search_readers(self, keyword):
        keyword = keyword.lower()
        return self.readers.find_all(lambda r:
            keyword in r.reader_id.lower() or
            keyword in r.name.lower() or
            keyword in r.khoa.lower() or
            keyword in r.nganh.lower()
        )

    def get_borrowed_count(self, reader_id):
        current_borrows = self.records.find_all(lambda r: 
            r.reader_id == reader_id and not r.actual_return_date
        )
        return current_borrows.size()

    def pay_fine(self, reader_id, amount):
        reader = self.readers.find(lambda r: r.reader_id == reader_id)
        if not reader:
            return False, "Không tìm thấy sinh viên."
        if reader.unpaid_fine <= 0:
            return False, "Sinh viên không nợ phí phạt."
        
        if amount >= reader.unpaid_fine:
            change = amount - reader.unpaid_fine
            reader.unpaid_fine = 0
            self.save_all()
            if change > 0:
                return True, f"Thanh toán thành công. Tiền thừa cần trả lại: {change} VND."
            return True, "Thanh toán thành công toàn bộ phí phạt."
        else:
            reader.unpaid_fine -= amount
            self.save_all()
            return True, f"Đã thanh toán {amount} VND. Còn nợ: {reader.unpaid_fine} VND."

    def import_readers(self, filepath):
        import file_io
        success, msg = file_io.import_readers_from_file(filepath, self.readers)
        if success:
            self.save_all()
        return success, msg

    # 3. QUẢN LÝ MƯỢN TRẢ
    def borrow_book(self, reader_id, book_id, borrow_date_str=""):
        reader = self.readers.find(lambda r: r.reader_id == reader_id)
        if not reader:
            return False, "Không tìm thấy bạn đọc."
            
        book = self.books.find(lambda b: b.book_id == book_id)
        if not book:
            return False, "Không tìm thấy sách."
            
        if book.available_quantity <= 0:
            return False, "Sách đã hết trong kho."

        # Tìm các sách đang mượn của bạn đọc này
        current_borrows = self.records.find_all(lambda rec: rec.reader_id == reader_id and rec.actual_return_date == "")
        
        # Kiểm tra quá hạn
        today = datetime.now()
        if borrow_date_str:
            try:
                today = datetime.strptime(borrow_date_str, "%Y-%m-%d")
            except ValueError:
                return False, "Ngày mượn sai định dạng YYYY-MM-DD."
                
        for rec in current_borrows:
            exp_date = datetime.strptime(rec.expected_return_date, "%Y-%m-%d")
            if today > exp_date:
                return False, "Sinh viên đang có sách quá hạn, không thể mượn thêm."
                
        # Kiểm tra nợ phí phạt
        if reader.unpaid_fine > 0:
            return False, f"Sinh viên đang nợ {reader.unpaid_fine} VND tiền phạt. Vui lòng thanh toán trước khi mượn."
                
        # Kiểm tra giới hạn mượn
        limit = self.borrow_limit
        if current_borrows.size() >= limit:
            return False, f"Sinh viên đã đạt giới hạn mượn ({limit} quyển)."

        # Tính hạn trả
        days = self.borrow_days
        expected_ret = today + timedelta(days=days)
        
        record_id = str(uuid.uuid4())[:8]
        today_str = today.strftime("%Y-%m-%d")
        exp_ret_str = expected_ret.strftime("%Y-%m-%d")
        
        new_record = BorrowRecord(record_id, reader_id, book_id, today_str, exp_ret_str, "")
        self.records.append(new_record)
        
        book.available_quantity -= 1
        book.borrow_count += 1
        
        self.save_all()
        return True, f"Mượn sách thành công. Hạn trả: {exp_ret_str}"

    def return_book(self, record_id, return_date_str=""):
        record = self.records.find(lambda r: r.record_id == record_id)
        if not record:
            return False, "Không tìm thấy bản ghi mượn sách.", 0
        if record.actual_return_date != "":
            return False, "Sách này đã được trả.", 0
            
        today = datetime.now()
        if return_date_str:
            try:
                today = datetime.strptime(return_date_str, "%Y-%m-%d")
            except ValueError:
                return False, "Ngày trả sai định dạng YYYY-MM-DD.", 0
                
        record.actual_return_date = today.strftime("%Y-%m-%d")
        # Cập nhật số lượng sách
        book = self.books.find(lambda b: b.book_id == record.book_id)
        if book:
            book.available_quantity += 1
            
        reader = self.readers.find(lambda r: r.reader_id == record.reader_id)
            
        # Kiểm tra trễ hạn
        exp_date = datetime.strptime(record.expected_return_date, "%Y-%m-%d")
        fine = 0
        if today > exp_date:
            days_late = (today - exp_date).days
            fine = days_late * self.fine_per_day
            if reader:
                reader.unpaid_fine += fine
            msg = f"Trả sách thành công. Trễ {days_late} ngày. Phạt: {fine} VND."
        else:
            msg = "Trả sách thành công. Đúng hạn."
            
        self.save_all()
        return True, msg, fine

    # 4. BÁO CÁO
    def get_borrowed_books(self):
        return self.records.find_all(lambda rec: rec.actual_return_date == "")
        
    def get_overdue_books(self):
        today = datetime.now().strftime("%Y-%m-%d")
        return self.records.find_all(lambda rec: rec.actual_return_date == "" and rec.expected_return_date < today)
        
    def get_top_5_books(self):
        # Sao chép danh sách sách để không làm hỏng thứ tự gốc
        cloned_books = LinkedList()
        for b in self.books:
            cloned_books.append(b)
            
        # Sắp xếp giảm dần theo lượt mượn sử dụng custom merge_sort
        merge_sort(cloned_books, lambda a, b: a.borrow_count >= b.borrow_count)
        
        top_5 = LinkedList()
        current = cloned_books.head
        count = 0
        while current is not None and count < 5:
            # Bỏ qua sách chưa được mượn lần nào nếu muốn, nhưng yêu cầu chỉ là top 5
            top_5.append(current.data)
            current = current.next
            count += 1
            
        return top_5
