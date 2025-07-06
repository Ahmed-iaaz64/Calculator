import sys

# Function to determine if an operator is left associative
def is_left_associative(operator):
    left_associative_operators = ['+', '-', '*', '/']
    if operator in left_associative_operators:
        return True
    # '^' (exponent) is right associative
    else:
        return False

# Function that returns the precedence of an operator
# Higher precedence operators will come first in the stack
def precedence(operator):
    if operator == '+' or operator == '-':
        return 1
    elif operator == '*' or operator == '/':
        return 2
    elif operator == '^':
        return 3

def shunting_yard_algorithm(tokenStr):
    operators = ['+', '-', '*', '/', '^']
    operator_stack = []

    output_queue = []

    tokens = []
    for i in range(len(tokenStr)):
        tokens.append(tokenStr[i])

    for i in range(len(tokens)):
        # is number
        if tokens[i].isnumeric() or is_float(tokens[i]):
            output_queue.append(tokens[i])

        # is operator
        if tokens[i] in operators:
            while operator_stack != [] and operator_stack[-1] != '(' and (precedence(operator_stack[-1]) > precedence(tokens[i]) or (precedence(tokens[i]) == precedence(operator_stack[-1]) and is_left_associative(tokens[i]))):
                output_queue.append(operator_stack.pop())
            operator_stack.append(tokens[i])

        # is left bracket
        if tokens[i] == '(':
            operator_stack.append(tokens[i])

        # is right bracket
        if tokens[i] == ')':
            while operator_stack != [] and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop())
            assert operator_stack[-1] == '('
            operator_stack.pop()

        # is comma
        if tokens[i] == ',':
            while operator_stack != [] and operator_stack[-1] != '(':
                output_queue.append(operator_stack.pop()) 
    
    # append remaining operators to output queue
    while operator_stack != []:
        output_queue.append(operator_stack.pop())

    return(output_queue)

def calculate(output_queue):
    stack = []
    for i in range(len(output_queue)):
        if output_queue[i].isnumeric() or is_float(output_queue[i]):
            stack.append(float(output_queue[i]))
        else:
            operand2 = stack.pop()
            operand1 = stack.pop()
            operator = output_queue[i]
            if operator == '+':
                stack.append(operand1 + operand2)
            elif operator == '-':
                stack.append(operand1 - operand2)
            elif operator == '*':
                stack.append(operand1 * operand2)
            elif operator == '/':
                if operand2 == 0:
                    raise ZeroDivisionError("division by zero")
                stack.append(operand1 / operand2)
            elif operator == '^':
                stack.append(operand1 ** operand2)

    return(stack[-1])


# check is string contains float
def is_float(str):
    try:
        float(str)
        return True
    except ValueError or TypeError:
        return False
    
def parse_equation(equation):
    operators = ['+', '-', '*', '/', '^']
    equation = equation + '/'
    equation = equation.replace(' ', '')
    stack = []
    rolling = 0
    last = 'num'
    for i in range(len(equation)):
        print(rolling)
        print(stack)

        if last == 'num' and (equation[i].isnumeric() or is_float(equation[i])):
            rolling += 1
        elif last == 'num' and equation[i] in operators:
            substr = equation[i-rolling:i]
            stack.append(substr)
            stack.append(equation[i])
            last = 'operator'
            rolling = 0
        elif last == 'operator' and (equation[i].isnumeric() or is_float(equation[i])):
            rolling += 1
            last = 'num'

        elif last == 'operator' and equation[i] == '(':
            stack.append(equation[i])
        elif last == 'num' and equation[i] == '(':
            stack.append('*')
            stack.append(equation[i])
            last = 'operator'
            rolling = 0

        elif last == 'num' and equation[i] == ')':
            substr = equation[i-rolling:i]
            stack.append(substr)
            stack.append(equation[i])
            last = 'operator'
            rolling = 0
        elif last == 'operator' and equation[i] == ')' and equation[i-1] != ')':
            return 1
        
        elif equation[i] == '/':
            substr = equation[i-rolling:i-1]
            stack.append(substr)

        elif last == 'operator' and equation[i] in operators and equation[i-1] != '(' and equation[i-1] != ')':
            return 1
        elif last == 'operator' and equation[i] in operators and equation[i-1] == ')':
            stack.append(equation[i])
    
    stack.pop()
    return stack


def calculator(equation):
    try:
        equation = equation[0]
        equation = parse_equation(equation)
        output_queue = shunting_yard_algorithm(equation)
        output = calculate(output_queue)
        return output

    except IndexError:
        print("""
            
            No arguments provided
            To run type python main.py '1 + 1' or any other problem

            '1 + 1' must be typed inside quotation marks
            NOTE: There must be a space between any characters
                eg: '3 + 4 * 2 / ( 1 - 5 ) ^ 2 ^ 3'
            
            """)