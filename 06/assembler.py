import sys
import os
import parser
import code
import symboltable
import logging

PREDEFINED_SYMBOLS = {'SP': 0,
                      'LCL': 1,
                      'ARG': 2,
                      'THIS': 3,
                      'THAT': 4,
                      'R0': 0,
                      'R1': 1,
                      'R2': 2,
                      'R3': 3,
                      'R4': 4,
                      'R5': 5,
                      'R6': 6,
                      'R7': 7,
                      'R8': 8,
                      'R9': 9,
                      'R10': 10,
                      'R11': 11,
                      'R12': 12,
                      'R13': 13,
                      'R14': 14,
                      'R15': 15,
                      'SCREEN': 16384,
                      'KBD': 24576}

def add_predefined_symbols(st):
     for symbol, address in PREDEFINED_SYMBOLS.items():
        st.add_entry(symbol, address)

def build_a_command(num_str):
    return "0{0:015b}".format(int(num_str))

def build_c_command(p):
    comp_mnemon = p.comp()
    comp_bin = code.comp(comp_mnemon)

    dest_mnemon = p.dest()
    dest_bin = code.dest(dest_mnemon)
   
    jump_mnemon = p.jump()
    jump_bin = code.jump(jump_mnemon)

    return "111{}{}{}".format(comp_bin, dest_bin, jump_bin)

def first_pass(asm_full_file_path, st):
    current_command_line_num = -1
    p = parser.Parser(asm_full_file_path)
    while p.has_more_commands():
        p.advance()
        if p.command_type() == parser.L_COMMAND:
            st.add_entry(p.symbol(), current_command_line_num + 1)
        else:
            current_command_line_num += 1

def get_symbol_num(st, symbol, var_alloc_num):
    logging.info("get_symbol_num: symbol: {}".format(symbol)) 
    if st.contains(symbol):
        address = st.get_address(symbol)
        logging.info("symbol table contains symbol: {}".format(address))
        return var_alloc_num, address 
    else:
        logging.info("symbol table does not contains symbol")  
        st.add_entry(symbol, var_alloc_num)
        return var_alloc_num + 1, var_alloc_num  

def build_a_command_with_symbol_support(st, p, var_alloc_num):
    symbol = p.symbol()
    logging.info("build_a_command_with_symbol_support: symbol: {}".format(symbol)) 
    if symbol.isdigit():
        logging.info("symbol is number") 
        command = build_a_command(symbol)
        return var_alloc_num, command
    else:
        logging.info("symbol is not number")
        var_alloc_num, symbol_num = get_symbol_num(st, symbol, var_alloc_num)
        command = build_a_command(symbol_num)
        return var_alloc_num, command

def second_pass(asm_full_file_path, st):
    logging.info("second_pass: symbol table{}".format(st.table))
    var_alloc_num = 16
    path, in_filename_w_ext = os.path.split(asm_full_file_path)
    filename, file_extension = os.path.splitext(in_filename_w_ext)

    out_filename_w_ext = filename + ".hack"
    out_file_path = os.path.join(path, out_filename_w_ext)
    logging.info("hack file: {}".format(out_file_path))
    out_file = open(out_file_path, 'w')

    p = parser.Parser(asm_full_file_path)
    command = ""
    while p.has_more_commands():
        p.advance()
        if p.command_type() == parser.L_COMMAND:
            continue
        elif p.command_type() == parser.A_COMMAND:
            logging.info("A command...")
            var_alloc_num, command = build_a_command_with_symbol_support(st, p, var_alloc_num)
            logging.info("var_alloc_num: {}".format(var_alloc_num))
        else:
            command = build_c_command(p)

        logging.info("command {}".format(command))
        out_file.write(command + '\n')

    out_file.close()

logging.getLogger().setLevel(logging.ERROR)
asm_full_file_path = sys.argv[1]

st = symboltable.SymbolTable()
add_predefined_symbols(st)
logging.info("symboltable: {}".format(st.table))

first_pass(asm_full_file_path, st)
second_pass(asm_full_file_path, st)



