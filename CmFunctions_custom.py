from CustomFunctions import *
import os

# --- 라인 구별용 -------------------------------------------------------------------------------------

# 찾는 라인인지 확인하는 함수
def check_target(line, conditions):
    if conditions['target_line_checkType'] == "and":
        return check_target_and(line, conditions)
    elif conditions['target_line_checkType'] == "or":
        return check_target_or(line, conditions)

# and
def check_target_and(line, conditions):
    if conditions['target_line_lowercaseAll']:
        target_line_lowercaseAll = [i.lower() for i in conditions['target_line']]
        for target in target_line_lowercaseAll:
            if target not in line.lower():
                return False
    else:
        for target in conditions['target_line']:
            if target not in line:
                return False
    return True

# or
def check_target_or(line, conditions):
    if conditions['target_line_lowercaseAll']:
        target_line_lowercaseAll = [i.lower() for i in conditions['target_line']]
        for target in target_line_lowercaseAll:
            if target in line.lower():
                return True
    else:
        for target in conditions['target_line']:
            if target in line:
                return True
    return False

# 제외되어야 하는 라인인지 확인하는 함수
def check_exclusions(line, conditions):
    if conditions['exclusions_lowercaseAll']:
        exclusions_lowercaseAll = [i.lower() for i in conditions['exclusions']]
        for exclusion in exclusions_lowercaseAll:
            if exclusion in line.lower():
                return False
    else:
        for exclusion in conditions['exclusions']:
            if exclusion in line:
                return False
    return True

# --- 라인 일부분 변수화 -------------------------------------------------------------------------------

def check_variable(conditions):
    if '[[var]]' in conditions['part_to_replace'][0]:
        return True
    return False

def replace_line_with_variable(conditions, line):
    #replace 부분과 index 변수화
    before_replace = conditions['part_to_replace'][0]
    after_replace = conditions['part_to_replace'][1]
    before_replace_str1 = before_replace[:before_replace.find("[[var]]")]
    before_replace_str2 = before_replace[before_replace.find("[[var]]") + len("[[var]]"):]
    after_replace_str1 = after_replace[:before_replace.find("[[var]]")]
    after_replace_str2 = after_replace[before_replace.find("[[var]]") + len("[[var]]"):]

    return replace_part(conditions, line, before_replace_str1, before_replace_str2, after_replace_str1, after_replace_str2)

# --- 한 줄에 변화 대상이 여러 개 있을 경우 ---
def replace_part(conditions, line, br_str1, br_str2, ar_str1, ar_str2):
    # variable과 변경 대상 변수화
    before_replace_index1 = line.find(br_str1)
    before_replace_index1_plusLen = before_replace_index1 + len(br_str1)
    before_replace_index2 = find_parenthesis(line, br_str1, br_str2, before_replace_index1_plusLen) # 괄호 세고 index 가져오기
    variable = line[before_replace_index1_plusLen:before_replace_index2]
    before_replace_original = line[before_replace_index1:before_replace_index2 + len(br_str2)]
    
    # 라인 replace 처리
    line = line.replace(before_replace_original, ar_str1 + variable + ar_str2)
    if conditions['replace_loopTF']:
        if br_str1 in line and br_str2 in line:
            return replace_part(line, br_str1, br_str2, ar_str1, ar_str2)
        else:
            return line
    else:
        return line
    
    def find_parenthesis(line, br_str1, br_str2, before_replace_index1_plusLen):
        if br_str1[-1:] == '(' and br_str2[-1:] == ')' and line.count('(') == line.count(')'):
            return parenthesis_count(line, before_replace_index1_plusLen, before_replace_index1_plusLen)
        else:
            return line.find(br_str2, before_replace_index1_plusLen + 1)
    
    def parenthesis_count(line, starting_index, end_index):
        parenthesis_close_index = line.find(')', end_index + 1)
        working_line = line[starting_index:parenthesis_close_index]
        if working_line.count('(') == working_line.count(')'):
            return parenthesis_close_index
        else:
            return parenthesis_count(line, starting_index, parenthesis_close_index)

# --- 출력용 -----------------------------------------------------------------------------------------

def print_count(conditions):
    if conditions['countTF']:
        conditions['count'] += 1
        print(f"({conditions['count']})", end="")
    return conditions

def write_count(conditions, fw):
    if conditions['countTF']:
        conditions['count'] += 1
        fw.write("(" + str(conditions['count']) + ")")
    return conditions

# --- 라인 처리용 -------------------------------------------------------------------------------------

# 라인 출력하는 함수
def print_lines(lines, file_path, conditions):

    # 파일 이름 출력하는 조건 설정
    pathNameTF = True

    # 찾는 라인을 출력하기
    for i, line in enumerate(lines):
        if check_target(line, conditions):
            if check_exclusions(line, conditions):

                # 파일 이름 출력
                if pathNameTF:
                    print(file_path)
                    pathNameTF = False

                # 카운트하기
                conditions = print_count(conditions)
                
                # 라인의 수와 라인 출력
                print(f"\t{i+1}\t{line.strip()}")
    return conditions['count']

# 라인 적는 함수
def write_lines(lines, file_path, conditions):

    # 파일 이름 출력하는 조건 설정
    pathNameTF = True

    fw = open(conditions["txt_path"], 'a', encoding='utf-8')
    # 찾는 라인을 출력하기
    for i, line in enumerate(lines):
        if check_target(line, conditions):
            if check_exclusions(line, conditions):

                # 파일 이름 적기
                if pathNameTF:
                    fw.write(file_path + "\n")
                    pathNameTF = False
                
                # 카운트하기
                conditions = write_count(conditions, fw)

                # 라인의 수와 라인 적기
                fw.write(" \t[" + str(i+1) + "]" + line.strip() + "\n")
    
    if pathNameTF == False:
        fw.write("\n")
    fw.close
    return conditions['count']

# 라인 적는 함수
def replace_lines(lines, file_path, conditions):

    pathNameTF = True

    fw = open(file_path, 'w', encoding='utf-8')
    # 찾는 라인을 출력하기
    for i, line in enumerate(lines):
        if check_target(line, conditions) and check_exclusions(line, conditions):

            # [[var]] 확인
            if check_variable(conditions):
                # variable 변수화
                line = replace_line_with_variable(conditions, line)
                fw.write(line)
            else:
                # replace 처리
                line = line.replace(conditions["part_to_replace"][0], conditions["part_to_replace"][1])
                fw.write(line)
            
            # 처리한 라인 print
            if pathNameTF:
                print(file_path)
                pathNameTF = False
            conditions = print_count(conditions)
            print(f"\t{i+1}\t{line.strip()}")

        else:
            fw.write(line)
    fw.close
    return conditions['count']

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
    if conditions["method"] == "print_lines":
        conditions['count'] = print_lines(lines, file_path, conditions)
    elif conditions["method"] == "write_lines":
        conditions['count'] = write_lines(lines, file_path, conditions)
    elif conditions["method"] == "replace_lines":
        conditions['count'] = replace_lines(lines, file_path, conditions)
    
    return conditions['count']

# 폴더이면 그 안의 내용물을 처리하는 함수
def process_dir(conditions):

    # 경로 변수
    path = conditions["path"]

    # 파일과 폴더의 목록을 가져오기
    item_list = os.listdir(path)

    # 하나씩 처리하기
    for item in item_list:

        # 폴더의 경로 + 파일 이름 = 파일의 경로
        current_path = path + '/' + item

        # 파일이면 처리
        if os.path.isfile(current_path):

            # 확장자 확인
            if current_path.endswith(conditions["extension"]):

                # 파일 처리
                conditions['count'] = process_file(current_path, conditions)
        
        # 폴더이면 재귀함수 실행
        elif os.path.isdir(current_path):
            conditions['path'] = current_path
            process_dir(current_path)

# 중간 작업
def mark_inbetween(conditions):
    if conditions["method"] == "print_lines" or conditions["method"] == "replace_lines":
        print("\n")
        print("###################################################")
        print("path : " + conditions["path"])
        print("target_line : [" + ", ".join(conditions["target_line"]) + "]")
        print("exclusions : [" + ", ".join(conditions["exclusions"]) + "]")
        if conditions["method"] == "replace_lines":
            print("part_to_replace : " + conditions["part_to_replace"][0] + " --> " + conditions["part_to_replace"][1])
        print("###################################################")
        print("\n")
    elif conditions["method"] == "write_lines":
        fw = open(conditions["txt_path"], 'a', encoding='utf-8')
        fw.write("\n")
        fw.write("###################################################\n")
        fw.write("path : " + conditions["path"] + "\n")
        fw.write("target_line : [" + ", ".join(conditions["target_line"]) + "]\n")
        fw.write("exclusions : [" + ", ".join(conditions["exclusions"]) + "]\n")
        fw.write("###################################################\n")
        fw.write("\n")
        fw.close

# 작업 실행
def init(conditions):
    for condition in conditions:
        mark_inbetween(condition)
        process_dir(condition)
