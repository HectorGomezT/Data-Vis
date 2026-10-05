# Configurar las entregas de tareas (Google Drive + Sheets)

La página **"Entrega tu tarea"** del sitio manda cada archivo a un pequeño programa de Google Apps Script que corre con
**tu** cuenta: guarda el archivo en una carpeta de tu Drive y anota la entrega en un Google Sheet. Solo tú ves las
entregas. Se configura una sola vez (~10 minutos).

## 1. Crea la carpeta y el Sheet
1. En Google Drive, crea una carpeta, por ejemplo **"Tareas Data Viz"**. Ábrela y copia su **ID**: es la parte final de
   la URL, después de `/folders/`.
2. Crea un Google Sheet vacío, por ejemplo **"Entregas Data Viz"**, y copia su **ID**: la parte de la URL entre `/d/` y
   `/edit`.

## 2. Crea el Apps Script
1. Entra a https://script.google.com → **New project**. Ponle nombre, por ejemplo "Receptor de tareas".
2. Borra el contenido de `Code.gs` y pega el de [`apps_script/Code.gs`](../apps_script/Code.gs).
3. Si tu grupo no está en el horario de Ciudad de México, cambia `ZONA` en la línea 16.
4. Ve a **Project Settings** (el engrane) → **Script properties** → agrega tres propiedades:

| Property | Value |
|---|---|
| `TOKEN` | una contraseña larga inventada por ti, por ejemplo 30 letras y números al azar |
| `FOLDER_ID` | el ID de la carpeta del paso 1 |
| `SHEET_ID` | el ID del Sheet del paso 1 |

## 3. Publícalo como web app
1. Arriba a la derecha: **Deploy → New deployment** → tipo **Web app**.
2. **Execute as: Me** · **Who has access: Anyone**. Así los alumnos no necesitan cuenta de Google; el token protege el acceso.
3. **Deploy**. Google te pedirá autorizar el acceso a Drive y Sheets: acepta. Si aparece "Google hasn't verified this
   app", entra en *Advanced → Go to … (unsafe)*: la app es tuya.
4. Copia la **Web app URL** (termina en `/exec`).

## 4. Conéctalo con el sitio
En https://share.streamlit.io → tu app → **⋮ → Settings → Secrets**, pega y guarda:

```toml
[entregas]
url = "https://script.google.com/macros/s/TU_ID/exec"
token = "LA_MISMA_CONTRASEÑA_DEL_PASO_2"
```

La app se reinicia sola. La página **Tarea → Entrega tu tarea** ya mostrará el formulario. Mientras no haya secrets,
muestra "Las entregas aún no están abiertas".

Para probar en tu computadora, pon lo mismo en `.streamlit/secrets.toml`. Está en `.gitignore`, nunca se sube al repo.

## 5. Prueba
Haz una entrega con cualquier imagen. Debe aparecer el archivo en la carpeta y una fila en el Sheet.

## Ajustes
- **Instrucciones y fecha límite:** edita `INSTRUCCIONES` y `FECHA_LIMITE` al inicio de `app/views/tarea.py`.
- **Cerrar las entregas:** borra los secrets en Streamlit Cloud, o cambia el `TOKEN` en el Apps Script.
- **Si cambias el código del Apps Script:** Deploy → Manage deployments → editar → *New version*, para que la URL no cambie.
