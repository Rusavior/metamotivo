document.getElementById('submit-btn').addEventListener('click', async () => {
    const inputText = document.getElementById('input-box').value;
    const stepsOutput = document.getElementById('steps-output');
    
    // 清空之前的输出
    stepsOutput.innerHTML = '';
    // 重置当前步骤文本为默认值
    document.getElementById('currentStep').value = 'current step';
    // 隐藏图片
    document.getElementById('streamImage').style.display = 'none';
    
    try {
        // 获取步骤拆解
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: inputText })
        });
        
        const data = await response.json();
        const steps = Array.isArray(data.steps) ? data.steps : [data.steps];
        
        // 显示步骤标题
        stepsOutput.innerHTML = '<p>show high-level behavior steps</p>';
        
        // 显示所有步骤
        steps.forEach((step, index) => {
            const stepElement = document.createElement('p');
            // stepElement.textContent = `${index + 1}. ${step}`;
            stepElement.textContent = `${step}`;
            stepsOutput.appendChild(stepElement);
        });

        // 顺序执行每个步骤
        let currentStepIndex = 0;
        
        function processNextStep() {
            if (currentStepIndex >= steps.length) {
                return; // 所有步骤处理完毕
            }

            const currentStep = steps[currentStepIndex];
            // 更新当前步骤文本
            // document.getElementById('currentStep').value = `${currentStepIndex + 1}. ${currentStep}`;
            document.getElementById('currentStep').value = `current step: ${currentStep}`;
            
            // 创建 EventSource
            const eventSource = new EventSource(`/stream/${currentStepIndex}`);
            
            eventSource.onmessage = function(event) {
                const data = JSON.parse(event.data);
                const img = document.getElementById('streamImage');
                if (data.image) {
                    img.src = `data:image/png;base64,${data.image}`;
                    img.style.display = 'block';
                }
                if (data.complete) {
                    eventSource.close();
                    currentStepIndex++; // 移动到下一步
                    processNextStep(); // 处理下一步
                }
            };
            
            eventSource.onerror = function(error) {
                console.error('EventSource failed:', error);
                eventSource.close();
                currentStepIndex++; // 移动到下一步
                processNextStep(); // 处理下一步
            };
        }

        // 开始处理第一个步骤
        processNextStep();
        
    } catch (error) {
        console.error('Error:', error);
        stepsOutput.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});