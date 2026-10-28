# CBD daily posts — playbook

Every day: research trending import/export and business topics, make **6 image posts** (one per category), write the caption with all the information, and schedule each post on **all 3 Buffer channels**. Images only — never reels or video.

Owner: Mesbah uddin, China Bond BD (CBD). Language of all post text: Bengali.

## Fixed facts

- Buffer organization: `My organization` — id `6ac0cc64d40717621231ce56`, timezone Asia/Dhaka (+06:00)
- Channels (post every item to all three):
  - China Bond BD (Facebook page) — `6ad9fda3778b240e2f8b559e`
  - Mesbah China Imports guide (Facebook page) — `6ad9fda3778b240e2f8b559f`
  - MESBAH UDDIN (LinkedIn profile) — `6ac5e1486a5c39ccb63c77a6`
- Image hosting: this repo. Public image URL = `https://raw.githubusercontent.com/Mesbah50/CBD-social-media-/main/posts/<date>/post-<slot>.png`
- Contact: `Mesbah Uddin — WhatsApp: 01606481782` in captions that need it (slot 6); every image footer shows `WhatsApp: 01606481782` + `China Bond BD` (brand guide). No other name or phone number ever appears in images or captions.
- Services: Factory Direct Import · Winning Product Research · Brand Name Custom Design · Shipping & Delivery Full Service
- Product categories: Baby Toy · Home & Pain Relief · Home Decor · Home Hacks

## The 6 categories and times (Asia/Dhaka)

| slot | time  | category key | what it is |
|------|-------|--------------|------------|
| 1 | 08:00 | `problem`  | A real importer problem and its solution (customs hold, supplier fraud, wrong goods, damaged cargo, payment issues) |
| 2 | 10:00 | `news`     | Today's Bangladesh or world trade news, explained: "what changes for a small importer" |
| 3 | 15:00 | `learn`    | "ইমপোর্ট শিখুন" — one step of the import process taught from KNOWLEDGE.md (1688 search, seller checks, factory vs trader, MOQ, negotiation, weight & landed cost, samples, damage agreement, shipping mark, packing list, order remark, agent choice…), hooked to a current news item |
| 4 | 18:00 | `cost`     | Cost / profit breakdown (factory price, freight, duty, delivery); framed as "why is profit low" |
| 5 | 19:00 | `alert`    | Scam alert, common beginner mistake, or myth vs fact |
| 6 | 21:30 | `idea`     | Business idea / seasonal opportunity, ending with the CBD services + contact line |

Most posts must solve a problem. Only slot 6 is a direct sales post.

## Daily steps

1. **Set up.** Attach and clone this repo (`Mesbah50/CBD-social-media-`, push access). Make sure Playwright's Chromium is installed (`python3 -m playwright install chromium` if rendering fails).
2. **Check what was already posted, and load the know-how.** Read `topics_log.md` — never repeat a topic or angle from the last 30 days. Read `KNOWLEDGE.md` — the owner's own sourcing and winning-product method. Build most posts on it (steps, checklists, mistakes, examples), and hook each one to something trending today.
   **News-first rule (owner's instruction):** every one of the 6 posts — not only the `news` slot — must be built on a current update or news item: Bangladesh first (NBR/customs duty and SRO changes, Bangladesh Bank, LC and dollar rate, Chattogram port, budget, e-commerce rules, local market prices), then the world (China export policy, freight and shipping rates, tariffs and trade wars, trade fairs, marketplace trends on 1688/Alibaba/TikTok/Amazon). Run separate searches for Bangladesh and for the world every day. Use the owner's know-how in KNOWLEDGE.md to explain what the news means for a small importer and what to do about it.
3. **Research today's trends** (WebSearch, several searches, recent results first):
   - Bangladesh: NBR customs duty / SRO changes, Bangladesh Bank LC and dollar rate news, Chattogram port situation, budget announcements, e-commerce rules.
   - World: container and air freight rate news, China export policy, trade fairs (Canton Fair etc.), tariffs.
   - Product trends in the 4 categories (seasonal demand: winter, Eid, Boishakh, school season…).
   - Import scams and common problems people are discussing.
   Use only facts you found in a source today. Never invent figures, rates, or laws. If a number cannot be verified, leave it out. For `news`, name the source in the caption ("সূত্র: …").
4. **Write `posts/<YYYY-MM-DD>/content.json`** in this shape:
   ```json
   {"date": "2026-10-29", "posts": [
     {"slot": 1, "category": "problem", "layout": "list",
      "hook": "সাপ্লায়ার টাকা নিয়ে [উধাও?]",
      "sub": "অর্ডারের আগে এই ৩টা জিনিস যাচাই করুন",
      "points": ["1688-এর ভেতরে পেমেন্ট করুন", "দোকানের বয়স আর রিভিউ দেখুন", "আগে ছোট স্যাম্পল অর্ডার"],
      "style": "contrast",
      "ai_prompt": "…English photo brief…",
      "fallback": "cartons",
      "caption": "…", "hashtags": "#ChinaBondBD …", "alt": "…", "sources": ["https://…"]}
   ]}
   ```
   - **Design = the owner's CBD Brand Post Guide (PDF, 28 Oct 2026; copy in `brand/CBD_Import_Brand_Post_Guide.pdf`).** `scripts/build.py` draws it; never hand-draw another look. Layouts (pick with `layout`, default per category):
     | layout | from the guide | used for (default) | fields |
     |---|---|---|---|
     | `hero` | "চীন থেকে সরাসরি আমদানি" — Congress Blue background, white headline, the `[highlight]` in a red pill, sub line, wide photo, red CTA pill, white footer | `news`, `idea` | `hook`, `sub`, optional `tag` |
     | `list` | "আমদানি হয় যেভাবে" — Athens Gray background, blue headline with the `[highlight]` word in red, portrait photo + up to 4 white numbered cards (০১–০৪), blue footer | `problem`, `learn` | `hook`, `sub`, `points` (2–4 items, ≤ 7 words each) |
     | `vs` | "সী ফ্রেইট vs এয়ার ফ্রেইট" — blue left half / gray right half, red VS circle, wide photo across both | `cost` (or any A-vs-B topic) | `art.left` / `art.right` each {`tag` (English, caps), `label` (2–3 Bengali words), `sub` (≤ 5 words)}; `hook` is still required (used in alt/caption) |
     | `notice` | "গুরুত্বপূর্ণ ঘোষণা" — red header band with the title + bell, white body, blue headline, wide photo, blue footer | `alert` | `hook`, optional `notice_title` (default "সতর্কতা") |
     The product templates in the guide (নতুন পণ্য, পাইকারি অফার, নতুন চালান) are NOT used (no product posts). The greeting template is only for festival days when the owner asks.
   - Colours are only the guide's: Congress Blue #05358B (~50%), Monza red #E40715 (max ~10%: one highlight word, the CTA pill, VS badge, alert header), Athens Gray #F0F0F2, Wedgewood #5274A4, white. Fonts: Anek Bangla ExtraBold for Bengali headlines, Hind Siliguri for Bengali body, Poppins for all English. The renderer already does this.
   - Footer on every image: `WhatsApp: 01606481782` (left) and `China Bond BD` (right) — owner's choice for the guide's footer. No other name or number on images.
   - **The image is the hook.** `hook`: 4–9 Bengali words, a question or curiosity/fear trigger, exactly one part wrapped in `[ ]` (the red highlight). `sub`: ≤ 10 words.
   - **Caption carries all the information**: open with the hook line, then the problem, then the full explanation / steps / numbers with sources, then a soft CTA ("কমেন্টে প্রশ্ন করুন" / follow), and for slot 6 the CBD services + the contact line `Mesbah Uddin — WhatsApp: 01606481782`. 120–250 words, short paragraphs, a few emojis are fine.
   - `hashtags`: 8–12, mixing Bengali and English. Always include #ChinaBondBD #CBD #ImportFromChina, then topic tags.
   - `alt`: one-line description of the image. `sources`: the exact links the facts came from.
   - **Photo inside the layout = a realistic Canva photo built on one of the owner's 7 creative ideas** (`style`). `ai_prompt` (English, 50–80 words) must describe that idea:
     | style | how the photo must look |
     |---|---|
     | `exaggeration` | the benefit or problem blown far beyond reality (a tiny parcel bursting into a flood of cartons, a giant container next to a tiny shop) |
     | `animal` | a real animal whose known trait is the message (ant carrying a huge carton stack = small importer carrying more; eagle = fast/direct; owl = checking; turtle/snail = slow shipping; bee = hard work) |
     | `material` | the object made of another material that carries the meaning (gold container = valuable, glass box = transparent deal, steel carton = protected, cotton/cloud = soft, feather = light, ice = cool) |
     | `shape` | many small objects (cartons, coins, containers) arranged into a meaningful shape: check mark, arrow, rising graph, heart, taka sign, stairs |
     | `benefit` | the subject hero-lit in the centre, clean and premium |
     | `contrast` | split frame: left side wrong way (grey, messy, dim), right side right way (bright, neat, blue) — best with the `vs` layout |
     | `shadow` | a real object whose shadow on the wall is what it can become or what it hides (small carton casting a warehouse shadow, cheap deal casting a trap shadow) |
     Write it like a photographer's brief: subject + the style's device named explicitly, import elements where they fit (cargo ship, containers, cartons, warehouse, factory, plane, truck), colour mood matching the guide (navy/Congress-blue tones with a touch of red, clean light-grey or deep-blue backdrop), studio or cinematic light, lens spec, composition fitted to the slot (`list` = vertical 4:5 subject centred; other layouts = wide 2:1 subject centred). Always end with "No text, no letters, no logos, no people, no faces." Never a specific product. Vary styles across the day.
   - `fallback`: kit drawing used if the photo fails — ship / containers / plane / route / cartons / truck / warehouse (the guide's import graphics kit).
5. **Render**: `python3 scripts/build.py posts/<date>/content.json` → for each slot `post-N.png` (fallback, kit drawing in the photo slot), `overlay-N.png` (the same design with a transparent rounded hole where the photo goes) and `slot-N.json` (photo rectangle + Canva aspect ratio). Open the post-N.png images and check text fits and nothing overlaps; shorten text and re-render if not. Commit and push (step 6) before the Canva step, so the overlay links work.
5b. **Make the realistic photo in Canva and compose** (Canva connector), one post at a time:
   1. `generate-image` with `ai_prompt` and `aspectRatio` from `slot-N.json`. Poll `get-generate-image-job` until SUCCESS and look at the preview: the style's device is clearly visible, no text/letters, no people. If not, regenerate once with a tightened prompt. Keep the media id.
   2. `upload-asset-from-url` with `https://raw.githubusercontent.com/Mesbah50/CBD-social-media-/main/posts/<date>/overlay-N.png` → asset id.
   3. `copy-design` the master design `DAHZQrCmCYM` (1080×1080) → new design id. Never edit the master itself.
   4. `read-design` the copy with `open_transaction: true` and `design_content`; note the locator_ids of its existing elements. One `edit-design` call (`keep_open`): `delete_element` every existing element, then `insert_fill` the photo (media id) at the slot's `left/top/width/height` from `slot-N.json`, then `insert_fill` the overlay asset at left 0, top 0, 1080×1080 (in this order, so the overlay is on top). Check the returned thumbnail (photo only inside the rounded slot, all text sharp and in place), then `finalize: "commit"`. Do NOT use update_fill for this (it keeps the old crop and shifts the overlay). The owner has approved these edits on copies of the master.
   5. `export-design` → `{"type":"png","width":1080,"height":1080}` → export URL (expires within hours; never give it to Buffer).
   6. `python3 scripts/store_image.py "<export URL>" posts/<date>/post-N-ai.png` — runs the fetch-image GitHub workflow, waits, and prints the permanent raw URL and size (must be 1080×1080). Run `git pull --rebase` before your next push (the workflow commits to main).
   7. Use `post-N-ai.png` as the Buffer image. If any step fails (e.g. Canva AI allowance used up), use `post-N.png` and say so in the report.
6. **Commit and push** the date folder and the updated `topics_log.md` (one line per post: `- <date> | <category> | <topic>`).
7. **Schedule in Buffer** — 18 posts (6 posts × 3 channels) with `create_post`:
   - `mode: "customScheduled"`, `dueAt: "<date>T<time>:00+06:00"`, `schedulingType: "automatic"`
   - `text`: caption + blank line + hashtags
   - `assets: [{"image": {"url": <raw URL>, "metadata": {"altText": <alt>}}}]`
   - Facebook channels also need `metadata: {"facebook": {"type": "post"}}`
   - If a slot time has already passed, schedule it 30 minutes from now instead. If Buffer cannot fetch the image right after the push, wait a minute and retry once.
8. **Report** to the owner with SendUserMessage, in Bengali: the 6 topics, the times, and anything that failed.

## Rules that never change

- DESIGN (owner's instruction, 28 Oct 2026): every image follows the CBD Brand Post Guide PDF — its colours, fonts, layouts, logo box, footer band and graphics kit — through `scripts/build.py`. The older designs (dot/square background, black hook boxes, bright-blue accents, scripts/build_v1.py) are retired; never use them. Inside the layout, the visual is a realistic Canva photo made on one of the 7 creative ideas; the kit drawing is only the fallback.
- Logo: the CBD logo in its white (or Athens Gray) rounded box, top-left, as the renderer places it. Never redraw or recolour it.
- Footer: `WhatsApp: 01606481782` and `China Bond BD` only. No other name or number on images. No people in images.

- NO PRODUCT POSTS (owner's instruction, 28 Oct 2026): never make a post about a specific product (no trending-product or "sell this item" posts). Product categories may be mentioned in passing, but no post is built around a particular product. This overrides any older rule about product posts or product photos.

- Every post in content.json must carry a `"sources": ["<url>", ...]` list with the exact links its facts came from, so the owner can open them. A source you cannot link to cannot be used.

- Never delete, rename or move an image in `posts/` after it is pushed — Buffer loads it from that exact link at posting time, and a missing file shows as a broken image.

- Never use the owner's photos unless he provides one for that post. Never use photos of real people.
- Images and captions only. No reels, no video.
- No copied text from articles: summarise in your own words, credit the source.
- Facebook-safe wording: no medical promises ("ব্যথা ভালো হয়ে যাবে", "৭ দিনে উধাও"), no hooks that point at the reader's body or condition ("আপনার কি কোমর ব্যথা?" → "যারা দীর্ঘক্ষণ বসে কাজ করেন…"), no before/after claims.
- Never mention any author, book title or other person's Facebook ID from the source material.
- Always write the marketplace name as `1688` in English digits — never `১৬৮৮` — in images, captions and hashtags.
