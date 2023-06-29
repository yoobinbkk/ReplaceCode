import os

# --- 라인 구별용 -------------------------------------------------------------------------------------

# 찾는 라인인지 확인하는 함수
def check_target(line, target_line):
    for target in target_line:
        if target not in line:
            return False
    return True

# 제외되어야 하는 라인인지 확인하는 함수
def check_exclusions(line, exclusions):
    for exclusion in exclusions:
        if exclusion in line:
            return False
    return True

# --- 라인 처리용 -------------------------------------------------------------------------------------

# 라인 출력하는 함수
def print_lines(lines, file_path, conditions):

    # 파일 이름 출력하는 조건 설정
    pathNameTF = True

    # 찾는 라인을 출력하기
    for i, line in enumerate(lines):
        if check_target(line, conditions["target_line"]):
            if check_exclusions(line, conditions["exclusions"]):

                # 파일 이름 출력
                if pathNameTF:
                    print(file_path)
                pathNameTF = False
                
                # 라인의 수와 라인 출력
                print(f"\t{i+1} {line.strip()}", end="")
                print()

# 라인 적는 함수
def write_lines(lines, file_path, conditions):

    # 파일 이름 출력하는 조건 설정
    pathNameTF = True

    fw = open(conditions["txt_path"], 'a', encoding='utf-8')
    # 찾는 라인을 출력하기
    for i, line in enumerate(lines):
        if check_target(line, conditions["target_line"]):
            if check_exclusions(line, conditions["exclusions"]):

                # 파일 이름 적기
                if pathNameTF:
                    fw.write(file_path + "\n")
                pathNameTF = False

                # 라인의 수와 라인 적기
                fw.write("\t[" + str(i+1) + "]" + line.strip() + "\n")
    
    if pathNameTF == False:
        fw.write("\n")
    
    fw.close

# 라인 적는 함수
def replace_lines(lines, file_path, conditions):

    fw = open(file_path, 'a', encoding='utf-8')
    # 찾는 라인을 출력하기
    for line in enumerate(lines):
        if check_target(line, conditions["target_line"]) and check_exclusions(line, conditions["exclusions"]):

            # 라인의 수와 라인 적기
            fw.write(line.replace(conditions["part_to_replace"][0], conditions["part_to_replace"][1]))
        else:
            fw.write(line)
    
    fw.close

# --- 파일 처리용 -------------------------------------------------------------------------------------

# 파일 읽는 함수
def read_file(file_path):
    fr = open(file_path, 'r', encoding='utf-8')
    lines = fr.readlines()
    fr.close
    return lines

# 결과를 출력하는 함수
def process_file(file_path, conditions):

    # 파일 읽기
    lines = read_file(file_path)

    # 라인 출력하기
    {conditions["method"]}(lines, file_path, conditions)

# 폴더이면 그 안의 내용물을 처리하는 함수
def process_dir(conditions):

    # 경로 변수
    path = conditions["path"]

    # 파일과 폴더의 목록을 가져오기
    item_list = os.listdir(path)

    # 하나씩 처리하기
    for item in item_list:

        # 폴더의 경로 + 파일 이름 = 파일의 경로
        current_path = os.path.join(path, item) ########## <--------------------------- 다른 방식 시도? [\ --> /]

        # 파일이면 처리
        if os.path.isfile(current_path):

            # 확장자 확인
            if current_path.endswith(conditions["extension"]):

                # 파일 처리
                process_file(current_path, conditions)
        
        # 폴더이면 재귀함수 실행
        elif os.path.isdir(current_path):
            process_dir(current_path)

# 작업 실행
def init(conditions):
    process_dir(conditions)



## 미완성!! --> 전역변수가 먹히는 지, 아니면 파라미터를 넘겨야 하는 지 확인해야 함.

# count += 1
# fw.write("("+str(count)+")")

# replace variable