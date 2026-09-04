# Ejercicio 1 — Cambiar la imagen de predicción en YOLO

## Contexto

La notebook `Visión computacional/Notebooks/13 YOLO ultralytics.ipynb` es un
tutorial corto de **YOLOv8** (paquete Ultralytics) pensado para **Google
Colab**. Hace tres cosas:

1. Instala `ultralytics` y comprueba el entorno.
2. Corre inferencia por CLI sobre la foto de muestra `zidane.jpg`.
3. Carga `yolov8n.pt`, entrena **3 épocas** en `coco128` y predice
   `bus.jpg`.

YOLO detecta objetos de las clases **COCO** (persona, auto, bus, corbata,
etc.) y dibuja cajas. En este ejercicio **sí vas a modificar código**, pero
solo un cambio pequeño y visible: **la imagen sobre la que predice**.

No toques `Visión computacional/project/`. Trabajas en **Colab**, sobre una
**copia** de la notebook.

## Objetivo

Correr la notebook en Colab **tal como está**, sustituir las dos imágenes de
muestra por **una imagen tuya** (la misma en ambas predicciones) y comparar
qué objetos detecta YOLO en la foto original frente a la tuya.

## Archivos a crear / modificar

No modifiques la notebook original del repositorio.

1. Sube a Colab una **copia** de `13 YOLO ultralytics.ipynb`
   (`Archivo` → `Subir notebook`) o ábrela desde Drive / GitHub.
2. En esa copia deja evidencia de la corrida **original** y de la
   **modificada** (puedes duplicar las celdas de predicción).

## Requisitos

1. Ejecuta **primero** la notebook **sin cambiar** `zidane.jpg` ni
   `bus.jpg`. Guarda las imágenes de salida (cajas y etiquetas).
2. El cambio pedido es **uno solo**: reemplaza ambas fuentes de predicción
   por **la misma imagen tuya**.

   - Celda CLI: el argumento `source=...` de
     `!yolo predict model=yolov8n.pt source='...'`.
   - Celda Python: el argumento de
     `model('...', save=True)`.

   La imagen puede ser:

   - un archivo que subas a Colab (p. ej. `mi_foto.jpg` en el panel de
     archivos), o
   - una **URL pública** a un `.jpg` / `.png`.

   Debe verse **al menos un objeto** que COCO sepa nombrar (persona, perro,
   silla, auto, taza, laptop, etc.). No uses un recorte abstracto ni un
   logo sin objetos.
3. **No** cambies el modelo (`yolov8n.pt`), las épocas (`epochs=3`) ni el
   dataset de entrenamiento (`coco128.yaml`). Si cambias varias cosas a la
   vez, no se ve qué provocó la diferencia.
4. El entrenamiento de 3 épocas **sí debe correr** (forma parte de la
   notebook). En Colab usa **Runtime → Change runtime type → GPU** (T4)
   para que no tarde de más.

## Pasos sugeridos

1. Abre [Google Colab](https://colab.research.google.com/) y carga la
   copia de la notebook.

2. Elige GPU y ejecuta **Runtime → Run all**. Anota:
   - las clases que aparecen sobre **Zidane** y sobre el **bus**;
   - cuántas cajas hay (aprox.) en cada foto;
   - la carpeta de resultados que imprime Ultralytics
     (suele ser `runs/detect/predict` y `runs/detect/train`).

3. Sube tu imagen (icono de carpeta → *Upload*) o ten lista la URL.

4. Duplica las celdas de predicción (o edítalas después de guardar
   capturas) y apunta `source` / `model(...)` a tu archivo o URL. Ejemplo
   si subiste el archivo a Colab:

   ```python
   !yolo predict model=yolov8n.pt source='mi_foto.jpg'
   ```

   ```python
   model('mi_foto.jpg', save=True)
   ```

5. Vuelve a correr **solo** esas celdas. Abre las imágenes guardadas en
   `runs/detect/` y compara con las de Zidane y el bus.

## Criterios de aceptación

- La notebook original corrió en **Colab** (no solo en tu máquina).
- El único cambio de código es la **fuente de la imagen** en las dos
  predicciones; el modelo sigue siendo `yolov8n.pt`.
- Tu imagen no es `zidane.jpg` ni `bus.jpg`.
- Hay capturas de las predicciones **originales** y de la **tuya**, con
  cajas visibles.
- El reporte nombra clases concretas (no basta “detectó cosas”).

## Entrega

1. Enlace de Colab (o el `.ipynb` modificado) con la corrida original y la
   predicción sobre tu imagen.
2. Capturas: salida sobre `zidane.jpg`, sobre `bus.jpg` y sobre **tu**
   foto.
3. Un breve reporte (media página) que responda:
   - ¿Qué clases detectó YOLO en las fotos de Ultralytics y cuáles en la
     tuya?
   - ¿Algún objeto evidente de tu foto **no** salió etiquetado? ¿Por qué
     podría pasar (clase que no está en COCO, objeto chico, recorte,
     umbral de confianza)?
   - ¿La predicción de la celda CLI y la de `model(...)` coinciden sobre
     tu misma imagen?
4. Evidencia de haber ejecutado en Colab (captura del entorno o del menú
   Runtime, idealmente con GPU).

## Reto opcional

- En la misma imagen tuya, corre otra vez el CLI con umbral más estricto:

  ```python
  !yolo predict model=yolov8n.pt source='mi_foto.jpg' conf=0.7
  ```

  Compara con el default (`conf=0.25`): ¿desaparecen cajas? ¿Cuáles?
- Cambia **solo** el modelo de la predicción CLI a `yolov8s.pt` (sin
  reentrenar) y mira si aparecen objetos que `yolov8n` se saltó.
- Prueba un video corto (`source='mi_video.mp4'`): YOLO procesa frame a
  frame; describe una escena en la que falle.

## Pistas

- Las salidas se guardan bajo `runs/detect/`. Cada corrida nueva suele
  crear `predict`, `predict2`, `train`, `train2`, … Abre el `.jpg` de
  ahí; no te quedes solo con el texto del log.
- COCO **no** tiene cualquier clase: una *torta*, un *cebolín* o un
  *escudo de un equipo* pueden no tener etiqueta aunque se vean claro.
- Si `source` es un path, el archivo tiene que estar en el directorio de
  trabajo de Colab (`/content/` por defecto). Si es URL, tiene que ser
  directa al archivo, no una página HTML.
- Si el runtime se desconecta, vuelve a correr la celda `%pip install
  ultralytics` antes de predecir.
- No hace falta entender el entrenamiento en `coco128` para este
  ejercicio: es un fine-tune corto de demostración. El cambio pedido es
  solo **qué foto** le pasas a YOLO ya entrenado.
