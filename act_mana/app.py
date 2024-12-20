from flask import Flask, render_template, request, jsonify, Response
from motivo_handler import MotivoHandler
from qianwen_api import QianwenAPI
import json
import time

app = Flask(__name__)
motivo_handler = MotivoHandler()
qianwen_api = QianwenAPI()
steps_data = {
    '1': 'Step 1 description',
    '2': 'Step 2 description',
    # Add more steps as needed
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.json.get('text', '')

    steps = qianwen_api.get_steps(input_text)
    
    global steps_data
    steps_data = {str(i): step for i, step in enumerate(steps)}
    
    return jsonify({
        'steps': steps
    })

@app.route('/stream/<step>')
def stream(step):
    '''处理step <step> 图像流'''
    def generate():
        step_index = int(step)
        print('Starting stream for step:', step_index)
        try:
            # 获取当前步骤的描述
            step_description = steps_data.get(str(step_index), 'Unknown step')
            for frame in motivo_handler.process_step(step_index):
                # print('Generated new frame')
                yield f'data: {json.dumps({"image": frame, "description": step_description})}\n\n'
                time.sleep(0.02)
            # 当前步骤完成时发送结束信号
            yield f'data: {json.dumps({"complete": True})}\n\n'
        except Exception as e:
            print(f'Error in stream generation: {str(e)}')
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
            
    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)