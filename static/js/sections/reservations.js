function elegirMesa(elemento) {
    var idReal = elemento.getAttribute('data-id');
    document.getElementById('table_id').value = idReal; 
    document.getElementById('table_display').value = "Mesa N° " + idReal;

    document.querySelector('.fixed-block').scrollIntoView({ behavior: 'smooth' });
}