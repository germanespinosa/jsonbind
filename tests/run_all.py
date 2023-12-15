from glob import glob
import subprocess

mymodules = {}
for test_file in glob("*_tests.py"):
    module_name = test_file.split("/")[-1].replace(".py", "")
    print("runing %s" % module_name)
    subprocess.run(["python", "-m", "unittest", module_name, "-v"])

