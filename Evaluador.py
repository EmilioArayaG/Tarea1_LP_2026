import re

digito = r"[0-9]"
letra_min = r"[a-z]"
letra_may = r"[A-Z]"
letra = rf"(?:{letra_min}|{letra_may})"
palabra = rf"{letra}(?:{letra}|{digito})*"

operacion = r"(?:\+|-|/|\*|==|=|<|>)"
booleano = r"(?:true|false)"
cadena_texto = rf'"{palabra}"'
caracter = rf"'{letra}'"
valor = rf"(?:{digito}+|{booleano}|{cadena_texto}|{caracter})"
tipo_dato = r"(?:int|bool|char|string|void)"

snake_case = rf"{letra_min}+(?:_{letra_min}+)*"
camelCase = rf"{letra_min}+(?:{letra_may}+{letra_min}+)+"
PascalCase = rf"(?:{letra_may}+{letra_min}*)+"
nombre_valido = rf"(?:{snake_case}|{camelCase}|{PascalCase})"

condicion = rf"(?:\(\s*{nombre_valido}\s*{operacion}\s*{valor}\))"
estructura_control = rf"(?:(?:if|while)\s*{condicion}\s*\{{)"
cierre_bloque = r"\}"
declaracion_funcion = rf"(?:{tipo_dato}\s+{nombre_valido}\s*\(\s*\)\{{)"
declaracion_variable = rf"(?:{tipo_dato}\s+{nombre_valido}\s*{operacion}\s*{valor}\s*;)"
