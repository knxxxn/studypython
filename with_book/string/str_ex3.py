#금지된 단어를 제외한 가장 흔하게 등장하는 단어를 출력해라. 대소문자 구분을 하지 않으며, 구두점(마침표, 쉼표 등) 또한 무시한다
#입력 paragraph = "hit a ball, the hit ball"  banned=["hit"]
#출력 "ball"

import re
from collections import Counter


def commonWord(paragraph, banned):
    # 1. 소문자로 변환
    paragraph = paragraph.lower()

    # 2. 구두점 제거 (알파벳만 남김)
    paragraph = re.sub(r'[^a-z]', ' ', paragraph)

    # 3. 단어 분리
    words = paragraph.split()

    # 4. 금지 단어 set
    banned_set = set(banned)

    # 5. 금지 단어 제외
    filtered_words = [word for word in words if word not in banned_set]

    # 6. 가장 흔한 단어 찾기
    counter = Counter(filtered_words)

    return counter.most_common(1)[0][0]
