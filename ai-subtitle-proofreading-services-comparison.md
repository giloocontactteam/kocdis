# AI 字幕校對服務比較（2026-09-04）

> 目的：給 Stage 4（`04-localize/`）在地化階段挑外部字幕供應商用的參考。整理市面上「AI 字幕 + 人工校對」規模較大的服務商，比較交件時間、語種、定價和適合場景。
>
> 這份文件不對應特定影片，是工具評估，性質類似 SOP 裡的「競品觀察」。

---

## 光譜：先搞清楚在比什麼

市面上這些服務不是同一種東西，先分三層，不然定價會比錯：

| 層級 | 特色 | 代表服務 |
|------|------|---------|
| **純 AI（無人工）** | 全自動語音辨識 + 機器翻譯，最便宜最快，但沒有人把關 | Maestra、Sonix（翻譯內建但非人工）、Simon Says AI（標準流程） |
| **AI 起稿 + 選配人工校對** | AI 先產出，加價請人工校對／潤飾，價格隨語言稀有度和急件程度變動 | Rev、Happy Scribe、GoTranscript |
| **人工為主（AI 輔助）／代理商模式** | 專業字幕師 / 譯者主導，AI 只是輔助工具，通常有 ADA / 無障礙合規保證 | Amara On Demand、3Play Media、Verbit |

**Giloo 的 SOP 硬規則**（`distribution-sop.md` Stage 4）：「AI 翻的東西一定要有人工 review checkpoint，AI 翻譯是起點，不是成品。」→ 純 AI 層級的工具**不能單獨拿來做正式字幕**，只能當「先跑一版草稿、壓低人工校對的分鐘數」的前處理工具。

---

## 比較表

| 服務商 | 定位 | 支援語言數 | 定價（人工校對／翻譯，每分鐘） | 交件時間 | 適合情境 |
|--------|------|-----------|-------------------------------|----------|---------|
| **Rev** | AI+人工混合，主流好用 | 翻譯字幕 17 種語言 | AI 字幕約 US$0.25/min；人工字幕約 US$1.50/min；翻譯字幕 US$6.99–15.99/min（依語言） | 人工英文字幕 12 小時內；翻譯字幕 48 小時內 | 需要快、語言是主流語種（中英日韓歐語系）、預算中等 |
| **Happy Scribe** | 性價比最高的專業人工字幕 | 轉錄 150+ 語言；專業人工字幕 60+ 語言 | 專業人工字幕從 US$2.25/min 起（依語言）；純人工校對加購 US$2.00/min | 主流語言 24 小時內，其他語言 24–48 小時 | 預算有限、需要多語言覆蓋、對「文化適配」要求中等 |
| **GoTranscript** | 群眾外包人工翻譯，價格最低 | 依語言而定，涵蓋主流+部分小眾語言 | 外語字幕從 US$12.80/min；純 AI 校對從 US$0.60/min | 1–3 天 | 極度控預算、時程有彈性、可以接受品質有波動（自由譯者品質不一） |
| **Amara On Demand** | 紀錄片／獨立影像圈老牌，PBS、Sundance 等常用 | 人工字幕師支援 30+ 語言 | 人工字幕與翻譯 US$2.50–15.00/min（依語言稀有度）；純 AI 字幕 US$0.35/min | 字幕標準 2–3 個工作天（30 分鐘內），翻譯標準 6–8 個工作天；有加急選項 | **最貼近 Giloo 的內容類型**——長期服務獨立紀錄片、非營利、影展圈，字幕師受過內容敏感度訓練 |
| **Sonix** | 純 AI 為主，翻譯是附加功能 | 54+ 語言 | 隨方案：Pay-as-you-go US$10/audio hour、訂閱制 US$5/audio hour（翻譯不額外收費） | 幾分鐘到數小時（全自動） | 只需要快速草稿、內部審閱、或當作人工校對前的第一版 |
| **Maestra** | 純 AI，語言覆蓋最廣 | 125+ 語言（配音/克隆語音 29 種） | 點數制，US$12/60 點數起（1 點 = 1 分鐘） | 幾分鐘內 | 語言小眾到其他服務沒有時的救急選項，但**不能跳過人工校對**直接上片 |
| **Simon Says AI** | 純 AI，剪輯軟體整合佳（Premiere/Resolve/Avid） | 100 種語言 | US$0.08/min（不分語言）；訂閱制 US$20–150/月 | 幾分鐘內 | 剪接階段抓 timecode、內部草稿用，不是交件用的正式字幕 |
| **3Play Media** | 企業級，無障礙合規（ADA/WCAG）取向 | 字幕/轉錄 25+ 語言；配音/在地化 50–90+ 語言 | 業界行情每分鐘 US$2–20（依語言對、急件程度），需業務報價 | 標準 4 個工作天，最快可到 2 小時加急 | 片量大、需要長期合規保證的機構（比較適合平台方，不是單片專案） |
| **Verbit** | 企業級，即時字幕+合規 | 後製字幕主打 6 種語言（英/法/西/俄/希伯來），ASR 涵蓋 30+ 語言 | 需業務報價；有 US$29/月自助方案、US$10/hr 隨用隨付 | 最快 4 小時 | 需要即時字幕（直播、座談）或機構合規需求，單片翻譯不是它的強項 |

---

## 給 Stage 4（`04-localize/`）的建議

**So what for distribution：**

1. **預設用 Happy Scribe 或 Amara On Demand 做正式交件字幕**，兩者都內建人工校對，滿足 SOP 的硬規則。Amara 更貼近紀錄片／獨立製片的內容敏感度（他們的字幕師本來就是服務這個圈子），但交件時間比較長（翻譯要 6–8 個工作天），要提早排時程；Happy Scribe 較快也較便宜，適合檔期趕的片子。

2. **GoTranscript 只在預算真的卡死時考慮**，而且交件回來一定要自己再過一輪文化適配檢查——群眾外包品質波動大，SOP 要求的「不是逐字翻譯、文化敏感點要標出來」不能完全指望供應商做到。

3. **Rev 是折衷選項**：語言涵蓋不如 Happy Scribe / Maestra 廣（只有 17 種），但主流語言（英/日/韓/西/法/中）交件快又穩定，適合已經排定發布日期、時間壓力大的片子。

4. **Sonix / Maestra / Simon Says AI 不要當成正式交件用的字幕服務**——這三個都是純 AI，沒有內建人工把關。可以用來：
   - 剪接階段先抓 timecode 和草稿台詞
   - 冷門語言先跑一版機器翻譯草稿，降低後續人工校對要看的量（等於把「全額人工翻譯」的錢，省成「人工校對機器初稿」的錢）
   - 但最終一定要走人工 review checkpoint 才能上片

5. **3Play Media / Verbit 目前對 Giloo 太重**——這兩家是給平台方或機構做長期無障礙合規用的，單片專案的性價比不如上面幾個。除非 Giloo 未來要為整個片庫做 ADA 合規字幕（美國發行擴大時可能會需要），否則不用列入常態供應商名單。

**待確認**：以上定價是各家官網和第三方評測整理，實際報價會依語言對（尤其中文 ↔ 小眾語言）、片長、急件程度浮動，正式下單前建議跟 2–3 家要具體報價單再比較。

---

## Sources

- [Rev Subtitles: Pricing, Quality, Turnaround, And Jobs (2026)](https://starpop.ai/blog/articles/rev-subtitles)
- [Subtitle Translation Services: 99% Accuracy, 17 Languages | Rev](https://www.rev.com/services/global-subtitles)
- [3Play Media Pricing for Media Accessibility & Localization Services](https://www.3playmedia.com/plans-pricing/)
- [The Cost of Translation: Breaking Down Vendor vs. In-House Options for Video — 3Play Media](https://www.3playmedia.com/blog/cost-translation-guide-video-content/)
- [Verbit Review 2026: Pricing, Features, and Alternatives • Sonix](https://sonix.ai/resources/verbit-review-pricing/)
- [Transcription Pricing & Solutions | Verbit](https://verbit.ai/pricing-package/)
- [Post-Production Captioning Services | Verbit](https://verbit.ai/solutions-captioning/post-production-captioning/)
- [Professional Human Subtitling Services in 60+ Languages | Happy Scribe](https://www.happyscribe.com/professional-subtitling)
- [How much is the Human-made transcription and subtitle service? | Happy Scribe Help Center](https://help.happyscribe.com/en/articles/6087164-how-much-is-the-human-made-transcription-and-subtitle-service)
- [Video subtitles translation services | GoTranscript](https://gotranscript.com/video-subtitles-translation-services)
- [Translation Cost Estimate | GoTranscript](https://gotranscript.com/translation-cost-estimate)
- [Subtitles cost & quotes - GoTranscript Help Center](https://help.gotranscript.com/docs/subtitles/pricing-payments/how-much-do-subtitles-cost/)
- [Professional Video Subtitling, Captioning & Translation Services – Amara On Demand](https://amara.org/purchase-subtitles/)
- [How to Choose Video Closed Captioning & Subtitling Service — Amara.org](https://blog.amara.org/2021/11/17/how-to-choose-closed-captioning-and-subtitling-service-companies-in-2021/)
- [Translate Audio & Video | 54+ Languages | Sonix](https://sonix.ai/translation)
- [How does Sonix Pricing Work | Sonix Help](https://help.sonix.ai/en/articles/4705360-how-does-sonix-pricing-work)
- [Pricing - Maestra Transcription Software](https://maestra.ai/pricing)
- [Maestra Pricing: How Much Does Maestra Really Cost in 2026 • Sonix](https://sonix.ai/resources/maestra-pricing/)
- [Pricing | Simon Says](https://www.simonsaysai.com/pricing)
- [Simon Says transcribes in 90 (ninety!) languages](https://www.simonsaysai.com/blog/simon-says-transcribes-in-90-ninety-languages-e282539c6e65)
