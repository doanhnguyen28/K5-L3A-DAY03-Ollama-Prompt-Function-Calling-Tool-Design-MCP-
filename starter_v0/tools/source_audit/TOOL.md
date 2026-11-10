---
name: source_audit
track: bonus
kind: local_formatter
provider: local_python
requires_env: []
inputs: [items, require_https]
outputs: [total_count, structurally_complete_count, issues, note]
side_effect: false
---

# source_audit

## Mục tiêu
Kiểm tra cấu trúc nguồn tham khảo, xử lý cục bộ, kết quả xác định được.

## Đầu vào
`items: list[object], require_https: boolean`

## Đầu ra
Danh sách vấn đề: thiếu title/summary/URL, URL không hợp lệ, trùng URL, HTTP (tùy chọn). Khi input không hợp lệ, trả về từ điển `{"error": "...", "message": "..."}`, không ném ngoại lệ do lỗi input thông thường.

## Khi nào gọi / khi nào không gọi
Dùng khi user muốn rà soát nguồn hoặc trước khi xuất báo cáo; KHÔNG xác thực tính đúng/sai của bài viết.

## Triển khai
Hàm Python `tools/source_audit/tool.py`, cùng tên `source_audit`. Không yêu cầu khóa API. Không có tác dụng phụ.

## Hạn chế
Công cụ chỉ xử lý dữ liệu được cung cấp; không tự tải, truy cập, hoặc xác minh nội dung website.
