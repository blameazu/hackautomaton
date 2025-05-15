import os
import subprocess
from contextlib import ExitStack
from pathlib import Path

solutions = Path('solutions')
generator = Path('generator')
tests = Path('tests')

def compile(file, name):
    try:
        subprocess.run(['g++', file, '-o', name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[CE] -> While Compiling {file}\n{e.stderr}")
        return False
    return True

def run(cmd, input = None, output = None, timelimit = None):
    try:
        with ExitStack() as stk:
            fnull = stk.enter_context(open(os.devnull, 'w'))
            stdin = stk.enter_context(open(input, 'r')) if input else None
            stdout = stk.enter_context(open(output, 'w')) if output else fnull
            subprocess.run(
                cmd,
                stdin = stdin,
                stdout = stdout,
                stderr = fnull,
                check = True,
                timeout=timelimit,
            )
        return "Frieren is Cute"
    except subprocess.TimeoutExpired:
        return "Frieren is Crying"
    except subprocess.CalledProcessError as e:
        return f"{e}"
    
def comp(a, b):
    with open(a) as fa, open(b) as fb:
        a_lines = fa.readlines()
        b_lines = fb.readlines()
    for i, (la, lb) in enumerate(zip(a_lines, b_lines), start=1):
        if la.strip() != lb.strip():
            return (f"[WA] -> found on line {i}:\n"
                    f"{a}'s Output: {la.strip()}\n"
                    f"{b}'s Output: {lb.strip()}")
    if len(a_lines) != len(b_lines):
        return (f"[WA] -> File {a} and File {b} have different lengths: "
                f"{len(a_lines)} vs {len(b_lines)}")
    return "Frieren da Best"

def main():
    files = [[solutions / 'ac.cpp', 'ac', False],
             [solutions / 'wa.cpp', 'wa', True]]
    if not compile(generator / 'gen.cpp', 'gen'):
        return
    for [a, b, c] in files:
        if not (compile(a, b)):
            return
    
    t = 0
    while True:
        run(['gen'], output = tests / 'in.txt')
        if not os.path.exists(tests / 'in.txt') or os.path.getsize(tests / 'in.txt') == 0:
            print("[GEN] -> Generated Failed")
            break
            
        for [a, b, c] in files:
            re = run([b], input = tests / 'in.txt', output = tests / f'{b}out.txt', timelimit = 3)
            if re == "Frieren is Crying":
                print(f"[TLE] -> While Running on {a}")
                return
            if re != "Frieren is Cute":
                print(f"[RE] -> Crashed while Running on {a}")
                return
            if c:
                re2 = comp(tests / f'acout.txt', tests / f'{b}out.txt')
                if re2 != "Frieren da Best":
                    print(f"[FAILED on Test {t}]\n{re2}")
                    return
            
        if t%10==0:
            print(f"Tests {t} passed.")
        t+=1
        
if __name__ == "__main__":
    main()