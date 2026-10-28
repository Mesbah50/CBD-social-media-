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
- Contact (only when a post needs one, e.g. slot 6): `Mesbah Uddin — WhatsApp: 01606481782`. No other name or phone number ever appears in images or captions.
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
   {"date": "2026-10-28", "posts": [
     {"slot": 1, "category": "problem",
      "hook": "সাপ্লায়ার টাকা নিয়ে [উধাও?]",
      "sub": "অর্ডারের আগে এই ৩টা জিনিস যাচাই করুন",
      "style": "contrast",
      "art": {"left": {"objects": ["money"], "arrange": "single", "label": "বাইরে পেমেন্ট"}, "right": {"objects": ["cart"], "arrange": "single", "label": "1688-এর ভেতরে"}},
      "caption": "…", "hashtags": "#ChinaBondBD …", "alt": "…"}
   ]}
   ```
   - **The image is the hook.** `hook`: 4–9 Bengali words, a question or a curiosity/fear trigger, one part wrapped in `[ ]` to highlight. `sub` (optional): ≤ 10 words. `points` (optional, best for `problem`): up to 3 items, ≤ 6 words each.
   - **Caption carries all the information**: open with the hook line, then the problem, then the full explanation / steps / numbers with sources, then a soft CTA ("কমেন্টে প্রশ্ন করুন" / follow), and for slot 6 the CBD services + the contact line `Mesbah Uddin — WhatsApp: 01606481782`. Slots 1–5 carry no name or phone number. 120–250 words, short paragraphs, a few emojis are fine.
   - `hashtags`: 8–12, mixing Bengali and English. Always include #ChinaBondBD #CBD #ImportFromChina, then topic tags.
   - `alt`: one-line description of the image.
   - **Every image is a creative concept in exactly one of 7 styles** (`"style"` + `"art"` in each post). Pick the style that fits the topic best and vary styles across the day. Never make an image outside these 7:
     | style | idea | `art` fields |
     |---|---|---|
     | `exaggeration` | benefit/problem blown up beyond reality | `mode`: stream (small `source` erupts into many `effect`) / giant (tiny `source` next to huge `effect`) / lift; `source`, `effect`, optional `label` |
     | `animal` | an animal's known trait = the message (ant carries far more than its size, eagle = speed/direct, owl = checking/wisdom, turtle/snail = slow, bee = hard work) | `animal`: ant/eagle/owl/turtle/snail/bee; `object`; optional `label` |
     | `material` | object made of another material (gold = valuable, glass = transparent, steel = protected, cloud/cotton = soft, feather = light, ice = cool) | `object`, `material`: gold/glass/steel/cloud/cotton/feather/ice; optional `label` |
     | `shape` | many small objects arranged into a meaningful shape | `unit`, `shape`: check/heart/arrow/graph/circle/stairs/taka; optional `label` |
     | `benefit` | product/service in the centre with up to 4 benefit callouts (≤ 4 words each) | `object`, `callouts` [..] |
     | `contrast` | split screen: wrong way (grey, ✗) vs right way (colour, ✓) | `left` {objects, arrange: messy/neat/single, label}, `right` {…} |
     | `shadow` | an object casts the shadow of what it can become / hides | `object`, `shadow`; optional `label` |
     Objects available: box, container, ship, plane, warehouse, factory, coin, money, cushion, cloud, blocks, magnifier, question, check, cross, tag, phone, cart, shop, lamp, trophy, chair, pan. Reference renders of all 7 are in `posts/styles/`.
   - With a creative image, keep `hook` short (≤ 7 words) and `sub` optional; don't use `points` (put lists in the caption).
   - **`ai_prompt` (required from 29 Oct 2026):** an English prompt for a realistic photo of the creative concept (the same style + idea as `style`/`art`). Write it like a photographer's brief, 50–80 words: subject and the metaphor (e.g. "a shipping container made of polished gold" for `material`, "a tiny ant carrying a huge stack of export cartons" for `animal`, split scene for `contrast`, real object casting a shadow of something else for `shadow`), import elements (cargo ship, containers, cartons, warehouse, factory, plane) where they fit, deep royal-blue / navy colour mood to match the CBD blue panel, studio or cinematic lighting, sharp detail, lens spec (35mm / 85mm), wide 2:1 composition with the subject centred. Always end with: "No text, no letters, no logos, no people, no faces." Never ask for a specific product (no product posts).
5. **Render**: `python3 scripts/build.py posts/<date>/content.json` → `post-1.png` … `post-6.png` (1080×1080, 1:1). Open the images and check that the hook fits and nothing overlaps; shorten text and re-render if not.
   **The AI photo must always BE the post's style — one of the owner's 7 ideas, never a plain/generic photo.** Build `ai_prompt` from the matching pattern:
     | style | how the photo must look |
     |---|---|
     | `exaggeration` | the benefit or problem blown far beyond reality (a tiny parcel bursting into a flood of cartons, a giant container next to a tiny shop) |
     | `animal` | a real animal whose known trait is the message (ant carrying a huge carton stack = small importer, carrying more; eagle = fast/direct; owl = checking; turtle/snail = slow shipping; bee = hard work) |
     | `material` | the object made of another material that carries the meaning (gold container = valuable, glass box = transparent deal, steel carton = protected, cotton/cloud = soft, feather = light, ice = cool) |
     | `shape` | many small objects (cartons, coins, containers) arranged into a meaningful shape: check mark, arrow, rising graph, heart, taka sign, stairs |
     | `benefit` | the subject hero-lit in the centre with clear space around it for the benefit message |
     | `contrast` | split frame: left side wrong way (grey, messy, dim), right side right way (bright, neat, blue) |
     | `shadow` | a real object whose shadow on the wall is what it can become or what it hides (small carton casting a warehouse shadow, cheap deal casting a trap shadow) |
     Before generating, check the prompt names the style's device explicitly; after generating, reject and regenerate if the photo does not show it.
   Because every post has `ai_prompt`, build.py also writes `overlay-<slot>.png`: the full brand layout (background, logo, quote mark, hook boxes, footer) with a transparent hole where the blue panel is. `post-<slot>.png` is the fallback image (drawn creative) if the AI steps fail.
5b. **Make the realistic image in Canva** (Canva connector), one post at a time, after pushing the overlays (step 6 can run first):
   1. `generate-image` with the post's `ai_prompt`, `aspectRatio: "LANDSCAPE_2_1"`. Poll `get-generate-image-job` until SUCCESS and look at the preview: no text/letters, no people, the concept is clear and on-theme. If it fails the check, regenerate once with a tightened prompt. Keep the media id.
   2. `upload-asset-from-url` with the overlay's raw URL `https://raw.githubusercontent.com/Mesbah50/CBD-social-media-/main/posts/<date>/overlay-<slot>.png` → asset id.
   3. `copy-design` the master design `DAHZQrCmCYM` ("CBD post master", 1080×1080) → new design id. Never edit the master itself.
   4. `read-design` the copy with `open_transaction: true` and `design_content`. It has two image elements: the creative (left 190, top 150, 850×440) and the overlay (full page 1080×1080, on top). `edit-design` with `update_fill` on each (creative ← generated media id, overlay ← overlay asset id), `finalize: "keep_open"`, check the returned thumbnail (photo inside the panel, hook boxes on top, logo visible), then `finalize: "commit"`. The owner has approved these daily edits on copies of the master.
   5. `export-design` → `{"type":"png","width":1080,"height":1080}` → export URL (it expires within hours, so never give it to Buffer).
   6. Store it permanently: POST `https://api.github.com/repos/Mesbah50/CBD-social-media-/actions/workflows/fetch-image.yml/dispatches` with headers `Authorization: Bearer $GH_TOKEN`, `Content-Type: application/json`, body `{"ref":"main","inputs":{"url":"<export URL>","path":"posts/<date>/post-<slot>-ai.png"}}` (build the JSON with python so the URL is escaped). Then poll `https://raw.githubusercontent.com/Mesbah50/CBD-social-media-/main/posts/<date>/post-<slot>-ai.png` (use a loop with short python sleeps) until it returns 200 and is 1080×1080. Run `git pull` before your next push, since the workflow commits to main.
   7. Use `post-<slot>-ai.png` as the Buffer image. If any step fails (e.g. Canva AI allowance used up), use `post-<slot>.png` instead and mention it in the report.
6. **Commit and push** the date folder and the updated `topics_log.md` (one line per post: `- <date> | <category> | <topic>`).
7. **Schedule in Buffer** — 18 posts (6 posts × 3 channels) with `create_post`:
   - `mode: "customScheduled"`, `dueAt: "<date>T<time>:00+06:00"`, `schedulingType: "automatic"`
   - `text`: caption + blank line + hashtags
   - `assets: [{"image": {"url": <raw URL>, "metadata": {"altText": <alt>}}}]`
   - Facebook channels also need `metadata: {"facebook": {"type": "post"}}`
   - If a slot time has already passed, schedule it 30 minutes from now instead. If Buffer cannot fetch the image right after the push, wait a minute and retry once.
8. **Report** to the owner with SendUserMessage, in Bengali: the 6 topics, the times, and anything that failed.

## Rules that never change

- NO PRODUCT POSTS (owner's instruction, 28 Oct 2026): never make a post about a specific product (no trending-product or "sell this item" posts). Product categories may be mentioned in passing, but no post is built around a particular product. This overrides any older rule about product posts or product photos.

- Every post in content.json must carry a `"sources": ["<url>", ...]` list with the exact links its facts came from, so the owner can open them. A source you cannot link to cannot be used.

- REAL PRODUCT PHOTO RULE (owner's instruction): whenever a post discusses a specific product, the image must show that product's real photo — never a drawing or a generic object. Real photos come only from the `product-photos/` folder (the owner uploads them). Use one with `"object": "photo:product-photos/<file>"` in any style that takes an object (best: `benefit`, `material`, `shadow`, `contrast`). Before choosing a product topic, list `product-photos/`; only pick products that have a photo there. If today's trending product has no photo, do not make a product-specific post — use a different, non-product angle for that slot, and in the final report tell the owner which product photos to upload. Never download or copy product photos from websites.

- Layout (fixed, follows the owner's reference post): brand background; CBD logo top-right; bright-blue (#0085FE) quote mark top-left; a CBD-blue (#02378F) panel holding the creative concept; the hook below it in stacked black boxes with white text and the highlighted part in bright blue (#1EA0FF); bottom-left a bright-blue bar with the category name in blue and the sub line in dark grey. Colours are only CBD blue, bright blue, black, white and the background — no red in the design (the logo stays as it is). No people in the image.

- Background: every image uses ONLY the CBD brand background (`scripts/background.py` / `brand/background.svg`: warm off-white #F7F3F2, faint dot grid, soft white centre glow, scattered light-blue rounded squares). No other background, ever.

- Never delete, rename or move an image in `posts/` after it is pushed — Buffer loads it from that exact link at posting time, and a missing file shows as a broken image.

- Brand name on images = the CBD logo only (`brand/cbd_logo_badge.png`, already in the template). Never redraw or recolour it.
- Import-related images always carry import elements (plane, cargo ship, containers, boxes, warehouse) — the template does this.
- Never use the owner's photos unless he provides one for that post. Never use photos of real people.
- Images and captions only. No reels, no video.
- Realistic AI photo (Canva) is the default creative from 29 Oct 2026; the drawn creative is only the fallback. The AI photo sits only inside the blue panel; logo, hook, footer and background always come from the overlay, never from AI.
- No copied text from articles: summarise in your own words, credit the source.
- Facebook-safe wording: no medical promises ("ব্যথা ভালো হয়ে যাবে", "৭ দিনে উধাও"), no hooks that point at the reader's body or condition ("আপনার কি কোমর ব্যথা?" → "যারা দীর্ঘক্ষণ বসে কাজ করেন…"), no before/after claims.
- Never mention any author, book title or other person's Facebook ID from the source material.
- Always write the marketplace name as `1688` in English digits — never `১৬৮৮` — in images, captions and hashtags.
- Images carry no phone number and no person's name. The only name/number allowed anywhere is `Mesbah Uddin — WhatsApp: 01606481782`, and only in captions that need a contact line.
