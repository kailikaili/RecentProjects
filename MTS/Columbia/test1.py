import subprocess
import datetime

print(datetime.datetime.now())
p1 = subprocess.Popen('sleep 3', shell = True)

print(datetime.datetime.now())
for i in range(0, 6):

    p = subprocess.Popen('sleep ' + str(i), shell = True)
    print i

print(datetime.datetime.now())

p1.wait()
p.wait()

print(datetime.datetime.now())
