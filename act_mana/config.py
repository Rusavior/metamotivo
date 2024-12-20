
sentence_transformer_model = '/home/xl/cspace/fft-codes/Robot-Behavior-Planner-App/fft-app/src-tauri/src/weights/all-MiniLM-L6-v2'
fbpcr_model = '/home/xl/Downloads/models/metamotivo-M-1'

with open('humenv_tasks.txt', 'r') as f:
    humenv_tasks = [line.strip() for line in f.readlines()]