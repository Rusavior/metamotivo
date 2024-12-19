文件teat.py中实现了完整的调用motivo的代码。请在此基础上帮我添加一个基于Flask的UI.
UI界面如图，其中各个功能区要求如下：
1. input box中输入文本内容。
2. 点击 submit 按钮，Flask后端调用 通义千问 API 实现机器人可执行步骤的详细拆解。拆解结果的格式要求是一行一个步骤。并把给结果输出到 Output|Advanced 文本框。
3. 得到拆解结果同时，每个步骤对应一次metamotivo推理（代码参考teat.py），并把对应的画面推流到 image display area. 
4. 要求整个项目代码结构清晰，所有代码文件都保存在 act_mana 目录中。