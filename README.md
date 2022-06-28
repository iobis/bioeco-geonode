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
docker-compose -f docker-compose.yml up --build --no-deps -d
```

- Change GeoNode and GeoServer passwords if necessary

### Data migration

- Run the first part of the notebook at https://github.com/iobis/bioeco-etl
- Copy over all shapefiles and JSON files

```
cd output
scp -r * root@geonode.bioeco.goosocean.org:/root/bioeco-geonode/import/
```

- Import entities

```
python manage.py loaddata import/users.json
python manage.py loaddata import/eovs.json
```

- Import layers (if this fails, check if the GeoServer password matches the one in `.env`, GeoServer processing can take a while)

```
docker exec -it django4geonode
python manage.py importlayers --verbosity=2 --overwrite import
```

- Not all imports may be visible in GeoNode, use this to generate paths for another import with `--overwrite`:

```
select 'import/' || name
from layers_layer
where store = ''
```

- Update database
- cron.sh

### Set up GeoServer

- Run custom command to create spatial table `_all_layers`

```
python manage.py spatialtable
```

- Enable MVT support

```
docker exec -it geoserver4geonode /bin/bash
cd /usr/local/tomcat/webapps/geoserver/WEB-INF/lib
wget http://sourceforge.net/projects/geoserver/files/GeoServer/2.18.3/extensions/geoserver-2.18.3-vectortiles-plugin.zip
unzip geoserver-2.18.3-vectortiles-plugin.zip
```

- Create style `collection`

```
<?xml version="1.0" encoding="UTF-8"?>
<StyledLayerDescriptor version="1.0.0"
 xsi:schemaLocation="http://www.opengis.net/sld StyledLayerDescriptor.xsd"
 xmlns="http://www.opengis.net/sld"
 xmlns:ogc="http://www.opengis.net/ogc"
 xmlns:xlink="http://www.w3.org/1999/xlink"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <NamedLayer>
    <Name>collection</Name>
    <UserStyle>
      <FeatureTypeStyle>
       <Rule>
          <PolygonSymbolizer>
            <Stroke>
              <CssParameter name="stroke">#FFFFFF</CssParameter>
              <CssParameter name="stroke-width">6</CssParameter>
            </Stroke>
          </PolygonSymbolizer>
          <LineSymbolizer>
            <Stroke>
              <CssParameter name="fill">#00FF00</CssParameter>
              <CssParameter name="stroke-width">2</CssParameter>
              <CssParameter name="stroke-linejoin">round</CssParameter>
              <CssParameter name="stroke-linecap">round</CssParameter>
            </Stroke>
          </LineSymbolizer>
         <PointSymbolizer>
              <Graphic>
                <Mark>
                  <WellKnownName>circle</WellKnownName>
                  <Fill>
                    <CssParameter name="fill">#0000FF</CssParameter>
                  </Fill>
                </Mark>
              <Size>9</Size>
            </Graphic>
          </PointSymbolizer>
      </Rule>
      </FeatureTypeStyle>
    </UserStyle>
  </NamedLayer>
</StyledLayerDescriptor>
```

- Create layer `all_layers`
- Set SQL view with parameter `where`

```
select * from public._all_layers %where%
```

- Set style in layer publishing tab
- Set all_layers cache expiration in the Tile Caching tab (GeoServer/GWC returning 400 was fixed by rebuilding the GeoServer container)
- Enable CORS, see https://docs.geoserver.org/latest/en/user/production/container.html:

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

- Restart, note that GeoServer does not come up again unless nginx4geonode is removed and rebuilt
- Enable mvt tile caching, add filter for `viewparams` with regex `.*`
- Update GeoServer URL in global settings
- Set GeoFence rules
  - first time not working
    - look into `GEOFENCE_SECURITY_ENABLED: 'False'`?
    - look into command `set_all_layers_public`?

### Cron

```
0 * * * * /root/bioeco-geonode/cron.sh > /root/cron.log 2>&1
```

### Email

Configure `DJANGO_EMAIL_HOST` and others in `.env`. Set up postfix on host, in config check `mynetworks` (should include container IP) and `inet_interfaces` (should include host IP).

Also set site name in admin module.

```
root@bioeco-geonode:~/bioeco-geonode# cat /etc/postfix/main.cf
# See /usr/share/postfix/main.cf.dist for a commented, more complete version


# Debian specific:  Specifying a file name will cause the first
# line of that file to be used as the name.  The Debian default
# is /etc/mailname.
#myorigin = /etc/mailname

smtpd_banner = $myhostname ESMTP $mail_name (Ubuntu)
biff = no

# appending .domain is the MUA's job.
append_dot_mydomain = no

# Uncomment the next line to generate "delayed mail" warnings
#delay_warning_time = 4h

readme_directory = no

# See http://www.postfix.org/COMPATIBILITY_README.html -- default to 2 on
# fresh installs.
compatibility_level = 2



# TLS parameters
smtpd_tls_cert_file=/etc/ssl/certs/ssl-cert-snakeoil.pem
smtpd_tls_key_file=/etc/ssl/private/ssl-cert-snakeoil.key
smtpd_tls_security_level=may

smtp_tls_CApath=/etc/ssl/certs
smtp_tls_security_level=may
smtp_tls_session_cache_database = btree:${data_directory}/smtp_scache


smtpd_relay_restrictions = permit_mynetworks permit_sasl_authenticated defer_unauth_destination
myhostname = bioeco-geonode-dev
alias_maps = hash:/etc/aliases
alias_database = hash:/etc/aliases
mydestination = $myhostname, bioeco-geonode, bioeco-geonode-dev, localhost.localdomain, localhost
relayhost =
mynetworks = 127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128 172.17.0.0/16 172.20.0.0/16
mailbox_size_limit = 0
recipient_delimiter = +
inet_interfaces = 127.0.0.1, [::1], 172.17.0.1
inet_protocols = all
```

## How to
### Develop

```
docker-compose -f docker-compose.development.yml up --build
```

To reload uwsgi in case there is no autoreload (check pidfile location in `uwsgi.ini`):

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

### Dumping and loading data

```
python manage.py dumpdata goos.Eov > eov.json
python manage.py dumpdata layers.Layer > layers.json
python manage.py dumpdata base.ResourceBase > resourcebase.json
python manage.py dumpdata base.ContactRole > contactrole.json
python manage.py loaddata users.json
```

### Thumbnails

```
python manage.py sync_geonode_layers --updatethumbnails
```
