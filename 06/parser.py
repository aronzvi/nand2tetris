A_COMMAND = 1
C_COMMAND = 2
L_COMMAND = 3

class Parser:
    def __init__(self, asm_file):
        self.file = open(asm_file, "r") 
        self.commands = []
        self.current_command_index = -1
        
        for line in self.file:
            if self.line_is_a_command(line):
                self.add_command(line)
                
    def remove_inline_comment(self, line):
        return line.split("//")[0]

    def extract_command_from_line(self, line):
        line = self.remove_inline_comment(line)
        return line.strip()

    def add_command(self, line):
        command = self.extract_command_from_line(line)
        self.commands.append(command)
        
    def line_is_not_comment(self, line):
        return not line.startswith("/")

    def line_is_not_whitespace(self, line):
        return not line.isspace()

    def line_is_a_command(self, line):
        return self.line_is_not_comment(line) and self.line_is_not_whitespace(line)

    def advance(self):
        self.current_command_index += 1

    def has_more_commands(self):
        return len(self.commands) > 0 and self.current_command_index < (len(self.commands) - 1)

    def current_command(self):
        return self.commands[self.current_command_index]
   
    def is_a_command(self):
        return self.current_command().startswith("@")

    def is_l_command(self):
        return self.current_command().startswith("(")

    def command_type(self):
        if self.is_a_command():
            return A_COMMAND
        elif self.is_l_command():
            return L_COMMAND
        else:
            return C_COMMAND

    def symbol(self):
        if self.is_a_command():
            return self.a_command_symbol()
        else:
            return self.l_command_symbol()

    def a_command_symbol(self):
        return self.current_command()[1:]

    def l_command_symbol(self):    
        return self.current_command()[1:-1]
    
    def dest(self):
        if "=" not in self.current_command():
            return "null"
        else:
            return self.current_command().split("=")[0]

    def command_discard_dest(self, command):
        if "=" in command:
            return  command.split("=")[1]
        else:
            return command

    def command_discard_jump(self, command):
        if ";" in command:
            return command.split(";")[0]
        else:
            return command

    def comp(self):
        command_no_dest = self.command_discard_dest(self.current_command())
        comp_no_dest_and_no_jump = self.command_discard_jump(command_no_dest) 
        return comp_no_dest_and_no_jump

    def jump(self):
        if ";" not in self.current_command():
            return "null"
        else:
            return self.current_command().split(";")[1]