---
name: dedupe_sources
track: bonus
kind: local_formatter
provider: local_python
requires_env: []
inputs: [items, keep]
outputs: [items, input_count, output_count, removed_count]
side_effect: false
---

# dedupe_sources

## Mục tiêu
Loại nguồn tìm kiếm trùng lặp, xử lý cục bộ, kết quả xác định được.

## Đầu vào
`items: list[object], keep: first|last`

## Đầu ra
Danh sách items không trùng dựa trên URL chuẩn hóa, hoặc tiêu đề nếu không có URL. Khi input không hợp lệ, trả về từ điển `{"error": "...", "message": "..."}`, không ném ngoại lệ do lỗi input thông thường.

## Khi nào gọi / khi nào không gọi
Dùng sau lookup, timeline, social_search khi dữ liệu có nguồn lặp; không dùng để tìm web.

## Triển khai
Hàm Python `tools/dedupe_sources/tool.py`, cùng tên `dedupe_sources`. Không yêu cầu khóa API. Không có tác dụng phụ.

## Hạn chế
Công cụ chỉ xử lý dữ liệu được cung cấp; không tự tải, truy cập, hoặc xác minh nội dung website.
