class Book:
    def __init__(self, book_id, title, author, genre, total_quantity, available_quantity, borrow_count=0):
        self.book_id = str(book_id)
        self.title = str(title)
        self.author = str(author)
        self.genre = str(genre)
        self.total_quantity = int(total_quantity)
        self.available_quantity = int(available_quantity)
        self.borrow_count = int(borrow_count)
        
    def to_string(self):
        return f"{self.book_id}|{self.title}|{self.author}|{self.genre}|{self.total_quantity}|{self.available_quantity}|{self.borrow_count}"
        
    @staticmethod
    def from_string(data_str):
        parts = data_str.strip().split('|')
        # Check length directly, avoiding built-in len() if absolutely constrained, but len() is a primitive function, not an advanced data structure. It's fine to use len().
        if len(parts) == 7:
            return Book(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6])
        return None

class Reader:
    def __init__(self, reader_id, name, khoa="", nganh="", unpaid_fine=0):
        self.reader_id = str(reader_id)
        self.name = str(name)
        self.khoa = str(khoa)
        self.nganh = str(nganh)
        self.unpaid_fine = int(unpaid_fine)
        
    def to_string(self):
        return f"{self.reader_id}|{self.name}|{self.khoa}|{self.nganh}|{self.unpaid_fine}"
        
    @staticmethod
    def from_string(data_str):
        parts = data_str.strip().split('|')
        if len(parts) >= 5:
            return Reader(parts[0], parts[1], parts[2], parts[3], parts[4])
        elif len(parts) == 4:
            return Reader(parts[0], parts[1], parts[2], parts[3])
        elif len(parts) == 2:
            return Reader(parts[0], parts[1])
        return None

class BorrowRecord:
    def __init__(self, record_id, reader_id, book_id, borrow_date, expected_return_date, actual_return_date=""):
        self.record_id = str(record_id)
        self.reader_id = str(reader_id)
        self.book_id = str(book_id)
        self.borrow_date = str(borrow_date) # YYYY-MM-DD format
        self.expected_return_date = str(expected_return_date)
        self.actual_return_date = str(actual_return_date)
        
    def to_string(self):
        return f"{self.record_id}|{self.reader_id}|{self.book_id}|{self.borrow_date}|{self.expected_return_date}|{self.actual_return_date}"
        
    @staticmethod
    def from_string(data_str):
        parts = data_str.strip().split('|')
        if len(parts) >= 5:
            actual_ret = parts[5] if len(parts) == 6 else ""
            return BorrowRecord(parts[0], parts[1], parts[2], parts[3], parts[4], actual_ret)
        return None
