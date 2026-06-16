"""  
1. Việc gán trực tiếp order_table1.total_amount = 0 từ bên ngoài đang vi phạm tính chất cốt lõi nào?
    đang vi phạm tính chất đóng gói của OOP. dữ liệu phải được bảo vệ không dc phép sửa trực tiếp ở bên ngoài
2. Để ngăn chặn việc truy cập và gán giá trị tự do từ bên ngoài, 
ta cần đổi tên thuộc tính total_amount thành gì để kích hoạt cơ chế Name Mangling trong Python?
    ta đổi tên total_amount thành __total_amount để kích hoạt cơ chế Name Mangling 
3. Sau khi đã che giấu thuộc tính total_amount, nếu muốn các phần khác của chương trình 
vẫn có thể xem được tổng tiền (chỉ đọc, không được sửa), ta cần dùng Decorator nào ?
    Sử dụng @property.Điều này cho phép tạo một getter an toàn, chỉ đọc giá trị mà không cho phép gán trực tiếp

4.Tại dòng lệnh self.vat_rate = new_rate trong hàm update_vat_rate, 
Python thực chất đang làm hành động gì? (Gợi ý: Trả lời dựa trên sự khác nhau giữa biến Instance và biến Class).
    Python đang tạo một biến instance mới tên vat_rate cho riêng đối tượng đó, 
    thay vì thay đổi biến class CoffeeOrder.vat_rate. Do đó, chỉ hóa đơn của bàn đó thay đổi, 
    các bàn khác vẫn giữ giá trị cũ.
5. Để phương thức cập nhật thuế có thể thay đổi biến vat_rate cho toàn bộ các hóa đơn (đối tượng) 
trong cửa hàng, ta phải cấu trúc lại hàm update_vat_rate bằng Decorator nào và thay tham số self bằng tham số gì?
    dùng @classmethod. Khi đó tham số đầu tiên là cls thay vì self,
    và việc cập nhật sẽ tác động lên class attribute vat_rate, đồng bộ cho tất cả các đối tượng.
"""


# Hệ thống quản lý hóa đơn Rikkei Coffee
class CoffeeOrder:
    # Thuộc tính của lớp (Class Attribute)
    vat_rate = 0.10  # Mặc định thuế VAT là 10%

    def __init__(self, table_number):
        self.table_number = table_number
        self.__total_amount = 0  # Bảo vệ bằng Name Mangling

    # Phương thức thêm tiền món ăn vào hóa đơn
    def add_item(self, price):
        if price > 0:
            self.__total_amount += price

    @property
    def total_amount(self):
        return self.__total_amount

    # Tính tổng tiền khách phải trả (đã cộng VAT)
    def calculate_final_bill(self):
        return self.__total_amount + (self.__total_amount * CoffeeOrder.vat_rate)

    # Cập nhật VAT cho toàn hệ thống
    @classmethod
    def update_vat_rate(cls, new_rate):
        cls.vat_rate = new_rate


# --- KỊCH BẢN KIỂM CHỨNG ---
order_table1 = CoffeeOrder("Bàn 1")
order_table2 = CoffeeOrder("Bàn 2")

# Khách gọi món
order_table1.add_item(50000) # Bàn 1 gọi Cà phê sữa
order_table2.add_item(30000) # Bàn 2 gọi Trà đào

# 1. Nhân viên gian lận thử gán đè số tiền (KHÔNG THỂ vì __total_amount bị ẩn)
# order_table1.__total_amount = 0  # Không có tác dụng, bị Name Mangling

print(f"Tổng tiền Bàn 1 (chưa VAT): {order_table1.total_amount} VNĐ")
print(f"Tổng tiền Bàn 2 (chưa VAT): {order_table2.total_amount} VNĐ")

# 2. Quản lý cập nhật thuế VAT xuống 8% cho toàn hệ thống
CoffeeOrder.update_vat_rate(0.08)

print(f"Tổng tiền Bàn 1 (sau VAT): {order_table1.calculate_final_bill()} VNĐ")
print(f"Thuế VAT đang áp dụng cho Bàn 1: {CoffeeOrder.vat_rate}")
print(f"Thuế VAT đang áp dụng cho Bàn 2: {CoffeeOrder.vat_rate}")
