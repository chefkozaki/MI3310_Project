import os
from data_structures import LinkedList
from models import Book, Reader

def load_objects_from_file(filepath, factory_func):
    """Đọc file và chuyển đổi thành đối tượng thông qua factory_func"""
    result = LinkedList()
    if not os.path.exists(filepath):
        return result
        
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                if line.strip():
                    obj = factory_func(line)
                    if obj:
                        result.append(obj)
                line = f.readline()
    except Exception as e:
        print(f"Lỗi khi đọc file {filepath}: {e}")
        
    return result

def save_objects_to_file(filepath, linked_list):
    """Lưu danh sách đối tượng vào file"""
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            for item in linked_list:
                f.write(item.to_string() + "\n")
        return True, "Lưu file thành công."
    except Exception as e:
        return False, f"Lỗi khi lưu file {filepath}: {e}"

def import_books_from_file(filepath, current_books):
    """Nhập sách từ file, làm mới bộ nhớ và nạp dữ liệu mới"""
    new_books = load_objects_from_file(filepath, Book.from_string)
    current_books.clear()
    count = 0
    for book in new_books:
        current_books.append(book)
        count += 1
    return True, f"Đã làm mới bộ nhớ và nạp {count} sách."

def import_readers_from_file(filepath, current_readers):
    """Nhập bạn đọc từ file, làm mới bộ nhớ và nạp dữ liệu mới"""
    new_readers = load_objects_from_file(filepath, Reader.from_string)
    current_readers.clear()
    count = 0
    for reader in new_readers:
        current_readers.append(reader)
        count += 1
    return True, f"Đã làm mới bộ nhớ và nạp {count} bạn đọc."
