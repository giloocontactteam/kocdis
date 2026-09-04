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

## 台灣本地服務比較 — 校對「AI 翻譯成的中文字幕」

上面整理的是國際規模較大的平台，但如果需求是**台灣在地服務、校對已經跑完 AI 翻譯的中文字幕**，市場結構完全不一樣：台灣沒有 Happy Scribe / Rev 那種標準化大平台，主要是「外包媒合平台」（案子開出去、譯者搶標／報價）和「小型字幕工作室」兩種。

| 服務／平台 | 性質 | 服務內容 | 定價 | 交件時間 | 適合情境 |
|---|---|---|---|---|---|
| **出任務 Tasker** | 外包媒合平台 | **英日語影片 AI 初譯 + 人工精校**（最直接對應「校對 AI 字幕」的服務） | NT$30–50/分鐘 | 平台平均 24 小時內媒合，實際交件依接案者排程 | 已有 AI 翻譯初稿、只想花錢請人校潤，預算優先 |
| **創作者俱樂部** | 小型字幕工作室 | 中文字幕聽打校對；中英雙語字幕翻譯 | 中文字幕 NT$50/分鐘起；中英雙語 NT$150/分鐘（含人工校對） | **1–3 小時**極速交件 | 檔期很趕、需要快速拿到成品；但他們主打「全程人工、不用 AI 語音辨識」，要先確認能不能接受的是「校對既有 AI 初稿」而非「從零聽打翻譯」 |
| **PRO360 達人網** | 外包媒合平台 | 字幕翻譯／校對接案 | 每字 NT$0.6–5（依難度）；YouTube 字幕 NT$100–300/分鐘 | 依接案者報價，需自行比價 | 想貨比三家、找長期配合的譯者 |
| **蜂擁翻譯** | 翻譯工作室 | 字幕翻譯（可用既有字幕文稿或無稿聽譯） | 有字幕文稿 NT$125/50 字；無字幕從頭翻譯 NT$250/分鐘 | 需洽詢 | 已有 AI 產出的字幕文字檔，只要校對潤飾 |
| **日台科技日文翻譯** | 專精日文的翻譯社 | 日文影片聽譯／校對 | 有原文字幕 NT$250–350/分鐘（每 10 分鐘 NT$2,500–3,500）；無原文字幕 NT$350–500/分鐘 | 需洽詢 | Giloo 若有日本合製或需要日文字幕的片子 |
| **好文數位文化（速可打 eztype）** | 逐字稿聽打工作室 | 中英文逐字稿聽打 + 校稿 + 斷句編排 | 英文 NT$60/分鐘；中文 NT$30/分鐘 | 需洽詢 | 拿 AI 逐字稿去對照校正、或抓正式翻譯前的中文聽打稿 |
| **104 外包網** | 外包媒合平台（本身不是服務商） | 各類字幕／翻譯接案 | 案件報價不一，平台另收 NT$500–3,000 成交費 | 依接案者而定 | 案件金額較大、想找穩定配合的譯者長期合作 |

**So what for distribution：**

1. **最貼近「校對 AI 翻譯字幕」這個需求的是出任務 Tasker 的「AI 初譯 + 人工精校」（NT$30–50/分鐘）**——這個定價明顯比「從零人工翻譯」（NT$150–500/分鐘）便宜 3–10 倍，邏輯就是先讓 AI 出稿、再花小錢請人校潤，跟 Giloo 現在想做的事完全對應。缺點是它是媒合平台，品質看接的譯者是誰，下單前要看過對方作品或先發一小段試譯。

2. **創作者俱樂部交件最快（1–3 小時）**，如果是檔期卡很緊的片子可以列入備案，但下單前務必先問清楚：他們的標準流程是不是「拒收 AI 初稿、要求全部重新聽打」——如果是，那就不是「校對」服務，會變成整份重做，價格和交件時間都要重算。

3. **PRO360 / 104 外包網是媒合平台不是單一服務商**，價格區間很寬（每字 NT$0.6–5），適合貨比三家但沒辦法直接拿一個固定報價；如果 Giloo 之後要固定配合譯者，這兩個平台適合用來「篩選」，找到人選後轉為長期外部合作，比每次重新開案划算。

4. **實際詢價的關鍵動作**：不要只問「字幕翻譯報價」，要明確說「已經有 AI 翻譯初稿，需要的是人工校對／潤飾，不是從零翻譯」——台灣譯者/工作室的報價單通常沒有拆這兩種服務，主動講清楚才能拿到比「整份重翻」更低的校對價，行情大約是重新翻譯報價的 3–6 成。

5. 上面的台灣報價多數是「聽打逐字稿」「YouTube 影片翻譯」「線上課程字幕」等一般商用內容的行情，跟國際大型平台（Amara On Demand、Happy Scribe）鎖定紀錄片／影展圈的專業字幕服務不完全是同一個市場——如果字幕最終要送影展或串流平台審核（格式、每行字數、閱讀速度 CPS 有硬性規範），下單前要跟接案者確認有沒有做過符合影展規格的字幕，不是所有台灣接案者都熟悉這塊。

---

## 附錄：這行的訂價邏輯 — 有沒有「成本＋固定%」公式？

沒有像餐飲業「食材成本 × 固定倍數」那種公式。餐飲業的核心成本是原料，翻譯／字幕校對業的核心成本是**人的時間**，材料成本（AI 工具訂閱費，每分鐘幾毛到幾塊台幣）幾乎可以忽略不計，所以「成本＋%」這個框架本身不太適用，真正決定報價的是「工時 × 目標時薪」。

不過業界有幾個可以當估算錨點的經驗法則：

| 產業／角色 | 訂價邏輯 | 大概倍數／比例 |
|---|---|---|
| 餐飲 | 食材成本 → 定價 | 食材成本抓 28–35%，反推 ≈ 成本 × 2.8–3.5 倍 |
| 零售 | 進貨成本 → 定價 | Keystone pricing，成本 × 2（毛利 50%） |
| 顧問／廣告代理商 | 全成本人力 → 收費 | Rule of Three，全薪資成本 × 3 |
| 翻譯社（有 PM/QA） | 譯者稿費 → 客戶報價 | 約 1.8–2.9 倍（依固定成本分攤，非統一比例；國外案例：付譯者 €0.075/字 → 客戶報價 €0.218/字，抓 20% 營業利潤率） |
| 純媒合平台（PRO360／104／Tasker） | 成交金額 → 抽成 | 10–25% 抽成，不是倍數訂價，因為平台不承擔 QA 責任 |
| **校對／編修 vs. 從零翻譯** | **工時比例反推** | **國際慣例（ATA／ProZ）：校對費 ≈ 全新翻譯費的 35–40%**（校對花的時間通常只有從零翻譯的 1/3–1/2） |

**跟台灣數字對照**：出任務 Tasker「AI 初譯＋人工精校」NT$30–50/分鐘，對比創作者俱樂部「從零人工雙語翻譯」NT$150/分鐘，比例落在 **20–33%**，比國際 35–40% 的慣例略低——合理解讀是台灣接案市場價格本來壓得比較緊，或「精校」被界定成比 ProZ 講的「editing」更輕量的潤飾。

**給 Giloo 的估算方式**：想知道「校對 AI 字幕」的合理報價區間，用「這部片找人從零翻譯要多少錢 × 20%」當下限、「× 35%」當上限，落在區間內算合理；目前台灣接案行情剛好貼著下限，代表現階段議價空間不大，算甜蜜點。

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
- [2026年8月翻譯寫作費用行情總覽｜出任務 Tasker](https://www.tasker.com.tw/services/writing-translation)
- [字幕/翻譯服務 – 創作者俱樂部](https://creators-club.org/service/)
- [專業中文字幕外包服務：1-3 小時極速交件 - 創作者俱樂部](https://creators-club.org/%E5%B0%88%E6%A5%AD%E4%B8%AD%E6%96%87%E5%AD%97%E5%B9%95%E5%A4%96%E5%8C%85%E6%9C%8D%E5%8B%99%EF%BC%9A1-3-%E5%B0%8F%E6%99%82%E6%A5%B5%E9%80%9F%E4%BA%A4%E4%BB%B6/)
- [2025 影片翻譯費用總整理，字幕翻譯收費每字$0.6起 - PRO360達人網](https://www.pro360.com.tw/price/video_translation)
- [Re: [問題] 請問英翻中字幕的計價方式 - 看板 translator - PTT](https://www.ptt.cc/bbs/translator/M.1499771629.A.F0D.html)
- [中英文字幕聽打翻譯服務 - 逐字稿 - 好文數位文化](https://rec-type.good-reading.com/subtitle.htm)
- [聽打逐字稿．上字幕請找速可打專業團隊 - eztype](https://www.eztype.cc/)
- [日文字幕翻譯,日文影片翻譯,日文聽譯 | 日台科技日文翻譯](https://www.jtt-h.com/jqavideo)
- [【2026最新】中翻英翻譯接案、外包報價行情費用參考｜104職場力](https://blog.104.com.tw/quotation-of-translation/)
- [網路接案、找工作或兼職必看，6大外包網推薦比較懶人包 - PRO360達人網](https://www.pro360.com.tw/blog/6_freelance_jobs_websites/)
- [Pricing Techniques in the Translation Industry - American Translators Association (ATA)](https://www.atanet.org/business-strategies/pricing-techniques-in-the-translation-industry/)
- [Comparing freelance and agency translation pricing models - INTERPROTRANS](https://interprotrans.net/comparing-freelance-and-agency-translation-pricing-models/)
- [Proofreading rates - industry standard? (ProZ.com: Translator Coop)](https://www.proz.com/forum/prozcom_translator_coop/6287-proofreading_rates_industry_standard.html)
- [What are the standard proofreading rates? (ProZ.com)](https://www.proz.com/forum/proofreading_editing_reviewing/221497-what_are_the_standard_proofreading_rates.html)
- [中英文翻譯價格怎麼算？看懂翻譯社報價的 4 大重點 | 元年翻譯](https://t-transera.com/translation-rates/)
