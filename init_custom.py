from CmFunctions import *

# 조건들
path = ""
txt_path = ""
extension = ""

conditions = [
  {
      "path":                       path
    , "txt_path":                   txt_path
    , "target_line":                []
    , "target_line_lowercaseAll":   False
    , "target_line_checkType":      "and"
    , "exclusions":                 []
    , "exclusions_lowercaseAll":    False
    , "extension":                  extension
    , "countTF":                    True
    , "count":                      0
    , "method":                     ""
    , "part_to_replace":            []
  }
]

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //////////// 실제 처리 내용 /////////////////////////////////////////////////////////////////////////////////////////////
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

# 파일 처리 실행
init(conditions)