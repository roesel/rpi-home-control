import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output

def get_shell(color):
    command_list = ['/home/pi/yee/light.sh', 'color', '{}'.format(color)]
    print(command_list)
    stdout = check_output(command_list).decode('utf-8')
    print(stdout)
    return stdout
    
from yeelight import Bulb, discover_bulbs
b = Bulb("192.168.1.67")
print(discover_bulbs())

