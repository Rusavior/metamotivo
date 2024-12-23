import requests
import os
from openai import OpenAI


class QianwenAPI:
    def __init__(self):
        self.llm_api = OpenAI(api_key=os.getenv('DASHSCOPE_API_KEY'), base_url='https://dashscope.aliyuncs.com/compatible-mode/v1')
        with open('system_prompts.txt') as f:
            self.sys_prompt = '\n'.join([line.strip() for line in f.readlines()])

    def get_steps(self, text):  
        try:     
            response = self.llm_api.chat.completions.create(
                model='qwen-plus', # 'deepseek-chat',
                messages=[
                    {'role': 'system', 'content': self.sys_prompt},
                    {'role': 'user', 'content': text},
                ],
                max_tokens=1024,
                # temperature=0.7,
                stream=False
                )
            response_ = response.choices[0].message.content.strip()
            
            # response_ = '\
            #     I will do the following steps (for test) \n \
            #     1. Scan the room to locate a red ball. \n \
            #     2. Navigate to the red ball once identified.  \n \
            #     3. Take a picture of the red ball. \n \
            #     4. Return to your location. \n \
            #     5. Show you the picture taken. \n \
            #     That is all. '
            
            # 处理返回的文本，分割成步骤列表
            steps = [step.strip() for step in response_.split('\n') if step.strip()]
            # # 过滤掉非步骤的行
            # steps = [step for step in steps if any(c.isdigit() for c in step)]
            
        except:
            steps = ['error when calling llm api.']
        return steps  # 返回列表而不是字符串


if __name__=='__main__':
    qianwen_api = QianwenAPI()
    steps = qianwen_api.get_steps('give me an apple.')
    print(steps)