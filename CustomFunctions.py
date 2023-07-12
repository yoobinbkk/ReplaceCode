import re

# 라인에 숫자가 있는지 확인
def check_number(line):
    if len(re.findall(r'\d+', line)) != 0:
        return True
    return False

    # 사용법
    # if check_target(line, conditions) and check_number(line):