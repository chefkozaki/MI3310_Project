import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from library_manager import LibraryManager

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ Thống Quản Lý Thư Viện")
        self.geometry("900x600")
        
        self.manager = LibraryManager()
        
        style = ttk.Style()
        style.theme_use('clam')
        
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)
        
        self.tab_books = ttk.Frame(self.notebook)
        self.tab_readers = ttk.Frame(self.notebook)
        self.tab_borrow = ttk.Frame(self.notebook)
        self.tab_reports = ttk.Frame(self.notebook)
        
        self.notebook.add(self.tab_books, text="Quản Lý Sách")
        self.notebook.add(self.tab_readers, text="Quản Lý Sinh Viên")
        self.notebook.add(self.tab_borrow, text="Mượn / Trả Sách")
        self.notebook.add(self.tab_reports, text="Báo Cáo")
        
        self.setup_books_tab()
        self.setup_readers_tab()
        self.setup_borrow_tab()
        self.setup_reports_tab()

    # --- SÁCH ---
    def setup_books_tab(self):
        frame_input = ttk.LabelFrame(self.tab_books, text="Thông tin Sách")
        frame_input.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_input, text="Mã Sách:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.ent_book_id = ttk.Entry(frame_input)
        self.ent_book_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Tên Sách:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.ent_book_title = ttk.Entry(frame_input)
        self.ent_book_title.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Tác giả:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.ent_book_author = ttk.Entry(frame_input)
        self.ent_book_author.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Thể loại:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.ent_book_genre = ttk.Entry(frame_input)
        self.ent_book_genre.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Số lượng:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.ent_book_qty = ttk.Entry(frame_input)
        self.ent_book_qty.grid(row=2, column=1, padx=5, pady=5)
        
        frame_btn = ttk.Frame(self.tab_books)
        frame_btn.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_btn, text="Thêm Sách", command=self.add_book).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Xóa Sách", command=self.delete_book).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Sửa Sách", command=self.edit_book).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Tìm Kiếm", command=self.search_book).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Làm Mới", command=self.refresh_books).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Nhập từ File", command=self.import_books_file).pack(side='left', padx=5)
        
        columns = ("id", "title", "author", "genre", "total", "avail", "borrowed")
        self.tree_books = ttk.Treeview(self.tab_books, columns=columns, show='headings')
        self.tree_books.heading("id", text="Mã Sách")
        self.tree_books.heading("title", text="Tên Sách")
        self.tree_books.heading("author", text="Tác Giả")
        self.tree_books.heading("genre", text="Thể Loại")
        self.tree_books.heading("total", text="Tổng SL")
        self.tree_books.heading("avail", text="Còn Lại")
        self.tree_books.heading("borrowed", text="Lượt Mượn")
        
        for col in columns:
            self.tree_books.column(col, width=100)
            
        self.tree_books.pack(expand=True, fill='both', padx=10, pady=5)
        
        self.tree_books.bind("<Double-1>", self.on_book_select)
        self.refresh_books()

    def on_book_select(self, event):
        selected = self.tree_books.selection()
        if not selected:
            return
        values = self.tree_books.item(selected[0], "values")
        self.ent_book_id.delete(0, tk.END)
        self.ent_book_id.insert(0, values[0])
        self.ent_book_title.delete(0, tk.END)
        self.ent_book_title.insert(0, values[1])
        self.ent_book_author.delete(0, tk.END)
        self.ent_book_author.insert(0, values[2])
        self.ent_book_genre.delete(0, tk.END)
        self.ent_book_genre.insert(0, values[3])
        self.ent_book_qty.delete(0, tk.END)
        self.ent_book_qty.insert(0, values[4])

    def add_book(self):
        b_id = self.ent_book_id.get()
        title = self.ent_book_title.get()
        author = self.ent_book_author.get()
        genre = self.ent_book_genre.get()
        qty = self.ent_book_qty.get()
        
        if not all([b_id, title, author, genre, qty]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
        if not qty.isdigit():
            messagebox.showerror("Lỗi", "Số lượng phải là số nguyên!")
            return
            
        success, msg = self.manager.add_book(b_id, title, author, genre, int(qty))
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_books()
        else:
            messagebox.showerror("Lỗi", msg)

    def edit_book(self):
        b_id = self.ent_book_id.get()
        title = self.ent_book_title.get()
        author = self.ent_book_author.get()
        genre = self.ent_book_genre.get()
        qty = self.ent_book_qty.get()
        if not all([b_id, title, author, genre, qty]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
            
        success, msg = self.manager.edit_book(b_id, title, author, genre, int(qty))
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_books()
        else:
            messagebox.showerror("Lỗi", msg)

    def delete_book(self):
        b_id = self.ent_book_id.get()
        if not b_id:
            messagebox.showerror("Lỗi", "Vui lòng nhập mã sách cần xóa!")
            return
        success, msg = self.manager.delete_book(b_id)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_books()
        else:
            messagebox.showerror("Lỗi", msg)
            
    def search_book(self):
        keyword = self.ent_book_title.get() or self.ent_book_id.get() or self.ent_book_author.get()
        if not keyword:
            self.refresh_books()
            return
        results = self.manager.search_books(keyword)
        self.update_books_tree(results)

    def refresh_books(self):
        self.update_books_tree(self.manager.books)

    def update_books_tree(self, books_list):
        for row in self.tree_books.get_children():
            self.tree_books.delete(row)
        for book in books_list:
            self.tree_books.insert("", "end", values=(
                book.book_id, book.title, book.author, book.genre,
                book.total_quantity, book.available_quantity, book.borrow_count
            ))

    def import_books_file(self):
        filepath = filedialog.askopenfilename(
            title="Chọn file sách",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if not filepath:
            return
        success, msg = self.manager.import_books(filepath)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_books()
        else:
            messagebox.showerror("Lỗi", msg)

    # --- SINH VIÊN ---
    def setup_readers_tab(self):
        frame_input = ttk.LabelFrame(self.tab_readers, text="Thông tin Sinh Viên")
        frame_input.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_input, text="Mã Sinh Viên (202xxxxxx):").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.ent_reader_id = ttk.Entry(frame_input)
        self.ent_reader_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Họ Tên:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.ent_reader_name = ttk.Entry(frame_input)
        self.ent_reader_name.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Khóa/Khoa:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.ent_reader_khoa = ttk.Entry(frame_input)
        self.ent_reader_khoa.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_input, text="Ngành:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.ent_reader_nganh = ttk.Entry(frame_input)
        self.ent_reader_nganh.grid(row=1, column=3, padx=5, pady=5)
        
        frame_btn = ttk.Frame(self.tab_readers)
        frame_btn.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_btn, text="Thêm Sinh Viên", command=self.add_reader).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Sửa Sinh Viên", command=self.edit_reader).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Thanh Toán Phí", command=self.pay_fine).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Tìm Kiếm", command=self.search_reader).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Làm Mới", command=self.refresh_readers).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Nhập từ File", command=self.import_readers_file).pack(side='left', padx=5)
        
        columns = ("id", "name", "khoa", "nganh", "borrowed", "fine")
        self.tree_readers = ttk.Treeview(self.tab_readers, columns=columns, show='headings')
        self.tree_readers.heading("id", text="Mã Sinh Viên")
        self.tree_readers.heading("name", text="Họ Tên")
        self.tree_readers.heading("khoa", text="Khóa/Khoa")
        self.tree_readers.heading("nganh", text="Ngành")
        self.tree_readers.heading("borrowed", text="Đang Mượn")
        self.tree_readers.heading("fine", text="Nợ Phí")
        
        self.tree_readers.pack(expand=True, fill='both', padx=10, pady=5)
        self.tree_readers.bind("<Double-1>", self.on_reader_select)
        self.refresh_readers()

    def on_reader_select(self, event):
        selected = self.tree_readers.selection()
        if not selected:
            return
        values = self.tree_readers.item(selected[0], "values")
        self.ent_reader_id.delete(0, tk.END)
        self.ent_reader_id.insert(0, values[0])
        self.ent_reader_name.delete(0, tk.END)
        self.ent_reader_name.insert(0, values[1])
        self.ent_reader_khoa.delete(0, tk.END)
        self.ent_reader_khoa.insert(0, values[2])
        self.ent_reader_nganh.delete(0, tk.END)
        self.ent_reader_nganh.insert(0, values[3])

    def add_reader(self):
        r_id = self.ent_reader_id.get()
        name = self.ent_reader_name.get()
        khoa = self.ent_reader_khoa.get()
        nganh = self.ent_reader_nganh.get()
        
        if not all([r_id, name, khoa, nganh]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
            
        success, msg = self.manager.add_reader(r_id, name, khoa, nganh)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_readers()
        else:
            messagebox.showerror("Lỗi", msg)

    def edit_reader(self):
        r_id = self.ent_reader_id.get()
        name = self.ent_reader_name.get()
        khoa = self.ent_reader_khoa.get()
        nganh = self.ent_reader_nganh.get()
        
        if not all([r_id, name, khoa, nganh]):
            messagebox.showerror("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
            
        success, msg = self.manager.edit_reader(r_id, name, khoa, nganh)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_readers()
        else:
            messagebox.showerror("Lỗi", msg)

    def search_reader(self):
        keyword = self.ent_reader_id.get() or self.ent_reader_name.get()
        if not keyword:
            self.refresh_readers()
            return
        results = self.manager.search_readers(keyword)
        self.update_readers_tree(results)

    def pay_fine(self):
        r_id = self.ent_reader_id.get()
        if not r_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn hoặc nhập Mã Sinh Viên!")
            return
            
        reader = self.manager.readers.find(lambda r: r.reader_id == r_id)
        if not reader:
            messagebox.showerror("Lỗi", "Không tìm thấy sinh viên.")
            return
            
        if reader.unpaid_fine <= 0:
            messagebox.showinfo("Thông báo", "Sinh viên không nợ phí phạt.")
            return

        amount = simpledialog.askinteger(
            "Thanh toán phí", 
            f"Sinh viên {reader.name} đang nợ: {reader.unpaid_fine} VND\nNhập số tiền muốn thanh toán:", 
            minvalue=1000
        )
        if amount is None:
            return
            
        success, msg = self.manager.pay_fine(r_id, amount)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_readers()
        else:
            messagebox.showerror("Lỗi", msg)

    def refresh_readers(self):
        self.update_readers_tree(self.manager.readers)

    def update_readers_tree(self, readers_list):
        for row in self.tree_readers.get_children():
            self.tree_readers.delete(row)
        for reader in readers_list:
            borrowed_count = self.manager.get_borrowed_count(reader.reader_id)
            limit = self.manager.borrow_limit
            borrow_str = f"{borrowed_count}/{limit}"
            fine_str = f"{reader.unpaid_fine} đ" if reader.unpaid_fine > 0 else "0 đ"
            self.tree_readers.insert("", "end", values=(reader.reader_id, reader.name, reader.khoa, reader.nganh, borrow_str, fine_str))

    def import_readers_file(self):
        filepath = filedialog.askopenfilename(
            title="Chọn file bạn đọc",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if not filepath:
            return
        success, msg = self.manager.import_readers(filepath)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_readers()
        else:
            messagebox.showerror("Lỗi", msg)

    # --- MƯỢN TRẢ ---
    def setup_borrow_tab(self):
        frame_input = ttk.LabelFrame(self.tab_borrow, text="Thao Tác Mượn / Trả")
        frame_input.pack(fill='x', padx=10, pady=5)
        
        ttk.Label(frame_input, text="Mã Sinh Viên:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.ent_bor_reader = ttk.Entry(frame_input)
        self.ent_bor_reader.grid(row=0, column=1, padx=5, pady=5)
        self.ent_bor_reader.bind("<KeyRelease>", self.on_bor_reader_change)
        
        ttk.Label(frame_input, text="Mã Sách:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.ent_bor_book = ttk.Entry(frame_input)
        self.ent_bor_book.grid(row=0, column=3, padx=5, pady=5)
        self.ent_bor_book.bind("<KeyRelease>", self.on_bor_book_change)
        
        ttk.Label(frame_input, text="Ngày Mượn (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.ent_bor_date = ttk.Entry(frame_input, width=15)
        self.ent_bor_date.grid(row=0, column=5, padx=5, pady=5)
        
        ttk.Button(frame_input, text="Mượn Sách", command=self.borrow_book).grid(row=0, column=6, padx=5, pady=5)
        
        self.lbl_bor_reader_info = ttk.Label(frame_input, text="", foreground="blue")
        self.lbl_bor_reader_info.grid(row=1, column=1, padx=5, sticky='w')
        
        self.lbl_bor_book_info = ttk.Label(frame_input, text="", foreground="blue")
        self.lbl_bor_book_info.grid(row=1, column=3, padx=5, sticky='w')
        
        ttk.Separator(frame_input, orient='horizontal').grid(row=2, column=0, columnspan=7, sticky='ew', pady=10)
        
        ttk.Label(frame_input, text="Mã Bản Ghi (Record ID):").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.ent_ret_record = ttk.Entry(frame_input)
        self.ent_ret_record.grid(row=3, column=1, padx=5, pady=5)
        self.ent_ret_record.bind("<KeyRelease>", self.on_ret_record_change)
        
        ttk.Label(frame_input, text="Ngày Trả (YYYY-MM-DD):").grid(row=3, column=2, padx=5, pady=5, sticky='e')
        self.ent_ret_date = ttk.Entry(frame_input, width=15)
        self.ent_ret_date.grid(row=3, column=3, padx=5, pady=5)
        
        ttk.Button(frame_input, text="Trả Sách", command=self.return_book).grid(row=3, column=4, padx=5, pady=5)
        
        self.lbl_ret_record_info = ttk.Label(frame_input, text="", foreground="blue")
        self.lbl_ret_record_info.grid(row=4, column=1, columnspan=2, padx=5, sticky='w')
        
        columns = ("rec_id", "reader", "book", "borrow_date", "exp_ret", "act_ret")
        self.tree_records = ttk.Treeview(self.tab_borrow, columns=columns, show='headings')
        self.tree_records.heading("rec_id", text="Mã Bản Ghi")
        self.tree_records.heading("reader", text="Mã Sinh Viên")
        self.tree_records.heading("book", text="Mã Sách")
        self.tree_records.heading("borrow_date", text="Ngày Mượn")
        self.tree_records.heading("exp_ret", text="Hạn Trả")
        self.tree_records.heading("act_ret", text="Ngày Trả Thực")
        
        self.tree_records.pack(expand=True, fill='both', padx=10, pady=5)
        self.tree_records.bind("<Double-1>", self.on_record_select)
        self.refresh_records()

    def on_record_select(self, event):
        selected = self.tree_records.selection()
        if not selected:
            return
        values = self.tree_records.item(selected[0], "values")
        self.ent_ret_record.delete(0, tk.END)
        self.ent_ret_record.insert(0, values[0])
        self.on_ret_record_change(None) # Trigger info update

    def on_bor_reader_change(self, event):
        r_id = self.ent_bor_reader.get()
        if not r_id:
            self.lbl_bor_reader_info.config(text="")
            return
        reader = self.manager.readers.find(lambda r: r.reader_id == r_id)
        if reader:
            borrowed_count = self.manager.get_borrowed_count(r_id)
            limit = self.manager.borrow_limit
            color = "blue"
            if borrowed_count >= limit or reader.unpaid_fine > 0:
                color = "red"
            fine_text = f" - Nợ: {reader.unpaid_fine}đ" if reader.unpaid_fine > 0 else ""
            self.lbl_bor_reader_info.config(text=f"Tên: {reader.name} (Đang mượn: {borrowed_count}/{limit}){fine_text}", foreground=color)
        else:
            self.lbl_bor_reader_info.config(text="Không tìm thấy SV", foreground="red")

    def on_bor_book_change(self, event):
        b_id = self.ent_bor_book.get()
        if not b_id:
            self.lbl_bor_book_info.config(text="")
            return
        book = self.manager.books.find(lambda b: b.book_id == b_id)
        if book:
            color = "blue" if book.available_quantity > 0 else "red"
            self.lbl_bor_book_info.config(text=f"{book.title} (Còn: {book.available_quantity})", foreground=color)
        else:
            self.lbl_bor_book_info.config(text="Không tìm thấy Sách", foreground="red")

    def on_ret_record_change(self, event):
        rec_id = self.ent_ret_record.get()
        if not rec_id:
            self.lbl_ret_record_info.config(text="")
            return
        record = self.manager.records.find(lambda r: r.record_id == rec_id)
        if record:
            status = "Đã trả" if record.actual_return_date else "Chưa trả"
            color = "blue" if not record.actual_return_date else "gray"
            self.lbl_ret_record_info.config(text=f"SV: {record.reader_id} | Sách: {record.book_id} [{status}]", foreground=color)
        else:
            self.lbl_ret_record_info.config(text="Không tìm thấy Bản Ghi", foreground="red")

    def borrow_book(self):
        r_id = self.ent_bor_reader.get()
        b_id = self.ent_bor_book.get()
        bor_date = self.ent_bor_date.get()
        
        if not r_id or not b_id:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã Sinh Viên và Mã Sách!")
            return
            
        success, msg = self.manager.borrow_book(r_id, b_id, bor_date)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.refresh_records()
            self.refresh_books()
        else:
            messagebox.showerror("Lỗi", msg)

    def return_book(self):
        rec_id = self.ent_ret_record.get()
        ret_date = self.ent_ret_date.get()
        if not rec_id:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã Bản Ghi (Record ID)!")
            return
            
        success, msg, fine = self.manager.return_book(rec_id, ret_date)
        if success:
            if fine > 0:
                messagebox.showwarning("Trả thành công", f"Trả sách thành công.\nBạn bị phạt: {fine} VND do quá hạn!")
            else:
                messagebox.showinfo("Thành công", msg)
            self.refresh_records()
            self.refresh_books()
        else:
            messagebox.showerror("Lỗi", msg)

    def refresh_records(self):
        for row in self.tree_records.get_children():
            self.tree_records.delete(row)
        for rec in self.manager.records:
            self.tree_records.insert("", "end", values=(
                rec.record_id, rec.reader_id, rec.book_id,
                rec.borrow_date, rec.expected_return_date, rec.actual_return_date
            ))

    # --- BÁO CÁO ---
    def setup_reports_tab(self):
        frame_btn = ttk.Frame(self.tab_reports)
        frame_btn.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(frame_btn, text="Sách Đang Mượn", command=self.report_borrowed).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Sách Quá Hạn", command=self.report_overdue).pack(side='left', padx=5)
        ttk.Button(frame_btn, text="Top 5 Mượn Nhiều Nhất", command=self.report_top_5).pack(side='left', padx=5)
        
        self.txt_report = tk.Text(self.tab_reports, font=('Consolas', 10))
        self.txt_report.pack(expand=True, fill='both', padx=10, pady=5)
        
    def write_report(self, title, items_list, formatter_func):
        self.txt_report.delete(1.0, tk.END)
        self.txt_report.insert(tk.END, f"=== {title} ===\n\n")
        if items_list.is_empty():
            self.txt_report.insert(tk.END, "Không có dữ liệu.\n")
            return
            
        count = 1
        for item in items_list:
            self.txt_report.insert(tk.END, f"{count}. {formatter_func(item)}\n")
            count += 1

    def report_borrowed(self):
        borrowed = self.manager.get_borrowed_books()
        def fmt(rec):
            return f"Mã Bản ghi: {rec.record_id} | Mã Sách: {rec.book_id} | Bạn đọc: {rec.reader_id} | Hạn trả: {rec.expected_return_date}"
        self.write_report("DANH SÁCH SÁCH ĐANG ĐƯỢC MƯỢN", borrowed, fmt)

    def report_overdue(self):
        overdue = self.manager.get_overdue_books()
        def fmt(rec):
            return f"Mã Bản ghi: {rec.record_id} | Mã Sách: {rec.book_id} | Bạn đọc: {rec.reader_id} | Hạn trả: {rec.expected_return_date} (QUÁ HẠN)"
        self.write_report("DANH SÁCH SÁCH QUÁ HẠN CHƯA TRẢ", overdue, fmt)

    def report_top_5(self):
        top5 = self.manager.get_top_5_books()
        def fmt(book):
            return f"Sách: {book.book_id} - {book.title} | Lượt mượn: {book.borrow_count}"
        self.write_report("TOP 5 SÁCH ĐƯỢC MƯỢN NHIỀU NHẤT", top5, fmt)


if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()
