#!/usr/bin/env python3
"""由 shops.json 產生 README.md、massage.kml（可匯入 Google 我的地圖）與 index.html（總地圖）。"""
import json, html, urllib.parse, pathlib, re

D = pathlib.Path(__file__).parent
shops = json.loads((D / 'shops.json').read_text(encoding='utf-8'))

def gmap(s):
    addr = re.sub(r'（[^）]*）', '', s['addr'])
    return 'https://www.google.com/maps/search/?api=1&query=' + urllib.parse.quote(f"{s['name']} {addr}") + '&hl=en'

for s in shops:
    s['gmap'] = gmap(s)

AREAS = ['夜市/長康路', '古城', '古城南/Wualai', '寧曼', '濱江區', '郊區', '清萊']
TIERS = ['平價', '中價', '中價連鎖', '中高價', '高價']

# ---------- README ----------
md = ['# 清邁按摩總整理（含 Google 地圖與總地圖）', '',
      '6 人清邁行程（2026/11/11–11/18，住 Loi Kroh Road）用的按摩/SPA 清單。',
      '每間店都有 Google 地圖連結，另外有一張**所有按摩店的總地圖**：', '',
      '- 🗺️ **互動總地圖**：打開 [`index.html`](index.html)（可篩選區域／價位，點標記看介紹與 Google 地圖）。底圖街道與地名為英文（Esri，右上角可切換泰文 OpenStreetMap）；也可切換「Google 地圖（英文）」看每間店周邊',
      '- 🔤 所有 Google 地圖連結都加上 `hl=en`，開啟後街道名稱顯示英文，方便對照路牌或給司機看',
      '- 📍 **Google 我的地圖版**：到 [Google 我的地圖](https://www.google.com/maps/d/) → 建立新地圖 → 匯入 → 上傳 [`massage.kml`](massage.kml)，就會得到一張可在手機 Google Maps 開啟的總圖',
      '', '> 價格、營業時間整理自公開資料（官網、Klook、KKday、Chiang Mai Citylife 等），可能變動，出發前請再確認。地圖上的標記位置為概略，精確位置請以各店 Google 地圖連結為準。', '',
      '## 怎麼選', '',
      '| 需求 | 推薦 |', '|---|---|',
      '| 每天平價按一下（250～350銖/小時） | Lila Thai Massage（古城多家）、女子監獄按摩、Green Bamboo、Daracha、Relax Express |',
      '| 清邁特有 Tok Sen 木槌按摩／寺廟按摩 | 潘萬寺（古城，可現場排）、銀廟 Wat Sri Suphan（需提前約一週預約） |',
      '| 晚上很晚還想按 | Let\'s Relax（到24:00）、Relax Express（到24:00）、Cozy 寧曼15巷（到01:00） |',
      '| 深度傳統泰醫體驗 | 舊醫院按摩學校、Baan Hom 草藥中心（含草藥蒸浴） |',
      '| 6 人同時預約、CP 值高 | Health Land（長康路）、Let\'s Relax（各分店營業到午夜） |',
      '| 想要環境氣氛（1,500銖起/2小時） | Fah Lanna、Makkha |',
      '| 奢華犒賞 | Oasis Spa、Zira Spa、RarinJinda、Dheva Spa（Dhara Dhevi） |',
      '| 免費飯店接送 | Kiyora Spa（市區內） |',
      '| 離民宿（Loi Kroh Rd）最近 | Makkha 夜市店、Fah Lanna 夜市店、Let\'s Relax Pavilion、Health Land |', '']
for area in AREAS:
    rows = [s for s in shops if s['area'] == area]
    if not rows: continue
    md += [f'## {area}', '', '| 店名 | 價位 | 價格 | 營業時間 | 地圖 | 預約 |', '|---|---|---|---|---|---|']
    for s in rows:
        k = f"[Klook]({s['klook']})" if s['klook'] else '現場/電話'
        md.append(f"| **{s['zh']}**<br>{s['name']} | {s['tier']} | {s['price']} | {s['hours']} | [📍 Google 地圖]({s['gmap']}) | {k} |")
    md.append('')
    for s in rows:
        md.append(f"- **{s['zh']}**：{s['desc']} 地址：{s['addr']}" + (f"；電話 {s['phone']}" if s['phone'] else '') + (f"。🗓️ {s['trip']}" if s['trip'] else ''))
    md.append('')
md += ['## 按摩小常識', '',
       '- **泰式按摩（Thai）**：不用油、穿寬鬆衣服，拉筋按壓，力道偏重；不喜歡痛可說 "soft, please"。',
       '- **腳底按摩（Foot）**：逛街走累最適合，約200～300銖/小時。',
       '- **精油按摩（Oil）**：放鬆舒壓，價格約泰式的1.5倍。',
       '- **草藥球（Herbal compress）**：熱敷草藥球，很多套餐會附。',
       '- **小費**：平價店每人約50～100銖，SPA 約100銖或總價10%。',
       '- **6 人同行**：中高價 SPA 房間/技師有限，請提前用 Klook 或電話預約；平價店可分兩批。', '',
       '## 資料來源', '',
       '- Klook 清邁按摩搜尋：https://www.klook.com/zh-TW/search/result/?query=%E6%B8%85%E9%82%81%20%E6%8C%89%E6%91%A9',
       '- Health Land 官網：https://www.healthlandspa.com/en/location/chiang-mai/chiang-mai',
       '- Let\'s Relax 分店：https://letsrelaxspa.com/branches/chiang-mai-thapae/',
       '- Makkha 分店：https://www.makkhahealthandspa.com/makkha-chiangmai-spa/',
       '- Fah Lanna 官網：https://fahlanna.com/',
       '- 慢活豬義 清邁SPA格價：https://piggyhygge.com/thailand-chiangmai-spa-massage/',
       '- 蔡小妞 清邁按摩推薦：https://tsnio.com/chiangmai-massage/',
       '- Time Out 寺廟按摩（銀廟/潘萬寺）：https://www.timeout.com/chiang-mai/attractions/chiang-mais-top-5-temple-massages',
       '- Jetsetting Fools 清邁泰式按摩：https://jetsettingfools.com/traditional-thai-massages/',
       '- Kiyora Spa 官網：https://kiyoraspa.com/contact-us/',
       '- Baan Hom Samunphrai 官網：https://homprang.com/',
       '- Dheva Spa（Chiang Mai Citylife）：https://chiangmaicitylife.com/citylife-articles/dheva-spa-wellness-centre',
       '- NBC 女子監獄按摩：https://www.nbcnews.com/news/asian-america/what-its-get-massage-thai-prison-n348986', '',
       '## 更新方式', '', '編輯 `shops.json` 後執行 `python3 build.py`，會重新產生 README.md、massage.kml、index.html。', '']
(D / 'README.md').write_text('\n'.join(md), encoding='utf-8')

# ---------- KML ----------
e = html.escape
pm = []
for s in shops:
    d = f"{s['desc']}<br>地址：{s['addr']}<br>價格：{s['price']}<br>營業：{s['hours']}" + (f"<br>電話：{s['phone']}" if s['phone'] else '') + (f"<br>預約：{s['klook']}" if s['klook'] else '')
    pm.append(f"<Placemark><name>{e(s['zh'])}</name><description><![CDATA[{d}]]></description><Point><coordinates>{s['lng']},{s['lat']},0</coordinates></Point></Placemark>")
folders = ''.join(f"<Folder><name>{e(a)}</name>" + ''.join(p for s, p in zip(shops, pm) if s['area'] == a) + '</Folder>' for a in AREAS)
(D / 'massage.kml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2"><Document><name>清邁按摩總圖</name>{folders}</Document></kml>\n', encoding='utf-8')

# ---------- index.html ----------
tpl = (D / 'template.html').read_text(encoding='utf-8')
(D / 'index.html').write_text(tpl.replace('/*SHOPS*/[]', json.dumps(shops, ensure_ascii=False)), encoding='utf-8')
print('built', len(shops), 'shops')
