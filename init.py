from ReplaceCode_CmFunctions import CmFunctions

# --- 경로 설정 -----------------------------------------------------------------------------------------

# 폴더 경로
path = ""

# txt path
txt_path = ""

# --- 작업 조건 설정 -------------------------------------------------------------------------------------

# 찾고 싶은 라인
target_line = []

# 제외해야 할 조건
exclusions = []

# 처리할 파일의 확장자
extension = ""

# 라인 카운트
countTF = True

# 처리 방식
method = "print_lines"

# method :
  # print_lines
  # write_lines
  # replace_lines

# 변환해야 할 부분
part_to_replace = ["", ""]

conditions = {
    "path":path
  , "target_line":target_line
  , "exclusions":exclusions
  , "extension":extension
  , "countTF":countTF
  , "method":method
  , "txt_path":txt_path
  , "part_to_replace":part_to_replace
}

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////// 실제 처리 내용 /////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# 파일 처리 실행
init(conditions)