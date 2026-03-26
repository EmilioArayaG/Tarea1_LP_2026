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

snake_case = rf"{letra_min}+(?:_{letra_min}+)+"
camelCase = rf"{letra_min}+(?:{letra_may}+{letra_min}+)+"
PascalCase = rf"(?:{letra_may}+{letra_min}*)+"
nombre_valido = rf"(?:{snake_case}|{camelCase}|{PascalCase})"

nombre_generico = rf"(?:{letra}|{digito}|_)+"

condicion = rf"(?:\(\s*{nombre_valido}\s*{operacion}\s*{valor}\s*\))"
estructura_control = rf"(?:(?:if|while)\s+{condicion}\s*\{{)"
cierre_bloque = r"\}"
declaracion_funcion = rf"(?:{tipo_dato})\s+({nombre_valido})\s*\("
declaracion_variable = rf"(?:{tipo_dato})\s+({nombre_valido})\s*(?:{operacion})\s*(?:{valor})\s*;"
retorno = rf"(?:\s*return\s+{nombre_valido}\s*;)"
comentario_one_line = rf"//\s*{palabra}"
comentario_multi_line = rf"/\*\s*{palabra}\s*\*/"

detec_func = rf"(?:{tipo_dato})\s+({nombre_generico})\s*\("
var_sin_pc = rf"^(?:{tipo_dato})\s+({nombre_valido})\s*(?:{operacion})\s*(?:{valor})\s*$"
retr_sin_pc = rf"^\s*return\s+(?:{nombre_valido})\s*$"

detec_var = rf"(?:{tipo_dato})\s+({nombre_generico})\s*(?:{operacion})\s*(?:{valor})\s*;"
var_sinpc = rf"^(?:{tipo_dato})\s+({nombre_generico})\s*(?:{operacion})\s*(?:{valor})\s*$"
retorno_sinpc = rf"^\s*return\s+(?:{nombre_generico})\s*$"
patron_ec = r"^\s*(?:if|while)(?:\s|\()"

def determinar_autor(nombre_funcion):
    '''
    ***
    Parametro 1: str
    ***
    Retorno: str
    ***
    Esta funcion recibe el nombre de una funcion detectado y retorna su autor
    '''
    if re.fullmatch(snake_case, nombre_funcion):
        return "snake"
    elif re.fullmatch(camelCase, nombre_funcion):
        return "camel"
    elif re.fullmatch(PascalCase, nombre_funcion):
        return "pascal"
    else:
        return "desconocido"

def incializar_archivos():
    '''
    ***
    Parametro 1: None
    ***
    Retorno: dict
    ***
    Esta funcion crea los archivos de salida y crea tambien el diccionario de estadisticas que sera impreso en la terminal
    '''
    archivos_salida = ['snake.txt', 'camel.txt', 'pascal.txt', 'desconocido.txt']
    for archivo in archivos_salida:
        with open(archivo, 'w', encoding='utf-8') as f:
            pass
    estadisticas = {
        "snake": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "camel": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "pascal": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []},
        "desconocido": {"funciones": [], "total_variables": 0, "errores_estilo": [], "errores_sintaxis": []}
    }
    return estadisticas

def escribir_bloque(contexto_actual, bloque_actual):
    '''
    ***
    Parametro 1: str
    Parametro 2: list
    ***
    Retorno: None
    ***
    Esta funcion abre el archivo del autor que le corresponda y escribe en este el bloque actual
    '''
    with open(f'{contexto_actual}.txt', 'a', encoding='utf-8') as f:
        f.writelines(bloque_actual)
        f.write('\n')

def evaluar_linea_interna(linea_limpia, contexto_actual, estadisticas):
    '''
    ***
    Parametro 1: str
    Parametro 2: str
    Parametro 3: dict
    ***
    Retorno: None
    ***
    Esta funcion se encarga de extraer toda la informacion necesaria de la linea que se le entrega, nombres de funciones, variables, errores de sintaxis y mas.
    Va almacenando toda la informacion en las estadisticas. 
    '''
    funcion_act = estadisticas[contexto_actual]["funciones"][-1]

    m_estricto = re.match(declaracion_variable, linea_limpia)
    m_broad = re.match(detec_var, linea_limpia)
    m_rota = re.match(var_sin_pc, linea_limpia)
    m_rota_broad = re.match(var_sinpc, linea_limpia)

    if m_estricto:
        nombre_var = m_estricto.group(1)
        estadisticas[contexto_actual]["total_variables"] += 1
        estilo_var = determinar_autor(nombre_var).lower()
        if estilo_var != contexto_actual:
            if contexto_actual == "snake": estilo_imp = "snake_case"
            elif contexto_actual == "camel": estilo_imp = "camelCase"
            elif contexto_actual == "pascal": estilo_imp = "PascalCase"
            else: estilo_imp = "desconocido"
            mensj_err = f"La variable '{nombre_var}' no es {estilo_imp}"
            estadisticas[contexto_actual]["errores_estilo"].append(mensj_err)

    elif m_broad and contexto_actual != "desconocido":
        nombre_var = m_broad.group(1)
        estadisticas[contexto_actual]["total_variables"] += 1
        if contexto_actual == "snake": estilo_imp = "snake_case"
        elif contexto_actual == "camel": estilo_imp = "camelCase"
        elif contexto_actual == "pascal": estilo_imp = "PascalCase"
        mensj_err = f"La variable '{nombre_var}' no es {estilo_imp}"
        estadisticas[contexto_actual]["errores_estilo"].append(mensj_err)

    elif m_broad:
        estadisticas[contexto_actual]["total_variables"] += 1

    elif m_rota:
        nombre_var = m_rota.group(1)
        estadisticas[contexto_actual]["total_variables"] += 1
        estilo_var = determinar_autor(nombre_var).lower()
        if estilo_var != contexto_actual:
            if contexto_actual == "snake": estilo_imp = "snake_case"
            elif contexto_actual == "camel": estilo_imp = "camelCase"
            elif contexto_actual == "pascal": estilo_imp = "PascalCase"
            else: estilo_imp = "desconocido"
            mensj_est = f"La variable '{nombre_var}' no es {estilo_imp}"
            estadisticas[contexto_actual]["errores_estilo"].append(mensj_est)
        mensj_err = f"Error en '{funcion_act}': Falta ';' en la línea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensj_err)

    elif m_rota_broad and contexto_actual != "desconocido":
        nombre_var = m_rota_broad.group(1)
        estadisticas[contexto_actual]["total_variables"] += 1
        if contexto_actual == "snake": estilo_imp = "snake_case"
        elif contexto_actual == "camel": estilo_imp = "camelCase"
        elif contexto_actual == "pascal": estilo_imp = "PascalCase"
        mensj_est = f"La variable '{nombre_var}' no es {estilo_imp}"
        estadisticas[contexto_actual]["errores_estilo"].append(mensj_est)
        mensj_err = f"Error en '{funcion_act}': Falta ';' en la línea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensj_err)

    elif m_rota_broad:
        estadisticas[contexto_actual]["total_variables"] += 1
        mensj_err = f"Error en '{funcion_act}': Falta ';' en la línea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensj_err)

    elif re.match(retorno, linea_limpia):
        pass
    
    elif re.match(retr_sin_pc, linea_limpia):
        mensj_err = f"Error en '{funcion_act}': Falta ';' en la línea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensj_err)

    elif re.match(retorno_sinpc, linea_limpia):
        mensj_err = f"Error en '{funcion_act}': Falta ';' en la línea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensj_err)
        
    elif re.match(estructura_control, linea_limpia):
        pass

    elif re.match(patron_ec, linea_limpia):
        mensj_err = f"Error en '{funcion_act}': Estructura de control mal formada en la línea '{linea_limpia}'"
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensj_err)

def procesar_archivo():
    '''
    ***
    Parametro : None
    ***
    Retorno: None
    ***
    Lee y procesa programa.txt linea por linea
    '''
    estadisticas = incializar_archivos()
    contexto_actual = None
    bloque_actual = []
    contador_llaves = 0

    with open('programa.txt', 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea_limpia = linea.strip()

            if not linea_limpia:
                continue

            linea_limpia = re.sub(comentario_one_line, '', linea_limpia).strip()
            linea_limpia = re.sub(comentario_multi_line, '', linea_limpia).strip()
            
            if not linea_limpia:
                continue

            match_funcion = re.match(declaracion_funcion, linea_limpia)
            if not match_funcion:
                match_funcion = re.match(detec_func, linea_limpia)
            
            if match_funcion:
                if contexto_actual is not None and contador_llaves > 0:
                    funcion_anterior = estadisticas[contexto_actual]["funciones"][-1]
                    mensaje = f"Error en '{funcion_anterior}': Bloque sin cerrar. Faltan {contador_llaves} llaves '}}' de cierre."
                    estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje)
                    escribir_bloque(contexto_actual, bloque_actual)

                nombre = match_funcion.group(1)
                contexto_actual = determinar_autor(nombre).lower()
                estadisticas[contexto_actual]["funciones"].append(nombre)

                bloque_actual = [linea]
                
                linea_sin_strings = re.sub(r'"[^"]*"', '""', linea_limpia)
                contador_llaves = linea_sin_strings.count('{') - linea_sin_strings.count('}')

            elif contexto_actual:
                bloque_actual.append(linea)
                evaluar_linea_interna(linea_limpia, contexto_actual, estadisticas)
                
                linea_sin_strings = re.sub(r'"[^"]*"', '""', linea_limpia)
                contador_llaves += linea_sin_strings.count('{') - linea_sin_strings.count('}')

                if contador_llaves == 0:
                    escribir_bloque(contexto_actual, bloque_actual)
                    bloque_actual = []
                    contexto_actual = None

    if contexto_actual is not None and contador_llaves > 0:
        funcion_anterior = estadisticas[contexto_actual]["funciones"][-1]
        mensaje = f"Error en '{funcion_anterior}': Bloque sin cerrar. Faltan {contador_llaves} llaves '}}' de cierre."
        estadisticas[contexto_actual]["errores_sintaxis"].append(mensaje)
        escribir_bloque(contexto_actual, bloque_actual)

    imprimir_reporte(estadisticas)

def imprimir_reporte(estadisticas):
    '''
    ***
    Parametro 1: dict
    ***
    Retorno: None
    ***
    Imprime el reporte final con estadisticas
    '''
    print("\n=== REPORTE DE EVALUACIÓN DE PRACTICANTES ===")
    orden_autores = ["snake", "camel", "pascal", "desconocido"]
    for autor in orden_autores:
        datos = estadisticas[autor]
        if len(datos["funciones"]) > 0:
            print(f"\nPRACTICANTE: {autor.capitalize()}")
            cant_funciones = len(datos["funciones"])
            nombres_funciones = ", ".join(datos["funciones"])
            print(f"Funciones creadas: {cant_funciones} ({nombres_funciones})")
            print(f"Variables declaradas: {datos['total_variables']}")

            cant_estilos = len(datos["errores_estilo"])
            if cant_estilos > 0:
                errores_str = ", ".join(datos["errores_estilo"])
                print(f"Diferencias de Estilo: {cant_estilos} ({errores_str})")
            else:
                print(f"Diferencias de Estilo: {cant_estilos}")
            
            cant_sintaxis = len(datos["errores_sintaxis"])
            print(f"Errores de Sintaxis: {cant_sintaxis}")

            for error in datos["errores_sintaxis"]:
                print(f"- {error}")

procesar_archivo()
