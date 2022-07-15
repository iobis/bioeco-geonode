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

        layers = Layer.objects.all().order_by('name')

        dbhost = os.getenv('DATABASE_HOST', 'db')
        dbport = os.getenv('DATABASE_PORT', 5432)

        #geonode_user = os.getenv('GEONODE_DATABASE', 'geonode')
        #geonode_pwd = os.getenv('GEONODE_DATABASE_PASSWORD', 'geonode')
        #geonode_dbname = os.getenv('GEONODE_DATABASE', 'geonode')

        data_user = os.getenv('GEONODE_GEODATABASE', 'geonode_data')
        data_pwd = os.getenv('GEONODE_GEODATABASE_PASSWORD', 'geonode_data')
        data_dbname = os.getenv('GEONODE_GEODATABASE', 'geonode_data')

        data_conn = None
        try:

            #geonode_conn = psycopg2.connect(dbname=geonode_dbname, user=geonode_user, host=dbhost, port=dbport, password=geonode_pwd)
            #geonode_cur = geonode_conn.cursor()

            data_conn = psycopg2.connect(dbname=data_dbname, user=data_user, host=dbhost, port=dbport, password=data_pwd)
            data_cur = data_conn.cursor()

            # create spatial table

            data_cur.execute("""
                drop table if exists public._all_layers
            """)
            data_cur.execute("""
                create table if not exists public._all_layers
                (pk int4, name varchar(128), keywords int4[], readiness_coordination int4, readiness_data int4, readiness_requirements int4, in_obis boolean)
            """)
            data_cur.execute("""
                select public.AddGeometryColumn('public', '_all_layers', 'the_geom', 4326, 'GeometryCollection', 2)
            """)
            data_cur.execute("""
                delete from public._all_layers
            """)

            # create indexes

            data_cur.execute("create index if not exists ix_all_pk on public._all_layers using btree (pk)")
            data_cur.execute("create index if not exists ix_all_name on public._all_layers using btree (name)")
            data_cur.execute("create index if not exists ix_all_coordination on public._all_layers using btree (readiness_coordination)")
            data_cur.execute("create index if not exists ix_all_data on public._all_layers using btree (readiness_data)")
            data_cur.execute("create index if not exists ix_all_requirements on public._all_layers using btree (readiness_requirements)")
            data_cur.execute("create index if not exists ix_all_keywords on public._all_layers using gin (keywords)")
            data_cur.execute("create index if not exists ix_all_geom on public._all_layers using gist (the_geom)")
            data_cur.execute("create index if not exists ix_all_inobis on public._all_layers using btree (in_obis)")

            # get layer table names

            #geonode_cur.execute("""
            #    select name from public.layers_layer
            #""")
            #layer_names = [row[0] for row in geonode_cur.fetchall()]

            data_cur.execute("""
                select table_name, f_geometry_column, srid
                from information_schema.tables
                left join geometry_columns gc on gc.f_table_name = tables.table_name
                where table_schema = 'public' and table_type = 'BASE TABLE' and f_geometry_column is not null
            """)
            rows = data_cur.fetchall()
            table_info = { row[0]: (row[1], row[2]) for row in rows }

            # populate spatial table

            for layer in layers:
                print(f"Processing layer {layer.name}")

                keywords = [keyword.id for keyword in layer.tkeywords.all()]

                if layer.name in table_info:
                    if table_info[layer.name][1] == 0:
                        print(f"ERROR: Table {layer.name} has SRID 0")
                        continue
                    q = f"""
                        insert into public._all_layers (pk, name, in_obis, keywords, readiness_coordination, readiness_data, readiness_requirements, the_geom)
                        select
                            %s as pk,
                            %s as name,
                            %s as in_obis,
                            %s as keywords,
                            %s as readiness_coordination,
                            %s as readiness_data,
                            %s as readiness_requirements,
                            ST_ForceCollection(st_transform({table_info[layer.name][0]}, 4326)) as the_geom
                        from public.\"{layer.name}\""""
                    data_cur.execute(q, (layer.pk, layer.name, layer.in_obis, keywords, None, None, None))
                else:
                    print(f"ERROR: Table {layer.name} not found")

            #data_conn.rollback()
            data_conn.commit()
            data_conn.close()

        except Exception as e:
            import traceback
            print(traceback.format_exc())
            print(f"ERROR: {e}")
