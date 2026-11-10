---
name: date_filter
track: bonus
kind: local_formatter
provider: local_python
requires_env: []
inputs: [items, start_date, end_date, include_undated]
outputs: [items, input_count, output_count, undated_count, start_date, end_date]
side_effect: false
---

# date_filter

## Mục tiêu
Lọc bài viết theo ngày phát hành, xử lý cục bộ, kết quả xác định được.

## Đầu vào
`items: list[object], start_date: YYYY-MM-DD, end_date: YYYY-MM-DD, include_undated: boolean`. Mỗi item có thể có `published_at`, `published_date`, `published`, `date`, hoặc `created_at`; chấp nhận ngày ISO và chuỗi ngày kiểu RFC 2822.

## Đầu ra
Danh sách items trong khoảng ngày (kể cả hai đầu); báo số item thiếu ngày. Khi input không hợp lệ, trả về từ điển `{"error": "...", "message": "..."}`, không ném ngoại lệ do lỗi input thông thường.

## Khi nào gọi / khi nào không gọi
Dùng sau khi có các item có ngày xuất bản; không dùng thay cho lookup để tìm nguồn.

## Triển khai
Hàm Python `tools/date_filter/tool.py`, cùng tên `date_filter`. Không yêu cầu khóa API. Không có tác dụng phụ.

## Hạn chế
Công cụ chỉ xử lý dữ liệu được cung cấp; không tự tải, truy cập, hoặc xác minh nội dung website.
