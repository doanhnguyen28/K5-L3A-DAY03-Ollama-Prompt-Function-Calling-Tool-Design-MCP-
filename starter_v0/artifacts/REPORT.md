# Day 03 Lab v2 Report — Research Agent

> File này gồm 2 phần, deadline khác nhau:
> - **PHẦN A — Giới thiệu agent**: ngắn gọn 1 trang để team khác hiểu nhanh agent có tool gì, làm được gì, thử bằng câu hỏi nào. **Xong trước 16:30** để làm tài liệu phụ trợ khi demo. Có thể làm thành poster HTML/SVG (`artifacts/poster.html` / `poster.svg`) để show cho team cùng zone.
> - **PHẦN B — Chi tiết / Bằng chứng**: bảng đầy đủ (v0–v3, failure, eval, chat) dựa trên log thật. **Có thể hoàn thiện sau buổi debate để nộp bài.**

## Team

- Team: Ollama
- Members: 
Nguyễn Đăng Doanh - 2A202603597
Đoàn Văn Tú - 2A202603595
Trần Đức Mạnh - 2A202603615
Lê Anh Quân - 2A202603576

- Provider/model: `openrouter` / `openai/gpt-4o-mini`

---

# PHẦN A — Giới thiệu. agent

## A1. Mục tiêu và chức năng

Research Agent hỗ trợ tìm tin trên web và Twitter/X, đọc nội dung từ URL, loại nguồn trùng, lọc theo ngày, trích từ khóa, rà soát cấu trúc nguồn và tổng hợp kết quả thành bản tin. Agent tự chọn công cụ phù hợp, hỏi lại khi thiếu thông tin, cập nhật yêu cầu qua nhiều lượt hội thoại và xin xác nhận trước khi gửi nội dung ra ngoài. Các bước xử lý danh sách nguồn được thực hiện cục bộ trên dữ liệu đã có, không cần thêm API hoặc tìm nguồn mới.


**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL: https://organ-clubs-polls-feel.trycloudflare.com

## A2. Công cụ trong phạm vi báo cáo

| Tool | Chức năng | Nhóm bổ sung |
|---|---|---|
| `clarify` | Hỏi thông tin còn thiếu hoặc xin xác nhận bằng `text`, `yes_no`, `choice`. | Không |
| `timeline` | Lấy bài đăng của một tài khoản Twitter/X; nhận `screenname`, `limit`. | Không |
| `social_search` | Tìm bài đăng theo chủ đề, chọn `Latest` hoặc `Top`. | Không |
| `lookup` | Tìm trên web, tách chủ đề, loại tin và khoảng thời gian. | Không |
| `fetch` | Đọc nội dung từ URL cụ thể. | Không |
| `format` | Định dạng danh sách kết quả thành bản tin Markdown. | Không |
| `dedupe_sources` | Chuẩn hóa khóa nhận diện nguồn để loại trùng; giữ bản đầu hoặc cuối. | Có |
| `date_filter` | Lọc theo khoảng ngày, bao gồm hai ngày biên; tùy chọn giữ mục không có ngày đọc được. | Có |
| `keyword_extract` | Trích từ khóa theo tần suất từ văn bản có sẵn. | Có |
| `source_audit` | Phát hiện thiếu trường, URL không hợp lệ, URL trùng và HTTP khi yêu cầu HTTPS. | Có |

## A3. Yêu cầu mẫu

1. “Lấy 3 tweet mới nhất của @sama.”
2. “Tìm tin AI hôm nay trên web và tìm thêm tweet về AI.”
3. “Tóm tắt bài viết này hộ tôi.” — Khi chưa có URL, agent cần hỏi lại.
4. “Loại nguồn trùng, giữ bản cuối: [{"title":"Bản đầu","url":"https://example.com/a"},{"title":"Bản cuối","url":"https://example.com/a"}].”
5. “Rà soát cấu trúc nguồn này và yêu cầu HTTPS; chỉ báo lỗi, không sửa dữ liệu: [{"title":"Tin A","url":"http://example.com/a","summary":"Tin về robot."}].”


# PHẦN B — Chi tiết và bằng chứng

## B1. Version Evidence

Bộ base gồm **20 case: 14 một lượt và 6 nhiều lượt**.

| Phiên bản/run | PASS | Case accuracy | Tool routing | Argument accuracy | Multiturn accuracy |
|---|---:|---:|---:|---:|---:|
| v0 | 14/20 | 70% | 75% | 70% | 100.00% |
| v1 | 19/20 | 95% | 95% | 95% | 83.33% |
| v2 | 17/20 | 85% | 95% | 85% | 83.33% |
| v3 — lần 1 | 19/20 | 95% | 95% | 95% | 100.00% |
| v3 — lần 2 | 20/20 | 100% | 100% | 100% | 100.00% |



| Phiên bản | Thay đổi/giả thuyết được ghi nhận | Accuracy trước → sau |
|---|---|---|
| v0 | Đo hành vi baseline trước khi tối ưu. | — → 70% |
| v1 | Bỏ chỉ dẫn gây đoán thông tin; bổ sung quy tắc hỏi lại và xác nhận. | 70% → 95% |
| v2 | Làm rõ khi dùng/không dùng từng tool và quy ước tham số. | 95% → 85% |
| v3 — lần 1 | Sau điều chỉnh, chỉ còn lỗi hỏi xác nhận không cần thiết ở R01. | 85% → 95% |
| v3 — lần 2 | Prompt phân biệt thiếu tài khoản với tên người đã rõ; tách từ khóa khỏi thời gian và loại tin. | 95% → 100% |

Các thay đổi và giả thuyết được đối chiếu với `artifacts/version_log.csv`, không xem mức tăng/giảm là bằng chứng nhân quả độc lập. Hash cho thấy cả prompt và tools đều đổi ở bước v1 → v2 và v2 → v3; cần thí nghiệm mỗi lần chỉ đổi một artifact để tách ảnh hưởng.

**Định danh bằng chứng:**

| Run | Prompt hash | Tools hash | File |
|---|---|---|---|
| v0 | `eb1c8179815bd79d34de7d326420bb99b3072e6e8ae96464c02d4411f905fc68` | `5b22a2476d41b989d5dc1e54f24ce7890e781909deb2f7afafb856ab53a6d7c0` | [runs/v0_B_base_openrouter_20261110T100630816017.json](https://github.com/doanhnguyen28/K5-L3A-DAY03-Ollama-Prompt-Function-Calling-Tool-Design-MCP-/blob/1a9054ab8216fa2ef80e30e2efde138213cc2bce/starter_v0/runs/v0_B_base_openrouter_20261110T100630816017.json) |
| v1 | `347b7c87ef949eb30e9b347ca02f392594c7e1f3f85a2491f1b086e8af720274` | `5b22a2476d41b989d5dc1e54f24ce7890e781909deb2f7afafb856ab53a6d7c0` | [runs/v1_B_base_openrouter_20261110T102046612325.json](https://github.com/doanhnguyen28/K5-L3A-DAY03-Ollama-Prompt-Function-Calling-Tool-Design-MCP-/blob/1a9054ab8216fa2ef80e30e2efde138213cc2bce/starter_v0/runs/v1_B_base_openrouter_20261110T102046612325.json) |
| v2 | `6329e62aa15cd021036fe3a5aea02a6fe8e621cecd94027d1628ca7c5234e086` | `20f89e93c623dd1652b0579bd7dbb5290ac28ffca35eb1dcf724c44667aa9330` | [runs/v2_B_base_openrouter_20261110T103033842772.json](https://github.com/doanhnguyen28/K5-L3A-DAY03-Ollama-Prompt-Function-Calling-Tool-Design-MCP-/blob/1a9054ab8216fa2ef80e30e2efde138213cc2bce/starter_v0/runs/v2_B_base_openrouter_20261110T103033842772.json) |
| v3 lần 1 | `8f11da2094179feb0037687b800e169a406f41707f4f9ec8c6d5add828292575` | `a49d622ccf4c0bebc9294a262634db377cf9787252a3f81af30b82cfe85e0510` | [runs/v3_B_base_openrouter_20261110T104718293787.json](https://github.com/doanhnguyen28/K5-L3A-DAY03-Ollama-Prompt-Function-Calling-Tool-Design-MCP-/blob/1a9054ab8216fa2ef80e30e2efde138213cc2bce/starter_v0/runs/v3_B_base_openrouter_20261110T104718293787.json) |
| v3 lần 2 | `4c296f7a161b93d5ef2bc2487328421f730c5aa41e6f5da8917e5afe7795fea8` | `a49d622ccf4c0bebc9294a262634db377cf9787252a3f81af30b82cfe85e0510` | [runs/v3_B_base_openrouter_20261110T105653574448.json](https://github.com/doanhnguyen28/K5-L3A-DAY03-Ollama-Prompt-Function-Calling-Tool-Design-MCP-/blob/1a9054ab8216fa2ef80e30e2efde138213cc2bce/starter_v0/runs/v3_B_base_openrouter_20261110T105653574448.json) |


## B2. Failure Analysis

| Run / case | Nhãn case | Hành vi thực tế và nguyên nhân quan sát được | Hướng sửa |
|---|---|---|---|
| v0 / R08 | `out_of_scope` | Gọi `send` để đưa ra câu trả lời toán học; kỳ vọng không gọi tool. | Quy định câu ngoài phạm vi trả lời/từ chối bằng văn bản; không dùng tool gửi để trả lời chat. |
| v0 / R10 | `missing_info` | Gọi `timeline(screenname="sama")` dù chưa có người/tài khoản. | Thiếu tài khoản phải `clarify(response_type="text")`; không tự chọn người. |
| v0 / R11 | `missing_info` | Gọi `fetch` với URL tự điền `https://example.com/article`. | Chỉ đọc URL người dùng đã cung cấp hoặc có trong ngữ cảnh; thiếu URL thì hỏi lại. |
| v0 / R12 | `wrong_boundary` | Gọi `send(text="Bản tin này")` thay vì hỏi xác nhận. | Dùng `clarify(response_type="yes_no")` trước hành động gửi. Log không có `confirmed=true`, không chứng minh đã gửi thành công. |
| v0 / R13 | `wrong_tool` | Đã gọi cả `lookup` và `social_search`; sai `query="AI news"` và thiếu `topic="news"`. | Sửa quy ước tham số: `query="AI"`, `topic="news"`, `timeframe="day"`. Không chẩn đoán thành thiếu tool thứ hai. |
| v0 / R14 | `out_of_scope` | Gọi `send` khi người dùng yêu cầu viết hàm Fibonacci. | Tách trả lời văn bản với hành động gửi ra ngoài. |
| v1, v2 / M06 | `wrong_tool` | Gọi cả `lookup` và `social_search` khi người dùng đã hủy Twitter; mismatch là `extra_tool_call`. | Ưu tiên yêu cầu mới nhất; giữ chủ đề nhưng bỏ nền tảng đã bị hủy. |
| v2 / R03, R13 | `wrong_tool` | Chọn đúng tool nhưng `query="tin tức AI hôm nay"` khác kỳ vọng `"AI"`; mismatch là `wrong_arg_value`. | Mô tả rõ việc chuyển thời gian và loại tin sang các trường riêng. |
| v3 lần 1 / R01 | `wrong_tool` | Gọi `clarify(yes_no)` hỏi có lấy tweet của Sam Altman không, thay vì `timeline`. | Không xin xác nhận cho thao tác đọc khi đã rõ tài khoản; phân biệt tên đã biết với tài khoản hoàn toàn chưa được cung cấp. |


## B3. Bộ đánh giá nhóm

Bộ đánh giá gồm **10 case: 5 một lượt và 5 nhiều lượt**, bao phủ bốn tool mới: `dedupe_sources`, `date_filter`, `keyword_extract` và `source_audit`.

Kết quả theo log `runs/v4_B_group_openrouter_20261110T141310183368.json` (v4) và `runs/v5_B_group_openrouter_20261110T221546153984.json` (v5, bản nộp), dataset `day04_v2_research_group`, model `openai/gpt-4o-mini`: **10/10 PASS** về chọn tool và tham số ở cả hai lần chạy.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| G01_dedupe_first | Một lượt: loại nguồn trùng, giữ bản đầu tiên. | Gọi `dedupe_sources`, truyền nguyên danh sách và `keep="first"`. | PASS |
| G02_filter_dates | Một lượt: lọc theo khoảng ngày, tính cả hai ngày biên và bỏ mục thiếu ngày. | Gọi `date_filter`, từ `2026-11-01` đến `2026-11-05`, `include_undated=false`. | PASS |
| G03_extract_keywords | Một lượt: trích từ khóa từ văn bản có sẵn. | Gọi `keyword_extract`, giữ nguyên văn bản và `max_keywords=3`. | PASS |
| G04_audit_sources | Một lượt: phát hiện lỗi cấu trúc nguồn và kiểm tra HTTPS. | Gọi `source_audit`, `require_https=true`; không tự sửa dữ liệu đầu vào. | PASS |
| G05_missing_account | Một lượt: hỏi lại khi chưa có tài khoản. | Gọi `clarify`, `response_type="text"`; không đoán handle. | PASS |
| G06_dedupe_change_keep | Nhiều lượt: đổi yêu cầu từ giữ bản đầu sang giữ bản cuối. | Gọi `dedupe_sources`, giữ danh sách từ ngữ cảnh và cập nhật `keep="last"`. | PASS |
| G07_filter_include_undated | Nhiều lượt: thay đổi yêu cầu để giữ cả mục thiếu ngày. | Gọi `date_filter`, giữ khoảng ngày và cập nhật `include_undated=true`. | PASS |
| G08_switch_to_web | Nhiều lượt: hủy tìm Twitter, chuyển sang web và giữ chủ đề. | Chỉ gọi `lookup`, `query="robotics"`, `topic="news"`, `timeframe="week"`. | PASS |
| G09_correct_handle_and_count | Nhiều lượt: sửa đồng thời tài khoản và số bài cần lấy. | Gọi `timeline`, `screenname="karpathy"`, `limit=2`. | PASS tool/args; API trả 403 khi thực thi. |
| G10_confirm_send | Nhiều lượt: hỏi xác nhận trước khi gửi nội dung. | Gọi `clarify`, `response_type="yes_no"`; chưa gọi `send`. | PASS |

**Nhận xét:** Cả 10 case đều chọn đúng tool và truyền đúng tham số theo evaluator. 


### Kết quả tổng hợp

| Chỉ số | Kết quả |
|---|---:|
| Tổng số case | 10 |
| Case được đo | 10 |
| Case PASS | **10/10** |
| Provider error cases | 0 |
| Case accuracy | **100%** |
| Tool routing accuracy | **100%** |
| Argument accuracy | **100%** |
| Multiturn accuracy | **100%** |
| Một lượt / nhiều lượt | **5/5 PASS / 5/5 PASS** |


### Kết quả từng case

| Case ID | Số lượt | Hành vi được kiểm tra và lời gọi thực tế | Chấm tool/args | Kết quả thực thi trong log |
|---|---:|---|---|---|
| G01_dedupe_first | 1 | `dedupe_sources`, truyền nguyên 3 nguồn, `keep="first"`. | PASS | Giữ Tin A và Tin B; loại 1 nguồn trùng. |
| G02_filter_dates | 1 | `date_filter`, từ `2026-11-01` đến `2026-11-05`, `include_undated=false`. | PASS | Giữ A, B ở hai ngày biên; loại C ngoài khoảng và D thiếu ngày. |
| G03_extract_keywords | 1 | `keyword_extract`, giữ nguyên văn bản, `max_keywords=3`. | PASS | Trả `robotics` (3), `automation` (2), `improves` (1). |
| G04_audit_sources | 1 | `source_audit`, giữ nguyên dữ liệu lỗi, `require_https=true`. | PASS | Báo `non_https_url` cho nguồn đầu và `invalid_or_missing_url` cho nguồn sau. |
| G05_missing_account | 1 | `clarify(response_type="text")`, hỏi tên/handle; không đoán tài khoản. | PASS | Trả câu hỏi và `awaiting_user=true`. |
| G06_dedupe_change_keep | 3 | `dedupe_sources`, cập nhật `keep="last"`, giữ nguyên danh sách từ ngữ cảnh. | PASS | Giữ Tin A cập nhật và Tin B; loại 1 nguồn trùng. |
| G07_filter_include_undated | 3 | `date_filter`, đổi `include_undated=true`, giữ khoảng ngày cũ. | PASS | Giữ A, B và D thiếu ngày; loại C ngoài khoảng. |
| G08_switch_to_web | 3 | Chỉ `lookup(query="robotics", topic="news", timeframe="week", max_results=5)`; không gọi Twitter. | PASS | Trả danh sách kết quả web. |
| G09_correct_handle_and_count | 3 | `timeline(screenname="karpathy", limit=2)` thay yêu cầu cũ. | PASS | Tool trả `HTTPError: 403 Forbidden` từ RapidAPI; chưa lấy được tweet. |
| G10_confirm_send | 3 | `clarify(response_type="yes_no")`, hỏi xác nhận nội dung đã có; không gọi `send`. | PASS | Trả câu hỏi xác nhận và `awaiting_user=true`; không có hành động gửi. |



## B4. Live Chat Evidence

### B4.1. `chat.py` — bản nộp v5

Transcript: `transcripts/v5_openrouter_20261110T231208001759.transcript.json` · `artifact_version = v5+p4c296f7a161b+tf45ea6b2f037` · `openai/gpt-4o-mini`

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin tức AI hôm nay có gì nổi bật? | `lookup(query="AI", topic="news", timeframe="day")` | v5+p4c296f7a161b+tf45ea6b2f037 | Đúng tool và args; trả danh sách tin AI trong ngày kèm link nguồn. Lưu ý: câu hỏi tiếng Việt nhưng agent trả lời tiếng Anh. |
| 2 | Tóm tắt bài này hộ mình | `clarify(response_type="text")` — "Bạn vui lòng cung cấp URL của bài viết…" | v5 | Thiếu URL nên hỏi lại, không bịa link; trạng thái `waiting_for_user`. |
| 3 | https://openai.com/research/ | `fetch(url="https://openai.com/research/")` | v5 | Đọc đúng URL người dùng vừa cung cấp và tóm tắt nội dung trang. |
| 4 | Đăng bản tin này lên Telegram giúp mình | `clarify(response_type="yes_no")` — "Bạn có chắc chắn muốn đăng…?" | v5 | Hành động ghi ra ngoài nên xin xác nhận trước; chưa gọi `send`. |
| 5 | có gửi đi | `send(text="### Tóm tắt nội dung nghiên cứu của OpenAI…")` | v5 | Chỉ gọi `send` sau khi người dùng đồng ý; nội dung lấy từ bản tóm tắt ở lượt 3. Tool trả `RuntimeError: Missing TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID` vì nhóm chưa cấu hình Telegram, nên không gửi thật; agent báo lỗi trung thực. |

### B4.2. UI Streamlit — v5

Transcript: `transcripts/v5_openrouter_ui_20261110T230359622067.transcript.json` · `artifact_version = v5+p4c296f7a161b+tf45ea6b2f037`

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1–2 | Lấy 3 tweet mới nhất của Andrej Karpathy | `timeline(screenname="karpathy", limit=3)` | v5 | Map đúng tên → handle `karpathy` và `limit=3`. RapidAPI trả `403 Forbidden`; agent báo lỗi, không bịa nội dung tweet. |
| 3 | Cho mình các tweet phổ biến nhất về Claude | `social_search(query="Claude", search_type="Top", limit=5)` | v5 | Đúng tool và `search_type="Top"` cho "phổ biến nhất". RapidAPI `403`. |
| 4 | Lọc giúp mình các bài từ 2026-11-01 đến 2026-11-05: [Tin A 11-01, Tin B 11-07, Tin C 11-04] | `date_filter(items=[…], start_date="2026-11-01", end_date="2026-11-05")` | v5 | Tool mới của nhóm chạy đúng: giữ Tin A, Tin C; loại Tin B ngoài khoảng. |
| 5 | Đọc giúp mình bài báo đó | `clarify(response_type="text")` | v5 | Không có URL nên hỏi lại. |
| 6 | Dịch câu "Good morning" sang tiếng Pháp giúp mình | (không gọi tool) | v5 | ⚠️ Không gọi tool nhưng trả lời luôn "Bonjour" thay vì từ chối yêu cầu ngoài phạm vi research. Một case `no_tool` sẽ chấm PASS dù hành vi chưa đúng — cần đọc nội dung câu trả lời. |

### B4.3. `chat.py` — v3 (do A chạy, để đối chiếu)

Transcript: `transcripts/v3_openrouter_20261110T113150973727.transcript.json` · `artifact_version = v3+p22edbe5efdd5+t5d540b419f0f` (cùng nội dung prompt/tools v3 nhưng file ở dạng CRLF nên hash khác `version_log.csv`)

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Tin tức AI hôm nay có gì nổi bật? | `lookup(query="AI", topic="news", timeframe="day")` | v3 (CRLF) | Đúng tool và args. |
| 2 | Tóm tắt 5 tweet mới nhất giúp mình | `timeline(screenname="elonmusk", limit=5)` | v3 (CRLF) | ❌ Không nói tài khoản nhưng agent tự đoán `elonmusk` thay vì `clarify`. Cùng câu này là case R10 trong eval base và đã PASS — lỗi chỉ lộ ra khi chat nhiều lượt (lượt 1 về tin AI làm agent "đoán" theo ngữ cảnh). |
| 3 | Đăng bản tin này lên Telegram giúp mình | `clarify(response_type="yes_no")` | v3 (CRLF) | Xin xác nhận trước khi gửi. |

**Tổng kết B4:** Ở bản nộp v5, cả 5 lượt `chat.py` chọn đúng tool và args, bao gồm luồng hỏi lại → bổ sung URL và luồng xác nhận → gửi. Hai điểm eval tự động không bắt được, chỉ thấy khi chat live: (1) trả lời câu ngoài phạm vi thay vì từ chối (UI lượt 6), (2) tự đoán tài khoản khi thiếu thông tin trong ngữ cảnh nhiều lượt (v3 lượt 2). Lỗi 403 / thiếu env là lỗi cấu hình API, không phải lỗi routing.


## B5. Reflection

- **Which fixes belonged in `system_prompt.md`?**  
  Các quy tắc hành vi chung: hỏi lại khi thiếu thông tin, không đoán tài khoản hoặc URL, không xin xác nhận cho thao tác đọc khi thông tin đã đủ, xin xác nhận trước khi gửi và ưu tiên yêu cầu mới nhất trong hội thoại. Khi người dùng hủy Twitter và chuyển sang web, agent phải ngừng gọi tool Twitter nhưng giữ chủ đề đang trao đổi.

- **Which fixes belonged in `tools.yaml`?**  
  Làm rõ chức năng, khi dùng và không dùng từng tool; mô tả kiểu dữ liệu, giá trị hợp lệ và quy ước tham số. Ví dụ, `lookup` cần tách từ khóa khỏi `topic` và `timeframe`; các tool xử lý nguồn phải nhận nguyên danh sách, không để model tự sửa hoặc lọc trước. Cần phân biệt `source_audit` để báo lỗi cấu trúc với `dedupe_sources` để loại nguồn trùng.

- **Which failure needed manual review instead of automatic grading?**  
  G09 được chấm PASS vì gọi đúng `timeline(screenname="karpathy", limit=2)`, nhưng kết quả thực thi trả lỗi RapidAPI `403 Forbidden`. Vì vậy cần đọc `tool_results` để xác nhận agent có thực sự lấy được dữ liệu. Ngoài ra, các case không gọi tool cần kiểm tra nội dung trả lời, vì không gọi tool chưa chắc đã đáp ứng đúng yêu cầu.

- **What would you improve next?**  
  Xử lý lỗi RapidAPI 403 và kiểm tra lại việc lấy tweet; bổ sung transcript hội thoại thực tế. Giữ cố định bộ group hiện tại để chạy lặp, đồng thời thêm bộ kiểm thử với cách diễn đạt tự nhiên, ít chỉ dẫn hơn. Sau mỗi thay đổi, chạy lại cả base và group, lưu model cùng hash của artifact, và đánh giá riêng độ chính xác gọi tool với mức độ thành công khi thực thi.


