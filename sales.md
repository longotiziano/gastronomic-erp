# Apartado de Ventas

## Secciones

### Carga de Informe de MaxiRest
Se podrá utilizar el informe de ventas del MaxiRest para subir los productos y la cantidad vendida.

Antes de la carga se muestra un mensaje de confirmación con la cantidad de registros a cargar. En caso de que se encuentren productos que no están en la base de datos, se le propondrá al usuario crearlos, aproximando el precio como `importe / unidad` hacia los 1000 más cercanos (ej. 14560 -> 15000). El usuario deberá seleccionar la categoría manualmente para cada producto nuevo antes de confirmar.

Finalmente, se le mostrará al usuario todos los registros propuestos, donde podrá modificar o eliminar antes de aceptar su creación.