const showFile = (uploader, fileName, show) => {
    const dropzone = uploader.querySelector('.upload-dropzone');
    const fileNameSpan = dropzone.querySelector('.file-name');
    const input = document.getElementById(dropzone.dataset.uploaderid);

    if (show) {
        dropzone.classList.add('has-file');
        fileNameSpan.textContent = fileName;
    } else {
        dropzone.classList.remove('has-file');
        fileNameSpan.textContent = '';
        input.value = '';
    }
};

const initUploaders = () => {
    document.querySelectorAll('.upload-dropzone').forEach((dropzone) => {
        const input = document.getElementById(dropzone.dataset.uploaderid);
        const cancelBtn = dropzone.querySelector('.x-btn');
        const uploader = dropzone.closest('.block');
        console.log(document.querySelector('.uploader'));
        console.log(uploader);
        console.log(input);
        document.querySelector('.uploader').addEventListener('submit', function(e) {
            if (input.files.length === 0) {
                console.log('evitandooo');
                e.preventDefault();
            }
        });

        input.addEventListener('change', function () {
            const file = this.files[0];
            if (file) showFile(uploader, file.name);
        });

        cancelBtn.addEventListener('click', (e) => {
            e.preventDefault();
            showFile(uploader, '', false);
        });
    });
};
initUploaders();