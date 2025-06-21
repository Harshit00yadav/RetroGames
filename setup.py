from os import listdir, system
from sys import platform

contents = listdir(".")
if ("genv" in contents):
    print("[ OK ] environment found")
else:
    ans = input("do you want to setup in this folder (Y/n):")
    if ans == 'n':
        exit()
    try:
        system("python -m venv genv")
        print("[ OK ] Virtual environment setup done!")
    except Exception as e:
        print("[ ERROR ]", e)

print("Installing module dependencies...")
if platform == "linux":
    print("No dependencies required")
elif platform == "win32":
    try:
        system(r"genv\scripts\activate && pip install -r requirements.txt")
    except Exception as e:
        print("[ ERROR ]", e)
        exit()
print("--[FINISHED]--")
