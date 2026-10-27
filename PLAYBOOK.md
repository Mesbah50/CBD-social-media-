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
| 2 | 11:00 | `news`     | Today's Bangladesh or world trade news, explained: "what changes for a small importer" |
| 3 | 13:00 | `trending` | A trending product in one of the 4 categories: what customer problem it solves, why it sells now |
| 4 | 16:00 | `cost`     | Cost / profit breakdown (factory price, freight, duty, delivery); framed as "why is profit low" |
| 5 | 19:00 | `alert`    | Scam alert, common beginner mistake, or myth vs fact |
| 6 | 21:00 | `idea`     | Business idea / seasonal opportunity, ending with the CBD services + contact line |

Most posts must solve a problem. Only slot 6 is a direct sales post.

## Daily steps

1. **Set up.** Attach and clone this repo (`Mesbah50/CBD-social-media-`, push access). Make sure Playwright's Chromium is installed (`python3 -m playwright install chromium` if rendering fails).
2. **Check what was already posted, and load the know-how.** Read `topics_log.md` — never repeat a topic or angle from the last 30 days. Read `KNOWLEDGE.md` — the owner's own sourcing and winning-product method. Build most posts on it (steps, checklists, mistakes, examples), and hook each one to something trending today.
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
5. **Render**: `python3 scripts/build.py posts/<date>/content.json` → `post-1.png` … `post-6.png` (1080×1080, 1:1). Open the images and check that the hook fits and nothing overlaps; shorten text and re-render if not.
6. **Commit and push** the date folder and the updated `topics_log.md` (one line per post: `- <date> | <category> | <topic>`).
7. **Schedule in Buffer** — 18 posts (6 posts × 3 channels) with `create_post`:
   - `mode: "customScheduled"`, `dueAt: "<date>T<time>:00+06:00"`, `schedulingType: "automatic"`
   - `text`: caption + blank line + hashtags
   - `assets: [{"image": {"url": <raw URL>, "metadata": {"altText": <alt>}}}]`
   - Facebook channels also need `metadata: {"facebook": {"type": "post"}}`
   - If a slot time has already passed, schedule it 30 minutes from now instead. If Buffer cannot fetch the image right after the push, wait a minute and retry once.
8. **Report** to the owner with SendUserMessage, in Bengali: the 6 topics, the times, and anything that failed.

## Rules that never change

- Layout (fixed, follows the owner's reference post): brand background; CBD logo top-right; bright-blue (#0085FE) quote mark top-left; a CBD-blue (#02378F) panel holding the creative concept; the hook below it in stacked black boxes with white text and the highlighted part in bright blue (#1EA0FF); bottom-left a bright-blue bar with the category name in blue and the sub line in dark grey. Colours are only CBD blue, bright blue, black, white and the background — no red in the design (the logo stays as it is). No people in the image.

- Background: every image uses ONLY the CBD brand background (`scripts/background.py` / `brand/background.svg`: warm off-white #F7F3F2, faint dot grid, soft white centre glow, scattered light-blue rounded squares). No other background, ever.

- Never delete, rename or move an image in `posts/` after it is pushed — Buffer loads it from that exact link at posting time, and a missing file shows as a broken image.

- Brand name on images = the CBD logo only (`brand/cbd_logo_badge.png`, already in the template). Never redraw or recolour it.
- Import-related images always carry import elements (plane, cargo ship, containers, boxes, warehouse) — the template does this.
- Never use the owner's photos unless he provides one for that post. Never use photos of real people.
- Images and captions only. No reels, no video.
- No copied text from articles: summarise in your own words, credit the source.
- Facebook-safe wording: no medical promises ("ব্যথা ভালো হয়ে যাবে", "৭ দিনে উধাও"), no hooks that point at the reader's body or condition ("আপনার কি কোমর ব্যথা?" → "যারা দীর্ঘক্ষণ বসে কাজ করেন…"), no before/after claims.
- Never mention any author, book title or other person's Facebook ID from the source material.
- Always write the marketplace name as `1688` in English digits — never `১৬৮৮` — in images, captions and hashtags.
- Images carry no phone number and no person's name. The only name/number allowed anywhere is `Mesbah Uddin — WhatsApp: 01606481782`, and only in captions that need a contact line.
