# Guía para demostrar el proyecto en clase

1. Abrir la carpeta completa en VS Code y mostrar el árbol de archivos.
2. Abrir `data/raw/` y preguntar qué problemas observan en clientes y ventas.
3. Abrir `src/pipeline.py` y explicar cada función: extraer, limpiar, transformar, integrar, validar y guardar.
4. Abrir `main.py` y explicar por qué una función principal coordina el flujo.
5. Mostrar `requirements.txt`, `.gitignore` y `README.md`.
6. Crear entorno virtual, instalar dependencias y ejecutar `python main.py`.
7. Abrir `outputs/ventas_consolidadas.csv` y `outputs/reporte_calidad.json`.
8. Ejecutar `python -m unittest discover -s tests -v`.
9. Simular un fallo: cambiar temporalmente el nombre de `clientes.csv`, ejecutar y leer el mensaje. Restaurar el archivo.
10. Simular una regla de calidad: cambiar temporalmente `validate="many_to_one"` por otra opción y discutir por qué la cardinalidad importa. Restaurar el código.
11. Explicar cómo registrar el primer commit y subir a GitHub sin incluir secretos.

**Preguntas al grupo:** ¿Por qué no eliminamos la venta del cliente 999? ¿Por qué no sobrescribimos el total reportado? ¿Cómo sabemos que el merge no multiplicó filas? ¿Cómo ejecutaría esto otro equipo sin ayuda?


## Demostración completa de las tres capas de datos
1. Abrir `data/raw/clientes.csv`: mostrar el duplicado y las ciudades con distinta escritura.
2. Ejecutar `python main.py` desde la terminal de VS Code.
3. Abrir `data/processed/clientes_limpios.csv`: comprobar que quedan tres clientes y ciudades normalizadas.
4. Abrir `data/processed/ventas_transformadas.csv`: mostrar `fecha_parseada`, `total_esperado`, `diferencia` y `total_correcto`.
5. Abrir `outputs/ventas_consolidadas.csv`: mostrar el `merge` y el cliente 999 sin correspondencia.
6. Abrir `outputs/reporte_calidad.json`: explicar los indicadores.
7. Ejecutar `python -m unittest discover -s tests -v`.

**Pregunta de reflexión:** ¿Por qué guardar los datos intermedios ayuda a identificar en qué etapa ocurrió un error?
