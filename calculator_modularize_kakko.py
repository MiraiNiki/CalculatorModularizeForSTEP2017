def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1

def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readMultiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def readDivide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

def readLeftParentheses(line, index, depth):
    token = {'type': 'LeftParentheses', 'depth': depth}
    return token, index + 1

def readRightParentheses(line, index, depth):
    token = {'type': 'RightParentheses', 'depth': depth}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    depth = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
        elif line[index] == '(':
            depth += 1
            (token, index) = readLeftParentheses(line, index, depth)
        elif line[index] == ')':
            (token, index) = readRightParentheses(line, index, depth)
            depth -= 1
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens

def executeFourOperations(tokens, depth):
    depthCnt = depth
    while depthCnt >= 0:
        index = 1
        d = 0
        while index < len(tokens):
            if tokens[index]['type'] == 'LeftParentheses':
                d = tokens[index]['depth']
                tokens = insertDummy(tokens, index + 1)
            elif tokens[index]['type'] == 'RightParentheses':
                d = tokens[index]['depth'] - 1
            elif depthCnt == d:
                if tokens[index]['type'] == 'NUMBER':
                    if tokens[index - 1]['type'] == 'MULTIPLY':
                        tokens[index - 2]['number'] *=  tokens[index]['number']
                        del tokens[index - 1:index + 1]
                        index = index - 2
                    elif tokens[index - 1]['type'] == 'DIVIDE':
                        tokens[index - 2]['number'] /=  tokens[index]['number']
                        del tokens[index - 1:index + 1]
                        index = index - 2 
            index += 1 
        index = 1
        d = 0
        while index < len(tokens):
            if tokens[index]['type'] == 'LeftParentheses':
                d = tokens[index]['depth']
                if depthCnt == d:
                    del tokens[index]
                    index -= 1
            elif tokens[index]['type'] == 'RightParentheses':
                if depthCnt == d:
                    del tokens[index]
                    index -= 1
                d -= 1
            elif depthCnt == d:
                if tokens[index]['type'] == 'NUMBER':
                    if tokens[index - 1]['type'] == 'PLUS':
                        tokens[index - 2]['number'] += tokens[index]['number']
                        del tokens[index - 1:index + 1]
                        index = index - 2
                    elif tokens[index - 1]['type'] == 'MINUS':
                        tokens[index - 2]['number'] -= tokens[index]['number']
                        del tokens[index - 1:index + 1]
                        index = index - 2
            index += 1
        depthCnt -= 1
    print tokens
    return tokens

def estimateDepth(tokens):
    depth = 0
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'LeftParentheses':
            if tokens[index]['depth'] > depth:
                depth = tokens[index]['depth']
        index += 1
    return depth

def insertDummy(tokens, index):
    tokens.insert(index, {'type': 'PLUS'}) # Insert a dummy '+' token
    tokens.insert(index, {'type': 'NUMBER', 'number': 0}) # Insert a dummy
    return tokens

def evaluate(tokens):
    answer = 0
    tokens = insertDummy(tokens,0)
    depth = estimateDepth(tokens)
    tokens = executeFourOperations(tokens, depth)
    answer = tokens[0]['number']
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("2+3*4", 14)
    test("2+3*4/2", 8)
    test("21+3*4/2-300+200*2", 127)
    test("2*(1+3)", 8)
    test("(1+4)*3", 15)
    test("2*(1+3*(2+4))", 38)
    test("2*(1+3*(2+4*3))", 2*(1+3*(2+4*3)))
    test("(3*2*(4+2*(1+3)))+2*(1+3*(2+4*3))", (3*2*(4+2*(1+3)))+2*(1+3*(2+4*3)))
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print "answer = %f\n" % answer
