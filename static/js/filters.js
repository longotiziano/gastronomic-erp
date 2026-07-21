document.querySelectorAll('.search-form').forEach(form => {
    form.addEventListener('submit', function(e) {
        e.preventDefault(); 
        const params = new URLSearchParams(window.location.search);
        const formData = new FormData(this);
        
        for (let targetInput of this.querySelectorAll('[name]')) {
            params.delete(targetInput.name);
        }
        
        formData.forEach((value, key) => {
            if (value.trim() !== '') {
                params.set(key, value.trim());
            }
        });
        
        window.location.search = params.toString();
    });
});
