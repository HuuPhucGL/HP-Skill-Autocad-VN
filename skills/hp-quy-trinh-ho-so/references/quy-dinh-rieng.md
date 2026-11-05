# Quy định riêng của bộ HP Skill Autocad VN

Những quy định dưới đây ưu tiên hơn số mặc định trong skill và trong bộ mẫu.

## Phạm vi

- Công trình chính: nhà phố, nhà ở.
- Bộ môn chính: kiến trúc. Phần kết cấu, cơ điện giữ lại nhưng chỉ làm khi được yêu cầu.
- Bốc tách mặc định: phần thô. Hỏi lại danh mục công tác của phần thô trước khi tính.

## Bản vẽ

- Đơn vị mm, vẽ tỷ lệ 1:1 trong Model. Khổ giấy chủ yếu A3.
- **Tỷ lệ in mặc định 1/50.** Dự án mới đặt `SC = "1/50"` ở đầu mỗi file vẽ và truyền tỷ lệ tường
  minh cho mọi hàm. Không dựa vào giá trị mặc định `1/100` của thư viện.
- Đánh số bản vẽ `KT-01`, `KT-02`...
- Hỏi trước ở mỗi dự án mới: trình bày bằng Layout + Viewport hay in từ Model.
- Font Unicode (Arial, Times New Roman), không dùng VNI, TCVN3, SHX cho chữ có dấu.
- In bằng file CTB theo màu. Chưa có file CTB thì hỏi lại.

## Kiểm tra khổ giấy trước khi chọn 1/50

Ở 1/50, 1 m ngoài thực tế dài 20 mm trên giấy. Vùng khung bản vẽ A3 rộng 390 mm. Theo các hằng số
trong `hpcad/standards.py`, ba lớp kích thước cộng bong bóng trục chiếm khoảng 42 mm mỗi bên.
Vì vậy mặt bằng có kích thước hai bên chỉ đặt vừa khi chiều dài nhà không quá khoảng **15,3 m**
(`(390 - 2 x 42) x 50`). Nhà dài hơn: báo lại để chọn cắt mặt bằng, khổ lớn hơn, hoặc tỷ lệ khác.
Không tự đổi tỷ lệ. Bộ mẫu nhà 18 m giữ 1/100 cũng vì lý do này.

## Khung tên và tài nguyên chưa có

- Chưa có: file mẫu `.dwt`, khung tên A3, file CTB, định mức nội bộ, nguồn đơn giá, mẫu Excel.
- Khi công việc cần đến các mục trên: hỏi lại, không tự giả định.
- Khung tên do thư viện vẽ chỉ là **bản tạm**, luôn in nhãn `KHUNG TEN TAM - CHUA DUYET`. Không
  giao cho khách bản còn nhãn này. Khung tên riêng được duyệt thì đặt `khung_ten_da_duyet = True`.

## Annotative

Quy định là Text style và Dim style dùng Annotative. Thư viện `hpcad` hiện **chưa làm được**: chữ
và kích thước được vẽ theo chiều cao quy đổi của từng tỷ lệ. Nói rõ điều này khi bàn giao file DXF.

## Bốc tách và dự toán

- Hỏi dự án dùng định mức nào trước khi tính. Không lấy số trong bộ mẫu làm định mức.
- Quy đổi về m, m², m³, kg hoặc tấn. Khối lượng làm tròn 2 số lẻ.
- Mỗi hạng mục có diễn giải cách tính và ghi rõ phần trừ, nhập ở cột `Dien giai, phan tru`.
- Excel dùng công thức. Tỷ lệ chi phí chung, dự phòng, thuế phải được hỏi và nhập vào ô riêng.

## Thư mục và file

- Tên dự án và tên file: `YYMMDD - Tên dự án - Địa chỉ`.
- Thư mục dự án gồm `01-Ho so dau vao`, `02-Ban ve CAD`, `03-PDF xuat ban`,
  `04-Boc tach du toan`, `_backup`.
- Không ghi đè, không xóa file bản vẽ gốc. Lưu bản mới bằng cách đổi ngày ở đầu tên file.
- Trước khi sửa file có sẵn, chép bản gốc vào `_backup/YYMMDD/` của dự án.
- Không xóa file hay thư mục khi chưa hỏi.

## Độ chính xác

- Không bịa số hiệu tiêu chuẩn, điều khoản, số liệu. Chưa chắc thì ghi "cần kiểm tra".
- Tách rõ số liệu gốc và ý kiến đề xuất.
- Nhắc kiểm tra hiệu lực tiêu chuẩn trước khi đưa vào hồ sơ.
