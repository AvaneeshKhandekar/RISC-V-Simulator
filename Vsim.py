# On my honor, I have neither given nor received any unauthorized aid on this assignment.
import sys

category_1 = {'00000': 'beq',
              '00001': 'bne',
              '00010': 'blt',
              '00011': 'sw'}

category_2 = {'00000': 'add',
              '00001': 'sub',
              '00010': 'and',
              '00011': 'or'}

category_3 = {'00000': 'addi',
              '00001': 'andi',
              '00010': 'ori',
              '00011': 'sll',
              '00100': 'sra',
              '00101': 'lw'}

category_4 = {'00000': 'jal',
              '11111': 'break'}

instructions = {}
values = {}

normal = ['add']
imm = ['addi', 'ori', 'andi', 'sll', 'sra']
cat_1_s = ['sw']

flag = False
count = 252
last_address = -1
first_imm_address = -1
cycle_count = 0
curr = 256
registers_x = [0] * 32

def print_registers(output_file, all_registers):
    output_file.write('Registers\n')
    output_file.write('x00:')
    for i in range(0, 8):
        output_file.write('\t' + str(all_registers[i]))
    output_file.write('\nx08:')
    for i in range(8, 16):
        output_file.write('\t' + str(all_registers[i]))
    output_file.write('\nx16:')
    for i in range(16, 24):
        output_file.write('\t' + str(all_registers[i]))
    output_file.write('\nx24:')
    for i in range(24, 32):
        output_file.write('\t' + str(all_registers[i]))

def print_data(output_file, first_immediate_address, data_values, last_cycle):
    if not last_cycle:
        output_file.write('\nData\n')
        split_values = [list(data_values.values())[i:i + 8] for i in range(0, len(list(data_values.values())), 8)]
        for i in split_values:
            if len(i) == 8:
                output_file.write(str(first_immediate_address) + ':\t' + '\t'.join(str(x) for x in i) + '\n')
                first_immediate_address += 32
            else:
                output_file.write(str(first_immediate_address) + ':\t' + '\t'.join(str(x) for x in i) + '\n')
    else:
        output_file.write('\nData\n')
        split_values = [list(values.values())[i:i + 8] for i in range(0, len(list(values.values())), 8)]
        for i in split_values:
            if len(i) == 8:
                output_file.write(str(first_immediate_address) + ':\t' + '\t'.join(str(x) for x in i) + '\n')
                first_immediate_address += 32
            else:
                output_file.write(str(first_immediate_address) + ':\t' + '\t'.join(str(x) for x in i))

with open(sys.argv[1], 'r') as file:
    with open('disassembly.txt', 'w+') as out_file:
        for line in file.readlines():
            count += 4
            line = line.rstrip()
            if not flag:
                code = line[-2:]
                opcode = line[-7:-2]
                if code == '11':
                    opcode = category_4[opcode]
                    if opcode == 'break':
                        flag = True
                        instr = str(count) + '\t' + opcode
                        out_file.write(line + '\t' + instr + '\n')
                        instructions[count] = opcode, instr
                        last_address = count
                        first_imm_address = count + 4
                    else:
                        immediate = line[0:20]
                        if immediate.startswith('1'):
                            rs_1 = int(immediate, 2) - (1 << len(immediate))
                        else:
                            rs_1 = int(immediate, 2)
                        rd = int(line[20:25],2)
                        instr = str(count) + '\t' + opcode + ' x' + str(rd) + ', #' + str(rs_1)
                        out_file.write(line + '\t' + instr + '\n')
                        instructions[count] = opcode, instr, [rd, int(rs_1)]

                elif code == '00':
                    opcode = category_1[opcode]
                    rd = int(line[12:17],2)
                    rs_1 = int(line[7:12],2)
                    immediate = str(line[0:7]) + str(line[20:25])

                    if immediate.startswith('1'):
                        rs_2 = int(immediate, 2) - (1 << len(immediate))
                    else:
                        rs_2 = int(immediate, 2)
                    if opcode in cat_1_s:
                        instr = str(count) + '\t' + opcode + ' x' + str(rd) + ', ' + str(rs_2) + '(x' + str(rs_1) + ')'
                        out_file.write(line + '\t' + instr + '\n')
                        instructions[count] = opcode, instr, [rd, int(rs_2), rs_1]
                    else:
                        instr = str(count) + '\t' + opcode + ' x' + str(rd) + ', x' + str(rs_1) + ', #' + str(rs_2)
                        out_file.write(line + '\t' + instr + '\n')
                        instructions[count] = opcode, instr, [rd, rs_1, int(rs_2)]

                elif code == '01':
                    opcode = category_2[opcode]
                    rd = int(line[-12:-7],2)
                    rs_1 = int(line[-20:-15],2)
                    rs_2 = int(line[-25:-20],2)
                    instr = str(count) + '\t' + opcode + ' x' + str(rd) + ', x' + str(rs_1) + ', x' + str(rs_2)
                    out_file.write(line + '\t' + instr + '\n')
                    instructions[count] = opcode, instr, [rd, rs_1, rs_2]

                elif code == '10':
                    opcode = category_3[opcode]
                    rd = int(line[-12:-7],2)
                    rs_1 = int(line[-20:-15],2)
                    immediate = line[0:12]

                    if immediate.startswith('1'):
                        rs_2 = int(immediate, 2) - (1 << len(immediate))
                    else:
                        rs_2 = int(immediate, 2)

                    if opcode in imm:
                        instr = str(count) + '\t' + opcode + ' x' + str(rd) + ', x' + str(rs_1) + ', ' + '#' + str(rs_2)
                        out_file.write(line + '\t' + instr + '\n')
                        instructions[count] = opcode, instr, [rd, rs_1,int(rs_2)]
                    else:
                        instr = str(count) + '\t' + opcode + ' x' + str(rd) + ', ' + str(rs_2) + '(x' + str(rs_1) + ')'
                        out_file.write(line + '\t' + instr + '\n')
                        instructions[count] = opcode, instr, [rd, int(rs_2), rs_1]
            else:
                if line.startswith('1'):
                    imm = int(line, 2) - (1 << len(line))
                    out_file.write(line + '\t' + str(count) + '\t' + str(imm) + '\n')
                    values[count] = imm
                else:
                    imm = int(line, 2)
                    out_file.write(line + '\t' + str(count) + '\t' + str(imm) + '\n')
                    values[count] = imm
    out_file.close()

with open('simulation.txt', 'w+') as out_file:
    while curr < last_address:
        cycle_count += 1
        instruction = instructions[curr]
        opcode = instruction[0]
        write_str = instruction[1]
        registers = instruction[2]
        if opcode == "add":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] + registers_x[registers[2]]
        elif opcode == "sub":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] - registers_x[registers[2]]
        elif opcode == "and":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] & registers_x[registers[2]]
        elif opcode == "or":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] | registers_x[registers[2]]
        elif opcode == "addi":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] + registers[2]
        elif opcode == "andi":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] & registers[2]
        elif opcode == "ori":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] | registers[2]
        elif opcode == "beq":
            if registers_x[registers[0]] == registers_x[registers[1]]:
                curr += 2 * registers[2]
            else:
                curr += 4
        elif opcode == "bne":
            if registers_x[registers[0]] != registers_x[registers[1]]:
                curr += 2 * registers[2]
            else:
                curr += 4
        elif opcode == "blt":
            if registers_x[registers[0]] < registers_x[registers[1]]:
                curr += 2 * registers[2]
            else:
                curr += 4
        elif opcode == "sll":
            curr += 4
            val = (registers_x[registers[1]] if registers_x[registers[1]] >= 0 else -registers_x[registers[1]])
            registers_x[registers[0]] = val << registers[2]
        elif opcode == "sra":
            curr += 4
            registers_x[registers[0]] = registers_x[registers[1]] >> registers[2]
        elif opcode == "lw":
            curr += 4
            registers_x[registers[0]] = values[registers[1] + registers_x[registers[2]]]
        elif opcode == "jal":
            registers_x[registers[0]] = curr + 4
            curr += 2 * registers[1]
        elif opcode == "sw":
            curr += 4
            values[registers[1] + registers_x[registers[2]]] = registers_x[registers[0]]
        out_file.write('-' * 20 + '\n' + 'Cycle ' + str(cycle_count) + ':\t' + write_str + '\n')
        print_registers(out_file, registers_x)
        print_data(out_file, first_imm_address, values, False)
        if curr == last_address:
            instruction = instructions[last_address]
            opcode = instruction[0]
            write_str = instruction[1]
            cycle_count += 1
            out_file.write('-' * 20 + '\n' + 'Cycle ' + str(cycle_count) + ':\t' + write_str + '\n')
            print_registers(out_file, registers_x)
            print_data(out_file, first_imm_address, values, True)
            curr = last_address
            break