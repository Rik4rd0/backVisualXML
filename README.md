# 🧾 XML Validator & Comment Enricher API

Este proyecto es una **API REST construida con Flask** que permite validar archivos XML contra un esquema XSD, extraer su información estructurada y enriquecerla con comentarios embebidos en un archivo SQL. También sirve una aplicación frontend estática y archivos de imagen.

---

## 📌 Objetivo

- Validar archivos XML con un esquema XSD.
- Parsear metadatos y bloques de contenido del XML.
- Extraer comentarios adicionales desde un archivo `.sql` que contiene fragmentos XML.
- Asociar los comentarios a los bloques del XML por `GUID`.
- Exponer toda la información estructurada mediante una API REST.
- Servir una aplicación frontend (SPA) y archivos estáticos.

---

## ⚙️ Funcionalidades

- ✅ **Validación de XML** usando `lxml` y un archivo XSD.
- 📄 **Extracción de datos** de nodos como `documentMetadata`, `block`, y `formatUnit`.
- 💬 **Enriquecimiento con comentarios** embebidos como XML en archivos `.sql`.
- 🔗 **Asociación inteligente** de comentarios a bloques por medio de su `GUID`.
- 📦 **API REST disponible** en `/api/data`.
- 🖼️ **Servidor de archivos estáticos** e imágenes.

---

## 🗂️ Estructura esperada

