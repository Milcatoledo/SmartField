document.addEventListener('DOMContentLoaded', () => {
  const sourceIsCamera = document.getElementById('camera-stream') !== null;
  const analysisSection = document.getElementById('analysis-section');
  const uploadInput = document.getElementById('upload-file');
  const imagePreview = document.getElementById('image-preview');



  if (uploadInput) {
    uploadInput.addEventListener('change', (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          imagePreview.src = e.target.result;
          analysisSection.style.display = 'block';
        };
        reader.readAsDataURL(file);
      }
    });
  }

  if (sourceIsCamera) {
    const cameraContainer = document.getElementById('camera-container');
    const cameraStream = document.getElementById('camera-stream');
    const captureButton = document.getElementById('capture-button');
    const capturedImageInput = document.getElementById('captured-image');
    const finalResult = document.getElementById('final-result');

    cameraContainer.classList.remove('hidden');


    navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } })
      .then(stream => {
        cameraStream.srcObject = stream;
      })
      .catch(err => {
        alert('No se pudo acceder a la cámara: ' + err);
        console.error('Error al acceder a la cámara:', err);
      });

    captureButton.addEventListener('click', () => {
      const canvas = document.createElement('canvas');
      canvas.width = cameraStream.videoWidth;
      canvas.height = cameraStream.videoHeight;
      const ctx = canvas.getContext('2d');
      ctx.drawImage(cameraStream, 0, 0, canvas.width, canvas.height);

      const imageDataUrl = canvas.toDataURL('image/png');

      imagePreview.src = imageDataUrl;
      analysisSection.style.display = 'block';
      resultCard.style.display = 'none';
      finalResult.classList.add('hidden');

      capturedImageInput.value = imageDataUrl;

      const tracks = cameraStream.srcObject.getTracks();
      tracks.forEach(track => track.stop());
      cameraStream.srcObject = null;
      cameraContainer.classList.add('hidden');
    });
  }
});
