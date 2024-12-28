input = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


def execute(initial_register_values, program):
    ip = 0
    buffer = []

    program = program.split(",")
    register = initial_register_values.copy()

    def combo(operand):
        if operand == 4:
            return register["A"]

        if operand == 5:
            return register["B"]

        if operand == 6:
            return register["C"]

        return operand

    while ip < len(program):
        opcode = int(program[ip])
        operand = int(program[ip + 1])

        match opcode:
            case 0:  # adv
                register["A"] = register["A"] // pow(2, combo(operand))
            case 1:  # bxl
                # bitwise exclusive or (either, but not both)
                register["B"] = register["B"] ^ operand
            case 2:  # bst
                register["B"] = combo(operand) % 8
            case 3:  # jmp
                if register["A"] > 0:
                    ip = operand - 2
            case 4:  # bxc
                register["B"] = register["B"] ^ register["C"]
            case 5:  # out
                buffer.append(str(combo(operand) % 8))
            case 6:  # bdv
                register["B"] = register["A"] // pow(2, combo(operand))
            case 7:  # cdv
                register["C"] = register["A"] // pow(2, combo(operand))

        ip += 2

    return ",".join(buffer)


registers = {"A": 0, "B": 0, "C": 0}

for line in input.strip().split("\n"):
    if "Register" in line:
        register, value = line.split(": ")
        registers[register.split()[1]] = int(value)
    elif "Program" in line:
        program = line.split(": ")[1]

print("Program output", execute(registers, program))

# EXAMPLE INSTRUCTIONS
# execute({"A": 0, "B": 0, "C": 9}, "2,6")
# execute({"A": 10, "B": 0, "C": 0}, "5,0,5,1,5,4")
# execute({"A": 2024, "B": 0, "C": 0}, "0,1,5,4,3,0")
# execute({"A": 0, "B": 29, "C": 0}, "1,7")
# execute({"A": 0, "B": 2024, "C": 43690}, "4,0")
