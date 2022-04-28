from django.core.management.base import BaseCommand
from geonode.layers.models import Layer
import os
import psycopg2
import json


class Command(BaseCommand):
    help = "Create table combining all spatial features"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        layers = Layer.objects.all()
        
        geouser = os.getenv('GEONODE_GEODATABASE', 'geonode_data')
        geopwd = os.getenv('GEONODE_GEODATABASE_PASSWORD', 'geonode_data')
        geodbname = os.getenv('GEONODE_GEODATABASE', 'geonode_data')
        dbhost = os.getenv('DATABASE_HOST', 'db')
        dbport = os.getenv('DATABASE_PORT', 5432)

        conn = None
        try:
            conn = psycopg2.connect(dbname=geodbname, user=geouser, host=dbhost, port=dbport, password=geopwd)
            cur = conn.cursor()

            # create spatial table

            cur.execute("""
                drop table if exists public._all_layers
            """)
            cur.execute("""
                create table if not exists public._all_layers
                (pk int4, name varchar(128), keywords int4[], readiness_coordination int4, readiness_data int4, readiness_requirements int4)
            """)
            cur.execute("""
                select public.AddGeometryColumn('public', '_all_layers', 'the_geom', 4326, 'GeometryCollection', 2)
            """)
            cur.execute("""
                delete from public._all_layers
            """)

            # create indexes

            cur.execute("create index if not exists ix_all_pk on public._all_layers using btree (pk)")
            cur.execute("create index if not exists ix_all_name on public._all_layers using btree (name)")
            cur.execute("create index if not exists ix_all_coordination on public._all_layers using btree (readiness_coordination)")
            cur.execute("create index if not exists ix_all_data on public._all_layers using btree (readiness_data)")
            cur.execute("create index if not exists ix_all_requirements on public._all_layers using btree (readiness_requirements)")
            cur.execute("create index if not exists ix_all_keywords on public._all_layers using gin (keywords)")
            cur.execute("create index if not exists ix_all_geom on public._all_layers using gist (the_geom)")

            # get layer table names

            cur.execute("""
                select table_name from information_schema.tables where table_schema = 'public' and table_type = 'BASE TABLE'
            """)
            table_names = [row[0] for row in cur.fetchall()]

            # populate spatial table

            for layer in layers:
                print(f"Processing layer {layer.name}")

                keywords = [keyword.id for keyword in layer.tkeywords.all()]

                if layer.name in table_names:
                    cur.execute("""
                        insert into public._all_layers (pk, name, keywords, readiness_coordination, readiness_data, readiness_requirements, the_geom)
                        select
                            %s as pk,
                            %s as name,
                            %s as keywords,
                            %s as readiness_coordination,
                            %s as readiness_data,
                            %s as readiness_requirements,
                            ST_ForceCollection(st_transform(the_geom, 4326)) as the_geom
                        from public.""" + layer.name, (layer.pk, layer.name, keywords, None, None, None)
                    )
                else:
                    print(f"Table {layer.name} not found")

            #conn.rollback()
            conn.commit()
            conn.close()

        except Exception as e:
            print(e)
