# Guía de Despliegue como Servicio Systemd

Esta guía documenta los pasos para exponer una aplicación FastHTML como servicio del sistema usando systemd.

## 📋 Requisitos Previos

- Python 3.10+
- Aplicación FastHTML funcional
- Acceso root o sudo
- Virtual environment configurado

## 🔧 Pasos de Configuración

### 1. Preparar el Entorno Virtual

```bash
cd /home/server-paulo/Software/my-calendar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```bash
nano .env
```

Contenido del `.env`:
```env
HOST=0.0.0.0
PORT=5015
PABLO_PASSWORD=***REMOVED***
EVA_PASSWORD=***REMOVED***
```

**Nota:** `HOST=0.0.0.0` permite acceder desde:
- Localhost: `http://localhost:5015`
- Red local: `http://192.168.1.145:5015` (usar tu IP real)
- Túnel Cloudflare (si está configurado)

### 3. Modificar main.py para Soportar Variables de Entorno

Asegurar que `main.py` lee las variables del `.env`:

```python
import os

from fasthtml.common import serve

from app import app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5001"))
    host = os.environ.get("HOST", "0.0.0.0")
    serve(host=host, port=port)
```

### 4. Crear el Archivo de Servicio Systemd

```bash
sudo nano /etc/systemd/system/mycalendar.service
```

Contenido del servicio:

```ini
[Unit]
Description=My-calendar FastHTML service
After=network-online.target
Wants=network-online.target

[Service]
# Usuario que ejecuta la app
User=server-paulo
Group=server-paulo

# Directorio del proyecto
WorkingDirectory=/home/server-paulo/Software/my-calendar

# Carga de variables de entorno desde .env
EnvironmentFile=/home/server-paulo/Software/my-calendar/.env

# Ejecutar el main.py usando el Python del venv
ExecStart=/home/server-paulo/Software/my-calendar/.venv/bin/python main.py

# Política de reinicio
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Importante:** Ajustar las rutas según tu configuración:
- `User` y `Group`: tu usuario del sistema
- `WorkingDirectory`: ruta completa al proyecto
- `EnvironmentFile`: ruta al archivo `.env`
- `ExecStart`: ruta al Python del venv + script principal

### 5. Configurar el Firewall

Abrir el puerto en UFW:

```bash
# Ver estado actual
sudo ufw status

# Abrir puerto de la aplicación
sudo ufw allow 5015/tcp

# Verificar
sudo ufw status | grep 5015
```

### 6. Activar y Arrancar el Servicio

```bash
# Recargar configuración de systemd
sudo systemctl daemon-reload

# Habilitar arranque automático en boot
sudo systemctl enable mycalendar.service

# Iniciar el servicio
sudo systemctl start mycalendar.service

# Verificar estado
sudo systemctl status mycalendar.service
```

### 7. Verificar que Funciona

```bash
# Ver que el puerto está escuchando
sudo ss -tulpn | grep 5015

# Obtener IP de red local
ip addr show | grep "inet.*192.168"

# Probar localmente
curl -L http://localhost:5015/login

# Probar desde la red local (usar tu IP)
curl -L http://192.168.1.145:5015/login
```

## 📊 Comandos Útiles de Gestión

### Ver logs en tiempo real
```bash
sudo journalctl -u mycalendar.service -f
```

### Ver últimas 50 líneas de log
```bash
sudo journalctl -u mycalendar.service -n 50
```

### Reiniciar el servicio
```bash
sudo systemctl restart mycalendar.service
```

### Detener el servicio
```bash
sudo systemctl stop mycalendar.service
```

### Deshabilitar arranque automático
```bash
sudo systemctl disable mycalendar.service
```

### Ver estado del servicio
```bash
sudo systemctl status mycalendar.service
```

## 🔍 Resolución de Problemas

### Error 203/EXEC
**Causa:** Ruta incorrecta al ejecutable de Python o permisos.

**Solución:**
```bash
# Verificar que existe el Python del venv
ls -la /home/server-paulo/Software/my-calendar/.venv/bin/python

# Verificar permisos del .env
ls -la /home/server-paulo/Software/my-calendar/.env
sudo chown server-paulo:server-paulo /home/server-paulo/Software/my-calendar/.env
```

### ModuleNotFoundError: No module named 'fasthtml'
**Causa:** FastHTML no instalado en el venv.

**Solución:**
```bash
/home/server-paulo/Software/my-calendar/.venv/bin/pip install fasthtml
```

### No conecta desde red local
**Causa:** 
1. Firewall bloqueando el puerto
2. HOST configurado en IP específica en lugar de `0.0.0.0`

**Solución:**
```bash
# 1. Verificar firewall
sudo ufw status
sudo ufw allow 5015/tcp

# 2. Verificar HOST en .env
cat /home/server-paulo/Software/my-calendar/.env
# Debe ser: HOST=0.0.0.0

# 3. Reiniciar servicio
sudo systemctl restart mycalendar.service

# 4. Verificar que escucha en todas las interfaces
sudo ss -tulpn | grep 5015
# Debe mostrar: 0.0.0.0:5015
```

### El servicio se reinicia constantemente
**Causa:** Error en la aplicación.

**Solución:**
```bash
# Ver logs detallados
sudo journalctl -u mycalendar.service -n 100

# Probar ejecutar manualmente
cd /home/server-paulo/Software/my-calendar
source .venv/bin/activate
python main.py
```

## 🌐 Acceso desde Diferentes Ubicaciones

### Desde el propio servidor
```
http://localhost:5015
http://127.0.0.1:5015
```

### Desde la red local (LAN)
```
http://192.168.1.145:5015
```
*(Usar la IP real del servidor)*

### Desde Internet (con Cloudflare Tunnel)
Configurar en Cloudflare una ruta apuntando a:
```
http://localhost:5015
```

## 📝 Modificar Configuración

### Cambiar puerto o host
1. Editar `.env`:
   ```bash
   nano /home/server-paulo/Software/my-calendar/.env
   ```

2. Reiniciar servicio:
   ```bash
   sudo systemctl restart mycalendar.service
   ```

3. Actualizar firewall si cambió el puerto:
   ```bash
   sudo ufw allow <NUEVO_PUERTO>/tcp
   sudo ufw delete allow 5015/tcp  # Borrar regla antigua si ya no se usa
   ```

### Cambiar usuario o rutas
1. Editar servicio:
   ```bash
   sudo nano /etc/systemd/system/mycalendar.service
   ```

2. Recargar y reiniciar:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl restart mycalendar.service
   ```

## ✅ Checklist de Verificación

- [ ] Virtual environment creado y con dependencias instaladas
- [ ] Archivo `.env` configurado con `HOST=0.0.0.0`
- [ ] `main.py` lee variables de entorno correctamente
- [ ] Archivo `mycalendar.service` creado en `/etc/systemd/system/`
- [ ] Rutas en el servicio son absolutas y correctas
- [ ] Usuario/grupo en el servicio tienen permisos sobre el proyecto
- [ ] Puerto abierto en firewall UFW
- [ ] Servicio habilitado con `systemctl enable`
- [ ] Servicio iniciado y en estado "active (running)"
- [ ] Puerto escuchando en `0.0.0.0` según `ss -tulpn`
- [ ] Acceso verificado desde localhost
- [ ] Acceso verificado desde red local

## 🔐 Seguridad

### Proteger el archivo .env
```bash
chmod 600 /home/server-paulo/Software/my-calendar/.env
chown server-paulo:server-paulo /home/server-paulo/Software/my-calendar/.env
```

### Añadir .env al .gitignore
```bash
echo ".env" >> .gitignore
```

### No commitear credenciales
Nunca subir el `.env` al repositorio. Usar variables de ejemplo:

```env
# .env.example
HOST=0.0.0.0
PORT=5015
PABLO_PASSWORD=changeme
EVA_PASSWORD=changeme
```

## 📚 Referencias

- [Systemd Service Documentation](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [FastHTML Documentation](https://docs.fastht.ml/)
- [UFW Firewall Guide](https://help.ubuntu.com/community/UFW)
