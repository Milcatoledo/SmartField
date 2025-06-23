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
            };
            reader.readAsDataURL(file);
        }
    });

    analyzeButton.addEventListener('click', () => {
        resultCard.style.display = 'block';
        loader.style.display = 'flex';
        finalResult.classList.add('hidden');
        
        setTimeout(() => {
            const results = [
                { text: 'INMADURO', color: 'text-red-600', borderColor: 'border-red-500' },
                { text: 'PINTÓN', color: 'text-yellow-600', borderColor: 'border-yellow-500' },
                { text: 'PUNTO ÓPTIMO', color: 'text-green-700', borderColor: 'border-green-600' },
                { text: 'SOBREMADURO', color: 'text-purple-600', borderColor: 'border-purple-500' }
            ];
            const randomResult = results[Math.floor(Math.random() * results.length)];

            resultText.textContent = randomResult.text;
            resultText.className = `text-4xl font-extrabold ${randomResult.color}`;
            resultCard.className = `mt-8 bg-white p-8 rounded-lg shadow-lg border-2 ${randomResult.borderColor}`;
            loader.style.display = 'none';
            finalResult.classList.remove('hidden');
        }, 2500);
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
    });

});