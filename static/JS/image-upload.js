/**
 * GM Express - Sistema de carga de imágenes con drag & drop
 * Permite arrastrar y soltar archivos o seleccionarlos manualmente
 * Compatible con formularios de Servicios y Productos
 */

document.addEventListener('DOMContentLoaded', function() {
    // Buscar todos los campos de imagen en el formulario
    const imageInputs = document.querySelectorAll('input[type="file"][accept="image/*"]');
    
    imageInputs.forEach(input => {
        initializeImageUpload(input);
    });
});

function initializeImageUpload(fileInput) {
    // Crear contenedor de drag & drop
    const dropZone = createDropZone(fileInput);
    
    // Insertar la zona de drop antes del input original
    fileInput.parentNode.insertBefore(dropZone, fileInput);
    
    // Ocultar el input original pero mantenerlo funcional
    fileInput.style.display = 'none';
    
    // Obtener elementos del dropZone
    const dropArea = dropZone.querySelector('.drop-area');
    const browseBtn = dropZone.querySelector('.browse-btn');
    const fileNameDisplay = dropZone.querySelector('.file-name');
    const previewImage = dropZone.querySelector('.preview-image');
    const removeBtn = dropZone.querySelector('.remove-btn');
    
    // Evento: Click en "Elegir archivo"
    browseBtn.addEventListener('click', () => fileInput.click());
    
    // Evento: Archivo seleccionado manualmente
    fileInput.addEventListener('change', function() {
        handleFiles(this.files);
    });
    
    // Eventos de drag & drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            dropArea.classList.add('drag-over');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, () => {
            dropArea.classList.remove('drag-over');
        });
    });
    
    dropArea.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles(files);
    });
    
    // Evento: Remover imagen
    removeBtn.addEventListener('click', function() {
        fileInput.value = '';
        fileNameDisplay.textContent = 'Ningún archivo seleccionado';
        previewImage.style.display = 'none';
        removeBtn.style.display = 'none';
        dropArea.style.display = 'block';
    });
    
    // Funciones auxiliares
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            
            // Validar que sea una imagen
            if (!file.type.startsWith('image/')) {
                alert('Por favor selecciona un archivo de imagen válido');
                return;
            }
            
            // Validar tamaño (máx 5MB)
            if (file.size > 5 * 1024 * 1024) {
                alert('El archivo es demasiado grande. Máximo 5MB');
                return;
            }
            
            // Asignar el archivo al input original
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
            
            // Mostrar nombre del archivo
            fileNameDisplay.textContent = file.name;
            
            // Mostrar vista previa
            const reader = new FileReader();
            reader.onload = function(e) {
                previewImage.src = e.target.result;
                previewImage.style.display = 'block';
                removeBtn.style.display = 'inline-block';
                dropArea.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    }
}

function createDropZone(fileInput) {
    const wrapper = document.createElement('div');
    wrapper.className = 'image-upload-wrapper';
    
    wrapper.innerHTML = `
        <div class="drop-area">
            <div class="upload-icon">
                <i class="fas fa-cloud-upload-alt"></i>
            </div>
            <h5>Arrastra tu imagen aquí</h5>
            <p class="text-muted">o</p>
            <button type="button" class="btn btn-outline-success browse-btn">
                <i class="fas fa-folder-open"></i> Elegir archivo
            </button>
            <p class="file-info text-muted mt-3">
                <small>Formatos: JPG, PNG, GIF. Máximo 5MB</small>
            </p>
        </div>
        <div class="preview-container" style="display: none;">
            <img class="preview-image" alt="Vista previa" style="display: none;">
            <button type="button" class="btn btn-danger btn-sm remove-btn" style="display: none;">
                <i class="fas fa-trash"></i> Remover imagen
            </button>
        </div>
        <div class="file-name text-center mt-2 text-muted">
            <small>Ningún archivo seleccionado</small>
        </div>
    `;
    
    return wrapper;
}
