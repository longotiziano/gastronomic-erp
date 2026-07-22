# Database models

## Special attributes
Created for code's abstraction

### Table's rendering
- ui-config: dict = {title, form_template, table_cols (displayed in screen)}

### Miscellaneous
- filterable_fields: list = Fields that can be selected to sort or filter records.

### Info 
- min_value: int
- title: bool = How the string record is stored in the database.
- 

## Special methods
- self.to_table_row() -> list = Returns a row of the rendered table