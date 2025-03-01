
import sys
import os
import subprocess
import time
import random

noLog = False


def test(file:str,padding:str):
    prc = subprocess.Popen(f"./{file}",
                     shell=False,
                     bufsize=64,
                     stdin=subprocess.PIPE,
                     stderr=subprocess.PIPE,
                     stdout=subprocess.PIPE)
    killed = ""
    for tmc in range(50):
        if(prc.poll() is None):
            time.sleep(0.1)
        else:
            break
    else:
        killed = "#"
        prc.kill()
    time.sleep(1)
    code = prc.wait()#returncode
    print(f"{padding} {file} - {hex(code)[2:]}{killed}")
    if(code not in (0,0x7f00)):
        if(noLog):return False
        for ln in prc.stdout:
            print(f"{padding}  {ln}");
        return False
    return True # success

def makeFile(file:str,padding:str):
    with  open(file,"r") as fptr:
        ln = fptr.readlines()[0]
        code = 1
        if('#!' in ln):
            p = ln.find('#!')
            r = ln[p+2:-1]
            print(f"{padding} {file} - {r}")
            code = os.system(r)
        elif('#@' in ln):
            p = ln.find('#@')
            r = ln[p+2:-1]
            raw = file[:-2]
            code = os.system(f"gcc {file} -o {raw}.out {r}");
            print(f"{padding} {file} - gcc {file} -o {raw}.out {r}")
        else:
            print(f"{padding} {file} - ##")

        if(code not in (0,0x7f00)):
            return False
    return True # success

def recursive(place:str,ending:str,fun):
    print(f"{place}cwd:{os.getcwd()}")
    progs = [k for k in os.listdir() if k.endswith(ending)]
    dirs = [k for k in os.listdir() if os.path.isdir(k)]
    random.shuffle(progs)
    random.shuffle(dirs)
    total = 0
    errCount = 0
    for d in dirs:
        total += 1
        os.chdir(d)
        if(not recursive(place+" ",ending,fun)):
            errCount += 1
        os.chdir("..")

    for p in progs:
        total += 1
        #if(not test(p,place)):
        if(not fun(p,place)):
            errCount += 1
    print(f"{place}{errCount}/{total} errors!");
    return errCount == 0 # if no error, then success


if __name__ == '__main__' and "help" in sys.argv:
    print("options:")
    print(" noLog")
    print(" make")
elif __name__ == '__main__':
    # setting up arguments
    if("noLog" in sys.argv):
        noLog = True
    # running
    if(not os.getcwd().endswith("test")):
        os.chdir("test")
    if("make" in sys.argv):
        recursive("",".c",makeFile)
    recursive("",".out",test)
