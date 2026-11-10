---
name: keyword_extract
track: bonus
kind: local_formatter
provider: local_python
requires_env: []
inputs: [text, max_keywords]
outputs: [keywords, total_tokens, candidate_tokens, method]
side_effect: false
---

# keyword_extract

## Mục tiêu
Trích từ khóa theo tần suất xuất hiện, xử lý cục bộ, kết quả xác định được.

## Đầu vào
`text: string, max_keywords: integer 1..20`

## Đầu ra
Danh sách từ khóa đếm theo tần suất, có loại bỏ từ dừng phổ biến. Khi input không hợp lệ, trả về từ điển `{"error": "...", "message": "..."}`, không ném ngoại lệ do lỗi input thông thường.

## Khi nào gọi / khi nào không gọi
Dùng khi user yêu cầu từ khóa từ một đoạn văn đã có; KHÔNG dùng khi muốn tìm web hay phân tích ngữ nghĩa sâu.

## Triển khai
Hàm Python `tools/keyword_extract/tool.py`, cùng tên `keyword_extract`. Không yêu cầu khóa API. Không có tác dụng phụ.

## Hạn chế
Công cụ chỉ xử lý dữ liệu được cung cấp; không tự tải, truy cập, hoặc xác minh nội dung website.
