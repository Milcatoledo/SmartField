document.addEventListener('DOMContentLoaded', () => {
  const sourceIsCamera = document.getElementById('camera-stream') !== null;

  if (sourceIsCamera) {
    const cameraContainer = document.getElementById('camera-container');
    const cameraStream = document.getElementById('camera-stream');
    const captureButton = document.getElementById('capture-button');
    const capturedImageInput = document.getElementById('captured-image');
    const imagePreview = document.getElementById('image-preview');
    const analysisSection = document.getElementById('analysis-section');
    const resultCard = document.getElementById('result-card');
    const finalResult = document.getElementById('final-result');

    // Mostrar contenedor de cámara
    cameraContainer.classList.remove('hidden');

    // Activar cámara
    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      .then(stream => {
        cameraStream.srcObject = stream;
      })
      .catch(err => {
        alert('No se pudo acceder a la cámara: ' + err);
        console.error('Error al acceder a la cámara:', err);
      });

    // Captura la imagen
    captureButton.addEventListener('click', () => {
      const canvas = document.createElement('canvas');
      canvas.width = cameraStream.videoWidth;
      canvas.height = cameraStream.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(cameraStream, 0, 0, canvas.width, canvas.height);

      const imageDataUrl = canvas.toDataURL('image/png');

      // Muestra vista previa
      imagePreview.src = imageDataUrl;
      analysisSection.style.display = 'block';
      resultCard.style.display = 'none';
      finalResult.classList.add('hidden');

      // Guarda imagen para enviar en formulario
      capturedImageInput.value = imageDataUrl;

      // Detiene la cámara
      const tracks = cameraStream.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      cameraStream.srcObject = null;
      cameraContainer.classList.add('hidden');
    });
  }
});
