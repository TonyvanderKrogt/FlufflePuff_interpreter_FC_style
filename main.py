import re
from typing import List, Callable
import sys
from time import sleep


class Commands:
    def __init__(self, tokens: str):
        self.tokens = tokenize(tokens)

    def __str__(self):
        return 'The tokens are: {self.tokens}'.format(self=self)

    def __repr__(self):
        return str(self)


class Iterator:
    def __init__(self, it: int, it_name: str):
        self.it = it
        self.it_name = it_name

    def __str__(self):
        return '{self.it_name} is at {self.it}'.format(self=self)

    def __repr__(self):
        return str(self)


class Memory(Iterator):
    def __init__(self, data: List[int], it: int, it_name: str):
        Iterator.__init__(self, it, it_name)
        self.data = data
        self.output = ""

    def __str__(self):
        if self.output == "":
            self.output = "None"
        return 'The data is: {self.data}\nAnd the current output is: {self.output}'.format(self=self)

    def __repr__(self):
        return str(self)


class GUI(Memory):
    def __init__(self, data: list, it: int, it_name: str):
        Memory.__init__(self, data, it, it_name)
        self.arrow_space_skip = ""

    def __str__(self):
        sleep(1)
        return '{self.data}\n{self.arrow_space_skip}^\n{self.arrow_space_skip}|\n\n\n\n'.format(self=self)

    def __repr__(self):
        return str(self)


# space_skipper:: Str -> Int -> Int -> Str
def space_skipper(data: str, spaces_skipped: int, point_place: int) -> str:
    if data[1] == ',':
        point_place -= 1
        spaces_skipped += 1
        return space_skipper(data[1:], spaces_skipped, point_place)
    if data[1] == ' ':
        spaces_skipped += 1
        return space_skipper(data[1:], spaces_skipped, point_place)
    if point_place == 0:
        return " " * (spaces_skipped + 1)
    spaces_skipped += 1
    return space_skipper(data[1:], spaces_skipped, point_place)


# print_gui :: str -> GUI -> None
def print_gui(mem: GUI) -> None:
    mem.arrow_space_skip = space_skipper(str(mem.data), 0, mem.it)
    print(mem)


# tokenize :: str -> [str]
def tokenize(source: str) -> List[str]:
    tokens = []
    def loop(source: str, tokens: List[str]) -> List[str]:
        temp = tokens.copy()
        if bool(re.match(r"pf", source)):
            temp.append('PLUS_ONE')
            return loop(source[2:], temp)
        elif bool(re.match(r"bl", source)):
            temp.append('MINUS_ONE')
            return loop(source[2:], temp)
        elif bool(re.match(r"b", source)):
            temp.append('MOV_RIGHT')
            return loop(source[1:], temp)
        elif bool(re.match(r"t", source)):
            temp.append('MOV_LEFT')
            return loop(source[1:], temp)
        elif bool(re.match(r"!", source)):
            temp.append('OUTPUT')
            return loop(source[1:], temp)
        elif bool(re.match(r"\?", source)):
            temp.append('INPUT')
            return loop(source[1:], temp)
        elif bool(re.match(r"\*gasp\*", source)):
            temp.append('OPEN_LOOP')
            return loop(source[6:], temp)
        elif bool(re.match(r"\*pomf\*", source)):
            temp.append('CLOSE_LOOP')
            return loop(source[6:], temp)
        elif len(source) == 0:
            return temp
        return loop(source[1:], temp)

    return loop(source, tokens)


# command :: Str -> Callable
def command(token: str) -> Callable:
    if token == "PLUS_ONE":
        return plus_one
    if token == "MINUS_ONE":
        return minus_one
    if token == "MOV_RIGHT":
        return move_right
    if token == "MOV_LEFT":
        return move_left
    if token == "OUTPUT":
        return output_mem
    if token == "INPUT":
        return input_mem
    if token == "OPEN_LOOP":
        return open_loop
    if token == "CLOSE_LOOP":
        return close_loop


# command_counter :: callable -> callable
def command_counter(func: Callable) -> Callable:
    #counter :: [Callable] -> Object -> Int -> Iterator -> None
    def counter(functions: [Callable], mem: object, numb_of_l: int, it_func: Iterator) -> None:
        func(functions, mem, numb_of_l, it_func)
        counter.count += 1
    counter.count = 0
    return counter


def error_it_mem() -> None:
    print("Memory Iterator is out of bounds")

def error_loop() -> None:
    print("Not enough loop endings or openings")

# map :: (Str -> Int -> Object -> Iterator -> Callable) -> Commands
def map(function: Callable[[str], Callable], tokens: List[str]) -> List[Callable]:
    if len(tokens) == 0:
        return []
    head, *tail = tokens
    return [function(head)] + map(function, tail)

# check_tokens :: [Str] -> Int -> Int -> Int -> Callable
def check_tokens(tokens: List[str], numb_of_l: int, it_mem: int, mem_size: int) -> Callable:
    if len(tokens) == 0:
        if it_mem < 0 or it_mem > mem_size:
            return error_it_mem
        if numb_of_l != 0:
            return error_loop
        return map
    if tokens[0] == "OPEN_LOOP":
        numb_of_l += 1
        return check_tokens(tokens[1:], numb_of_l, it_mem, mem_size)
    elif tokens[0] == "CLOSE_LOOP":
        numb_of_l -= 1
        return check_tokens(tokens[1:], numb_of_l, it_mem, mem_size)
    elif tokens[0] == "MOV_LEFT":
        it_mem -= 1
        return check_tokens(tokens[1:], numb_of_l, it_mem, mem_size)
    elif tokens[0] == "MOV_RIGHT":
        it_mem += 1
    return check_tokens(tokens[1:], numb_of_l, it_mem, mem_size)

# plus_one :: Object -> None
def plus_one(mem: object) -> None:
    mem.data[mem.it] += 1

# minus_one :: Object -> None
def minus_one(mem: object) -> None:
    mem.data[mem.it] -= 1

# move_right :: Object -> None
def move_right(mem: object) -> None:
    mem.it += 1

# move_left :: Object -> None
def move_left(mem: object) -> None:
    mem.it -= 1

# input_mem :: Object -> None
def input_mem(mem: object) -> None:
    user_input = input('')
    mem.data[mem.it] = ord(user_input)

# output_mem :: Object -> None
def output_mem(mem: object) -> None:
    mem.output += (chr(mem.data[mem.it]))

# open_loop :: Object -> Int -> [Callable], Iterator -> None
def open_loop(mem: object, numb_of_l: int, functions: [Callable], it_func: Iterator) -> None:
    if mem.data[mem.it] == 0:
        it_func.it += 1
        # loop :: Int -> [Callable] -> Iterator -> None
        def loop(numb_of_l: int, functions: [Callable], it_func: Iterator) -> None:
            if numb_of_l > 0 or functions[it_func.it] != close_loop:
                if functions[it_func.it] == close_loop:
                    numb_of_l -= 1
                if functions[it_func.it] == open_loop:
                    numb_of_l += 1
                it_func.it += 1
                return loop(numb_of_l, functions, it_func)
        loop(numb_of_l, functions, it_func)
    it_func.it += 1

# close_loop :: Object -> Int -> [Callable], Iterator -> None
def close_loop(mem: object, numb_of_l: int, functions: [Callable], it_func: Iterator) -> None:
    if mem.data[mem.it] != 0:
        it_func.it -= 1
        # loop :: Int -> [Callable] -> Iterator -> None
        def loop(numb_of_l: int, functions: [Callable], it_func: Iterator):
            if numb_of_l > 0 or functions[it_func.it] != open_loop:
                if functions[it_func.it] == close_loop:
                    numb_of_l += 1
                if functions[it_func.it] == open_loop:
                    numb_of_l -= 1
                it_func.it -= 1
                return loop(numb_of_l, functions, it_func)
        loop(numb_of_l, functions, it_func)
    it_func.it += 1

# function_cellar :: [Callable] -> Object -> int -> Iterator -> None
def function_caller(functions: [Callable], mem: object, numb_of_l: int, it_func: Iterator) -> None:
    if len(functions) == it_func.it:
        if isinstance(mem, GUI):
            print_gui(mem)
        sleep(1)
        if mem.output != "":
            print("The output is: ", mem.output)
        else:
            print("There is no output")
        sleep(1)
        return None
    if isinstance(mem, GUI):
        print_gui(mem)
    if functions[it_func.it] == open_loop or functions[it_func.it] == close_loop:
        functions[it_func.it](mem, numb_of_l, functions, it_func)
        return function_caller(functions, mem, numb_of_l, it_func)
    functions[it_func.it](mem)
    it_func.it += 1
    return function_caller(functions, mem, numb_of_l, it_func)

if __name__ == "__main__":
    src = "pfpfpfpfpfpfpfpfpfpf*gasp*bpfpfpfpfpfpfpfbpfpfpfpfpfpfpfpfpfpfbpfpfpfbpfttttbl*pomf*bpfpf!bpf!pfpfpfpfpfpfpf!!pfpfpf!bpfpf!ttpfpfpfpfpfpfpfpfpfpfpfpfpfpfpf!b!pfpfpf!blblblblblbl!blblblblblblblbl!bpf!b!"
    # src = "pfpfbpfpf*gasp*"
    sys.setrecursionlimit(10**8)
    data = [0] * 100
    mem = GUI(data, 0, "It_memory")
    tokens = Commands(src)
    which_func = check_tokens(tokens.tokens, 0, 0, len(tokens.tokens))
    if which_func == map:
        map_commands = map(command, tokens.tokens)
        function_caller = command_counter(function_caller)
        function_caller(map_commands, mem, 0, Iterator(0, "It_func"))
    else:
        which_func()



