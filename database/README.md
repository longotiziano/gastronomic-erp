# Database models

## DimensionalMixin
All dimensional tables have both `id` and `name` fields. If a different label is used to name the column, the web page rendering may fail. This is the reason for the `DimensionalMixin` class.

## Special attributes
Created for code abstraction.

### Table rendering
- `ui_config: dict` = {
    `title`, -> str, the page/section title displayed in the UI (e.g. "Categorías")
    `form_template`, -> str, path to the form template used for create/edit
    `table_cols` -> list[str], column headers displayed on screen
}

### Miscellaneous
- `filterable_fields: list` = Fields that can be selected to sort or filter records.
  > Note: as of the new filter system, filterable fields are detected automatically from columns that declare `filter_type` in their `info`. This list may become redundant — confirm whether it's still read anywhere before removing it.
- `entity_name: str` = How the record is named in error messages (e.g. "materia prima").

### Column `info` dict
- `title: bool` = Whether the string value gets normalized/title-cased on save (e.g. "juan perez" -> "Juan Perez"). Not related to `ui_config.title`.
- `label: str` = Display name for the field in forms and filters (e.g. "Unidad de Medida").
- `min_value: int` / `max_value: int` = Numeric bounds enforced during validation.
- `filter_type: enum` = [
    `'select'`, -> selectable with the column's Enum options
    `'select_fk'`, -> selectable with the related dimensional table's `name` field
    `'search'`, -> free-text search
    `'bool'` -> selectable Sí/No (Activo/Inactivo)
]

## Special methods
- `to_table_row(self) -> list` = Returns a row of the rendered table.