document.addEventListener('DOMContentLoaded', () => {
  const uploadInput = document.getElementById('upload-file');
  const capturedImageInput = document.getElementById('captured-image');
  const imagePreview = document.getElementById('image-preview');
  const analysisSection = document.getElementById('analysis-section');
  const resultCard = document.getElementById('result-card');
  const finalResult = document.getElementById('final-result');
  const cameraContainer = document.getElementById('camera-container');
  const cameraStream = document.getElementById('camera-stream');
  const captureButton = document.getElementById('capture-button');

  if (cameraContainer) {

    const openCamera = async () => {
      cameraContainer.classList.remove('hidden');

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } });
        cameraStream.srcObject = stream;
      } catch (err) {
        alert("No se pudo acceder a la cámara: " + err);
        console.error("Error al acceder a la cámara:", err);
      }
    };

    openCamera();
  }

  if (uploadInput) {
    uploadInput.addEventListener('change', (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          imagePreview.src = e.target.result;
          analysisSection.style.display = 'block'; // Mostrar la sección de análisis
          resultCard.style.display = 'none';
          finalResult.classList.add('hidden');
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (captureButton) {
    captureButton.addEventListener('click', () => {
      const canvas = document.createElement('canvas');
      canvas.width = cameraStream.videoWidth;
      canvas.height = cameraStream.videoHeight;
      const context = canvas.getContext('2d');
      context.drawImage(cameraStream, 0, 0, canvas.width, canvas.height);
      const imageDataUrl = canvas.toDataURL('image/png');
      imagePreview.src = imageDataUrl;
      console.log("Captured image data URL:", imageDataUrl); // Log para depuración

      capturedImageInput.value = imageDataUrl;

      cameraStream.srcObject.getTracks().forEach(track => track.stop());
      cameraContainer.classList.add('hidden');
      analysisSection.style.display = 'block';
      resultCard.style.display = 'none';
      finalResult.classList.add('hidden');
    });
  }
});
