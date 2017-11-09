"""The automatic cryptography challenge solver

decrypt0 can use stages (filters) to complete your challenge"""
__author__ = "ex0dus"
__version__ = "1.0"

import base64, argparse, types, sys

def unicode_unescape(text):
    return bytes(text, "utf-8").decode("unicode-escape")

def base_64(text):
    return str(base64.decodestring(text.encode("utf-8")), "utf-8")

def caesar(text):
    results = list()
    for key in range(1, 27):
        result = str()
        for c in text:
            if c.isalpha():
                num = ord(c) + key
                if num > ord("Z" if c.isupper() else "z"):
                    num -= 26
                elif num < ord("A" if c.isupper() else "a"):
                    num += 26
                result += chr(num)
            else:
                result += c
        results.append(result)
    return results

def _print_results(data):
    if len(data) == 1:
        print("Result: {data}".format(data=data[0]))
    else:
        padding = len(str(len(data))) + 1
        for i, d in enumerate(data, start=1):
            print("Result {i}{padding}: {d}".format(
                i=i,
                padding=" " * (padding - len(str(i))),
                d=d))

def _eval(cmd, text):
    result = eval(cmd)
    if result is True:
        return text
    elif result is False:
        return None
    else:
        return result

parser = argparse.ArgumentParser(description="The automatic cryptography challenge solver")
parser.add_argument("code",
                    type=str,
                    help="the input code")
parser.add_argument("stages",
                    type=str,
                    nargs="+",
                    help="the decoding stages")
parser.add_argument("-p", "--print",
                    action="store_true",
                    help="print the result at each stage")
parser.add_argument("-s", "--save",
                    type=str,
                    required=False,
                    help="save the result to a file")
args = parser.parse_args()

codes = [args.code]
stages = args.stages
always_print = args.print
save = args.save
functions = dict([x for x in sys.modules[__name__].__dict__.items()
        if type(x[1]) is types.FunctionType and not x[1].__name__.startswith("_")])

for stage in stages:
    print("Running stage {stage}...".format(stage=stage), end=" ")
    new_codes = list()
    errors = 0
    for code in codes:
        func = functions[stage] if stage in functions else None
        try:
            result = _eval(stage, code) if func is None else func(code)
            if type(result) == list and len(result) != 0:
                new_codes.extend(result)
            elif result is not None:
                new_codes.append(result)
        except:
            errors += 1
    codes = new_codes
    print("Complete ({count} result(s){errors})".format(
        count=len(new_codes) if len(new_codes) != 0 else "No",
        errors="" if errors == 0 else ", {count} errors".format(count=errors)))
    if len(new_codes) == 0:
        break
    if always_print:
        _print_results(codes)
if not always_print:
    _print_results(codes)
if save is not None:
    print("Saving...", end=" ")
    with open(save, "w") as file:
        file.writelines("\n".join(codes))
    print("Complete")
