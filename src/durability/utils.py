from string.templatelib import Template, Interpolation

def useVar(template: Template, newValue: str) -> Template:
    parts = []
    for item in template:
        if isinstance(item, Interpolation):
            parts.append(Interpolation(newValue, item.expression, item.conversion, item.format_spec))
        else:
            parts.append(item)

    return Template(*parts)

def toStr(template: Template) -> str:
    result = []
    for i, segment in enumerate(template.strings):
        result.append(segment)
        if i < len(template.values):
            result.append(str(template.values[i]))

    return "".join(result)