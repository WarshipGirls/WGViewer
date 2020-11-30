# WGR API

This module holds Warship Girls (R) APIs.

- Most of these APIs are collected manually using Fiddler
- Some APIs are collected from a very early auto tool, protector-moe
- Not every API is tested at this point

## Documentation guideline

For maintenance purpose, please ensure following when making changes:

- Make modifications of functions according to their URL prefix (e.g. `boat/repair` is put under `boat.py`)
    - API that is used only one time or is rarely used may be put under `api.py`
- Name functions according to the URL
- Order functions alphabetically
- Define argument type
    - To avoid redundant type cast at URL concatenation, force all `int` inputs to `str`
- Provide necessary comment if the function name is not intuitive enough
- Provide necessary example if the function is not intuitive enough
- When writing URL,
    - please follow existing format:
        - `"boat/repair/" + ship_id + '/0/'`
    - hence, NO:
        - `"f{arg_name}"` 
        - `"{}/{}".format(arg_1, arg_2)"`