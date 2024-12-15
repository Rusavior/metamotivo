
'''
>> env.render() 报错. ERROR: could not initialize GLFW
apt-get install  libglew-dev
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so

>> gladLoadGL error
apt install xvfb
xvfb-run -a python test.py
'''