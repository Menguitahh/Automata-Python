import re


def solve(expression: str) -> int:
    numbers = list(map(int, re.findall(r'\d+', expression)))
    operators = re.findall(r'[+*]', expression)
    
    
    i = 0
    while i < len(operators):
        if operators[i] == '*':
            numbers[i] *= numbers[i + 1]
            del numbers[i + 1]
            del operators[i]
        else:
            i += 1
    
    
    result = numbers[0]
    for i in range(len(operators)):
        result += numbers[i + 1]
    
    return result


print(solve("2 + 7 * 2 + 1"))   
print(solve("2 * 2 * 2 + 32 * 2"))  
print(solve("2 * 2 + 2"))  
