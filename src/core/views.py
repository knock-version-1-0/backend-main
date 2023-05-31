import re

def parse_max_age(header):
    # 정규 표현식을 사용하여 max-age 값을 추출
    max_age_match = re.search(r'max-age=(\d+)', header)
    if max_age_match:
        max_age_str = max_age_match.group(1)
        # 추출한 max-age 값을 정수로 변환하여 반환
        return int(max_age_str)
    else:
        return None
