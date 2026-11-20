# stories.py — ONE editable story-data file for news-image-20261120 v2.
# Sources: ~/workspace/makefun/news-image-20261120-evening-candidates.md
# (§§A + G, incl. G.2 updates) and ~/workspace/makefun/news-image-20261120-concept/
# research-v2-verified.md (R1–R21). Every number traces to one of those files,
# or to the builder's own live verification noted below.
#
# LIVE VERIFICATIONS by this builder (Sat 21 Nov ~01:00 WIB, before render):
#  * Kyiv toll: Reuters (via SRN) + The Times + Fox + h.ua + Devdiscourse agree
#    8 killed (6 Kyiv + 2 Lviv), 28 injured; 15 injured in Kyiv. The "9 total"
#    figure is CNN single-outlet — NOT used. Coordinator's earlier "7 Kyiv / 9
#    overall" instruction is superseded by this multi-source check; the 04:30
#    re-check must freeze the toll (RESERVED below).
#  * Hodeidah strike: Reuters (via TBS/SRN) — coalition said it struck Hodeidah
#    port on Fri 20 Nov to destroy Houthi capabilities; warning 10:39 GMT,
#    strike announced 13:31 GMT. Added to the Houthis deck.
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
    ("8", "killed in Kyiv and Lviv"),
    ("24.58m", "GTA VI copies, day-one est."),
    ("100,000", "youth scheme cap, each side"),
    ("\u00a317.0bn", "UK October borrowing"),
    ("73", "German protest cities"),
    ("20,000", "Kenya phase-1 barrels a day"),
]

REGIONS = [
    ("EUROPE", 10, "#2B5EA7"),
    ("ASIA", 11, "#B3271E"),
    ("OCEANIA", 2, "#2E7D6B"),
    ("AMERICAS", 4, "#7A4A9E"),
    ("MIDDLE EAST", 3, "#B7791F"),
    ("WORLD", 5, "#555555"),
    ("AFRICA", 2, "#8A5A2B"),
]

FIELDS = [
    ("WAR", 5),
    ("ECONOMY", 11),
    ("DISASTERS", 1),
    ("SPORT", 4),
    ("JUSTICE", 2),
    ("POLITICS", 6),
    ("SOCIETY", 5),
    ("TECH", 2),
    ("CLIMATE", 1),
]

# id, region, field, place line, headline, deck, art key, source tag.
# Leads (ids 1-13) get illustrated cards; the rest are ALSO ON briefs.
STORIES = [
    dict(id=1, region="Europe", field="War", place="KYIV, UKRAINE",
         headline="Russian missiles hit Kyiv bridges overnight",
         deck="At least 8 killed \u2014 6 in Kyiv, 2 in Lviv; 3 bridges hit, "
              "power cut in several districts.",
         art="kyiv", src="Reuters"),
    dict(id=2, region="Asia", field="Disasters", place="ODISHA, INDIA",
         headline="Cyclone Akvan comes ashore in eastern India",
         deck="Crossed near Gopalpur 07:30\u201308:30 IST; 372,000 evacuated, "
              "423 teams; officials: no major damage yet.",
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
         headline="Coalition strikes Hodeidah after warning",
         deck="Civilians told to leave, then the coalition hits the port; "
              "Saree says Jeddah would be hit if it attacks.",
         art="houthis", src="Reuters"),
    dict(id=9, region="World", field="Society", place="WORLD",
         headline="GTA VI day-one sales put at $2.36bn \u2014 estimate",
         deck="Sensor Tower estimate: ~24.58m copies on launch day; "
              "PS5 ~75%. No official figures yet.",
         art="gta", src="Sensor Tower"),
    dict(id=10, region="World", field="Tech", place="SPACE",
         headline="Spacecraft set for Mercury orbit on Saturday",
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
         deck="Expected to withdraw within a month; Kataib forces enter "
              "Jurf al-Sakhar under a deal.",
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
         headline="US stocks slide again \u2014 intraday",
         deck="SPY \u22120.6%, QQQ \u22121.2% early; Anthropic down "
              "~6\u201310% premarket.",
         art=None, src="StockSetups"),
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
         deck="No exploitation reported; fixes shipped. Censys tracker "
              "(19 Nov, upper bound).",
         art=None, src="Censys"),
    dict(id=23, region="World", field="Economy", place="WORLD",
         headline="Oil falls for third week \u2014 intraday",
         deck="Brent ~$90.50, down ~5% on the week. Close pending.",
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
         deck="Final 8 in Bologna ends his 17 years.",
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
         headline="Trump holds White House presser after Asia trip",
         deck="$17bn+ in deals claimed; Thailand trade deal, "
              "Philippines pledge.",
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
    "dated in the deck. Contested claims are attributed; intraday figures labelled. "
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
    (1, 0.575, 0.235), (2, 0.75, 0.42), (3, 0.86, 0.32),
    (4, 0.51, 0.235), (5, 0.45, 0.24), (6, 0.62, 0.35),
    (7, 0.46, 0.325), (8, 0.64, 0.43), (9, 0.17, 0.35),
    (10, 0.52, 0.325), (11, 0.53, 0.52), (12, 0.86, 0.30),
    (33, 0.22, 0.26),
]

# ---------------------------------------------------------------------------
# RESERVED — 04:30 WIB Sat re-check (do NOT fill before it lands; edit this
# file only, then re-render). Items that slot in as a final revision before
# the 08:00 freeze:
#   * A1 Kyiv toll freeze: live multi-source figure at build time is 8 killed
#     (6 Kyiv + 2 Lviv), 28 injured. If the re-check moves it (e.g. CNN's 9
#     gains a second source), update story 1 deck + NUMBERS slot 1.
#   * COP31 final text (story 6): deadlock/overtime now; if a final text is
#     adopted, replace the deck with the adopted outcome (fossil-fuel
#     language in/out, adaptation-finance figure) — never claim an outcome
#     that has not happened.
#   * Trump presser follow-up (story 33): any overnight follow-up.
#   * US Fri close (story 18): replace intraday SPY/QQQ + Anthropic
#     premarket figures with the final close; drop "intraday" from the
#     headline when the close is in.
#   * Oil Fri close (story 23): replace intraday Brent ~$90.50 with the
#     final settle + confirmed weekly fall; drop "intraday" when in.
#   * R18 MARAD memo: DROPPED from this image (single primary source).
#     Revisit only if a second independent source confirms it.
# ---------------------------------------------------------------------------
