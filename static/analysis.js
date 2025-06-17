 document.addEventListener('DOMContentLoaded', () => {
            const uploadInput = document.getElementById('upload-file');
            const photoInput = document.getElementById('take-photo');
            const imagePreview = document.getElementById('image-preview');
            const analysisSection = document.getElementById('analysis-section');
            const inputSection = document.getElementById('input-section');
            const analyzeButton = document.getElementById('analyze-button');
            
            const resultCard = document.getElementById('result-card');
            const resultContent = document.getElementById('result-content');
            const loader = document.getElementById('loader');
            const finalResult = document.getElementById('final-result');
            const resultText = document.getElementById('result-text');

            const handleFileSelect = (event) => {
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
            };

            uploadInput.addEventListener('change', handleFileSelect);
            photoInput.addEventListener('change', handleFileSelect);

            analyzeButton.addEventListener('click', () => {
                resultCard.style.display = 'block';
                loader.style.display = 'flex';
                finalResult.classList.add('hidden');
                
                // Simulate analysis delay
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
        });