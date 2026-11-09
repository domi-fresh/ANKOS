import argparse


SYMBOL_0 = " "
SYMBOL_1 = "#"

def bitParser(number):
    if number > 255 or number < 0:
        print("Please specify a number between 0 and 255!\n")
        return []

    bits = []

    while number != 0:
        # print(f"number during while: {number}")

        if number % 2 == 0:
            bits.append(SYMBOL_0)
        else:
            bits.append(SYMBOL_1)
            number = number - 1
        number = number / 2

    while list.__len__(bits) < 8:
        bits.append(SYMBOL_0)

    bits.reverse()

    return bits


def setup_automaton(number: int = 30, width: int = 80, height: int = 160):

    bits = bitParser(number)

    rules = {SYMBOL_0+SYMBOL_0+SYMBOL_0: bits[7],
             SYMBOL_0+SYMBOL_0+SYMBOL_1: bits[6],
             SYMBOL_0+SYMBOL_1+SYMBOL_0: bits[5],
             SYMBOL_0+SYMBOL_1+SYMBOL_1: bits[4],
             SYMBOL_1+SYMBOL_0+SYMBOL_0: bits[3],
             SYMBOL_1+SYMBOL_0+SYMBOL_1: bits[2],
             SYMBOL_1+SYMBOL_1+SYMBOL_0: bits[1],
             SYMBOL_1+SYMBOL_1+SYMBOL_1: bits[0]
             }

    cur_state = []
    for i in range(0, width):
        cur_state.append(SYMBOL_0)
    cur_state[int(width/2)] = SYMBOL_1

    print(f"Rules: {rules}\n")
    print(f"Width: {width}, Iterations: {height}")
    print(f"STARTING STATE: {''.join(cur_state)}\n")

    for y in range(height):
        next_state = []
        for x in range(width):
            snippet = cur_state[x-1] + cur_state[x] + cur_state[(x+1)%(width-1)]
            next_state.append(rules[snippet])

        print("".join(cur_state))
        cur_state = next_state

def main():

    parser = argparse.ArgumentParser(description="Specify the Rule number (0=< n < 256) for the Automaton to follow and optionally render dimensions.")

    parser.add_argument("--rule", "-r", type=int, default=30, help="Rule number. Gets converted to binary and encodes the action with every positional bit and its positions binary representation.")
    parser.add_argument("--width","-w", type=int, default=240, help="width of the automaton world")
    parser.add_argument("--iterations", "-i", type=int, default=240, help="number of iterations to run the automaton for")

    args = parser.parse_args()

    rule = args.rule

    print(f"Rule {rule} in binary is {bitParser(rule)} !")

    setup_automaton(number=rule, width=args.width, height=args.iterations)

if __name__=="__main__":
    main()
