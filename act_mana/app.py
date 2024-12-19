from flask import Flask, render_template, request, jsonify, Response
from motivo_handler import MotivoHandler
from qianwen_api import QianwenAPI
import json

app = Flask(__name__)
motivo_handler = MotivoHandler()
qianwen_api = QianwenAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.json.get('text', '')

    # 调用LLM API获取步骤拆解
    steps = qianwen_api.get_steps(input_text)
    
    return jsonify({
        'steps': steps
    })

@app.route('/stream/<step>')
def stream(step):
    '''处理图像流'''
    def generate():
        print('Starting stream for step:', step)
        try:
            for frame in motivo_handler.process_step(step):
                print('Generated new frame')
                yield f'data: {json.dumps({"image": frame})}\n\n'
        except Exception as e:
            print(f'Error in stream generation: {str(e)}')
            
    return Response(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 