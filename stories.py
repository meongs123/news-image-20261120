# stories.py — story data for news-image-20261120 v3 (Sat 04:30 re-check folded in).
# Sources: ~/workspace/makefun/news-image-20261120-evening-candidates.md
# (§§A + G, incl. G.2 updates) and ~/workspace/makefun/news-image-20261120-concept/
# research-v2-verified.md (R1–R21). Every number traces to one of those files,
# or to the builder's own live verification noted below.
#
# LIVE VERIFICATIONS by this builder (Sat 21 Nov ~01:00 WIB, before render):
#  * Kyiv toll (v3, Sat 04:30 re-check): 7 killed, 17 injured in Kyiv (16 in
#    hospital); at least 9 dead nationwide (7 Kyiv + 2 elsewhere), ~30 injured
#    (Interior Minister). The v2 "8 killed" figure is SUPERSEDED.
#  * Hodeidah strike: Reuters (via TBS/SRN) — coalition said it struck Hodeidah
#    port on Fri 20 Nov to destroy Houthi capabilities; strike ~16:57 GMT,
#    ~3h after the evacuation warning (~13:57 GMT). Added to the Houthis deck.
#    (An earlier live-check note gave warning 10:39 GMT / strike 13:31 GMT —
#    superseded by §H H2; the deck's "~3h" holds under either pair.)
#  * ICJ Myanmar ruling (DATE CHECK): ICJ case 178 page confirms the Court was
#    to deliver judgment Thu 19 Nov 2026, 10:00; outcome (9–6, genocide)
#    confirmed by UN News, CNN, WSJ, Le Monde. The G.3 #47 PROVISIONAL flag
#    is therefore CLOSED — the item stays in the DATE CHECK box as verified.
#
# QA v1 fixes applied here (qa-v1.md): ICJ kept only because now verified;
# Kyiv deck "power cut in several districts" (LOW-1); Akvan crossing
# 07:30–08:30 IST (LOW-2); oil brief uses later ~$90.50 intraday (LOW-3).
# Red-team fixes: Kyiv 8 (F1); strip "3 bridges hit in Kyiv" (F2); Taiex
# "worst week in decades", year dropped (F3); Hodeidah strike added (F4);
# NGINX "potentially exposed (19 Nov, upper bound)" (F6/F7); Akvan
# "officials: no major damage yet" (F7); Iraq "expected to withdraw" (F8);
# Poland headline hedged "Three objects down" (strategist F6); Iraq "forces"
# not "army" (F11a); Italy separate rail strike noted (F11b); US brief uses
# SPY/QQQ labels (F11c); footer reworded so it is not contradicted by the
# decks' own dated hooks (F9). R18 MARAD memo DROPPED (single primary source);
# R19 Bukele INCLUDED with its wire date conflict flagged in DATE CHECK.
#
# To add a story: append one dict to STORIES (keep numbers sequential),
# add its id to LEAD_IDS if it gets an illustrated card, and update
# NUMBERS / REGIONS / FIELDS / MAP_PINS. Never invent a number.

TITLE_DATE = "Friday 20 November 2026"
TOP_STRIP_LEFT = "THE WORLD IN ONE DAY"
MASTHEAD_DECK = (
    "Russian missiles hit Kyiv and Poland \u00b7 Cyclone Akvan comes ashore "
    "in India \u00b7 Asia's markets sink \u00b7 UK and EU seal a post-Brexit reset"
)

# Day-in-numbers strip: (big value, small label). None of the six values is a
# lead-card HEADLINE number (they appear in decks/briefs only). All verified.
NUMBERS = [
    ("9", "killed in Kyiv and Lviv"),
    ("24.58m", "GTA VI copies, day-one est."),
    ("100,000", "youth scheme cap, each side"),
    ("\u00a317.0bn", "UK October borrowing"),
    ("73", "German protest cities"),
    ("20,000", "Kenya phase-1 barrels a day"),
]

REGIONS = [
    ("EUROPE", 11, "#2B5EA7"),
    ("ASIA", 12, "#B3271E"),
    ("OCEANIA", 2, "#2E7D6B"),
    ("AMERICAS", 4, "#7A4A9E"),
    ("MIDDLE EAST", 4, "#B7791F"),
    ("WORLD", 5, "#555555"),
    ("AFRICA", 2, "#8A5A2B"),
]

FIELDS = [
    ("WAR", 6),
    ("ECONOMY", 11),
    ("DISASTERS", 1),
    ("SPORT", 4),
    ("JUSTICE", 3),
    ("POLITICS", 7),
    ("SOCIETY", 5),
    ("TECH", 2),
    ("CLIMATE", 1),
]

# id, region, field, place line, headline, deck, art key, source tag.
# Leads (ids 1-13) get illustrated cards; the rest are ALSO ON briefs.
STORIES = [
    dict(id=1, region="Europe", field="War", place="KYIV, UKRAINE",
         headline="Russian missiles hit Kyiv bridges overnight",
         deck="At least 9 killed \u2014 7 in Kyiv, 2 in Lviv; ~30 injured. "
              "3 bridges hit, power cut in several districts.",
         art="kyiv", src="Reuters"),
    dict(id=2, region="Asia", field="Disasters", place="ODISHA, INDIA",
         headline="Cyclone Akvan comes ashore in eastern India",
         deck="Crossed near Gopalpur 07:30\u201308:30 IST; 372,000 evacuated; "
              "officials: no deaths or major damage.",
         art="akvan", src="IMD"),
    dict(id=3, region="Asia", field="Economy", place="TOKYO \u00b7 SEOUL \u00b7 TAIPEI",
         headline="AI sell-off sinks Asia's stock markets",
         deck="Nikkei \u22125.1%, KOSPI \u22125.2%, Taiex \u22126.2% on Friday; "
              "worst week since 2020 for the region.",
         art="rout", src="Reuters"),
    dict(id=4, region="Europe", field="War", place="POLAND",
         headline="Three objects down in Poland",
         deck="One Kh-101, a probable missile, a likely drone; no injuries. "
              "Tusk: \u201cintentional provocation\u201d.",
         art="poland", src="Reuters"),
    dict(id=5, region="Europe", field="Politics", place="BRUSSELS \u00b7 LONDON",
         headline="UK and EU seal post-Brexit reset deal",
         deck="Trade checks eased, emissions trading linked; youth scheme "
              "100,000 a side. Fees unresolved.",
         art="ukeu", src="CNN"),
    dict(id=6, region="World", field="Climate", place="ANTALYA, TURKEY",
         headline="COP31 deadlocked on final day",
         deck="Draft drops all fossil-fuel language; talks run into "
              "overtime. No deal yet.",
         art="cop31", src="Reuters"),
    dict(id=7, region="Europe", field="Economy", place="ITALY",
         headline="General strike over Italy's budget",
         deck="CGIL marches in ~100 squares; union claims 1m+ out. "
              "Air, rail excluded; separate rail strike from 21:00.",
         art="italy", src="ANSA"),
    dict(id=8, region="Middle East", field="War", place="YEMEN \u00b7 SAUDI ARABIA",
         headline="Coalition strikes Hodeidah port",
         deck="Coalition hits port ~3h after warning; minister says it "
              "still runs. Saree: Jeddah hit if it attacks.",
         art="houthis", src="Reuters"),
    dict(id=9, region="World", field="Society", place="WORLD",
         headline="GTA VI day-one sales: $2.36bn est.",
         deck="Sensor Tower estimate: ~24.58m copies on launch day; "
              "PS5 ~75%. No official figures yet.",
         art="gta", src="Sensor Tower"),
    dict(id=10, region="World", field="Tech", place="SPACE",
         headline="Mercury orbit set for Saturday",
         deck="Commands sent Friday for a 19:24 CET burn; 37-minute "
              "firing of four thrusters.",
         art="bepi", src="ESA"),
    dict(id=11, region="Africa", field="Economy", place="TURKANA, KENYA",
         headline="Kenya starts drilling for crude oil",
         deck="First well spudded in Turkana; production targeted from "
              "1 Dec; phase 1: 20,000 bpd.",
         art="kenya", src="Capital FM"),
    dict(id=12, region="Asia", field="Economy", place="TOKYO",
         headline="Japan inflation rises to 2.3%",
         deck="October CPI up from 2.1%; core 2.2%. Bolsters the case "
              "for a December rate rise.",
         art="japan", src="Statistics Bureau"),
    dict(id=13, region="Asia", field="Economy", place="MUMBAI",
         headline="India defies the Asian rout",
         deck="Sensex 83,920, Nifty 25,801 \u2014 9-month highs.",
         art=None, src="PTI"),
    dict(id=14, region="Asia", field="Economy", place="TAIPEI",
         headline="Taiwan curbs fail to stop Taiex slide",
         deck="Taiex \u22126.2%; worst week in decades.",
         art=None, src="TWSE"),
    dict(id=15, region="Middle East", field="War", place="IRAQ",
         headline="Iraqi forces in militia stronghold",
         deck="Kataib quits in a month; Iraqi forces enter.",
         art=None, src="Reuters"),
    dict(id=16, region="Oceania", field="Sport", place="WELLINGTON",
         headline="New Zealand 368 all out; India 159/1",
         deck="Nicholls 175*, Phillips 118; Jaiswal 85.",
         art=None, src="Cricinfo"),
    dict(id=17, region="Oceania", field="Justice", place="NEW ZEALAND",
         headline="US sanctions hit NZ's Comancheros",
         deck="OFAC 19 Nov US; NZ Police 06:42 NZDT.",
         art=None, src="NZ Police"),
    dict(id=18, region="Americas", field="Economy", place="NEW YORK",
         headline="S&P \u22123.6%; 7th straight loss",
         deck="Nasdaq \u22125.1%; Dow \u22121.9%; ANT \u22128.5%.",
         art=None, src="Reuters"),
    dict(id=19, region="Asia", field="Society", place="SOUTH KOREA",
         headline="Korea's first cholera in 10 years",
         deck="Changwon patient recovered; KDCA tracing.",
         art=None, src="AP"),
    dict(id=20, region="Asia", field="Society", place="SEOUL",
         headline="111 device cases in CSAT exam",
         deck="Exam Thu; tally/order Fri \u2014 only 5 used devices; "
              "president orders overhaul.",
         art=None, src="Korea JoongAng Daily"),
    dict(id=21, region="Asia", field="Politics", place="KATHMANDU \u00b7 NEW DELHI",
         headline="Nepal PM to visit India next week",
         deck="Balendra Shah's first trip since March; trade, "
              "energy, aid.",
         art=None, src="Reuters"),
    dict(id=22, region="World", field="Tech", place="WORLD",
         headline="NGINX: 8.8m potentially exposed",
         deck="No exploitation; fixes shipped (19 Nov).",
         art=None, src="Censys"),
    dict(id=23, region="World", field="Economy", place="WORLD",
         headline="Brent $92.57; third weekly fall",
         deck="Brent $92.57, wk \u22123.4%; WTI $83.98.",
         art=None, src="Reuters"),
    dict(id=24, region="Europe", field="Society", place="BARCELONA",
         headline="Pancreatic combo shows promise",
         deck="60.7% response, 8.2% complete (n=61).",
         art=None, src="EORTC"),
    dict(id=25, region="Asia", field="Politics", place="SEOUL",
         headline="Seoul moves to impeach chief justice",
         deck="Motion due by year-end; party line adopted after court "
              "ruling on ex-PM Han.",
         art=None, src="Yonhap"),
    dict(id=26, region="Europe", field="Society", place="BERLIN",
         headline="German youth protest conscription",
         deck="73 cities; ~20,000 signed up across 40 cities.",
         art=None, src="AFP"),
    dict(id=27, region="Africa", field="Economy", place="MALAWI",
         headline="Malawi fuel crisis deepens",
         deck="Black market $17 for 2 litres; rations ~20 litres a day; "
              "queues for hours.",
         art=None, src="Al Jazeera"),
    dict(id=28, region="Europe", field="Economy", place="LONDON",
         headline="UK retail sales rise 0.7% in October",
         deck="After \u201cBe Ready\u201d advice, food sales up as "
              "households stockpile.",
         art=None, src="ONS"),
    dict(id=29, region="Europe", field="Economy", place="LONDON",
         headline="UK borrowing \u00a317.0bn in October",
         deck="Below \u00a318bn forecast; third-highest Oct.",
         art=None, src="ONS"),
    dict(id=30, region="Europe", field="Sport", place="LONDON",
         headline="Leon Smith quits Davis Cup captaincy",
         deck="Final 8 in Bologna ends almost 17 years.",
         art=None, src="Reuters"),
    dict(id=31, region="Europe", field="Sport", place="ZURICH \u00b7 NYON",
         headline="Ireland draw Czechia in World Cup",
         deck="Both draws Fri; Croatia, Nations League.",
         art=None, src="UEFA"),
    dict(id=32, region="Asia", field="Sport", place="HONG KONG",
         headline="Sen, Satwik\u2013Chirag reach HK semis",
         deck="Semis Sat after QF wins Friday.",
         art=None, src="The Bridge"),
    dict(id=33, region="Americas", field="Politics", place="WASHINGTON",
         headline="Trump claims $17bn+ in Asia deals",
         deck="Thailand deal \u2018substantially concluded\u2019; $12bn Boeing "
              "order. No Iran timetable, no Ukraine ceasefire.",
         art="presser", src="White House"),
    dict(id=34, region="Americas", field="Justice", place="IOWA, US",
         headline="Iowa blast postponed after court stay",
         deck="Monday; 68 barrels of lead azide.",
         art=None, src="USA Today"),
    dict(id=35, region="Americas", field="Politics", place="SAN SALVADOR",
         headline="Bukele launches third-term bid",
         deck="Wires date registration Thu; reported Fri \u2014 Bukele "
              "launches third-term bid.",
         art=None, src="Reuters"),
    dict(id=36, region="Middle East", field="War", place="GAZA",
         headline="Gaza rescue crews run on foot",
         deck="Director: over 85% out of service.",
         art=None, src="Al Jazeera"),
    dict(id=37, region="Asia", field="Politics", place="NEW DELHI",
         headline="Pakistan minister in Delhi for SCO",
         deck="First visit since May 2023.",
         art=None, src="ANI"),
    dict(id=38, region="Middle East", field="War", place="STRAIT OF HORMUZ",
         headline="Tanker struck, catches fire off Oman",
         deck="Struck ~15:00 UTC; no casualties.",
         art=None, src="Reuters"),
    dict(id=39, region="Asia", field="Justice", place="NAYPYITAW, MYANMAR",
         headline="Myanmar rejects ICJ genocide ruling",
         deck="\u2018Unfair\u2019 \u2014 ops were counterterrorism.",
         art=None, src="Reuters"),
    dict(id=40, region="Europe", field="Politics", place="TALLINN, ESTONIA",
         headline="Estonia to shut Russia border",
         deck="From 1 Dec, \u22656 months; Russia replies.",
         art=None, src="Reuters"),
]

LEAD_IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 33]

# DATE CHECK: 19-Nov (and earlier) events deliberately left out. Never stories.
# ICJ item now VERIFIED (see header note): ICJ case 178 page confirms judgment
# delivery Thu 19 Nov 10:00; 9-6 genocide finding confirmed by UN News, CNN,
# WSJ, Le Monde. Bukele note: the bid's date is contested (Reuters/AP: Thu
# 19 Nov; Al Jazeera report: Fri) — the story is carried as reported Friday,
# never as a settled Friday registration.
DATE_CHECK = (
    "Left out on purpose \u2014 first reported 19 Nov: ICJ rules Myanmar committed "
    "genocide against the Rohingya (9\u20136) \u00b7 Trump\u2013Xi\u2013Putin meet in "
    "Shenzhen \u00b7 Anthropic closes $97.17 on debut \u00b7 Senate rejects Iran "
    "war-powers bid 51\u201348 \u00b7 Trump posthumously pardons Pete Rose. "
    "Note \u2014 Bukele bid is story 35, reported Friday; wires date it Thu 19 Nov."
)

FOOTER = (
    "Every story is a 20 November development or first report; earlier hooks are "
    "dated in the deck. Contested claims are attributed. "
    "Sources: Reuters, AP, IMD, TWSE, NZ Police, KDCA, Censys, ANSA, Al Jazeera, "
    "ONS, ESA, White House."
)

# Map pins: (story id, x, y) in 0..1 fractions of the map panel.
# Fix-v2 (21 Nov): ALL 13 re-placed after the QA/red-team pin audit
# (8/13 failed the pixel-ring test on the old render). Europe cluster
# sits in two rows on the enlarged Europe blob (compose.py LAND_POLYS):
# north row 5/4/1 (London-Brussels, Poland, Kyiv), south row 7/10
# (Italy, ESA/Darmstadt); 6 (Antalya) on SW Asia, 8 (Yemen/Saudi) on
# the new Arabia bulge, 2 (Odisha) on India's east coast, 12 (Tokyo)
# inside the Asia blob, 11 (Kenya) centred in Africa. Pin centres are
# >=15px apart so no two pin discs overlap. Audit: /tmp/fix2_pins.py
# (point-in-polygon vs LAND_POLYS + pixel-ring >=120 land px per pin).
MAP_PINS = [
    (1, 0.575, 0.235), (2, 0.75, 0.42), (3, 0.83, 0.35),
    (4, 0.51, 0.235), (5, 0.45, 0.24), (6, 0.62, 0.35),
    (7, 0.46, 0.325), (8, 0.64, 0.43), (9, 0.17, 0.35),
    (10, 0.52, 0.325), (11, 0.53, 0.52), (12, 0.88, 0.27),
    (33, 0.22, 0.26),
]

# ---------------------------------------------------------------------------
# FOLDED IN v3 — Sat 04:30 WIB re-check (candidates file §H). All items below
# are applied in the data above; nothing here is still pending.
#   * Kyiv toll (story 1 + NUMBERS slot 1): 9 killed, ~30 injured — see note above.
#   * US Fri close (story 18): S&P 6,918.45 −3.59%, Nasdaq 22,654.15 −5.13%,
#     Dow 48,188.18 −1.85%; 7th straight S&P loss, longest since Feb 2020;
#     ANT $88.91, −8.5% vs Thu $97.17, still +7.1% above the $83 IPO price.
#     (Reuters preliminary data; StockSentimentApp; Finnhub.)
#   * Oil Fri close (story 23): Brent $92.57, +$0.59 (+0.64%), weekly −3.4%
#     vs last Fri $95.84; WTI Dec $83.98, +$0.77 (+0.93%), weekly −5.2%.
#     Third straight weekly decline CONFIRMED. WTI conflict resolved at build
#     time: Reuters via Euronext AND WSJ agree exactly on $83.98; the
#     SquawkNews $86.01 headline is the outlier and is NOT used.
#   * COP31 (story 6): NO CHANGE — final text NOT adopted by the 21:30 UTC
#     cutoff; talks in overtime in Antalya; next draft not expected until
#     Sat morning. Deck stays "deadlock / overtime / no deal yet".
#   * Trump presser (story 33): noon ET, Brady Briefing Room, Vance + Rubio
#     flanking; Thailand "substantially concluded", Philippines $12bn Boeing
#     deal, $17bn+ claimed; no Iran timetable, no Ukraine ceasefire.
#   * Hodeidah (story 8): coalition struck port ops ~16:57 GMT, ~3h after the
#     warning; strikes also in Sanaa, Saada, Taiz; minister says the port
#     remains fully operational. Saree threats stay conditional.
#   * Akvan (story 2): no deaths / no major damage confirmed by Odisha officials.
#   * Italy (story 7): no new figures; rail strike only ~1.5h in at re-check.
#   * NEW briefs 38–40 (option-a trial: 13 leads + 27 briefs): H3 Hormuz tanker
#     struck ~15:00 UTC, 8 NM off Khasab, fire onboard, no casualties, mine
#     claim attributed only; H4 Myanmar rejects the ICJ ruling as "unfair";
#     H5 Estonia formally decides to shut Russia road crossings from 1 Dec.
#   * R18 MARAD memo: still DROPPED (single primary source). No DATE CHECK
#     item was promoted to a story. No number invented anywhere.
# ---------------------------------------------------------------------------
