# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team:
- Members:
- Provider/model:

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL: 

## A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

## A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

---

# PHẦN B — Chi tiết / Bằng chứng

## B1. Version Evidence

Fill from `artifacts/version_log.csv` and `runs/*.json`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đo hành vi chưa tối ưu trước khi sửa | - | 0.70 | runs/v0_B_base_openrouter_20261110T100630816017.json |
| v1 | system_prompt.md | Bỏ 3 chỉ dẫn xấu, thêm clarify khi thiếu info và confirm khi gửi | 0.70 | 0.95 | runs/v1_B_base_openrouter_20261110T102046612325.json |
| v2 | tools.yaml | Viết lại description chi tiết (when to use/not) và convention tham số | 0.95 | 0.85 | runs/v2_B_base_openrouter_20261110T103033842772.json |
| v3 | system_prompt.md | Phân định rõ clarify vs timeline, rút gọn query lookup | 0.85 | 1.00 | runs/v3_B_base_openrouter_20261110T105653574448.json |

## B2. Failure Analysis

Use actual failures from `results[*].result.failures`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| R08_out_of_scope | out_of_scope | [lookup] | Cố gọi tool cho bài toán tích phân | Thêm rule trong prompt: câu hỏi ngoài phạm vi research không gọi tool, trả lời trực tiếp |
| R10_missing_handle | missing_info | [timeline] (đoán handle) | Tự đoán handle người nổi tiếng thay vì hỏi | Thêm rule: thiếu người/handle thì gọi clarify(response_type='text') |
| R11_missing_url | missing_info | [fetch] (bịa URL) | Tự bịa URL khi user không cung cấp link | Thêm rule: thiếu URL thì gọi clarify(response_type='text') |
| R12_confirm_before_send | wrong_boundary | [send(confirmed=true)] | Tự động gửi tin nhắn Telegram không xin phép | Thêm rule: hành động ghi/gửi phải xin xác nhận clarify(response_type='yes_no') |
| R13_parallel_web_and_tweets | wrong_tool | [lookup] | Chỉ gọi 1 tool duy nhất (do starter ép 1 bước) | Thêm rule: gọi song song nhiều tool khi user yêu cầu cả web và mạng xã hội |
| R14_out_of_scope_coding | out_of_scope | [lookup] | Cố gọi tool khi user nhờ viết code Python | Bổ sung rule out-of-scope xử lý câu hỏi lập trình |
| M06_switch_tool | wrong_tool | [lookup, social_search] | Giữ lại tool cũ Twitter khi user đã bảo bỏ | Thêm rule theo dõi ngữ cảnh: ngừng gọi tool bị hủy khi user chuyển tool |

## B3. Team Eval Cases

List the 10 cases added to `data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

## B4. Live Chat Evidence

Use `transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

## B5. Bonus Evidence

Only fill if your team did bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| send (Telegram) |  |  |  |
| arXiv/company policy |  |  |  |
| UI |  |  |  |
| Tool unit tests (`tests/`) | `pytest` output |  |  |

Tool unit tests: số test đã viết, số bug tìm được trong tool có sẵn (nếu có), và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

## B6. Reflection

- Which fixes belonged in `system_prompt.md`?
- Which fixes belonged in `tools.yaml`?
- Which failure needed manual review instead of automatic grading?
- What would you improve next?

## B7. Small Local Model Challenge (bonus)

Only fill if your team did the local model challenge.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v3-... | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?
