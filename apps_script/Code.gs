/**
 * Receptor de tareas para el sitio "Béisbol sin fronteras".
 *
 * Guarda cada archivo en una carpeta de tu Google Drive y agrega una fila a un Google Sheet.
 * Configura en "Project Settings → Script properties":
 *   TOKEN      el mismo valor que pones en los secrets de Streamlit
 *   FOLDER_ID  el ID de la carpeta de Drive donde se guardan las tareas
 *   SHEET_ID   el ID del Google Sheet donde se registran las entregas
 *
 * Despliega como "Web app" → Execute as: Me · Who has access: Anyone.
 * Instrucciones completas: docs/entregas_setup.md
 */

const TIPOS_OK = ['image/png', 'image/jpeg', 'application/pdf'];
const MAX_BYTES = 10 * 1024 * 1024;
const ZONA = 'America/Mexico_City';

function doPost(e) {
  const props = PropertiesService.getScriptProperties();
  let datos;
  try {
    datos = JSON.parse(e.postData.contents);
  } catch (err) {
    return responder({ ok: false, error: 'Solicitud inválida.' });
  }
  if (!datos.token || datos.token !== props.getProperty('TOKEN')) {
    return responder({ ok: false, error: 'No autorizado.' });
  }
  if (TIPOS_OK.indexOf(datos.mimetype) === -1) {
    return responder({ ok: false, error: 'El archivo debe ser PNG, JPG o PDF.' });
  }

  const bytes = Utilities.base64Decode(datos.data);
  if (bytes.length > MAX_BYTES) {
    return responder({ ok: false, error: 'El archivo supera los 10 MB.' });
  }

  const lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    const ahora = new Date();
    const sello = Utilities.formatDate(ahora, ZONA, 'yyyy-MM-dd HHmm');
    const nombre = String(datos.nombre || '').trim().slice(0, 80);
    const correo = String(datos.correo || '').trim().slice(0, 120);
    const original = String(datos.filename || 'tarea').replace(/[\\/]/g, '_');

    const blob = Utilities.newBlob(bytes, datos.mimetype, sello + ' · ' + nombre + ' · ' + original);
    const archivo = DriveApp.getFolderById(props.getProperty('FOLDER_ID')).createFile(blob);

    const hoja = SpreadsheetApp.openById(props.getProperty('SHEET_ID')).getSheets()[0];
    if (hoja.getLastRow() === 0) {
      hoja.appendRow(['Fecha', 'Nombre', 'Correo', 'Archivo', 'Link en Drive', 'Tamaño (KB)']);
    }
    hoja.appendRow([ahora, nombre, correo, archivo.getName(), archivo.getUrl(), Math.round(bytes.length / 1024)]);

    return responder({ ok: true, hora: Utilities.formatDate(ahora, ZONA, 'HH:mm') });
  } catch (err) {
    return responder({ ok: false, error: 'No pudimos guardar tu archivo. Avísale a tu profesor.' });
  } finally {
    lock.releaseLock();
  }
}

function responder(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
