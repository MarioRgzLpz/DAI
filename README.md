# DAI

Repositorio para las prácticas de DAI

### Iniciar contenedor docker

```bash
docker compose run app Seed.py
```

### Detener contenedor docker

```bash
docker compose down
```
### Copia de seguridad usando mongodump desde el host

```bash
sudo docker compose run mongo mongodump --host mongo --port 27017 --db tienda --out backup/
```
Para que funcione he cambiado el `docker-compose.yml`, añadiendo la línea `- ./backup:/backup` y tras hacer `docker compose up`  le he dado privilegios a la carpeta con `sudo chmod o+w backup/`

### Crear App Django

Una vez añadida las nuevas dependencias, hay que ejecuta `docker compose build` para instalarlas y se crea el proyecto con:

```bash
docker compose run --rm app django-admin startproject Ecommerce .
```
Para ejecutarlo simplemente hacemos `docker compose up` y podemos ver si la instalación ha ido correctamente en http://127.0.0.1:8000/

Para crear la aplicación hacemos:

```bash
docker compose run app python manage.py startapp etienda
```

### Vite con ReactBootstrap

Primero tenemos que tener instalados `nodejs 18` o superior y `npm`:

```bash
npm install react-bootstrap bootstrap
npm create-vite@latest

cd <nombre de directorio que hayas escogido al ejecutar el comando anterior>
npm install
npm run dev
```

Para las estrellas:

```bash
npm install primereact
```

### Despliegue

- Crear carpeta nginx y documentarlo con la configuración y el dockerfile (como está)
- Crear y añadir nginx docker-compose-prod

```bash
docker compose -f ./docker-compose-prod.yml build
docker compose -f ./docker-compose-prod.yml up
docker compose -f ./docker-compose-prod.yml down
```

- Cambiar las busquedas en react y la configuración para que se ejecuten los extras (en dist no se crea la carpeta public, directamente la de imagenes - a tener en cuenta en resultados.jsx)

```bash
npm run build
```

- Pasar las imagenes a static
- Ejecutar docker compose y ya tenemos todo

```bash
localhost/etienda
localhost/react
```
