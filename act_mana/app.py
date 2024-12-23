from flask import Flask, render_template, request, jsonify, Response
import json
import time
from config import humenv_tasks, sentence_transformer_model, fbpcr_model
from motivo_handler import MotivoHandler
from qianwen_api import QianwenAPI
from semantic1 import SentTransformer
# from semantic2 import SentTfidf
# semantic_mapper = SemanticMapper()

semantic_mapper = SentTransformer(sentence_transformer_model)

app = Flask(__name__)
motivo_handler = MotivoHandler(fbpcr_model)
qianwen_api = QianwenAPI()
steps_data = {
    '1': ('Step 1 description', 'Task 1', 0.5),
    '2': ('Step 2 description', 'Task 3', 0.7),
    # Add more steps as needed
}

sim_threshold = 0.3
unmatched_task = 'Unknown Task'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    input_text = request.json.get('text', '')

    steps = qianwen_api.get_steps(input_text)
    
    global steps_data
    steps_data = {}
    matched = []
    for i,step_desc in enumerate(steps):
        most_similar_task, similarity = semantic_mapper.find_most_similar(step_desc, humenv_tasks)
        if similarity < sim_threshold:
            most_similar_task = unmatched_task
            # similarity = 0.0
        steps_data[str(i)] = (step_desc, most_similar_task, similarity) 
        matched.append(f' <=> {similarity:.2f}, {most_similar_task}')
    
    return jsonify({
        'steps': steps,
        'matched_info': matched
    })

@app.route('/stream/<step>')
def stream(step):
    '''处理step <step> 图像流'''
    def generate():
        step_index = int(step)
        print('Starting stream for step:', step_index)
        try:
            # 获取当前步骤
            step_desc, most_similar_task, _ = steps_data.get(str(step_index), unmatched_task)
            if most_similar_task != unmatched_task:                
                for frame in motivo_handler.process_step(step_index, most_similar_task):
                    # print('Generated new frame')
                    yield f'data: {json.dumps({"image": frame})}\n\n'
                    time.sleep(0.02)
            else:
                print('Unknown step, skipping...')
                time.sleep(2)
            # 当前步骤完成时发送结束信号
            yield f'data: {json.dumps({"complete": True})}\n\n'
        except Exception as e:
            print(f'Error in stream generation: {str(e)}')
            yield f'data: {json.dumps({"error": str(e)})}\n\n'
            
    return Response(generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)