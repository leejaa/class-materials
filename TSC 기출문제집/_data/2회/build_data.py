# -*- coding: utf-8 -*-
import json
STYLE = ("Flat 2D Korean-textbook illustration for a language exam. Bold clean uniform black outlines, "
         "simple flat cel colors, minimal shading, simple uncluttered background, bright friendly palette. "
         "No text, no letters, no numbers, no speech bubbles, no watermark.")

Q = [
 (1,"제1부분","1","你叫什么名字？","이름이 무엇입니까?",None),
 (2,"제1부분","2","请说出你的出生年月日。","생년월일을 말해 보세요.",None),
 (3,"제1부분","3","你家有几口人？","가족이 몇 명입니까?",None),
 (4,"제1부분","4","你在什么地方工作？或者你在哪个学校上学？","어디에서 일합니까? 또는 어느 학교에 다닙니까?",None),

 (5,"제2부분","1","男的在做什么？","남자는 무엇을 하고 있습니까?",
  "A man wearing a bicycle helmet riding a yellow bicycle along a riverside bike path. He wears a teal long-sleeve "
  "shirt and blue trousers. Behind him a wide blue river, a long bridge, and a city skyline under a blue sky. Side view."),
 (6,"제2부분","2","谁比较快？","누가 더 빠릅니까?",
  "Two children running to the left across a sandy beach chasing a colorful beach ball that is rolling ahead of them. "
  "The GIRL with a ponytail in an orange shirt and blue shorts is clearly AHEAD, closer to the ball. The BOY in a "
  "white shirt and green shorts is BEHIND her. Blue sea and sky in the background."),
 (7,"제2부분","3","照相机多少钱？","카메라는 얼마입니까?",None),  # 가격표 → 직접 렌더링
 (8,"제2부분","4","他们在书店吗？","그들은 서점에 있습니까?",
  "A doctor's examination room in a clinic. A male doctor in a white coat with a stethoscope sits on a stool holding "
  "a medical instrument, examining a small girl who sits on her mother's lap. The mother wears a pink cardigan. "
  "An X-ray viewer on the wall and a computer on a desk behind them. Clearly a hospital, not a shop."),

 (9,"제3부분","1","周末你一般做什么？","주말에 보통 무엇을 하나요?",
  "A male student in a yellow sweater with a shoulder bag talking to a female student in a pink cardigan with a "
  "backpack, standing outdoors on a school campus in front of school buildings. Daytime, casual conversation."),
 (10,"제3부분","2","我这次英语考试成绩不太好。","이번 영어 시험 성적이 별로 안 좋아.",
  "Inside a classroom. A female student in a red cardigan stands at her desk holding a test paper with a worried, "
  "disappointed face. A male student in a green patterned sweater sits at the desk beside her, looking at her with "
  "concern. Plain warm-toned background with silhouettes of other students."),
 (11,"제3부분","3","您要换的这顶帽子是什么时候买的？","교환하시려는 이 모자는 언제 사셨나요?",
  "Inside a hat shop with shelves of colorful hats on the walls. A male shop clerk in a navy vest and white shirt "
  "stands behind the counter, receiving a yellow paper shopping bag from a female customer in a pink cardigan with "
  "a brown shoulder bag standing on the other side of the counter."),
 (12,"제3부분","4","你一般多长时间去一次电影院？","보통 얼마나 자주 영화관에 가나요?",
  "Two women sitting across a small round table in a bright cafe with large windows showing a city view, each "
  "holding a white coffee cup and chatting. One wears a purple striped sweater, the other a light blue striped sweater."),
 (13,"제3부분","5","剩下很多菜，怎么办？","음식이 많이 남았는데 어떡하죠?",
  "A man in a green sweater and a woman in an orange sweater sitting across a round restaurant table with a yellow "
  "tablecloth. Several dishes with LOTS OF LEFTOVER FOOD remain on the table. The man looks troubled at the leftovers. "
  "Other diners at tables in the blurred background."),

 (14,"제4부분","1","在你的家人中，你跟谁最像？请简单谈谈看。","가족 중 누구와 가장 닮았습니까?",None),
 (15,"제4부분","2","你平时常喝可乐、汽水之类的饮料吗？请简单谈谈。","평소 콜라, 탄산음료 같은 것을 자주 마십니까?",None),
 (16,"제4부분","3","你跟朋友一起去旅行过吗？请简单说一说。","친구와 함께 여행을 가 본 적이 있습니까?",None),
 (17,"제4부분","4","你家附近有银行、百货商店、电影院等生活服务设施吗？请简单谈一谈。","집 근처에 은행, 백화점, 영화관 같은 편의시설이 있습니까?",None),
 (18,"제4부분","5","你喜欢管理个人网页或博客吗？请简单说说。","개인 홈페이지나 블로그 운영을 좋아합니까?",None),

 (19,"제5부분","1","你认为压力会影响人们的健康吗？请说说你的想法。","스트레스가 건강에 영향을 준다고 생각합니까?",None),
 (20,"제5부분","2","很多大学生找工作时只想进大企业，对于这种现象你怎么看？","많은 대학생이 대기업만 가려 합니다. 이 현상을 어떻게 봅니까?",None),
 (21,"제5부분","3","你认为网上购物的普遍化给人们的生活带来了什么变化？请谈谈你的看法。","온라인 쇼핑의 보편화가 생활에 어떤 변화를 가져왔다고 봅니까?",None),
 (22,"제5부분","4","你认为个人的性格和他选择什么方式度过业余生活有关系吗？请谈谈你的看法。","개인의 성격과 여가 생활 방식이 관계가 있다고 봅니까?",None),

 (23,"제6부분","1","你跟朋友约好周六晚上见面，但突然得到了喜欢的歌手那天的演唱会门票，不能跟朋友见面了。请你给她打电话说明情况，并改约时间。",
  "친구와 토요일 저녁 약속을 했는데 좋아하는 가수의 그날 콘서트 표가 생겨 만날 수 없게 되었습니다. 전화로 상황을 설명하고 약속을 다시 잡으세요.",
  "A man in a blue polo shirt standing in a living room, holding a mobile phone to his ear with one hand and "
  "scratching his head with the other, wearing an awkward apologetic expression. A TV on a low stand on the left, "
  "a large window with a curtain on the right."),
 (24,"제6부분","2","你的同屋是刚来留学不久的中国人，她向你打听超市在哪儿。请你给她推荐一个地方，并告诉她怎么走。",
  "룸메이트가 유학 온 지 얼마 안 된 중국인인데 슈퍼마켓이 어디인지 묻습니다. 한 곳을 추천하고 가는 길을 알려 주세요.",
  "Two female students in a dormitory room with a bunk bed. One in a yellow sweater sits on the edge of the lower "
  "bunk listening. The other in a green sweater sits on a chair at a desk, gesturing with one hand as she explains "
  "directions. A notebook on the desk."),
 (25,"제6부분","3","你把手套落在地铁上了。请你去地铁站的失物招领中心说明情况，并请求帮助。",
  "지하철에 장갑을 두고 내렸습니다. 역 분실물 센터에 가서 상황을 설명하고 도움을 요청하세요.",
  "A lost-and-found office counter at a subway station. A man in a blue sweater stands at the counter gesturing as "
  "he explains something with a worried face. A female staff member in a red vest and white shirt stands behind the "
  "counter listening. Tall grey shelves full of stored items behind her, a monitor on the counter."),

 (26,"제7부분","1","现在请根据图片的内容讲述故事，请尽量完整、详细。讲述时间是90秒。","그림 내용에 따라 이야기를 해 보세요. 90초입니다.","__STORY__"),
]

STORY = """A 4-panel comic strip arranged left to right in a single row, each panel with a thin black border.
""" + STYLE + """
The SAME characters must look IDENTICAL in all four panels:
- FATHER: short dark hair, dark green sweater over shirt, dark trousers, carries a brown briefcase
- MOTHER: shoulder-length dark wavy hair, red top, blue skirt
- SON: about 6 years old, green sweater, blue trousers, short dark hair

PANEL 1 - Home entrance hallway. The FATHER stands ready to leave for work, his brown briefcase on the floor beside
him with a black mobile phone lying on top of it. The little SON stands in front holding a PINK toy phone, looking
mischievous. The MOTHER walks in from the right carrying a tray with a mug.

PANEL 2 - The FATHER walks out through the front door carrying his briefcase, waving goodbye; the SON waves back
happily. In the foreground the MOTHER has a SHOCKED alarmed face with a hand raised to her cheek, because she has
just noticed the black phone left behind and realizes the boy swapped them.

PANEL 3 - An office with desks and colleagues. The FATHER stands holding his briefcase, taking a phone out of his
pocket with a puzzled startled expression as it rings. Music notes float in the air. Colleagues at nearby desks
turn to look.

PANEL 4 - THE PUNCHLINE, must show embarrassment: the FATHER is holding up the PINK TOY PHONE which is loudly
playing a childish tune, with a mortified red-faced expression and sweat drops. The colleagues around him are
LAUGHING. Music notes and motion lines around the toy."""

data = []
for n, part, num, zh, ko, p in Q:
    img = None
    if p == "__STORY__":
        img = {"file": "g2_7.png", "prompt": STORY, "size": "1536x1024"}
    elif p:
        img = {"file": f"g2_{n:02d}.png", "prompt": f"{STYLE}\n\n{p}", "size": "1024x1024"}
    data.append({"n": n, "part": part, "num": num, "zh": zh, "ko": ko, "img": img})

json.dump({"_meta": {"source": "TSC 기출문제집 온라인 영상 테스트 기출 2회 (YouTube 1UF4jkOG_Jw)",
                     "note": "질문=화면 OCR+구간별 개별 전사. Q7은 가격표라 직접 렌더링."},
           "questions": data}, open("tsc_yt02.json","w"), ensure_ascii=False, indent=1)
print("문항", len(data), "/ 생성대상", sum(1 for d in data if d["img"]))
