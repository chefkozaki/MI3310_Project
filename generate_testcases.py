import os
import random

def generate_testcases():
    test_dir = os.path.dirname(os.path.abspath(__file__))
    books_file = os.path.join(test_dir, "books.txt")
    readers_file = os.path.join(test_dir, "readers.txt")
    
    # Dữ liệu mẫu thực tế cho Sách
    book_prefixes = ["Giáo trình", "Nhập môn", "Cơ sở", "Nâng cao", "Sổ tay", "Nghệ thuật", "Từ điển", "Cẩm nang", "Hướng dẫn", "Đại cương"]
    book_topics = [
        "Toán rời rạc", "Lập trình Python", "Cơ sở dữ liệu", "Cấu trúc dữ liệu và giải thuật", 
        "Mạng máy tính", "Trí tuệ nhân tạo", "Hệ điều hành", "Phân tích thiết kế hệ thống", 
        "Kinh tế vi mô", "Tâm lý học", "Triết học Mác - Lênin", "Vật lý đại cương", 
        "Hóa học", "Quản trị kinh doanh", "Marketing", "Kỹ năng giao tiếp", "Điện toán đám mây"
    ]
    real_books = [
        "Đắc Nhân Tâm", "Nhà Giả Kim", "Tội Ác Và Hình Phạt", "Hai Số Phận", 
        "Bố Già", "Lược Sử Loài Người", "Tư Duy Nhanh Và Chậm", "Sự Im Lặng Của Bầy Cừu"
    ]
    
    authors = [
        "Nguyễn Hữu Anh", "Lê Văn B", "Trần Thị C", "Vũ Minh D", "Phạm Hoàng E", 
        "Dale Carnegie", "Paulo Coelho", "Yuval Noah Harari", "Daniel Kahneman", 
        "Mario Puzo", "Thomas Harris", "Ngô Bảo Châu", "Lê Bá Khánh Trình", 
        "Nguyễn Nhật Ánh", "Tô Hoài", "Nam Cao", "Vũ Trọng Phụng"
    ]
    genres = ["Khoa học", "Giáo trình", "Văn học", "Kỹ thuật", "Kinh tế", "Lịch sử", "Tiểu thuyết", "Kỹ năng sống", "Tâm lý", "Ngoại ngữ"]
    
    # Dữ liệu mẫu thực tế cho Bạn đọc (Tên người Việt)
    ho_viet = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
    dem_nam = ["Văn", "Hữu", "Minh", "Đức", "Hoàng", "Xuân", "Quang", "Công", "Ngọc", "Thái", "Hải", "Đình"]
    dem_nu = ["Thị", "Ngọc", "Thu", "Phương", "Thanh", "Mai", "Kim", "Diễm", "Bích", "Hồng", "Tuyết", "Kiều"]
    ten_nam = ["Anh", "Bình", "Cường", "Dũng", "Đạt", "Hải", "Hùng", "Khoa", "Long", "Nam", "Phong", "Quân", "Sơn", "Thắng", "Thành", "Tuấn", "Việt"]
    ten_nu = ["An", "Châu", "Chi", "Hoa", "Hương", "Linh", "Ly", "Mai", "Nga", "Nhung", "Oanh", "Phương", "Quyên", "Thủy", "Trang", "Uyên", "Yến"]
    
    khoa_list = ["K64", "K65", "K66", "K67", "K68", "K69"]
    nganh_list = ["Khoa học máy tính", "Hệ thống thông tin", "Kỹ thuật phần mềm", "Toán tin", "Quản trị kinh doanh", "Kinh tế quốc tế", "Cơ điện tử"]

    print("Đang tạo 10000 testcases thực tế cho sách...")
    with open(books_file, "w", encoding="utf-8") as f:
        for i in range(1, 10001):
            book_id = f"B{i:05d}"
            
            # Tạo tên sách ngẫu nhiên hoặc lấy từ sách có thật
            if random.random() < 0.15:
                title = random.choice(real_books)
            else:
                title = f"{random.choice(book_prefixes)} {random.choice(book_topics)}"
                
            # Đôi khi thêm (Tập X) hoặc (Tái bản)
            rand_suffix = random.random()
            if rand_suffix < 0.2:
                title += f" (Tập {random.randint(1, 5)})"
            elif rand_suffix < 0.3:
                title += " (Tái bản)"
                
            author = random.choice(authors)
            genre = random.choice(genres)
            total = random.randint(3, 50)
            
            line = f"{book_id}|{title}|{author}|{genre}|{total}|{total}|0\n"
            f.write(line)
            
    print("Đang tạo 10000 testcases thực tế cho sinh viên...")
    with open(readers_file, "w", encoding="utf-8") as f:
        for i in range(1, 10001):
            # Mã SV: 202 + 6 số (chạy từ 000001 đến 010000)
            reader_id = f"202{i:06d}"
            
            # Tạo tên ngẫu nhiên
            ho = random.choice(ho_viet)
            if random.random() < 0.5: # Nam
                dem = random.choice(dem_nam)
                ten = random.choice(ten_nam)
            else: # Nữ
                dem = random.choice(dem_nu)
                ten = random.choice(ten_nu)
            
            # Thỉnh thoảng không có tên đệm
            if random.random() < 0.1:
                name = f"{ho} {ten}"
            else:
                name = f"{ho} {dem} {ten}"
                
            khoa = random.choice(khoa_list)
            nganh = random.choice(nganh_list)
                
            line = f"{reader_id}|{name}|{khoa}|{nganh}\n"
            f.write(line)
            
    print("Tạo dữ liệu mẫu thực tế thành công!")
    print(f"- File sách: {books_file}")
    print(f"- File sinh viên: {readers_file}")

if __name__ == "__main__":
    generate_testcases()
