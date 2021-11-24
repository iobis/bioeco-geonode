# bioeco-geonode

This is a fork of https://github.com/GeoNode/geonode with customizations for the GOOS BioEco data portal.

## Installation
### GeoNode deployment
- Git clone
- Checkout `eov_develop` branch
- Copy `.env_prod` to `.env`
- Set admin passwords, email settings, and domains in `.env`
- Start containers

```
docker-compose -f docker-compose.yml up --build -d
```

- Change GeoNode and GeoServer passwords if necessary

### Data migration

- Run the first part of the notebook at https://github.com/iobis/bioeco-etl
- Copy over all shapefiles and JSON files

```
cd output
scp -r * root@geonode.bioeco.goosocean.org:/root/bioeco-geonode/import/
```

- Import layers (if this fails, check if the GeoServer password matches the one in `.env`)

```
docker exec -it django4geonode
python manage.py importlayers --verbosity=2 --overwrite import
```

- Import entities

```
python manage.py loaddata import/users.json
python manage.py loaddata import/eovs.json
```

- Update database

## How to
### Develop

```
docker-compose -f docker-compose.development.yml up --build
```

To reload uwsgi in case there is no autoreload:

```
docker exec -it django4geonode /bin/bash
uwsgi --reload /tmp/geonode.pid
```

Check Django logs:

```
docker exec -it django4geonode /bin/bash
tail -f /var/log/geonode.log
```

All Docker logs:

```
docker-compose -f docker-compose.development.yml logs --tail=0 --follow
```

Check GeoServer logs:

```
docker exec -it geoserver4geonode /bin/bash
tail -f /geoserver_data/data/logs/geoserver.log
```

### Importing layers

```
python manage.py importlayers import
```

### Dumping and loading data

```
python manage.py dumpdata goos.Eov > eov.json
python manage.py dumpdata layers.Layer > layers.json
python manage.py dumpdata base.ResourceBase > resourcebase.json
python manage.py dumpdata base.ContactRole > contactrole.json

python manage.py loaddata users.json
```

### Setup GeoServer

Create SQL view:

- 

MVT support:

```
docker exec -it geoserver4geonode /bin/bash
cd /usr/local/tomcat/webapps/geoserver/WEB-INF/lib
wget http://sourceforge.net/projects/geoserver/files/GeoServer/2.18.3/extensions/geoserver-2.18.3-vectortiles-plugin.zip
unzip geoserver-2.18.3-vectortiles-plugin.zip
```

Enable CORS, see https://docs.geoserver.org/latest/en/user/production/container.html:

```
docker exec -it geoserver4geonode /bin/bash
cd /usr/local/tomcat/webapps/geoserver/WEB-INF
vim web.xml
```

```
<filter>
  <filter-name>cross-origin</filter-name>
  <filter-class>org.apache.catalina.filters.CorsFilter</filter-class>
  <init-param>
    <param-name>cors.allowed.origins</param-name>
    <param-value>*</param-value>
  </init-param>
  <init-param>
    <param-name>cors.allowed.methods</param-name>
    <param-value>GET,POST,PUT,DELETE,HEAD,OPTIONS</param-value>
  </init-param>
  <init-param>
    <param-name>cors.allowed.headers</param-name>
    <param-value>*</param-value>
  </init-param>
</filter>

<filter-mapping>
  <filter-name>cross-origin</filter-name>
  <url-pattern>/*</url-pattern>
</filter-mapping>
```

Set GeoFence rules:

- 

Add filter for `viewparams`.
