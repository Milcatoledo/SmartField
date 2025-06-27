document.addEventListener('DOMContentLoaded', () => {
    const scrollTopBtn = document.getElementById("scrollTopBtn");
    const uploadInput = document.getElementById('upload-file');
    const imagePreview = document.getElementById('image-preview');
    const analysisSection = document.getElementById('analysis-section');
    const inputSection = document.getElementById('input-section');
    const analyzeButton = document.getElementById('analyze-button');
    const resultCard = document.getElementById('result-card');
    const loader = document.getElementById('loader');
    const finalResult = document.getElementById('final-result');
    const resultText = document.getElementById('result-text');

        window.addEventListener("scroll", () => {
            if (window.scrollY > 200) {
                scrollTopBtn.style.display = "block";
            } else {
                scrollTopBtn.style.display = "none";
            }
        });

        scrollTopBtn.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });

        scrollTopBtn.style.display = "none";

    uploadInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                inputSection.style.display = 'none';
                analysisSection.style.display = 'block';
                resultCard.style.display = 'none';
                finalResult.classList.add('hidden');
                // Limpiar contenido previo de resultados
                clearPreviousResults();
            };
            reader.readAsDataURL(file);
        }
    });

    analyzeButton.addEventListener('click', async () => {
        resultCard.style.display = 'block';
        loader.style.display = 'flex';
        finalResult.classList.add('hidden');
        
        try {
            // Obtener la imagen como base64
            const imageDataUrl = imagePreview.src;
            
            // Enviar imagen al backend
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageDataUrl,
                    model: 'cacao_model' // Puedes hacer esto configurable
                })
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Mostrar resultado exitoso
                resultText.textContent = result.class;
                resultText.className = `text-4xl font-extrabold ${result.color}`;
                resultCard.className = `mt-8 bg-white p-8 rounded-lg shadow-lg border-2 ${result.border_color}`;
                
                // Añadir información de confianza si está disponible
                if (result.confidence) {
                    const confidenceText = document.createElement('p');
                    confidenceText.className = 'text-sm text-gray-500 mt-2';
                    confidenceText.textContent = `Confianza: ${(result.confidence * 100).toFixed(1)}%`;
                    finalResult.appendChild(confidenceText);
                }
                
                // Añadir modelo usado
                if (result.model_used) {
                    const modelText = document.createElement('p');
                    modelText.className = 'text-xs text-gray-400 mt-1';
                    modelText.textContent = `Modelo: ${result.model_used}`;
                    finalResult.appendChild(modelText);
                }
                
                loader.style.display = 'none';
                finalResult.classList.remove('hidden');
            } else {
                // Mostrar error
                resultText.textContent = 'ERROR EN ANÁLISIS';
                resultText.className = 'text-4xl font-extrabold text-red-600';
                resultCard.className = 'mt-8 bg-white p-8 rounded-lg shadow-lg border-2 border-red-500';
                
                // Mostrar mensaje de error específico
                const errorText = document.createElement('p');
                errorText.className = 'text-sm text-red-500 mt-2';
                errorText.textContent = result.error || 'Error desconocido';
                finalResult.appendChild(errorText);
                
                loader.style.display = 'none';
                finalResult.classList.remove('hidden');
            }
            
        } catch (error) {
            console.error('Error en la predicción:', error);
            
            // Mostrar error de conexión
            resultText.textContent = 'ERROR DE CONEXIÓN';
            resultText.className = 'text-4xl font-extrabold text-red-600';
            resultCard.className = 'mt-8 bg-white p-8 rounded-lg shadow-lg border-2 border-red-500';
            
            const errorText = document.createElement('p');
            errorText.className = 'text-sm text-red-500 mt-2';
            errorText.textContent = 'No se pudo conectar con el servidor';
            finalResult.appendChild(errorText);
            
            loader.style.display = 'none';
            finalResult.classList.remove('hidden');
        }
    });

    // --- Cámara ---
    const openCameraButton = document.getElementById('open-camera');
    const cameraContainer = document.getElementById("camera-container");
    const cameraStream = document.getElementById("camera-stream");
    const captureButton = document.getElementById("capture-button");

    openCameraButton.addEventListener('click', async () => {
        inputSection.style.display = 'none';
        cameraContainer.classList.remove('hidden');
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
            cameraStream.srcObject = stream;
        } catch (err) {
            alert("No se pudo acceder a la cámara: " + err);
        }
    });

    captureButton.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        canvas.width = cameraStream.videoWidth;
        canvas.height = cameraStream.videoHeight;
        const context = canvas.getContext('2d');
        context.drawImage(cameraStream, 0, 0, canvas.width, canvas.height);
        const imageDataUrl = canvas.toDataURL('image/png');
        imagePreview.src = imageDataUrl;
        cameraStream.srcObject.getTracks().forEach(track => track.stop());
        cameraContainer.classList.add('hidden');
        analysisSection.style.display = 'block';
        resultCard.style.display = 'none';
        finalResult.classList.add('hidden');
        // Limpiar contenido previo de resultados
        clearPreviousResults();
    });

    // Función para limpiar resultados previos
    function clearPreviousResults() {
        // Limpiar elementos adicionales que se puedan haber añadido
        const additionalElements = finalResult.querySelectorAll('p:not(#result-text):not(.text-lg)');
        additionalElements.forEach(element => element.remove());
    }

});