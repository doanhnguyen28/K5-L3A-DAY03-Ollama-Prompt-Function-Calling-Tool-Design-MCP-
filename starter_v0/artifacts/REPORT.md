# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: Group 3
- Members: Người A (Prompt & Tools), Người B (Eval & Benchmark), Người C (Tool Engineer), Người D (UI & Demo)
- Provider/model: openrouter (openai/gpt-4o-mini)

---

# PHẦN A — Giới thiệu agent

## A1. Agent này làm được gì

Research Agent hỗ trợ nghiên cứu và tổng hợp thông tin đa nguồn tự động: tìm kiếm tin tức trên web (`lookup`), theo dõi bài đăng và tìm thảo luận trên mạng xã hội (`timeline`, `social_search`), đọc toàn văn bài viết từ URL (`fetch`, `papers`), xử lý làm sạch và kiểm định dữ liệu nguồn (`dedupe_sources`, `date_filter`, `source_audit`, `keyword_extract`), định dạng bản tin có cấu trúc markdown (`format`), và gửi bản tin qua Telegram (`send`) khi và chỉ khi có sự xác nhận rõ ràng của người dùng (`clarify`).

**Link dùng thử (deploy):**

> URL: http://localhost:8501 (Streamlit App cục bộ hoặc link public Cloudflare Tunnel do Người D cấu hình)

## A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng để làm rõ thông tin thiếu hoặc xin xác nhận yes/no trước khi thực hiện hành động ghi/gửi | không |
| timeline | Lấy danh sách các bài đăng (tweets) gần đây nhất từ một tài khoản cụ thể trên mạng xã hội Twitter/X | không |
| social_search | Tìm kiếm các bài thảo luận trên mạng xã hội Twitter/X theo từ khóa hoặc chủ đề | không |
| lookup | Tra cứu và tìm kiếm tin tức thời sự trên Internet qua web search engine | không |
| fetch | Tải và đọc toàn bộ nội dung văn bản từ một địa chỉ URL trang web cụ thể | không |
| format | Định dạng và tổng hợp danh sách tin bài thu thập được thành bản tin digest markdown có cấu trúc | không |
| send | Gửi thông điệp hoặc bản tin lên kênh Telegram bên ngoài khi đã được xác nhận (confirmed=True) | không |
| policy | Tra cứu quy định, chính sách nội bộ của công ty trong kho tài liệu markdown cục bộ | không |
| papers | Tìm kiếm bài báo khoa học, nghiên cứu học thuật trên arXiv theo từ khóa | không |
| paper_text | Tải PDF từ arXiv và trích xuất nội dung văn bản để đọc chi tiết | không |
| dedupe_sources | Loại bỏ nguồn trùng từ danh sách kết quả theo URL chuẩn hóa hoặc tiêu đề | **Có (Người C)** |
| date_filter | Lọc danh sách bài viết đã có theo khoảng ngày phát hành (start_date, end_date) | **Có (Người C)** |
| source_audit | Rà soát chất lượng cấu trúc danh sách nguồn: URL hợp lệ, định dạng HTTPS, tiêu đề, tóm tắt | **Có (Người C)** |
| keyword_extract | Trích xuất các từ khóa xuất hiện nhiều nhất trong văn bản theo tần suất từ | **Có (Người C)** |

## A3. Câu hỏi mẫu để thử

1. Tin tức về công nghệ Robotics trong tuần này có gì mới? Hãy tìm kiếm và tóm tắt giúp tôi.
2. Lấy 3 bài đăng gần nhất của Elon Musk (@elonmusk) trên mạng xã hội Twitter.
3. Đọc nội dung và tóm tắt bài báo nghiên cứu tại đường link: `https://arxiv.org/abs/2301.00001`
4. Lọc bỏ các bài báo trùng lặp và giữ lại các bài xuất bản từ ngày 2026-11-01 đến 2026-11-05 trong danh sách sau: `[{"title":"Tin A","url":"https://example.com/a","published_at":"2026-11-02"},{"title":"Tin A trùng","url":"https://example.com/a","published_at":"2026-11-02"},{"title":"Tin B","url":"https://example.com/b","published_at":"2026-11-08"}]`
5. Hãy chuẩn bị gửi bản tin tóm tắt này lên Telegram, lưu ý phải hỏi xác nhận tôi trước khi gửi.

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
| v4 | integrated | Nghiệm thu 10 case nhóm kết hợp 4 tool mới của Người C | 1.00 | 1.00 | runs/v4_B_group_openrouter_20261110T141310183368.json |

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

- **Which fixes belonged in `system_prompt.md`?**
  - **Ranh giới an toàn và phạm vi tác vụ (Scope & Guardrails):** Cấm gọi tool đối với các câu hỏi ngoài phạm vi (như lập trình Python hay giải bài toán tích phân), yêu cầu trả lời từ chối trực tiếp bằng lời một cách lịch sự.
  - **Chính sách xử lý thiếu thông tin bắt buộc (Missing Information):** Bắt buộc gọi `clarify(response_type='text')` khi người dùng chưa cung cấp đủ định danh (tên tài khoản khi xem tweet, URL bài viết khi đọc báo) thay vì để mô hình tự suy đoán handle hay bịa đặt URL.
  - **Quy trình xác nhận hành vi ghi (Action Confirmation):** Quy định nghiêm ngặt: mọi hành động phát sinh tác động bên ngoài (như gửi tin nhắn Telegram `send`) bắt buộc phải xin xác nhận đồng ý của người dùng qua `clarify(response_type='yes_no')`.
  - **Theo dõi và chuyển đổi ngữ cảnh đa lượt (Multi-turn Context Persistence):** Yêu cầu mô hình cập nhật trạng thái liên tục; khi người dùng đổi ý hoặc hủy bỏ yêu cầu trước đó (ví dụ: chuyển từ Twitter sang Web), lập tức dừng gọi các tool liên quan đến yêu cầu đã hủy.

- **Which fixes belonged in `tools.yaml`?**
  - **Phân định ranh giới chức năng qua Description:** Bổ sung cấu trúc chuẩn hóa `DÙNG KHI:` và `KHÔNG DÙNG KHI:` trong mô tả của từng tool, giúp LLM phân biệt chính xác các cặp tool có độ tương đồng ngữ nghĩa cao (`lookup` tin tức tổng quát vs `social_search` thảo luận mạng xã hội; `timeline` lấy bài cá nhân cụ thể vs `social_search` tìm từ khóa; `fetch` đọc URL cụ thể vs `lookup` tìm kiếm).
  - **Chuẩn hóa quy ước tham số (Argument Convention):** Quy định rõ trong tham số `query` của tool `lookup` chỉ chứa các từ khóa cốt lõi cần tra cứu, loại bỏ việc model tự ý chèn các từ chỉ thời gian ("hôm nay", "tuần này") vào query vì các yếu tố này đã được quản lý chuyên biệt bởi tham số `timeframe` và `topic`.

- **Which failure needed manual review instead of automatic grading?**
  - Các ca kiểm thử ngoài phạm vi (`out_of_scope` như case R08 giải toán, R14 viết code Python): Bộ kiểm thử tự động chỉ xác minh điều kiện kỹ thuật là mô hình không được gọi bất kỳ tool nào (`tool_calls == []`). Tuy nhiên, chất lượng thực tế của câu trả lời văn bản (tính lịch sự, thái độ từ chối khéo léo, giải thích rõ phạm vi hoạt động của Research Agent) bắt buộc phải do con người trực tiếp đọc và đánh giá.

- **What would you improve next?**
  - **Tối ưu hóa độ trễ (Latency):** Hỗ trợ gọi song song độc lập (parallel tool calling) khi các tham số không bị phụ thuộc dữ liệu vào nhau nhằm giảm thiểu thời gian phản hồi cho chuỗi tác vụ phức tạp.
  - **Khả năng tự phục hồi và thích ứng (Graceful Degradation & Self-Correction):** Bổ sung cơ chế fallback dự phòng khi các API bên ngoài gặp sự cố mạng hoặc cạn kiệt quota (tự động thông báo rõ ràng cho người dùng thay vì làm gián đoạn luồng), và hướng dẫn model tự động chỉnh sửa tham số (self-correction) khi tool trả về thông báo lỗi định dạng dữ liệu.

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
