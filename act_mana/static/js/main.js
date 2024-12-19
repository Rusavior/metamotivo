document.getElementById('submit-btn').addEventListener('click', async () => {
    const inputText = document.getElementById('input-box').value;
    const stepsOutput = document.getElementById('steps-output');
    const imageContainer = document.getElementById('image-container');
    
    // 清空之前的输出
    stepsOutput.innerHTML = '';
    imageContainer.innerHTML = '';
    
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
        
        // 确保steps是数组
        const steps = Array.isArray(data.steps) ? data.steps : [data.steps];
        
        // 显示步骤
        steps.forEach((step, index) => {
            const stepElement = document.createElement('p');
            stepElement.textContent = step;
            stepsOutput.appendChild(stepElement);
            
            // 为每个步骤创建EventSource
            const eventSource = new EventSource(`/stream/${encodeURIComponent(step)}`);
            
            eventSource.onmessage = function(event) {
                try {
                    const frameData = JSON.parse(event.data);
                    if (!frameData.image) {
                        console.error('No image data received');
                        return;
                    }
                    
                    const img = document.createElement('img');
                    img.onerror = function() {
                        console.error('Failed to load image');
                    };
                    img.onload = function() {
                        // 清除之前的图像
                        imageContainer.innerHTML = '';
                        imageContainer.appendChild(img);
                    };
                    img.src = `data:image/png;base64,${frameData.image}`;
                } catch (error) {
                    console.error('Error processing frame:', error);
                }
            };
            
            eventSource.onerror = function(error) {
                console.error('EventSource failed:', error);
                eventSource.close();
            };
        });
        
    } catch (error) {
        console.error('Error:', error);
        stepsOutput.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
}); 