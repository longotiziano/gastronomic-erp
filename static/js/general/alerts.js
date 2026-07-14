/*
Utiliza la libreria SweetAlert2 para mostrar alertas personalizadas con estilos adaptados a la estética del sitio.
*/
export const showAlert = (title, text, icon) => {
    return Swal.fire({
        title: title,
        text: text,
        icon: icon,
        confirmButtonText: 'Aceptar',
        ...(icon === 'warning' && {
            showCancelButton: true,
            cancelButtonText: 'Cancelar'
        }),
        confirmButtonColor: '#ffffff71',
        background: 'rgb(43, 43, 43)',      
        color: '#ffffff',              
        customClass: {
            confirmButton: 'submit-btn',
            popup: 'block'
        } 
});
}