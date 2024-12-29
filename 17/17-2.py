input = """
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

input = """
Register A: 63281501
Register B: 0
Register C: 0

Program: 2,4,1,5,7,5,4,5,0,3,1,6,5,5,3,0"""


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

    print("output: ", ",".join(buffer))
    return ",".join(buffer)


register = {"A": 0, "B": 0, "C": 0}

for line in input.strip().split("\n"):
    if "Register" in line:
        reg, value = line.split(": ")
        register[reg.split()[1]] = int(value)
    elif "Program" in line:
        program = line.split(": ")[1]


program_array = program.split(",")

A = 0

for i in reversed(range(len(program_array))):

    # I read the following hint online, which means you can search A from the right-most bits (least sig)
    # and using these to match the output. This means you can match A, one output at a time
    # left shifting by 3 bits (by multiplying by 8, or 2^3) to work on the next digit
    #
    # (https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m3hmq2y)
    # > if you can get 3 bits in A that gives a valid out value, it will
    # >  always output the same 3 bit value if lshifted by 3

    print(f"left shifting A by 3 digits (*{pow(2, 3)}) {A} -> {A << 3}")
    A = A * 8
    register["A"] = A
    print(
        f"looking at the {len(program_array)-i} right-most digits , starting A={A} -- looking for right side matching {','.join(program.split(',')[i:])}"
    )
    while execute(register, program).split(",") != program.split(",")[i:]:
        A += 1
        register["A"] = A
    print("matched ", A, "---", ",".join(program.split(",")[i:]))
