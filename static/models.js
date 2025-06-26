import tensorflow as tf;
document.addEventListener('DOMContentLoaded', function() {
    const analyzeButton = document.getElementById('analyze-button');
    const usedModelSpan = document.getElementById('used-model');
    
    function getSelectedModel() {
        const selectedModel = document.querySelector('input[name="ai-model"]:checked');
        return selectedModel ? selectedModel.value : 'resnet';
    }
    
    function getModelName(modelValue) {
        const modelNames = {
            'resnet': 'Modelo Básico v1.0',
            'mobile': 'Modelo Avanzado v2.0',
            'xception': 'Modelo Especializado v1.5',
            'ponchi': 'Modelo Personalizado'
        };
        return modelNames[modelValue] || 'Desconocido';
    }
    function executeAnalysis() {
        const selectedModel = getSelectedModel();
        const modelName = getModelName(selectedModel);
        
        usedModelSpan.textContent = modelName;
        
        console.log('Modelo seleccionado:', selectedModel);
        
        
    }
    
    analyzeButton.addEventListener('click', function() {
        const selectedModel = getSelectedModel();
        const modelName = getModelName(selectedModel);
        
        usedModelSpan.textContent = modelName;
        
        console.log('Modelo seleccionado:', selectedModel);
        
        executeAnalysis();


    });
});