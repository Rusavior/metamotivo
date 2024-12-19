# Issues & FIXes when running motivo
```
>>
Issue: env.render() 报错. ERROR: could not initialize GLFW
OR 前边能运行但是代码结束时报错：
Exception ignored in: <function Renderer.__del__ at 0x7775a838aef0>
Traceback (most recent call last):
  File "...../lib/python3.10/site-packages/mujoco/renderer.py", line 335, in __del__
  File "...../lib/python3.10/site-packages/mujoco/renderer.py", line 321, in close
  File "...../lib/python3.10/site-packages/mujoco/glfw/__init__.py", line 35, in free
TypeError: 'NoneType' object is not callable
Exception ignored in: <function GLContext.__del__ at 0x7775a838a560>
Traceback (most recent call last):
  File "...../lib/python3.10/site-packages/mujoco/glfw/__init__.py", line 41, in __del__
  File "...../lib/python3.10/site-packages/mujoco/glfw/__init__.py", line 35, in free
TypeError: 'NoneType' object is not callable

FIX:
sudo apt-get install libglew-dev
export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so
注意：安装完libglew-dev后，库文件libGLEW.so在系统中的名字可能会带版本号后缀。添加环境变量前先确认这一点。
step1: 在 /usr/lib/中查找库文件：  grep -r libGLEW /usr/lib/ 
step2: 找到后再添加环境变量，比如我的是libGLEW.so.2.2.0。 export LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libGLEW.so.2.2.0


>>
Issue: 根据项目提示安装后，运行时报错一些so文件找不到。大多原因是安装目录与项目搜索路径不一致。
FIX: 
step1: locate 命令找一下so文件位置
step2: 建立软链接： ln -sf so文件位置  项目搜索路径


>>
Issue: gladLoadGL error (when run it in vm on the cloud)
FIX: 
apt install xvfb
xvfb-run -a python test.py
```