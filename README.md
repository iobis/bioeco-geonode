# bioeco-geonode

This is a fork of https://github.com/GeoNode/geonode with customizations for the GOOS BioEco data portal.

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

### Dumping and loading data

```
python manage.py dumpdata goos.Eov > geonode/goos/fixtures/eov.json
python manage.py loaddata users.json
```