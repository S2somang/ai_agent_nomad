from crewai.tools import tool

@tool
def count_letters(sentence:str):
    # crew ai가 이 """을 통해 우리가 이전 섹션에서 만들었던 schema랑 같은걸 생성함
    """ 
    이 함수는 문장안에 있는 글자수를 세는 함수입니다. 
    input은 sentence 문자이며
    output은 숫자다.
    """ 
    print("tool calle with input: ", sentence)
    return len(sentence)