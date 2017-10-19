# A Python microservice stack

http://flagzeta.org/blog/a-python-microservice-stack/?lipi=urn%3Ali%3Apage%3Ad_flagship3_pulse_read%3BkynUztgmQwe56oSyWHTmEw%3D%3D

# 

```bash
mkvirtualenv --python=/usr/bin/python3.5 py3.5_grpcio
python -m pip install --upgrade pip

pip install grpcio
pip install grpcio-tools

(git clone -b v1.6.x https://github.com/grpc/grpc)

(pip install ipython memory_profilter)
workon py3.5_grpcio

mkdir -p proto/build
python -m grpc.tools.protoc -I. --python_out=proto/build/. --grpc_python_out=proto/build/. proto/search.proto
```bash
┗ tree      
.
├── proto
│   ├── build
│   │   └── proto
│   │       ├── search_pb2_grpc.py
│   │       └── search_pb2.py
│   └── search.proto
└── src
	├── models.py
	├── search_client.py
	└── search_server.py

# Create/Edit: 
# - search_server.py
# - search_client.py
# - models.py

# https://stackoverflow.com/questions/21641696/python-dns-module-import-error

pip install \
	sqlalchemy \
	geoalchemy2 \
	psycopg2 \
	python-consul \
	statsd \
	dnspython
```

# Docker - Consul

- https://python-consul.readthedocs.io/en/latest/#consul-agent
- https://hub.docker.com/r/ciscocloud/consul-cli/
- https://github.com/mantl/consul-cli/wiki/Agent#services
- https://hub.docker.com/_/consul/

```bash
┗ docker run --net=host consul agent -server -ui -bootstrap -bind=127.0.0.1
bootstrap = true: do not enable unless necessary
==> Starting Consul agent...
==> Consul agent running!
	       Version: 'v1.0.0'
	       Node ID: '6f63d3d1-0686-de4b-bab2-ed3ba6747664'
	     Node name: 'crawler'
	    Datacenter: 'dc1' (Segment: '<all>')
	        Server: true (Bootstrap: true)
	   Client Addr: [127.0.0.1] (HTTP: 8500, HTTPS: -1, DNS: 8600)
	  Cluster Addr: 127.0.0.1 (LAN: 8301, WAN: 8302)
	       Encrypt: Gossip: false, TLS-Outgoing: false, TLS-Incoming: false

==> Log data will now stream in as it occurs:

	2017/10/19 09:43:57 [INFO] raft: Initial configuration (index=1): [{Suffrage:Voter ID:6f63d3d1-0686-de4b-bab2-ed3ba6747664 Address:127.0.0.1:8300}]
	2017/10/19 09:43:57 [INFO] raft: Node at 127.0.0.1:8300 [Follower] entering Follower state (Leader: "")
	2017/10/19 09:43:57 [INFO] serf: EventMemberJoin: crawler.dc1 127.0.0.1
	2017/10/19 09:43:57 [INFO] serf: EventMemberJoin: crawler 127.0.0.1
	2017/10/19 09:43:57 [INFO] agent: Started DNS server 127.0.0.1:8600 (udp)
	2017/10/19 09:43:57 [INFO] consul: Handled member-join event for server "crawler.dc1" in area "wan"
	2017/10/19 09:43:57 [INFO] agent: Started DNS server 127.0.0.1:8600 (tcp)
	2017/10/19 09:43:57 [INFO] consul: Adding LAN server crawler (Addr: tcp/127.0.0.1:8300) (DC: dc1)
	2017/10/19 09:43:57 [INFO] agent: Started HTTP server on 127.0.0.1:8500 (tcp)
	2017/10/19 09:44:03 [WARN] raft: Heartbeat timeout from "" reached, starting election
	2017/10/19 09:44:03 [INFO] raft: Node at 127.0.0.1:8300 [Candidate] entering Candidate state in term 2
	2017/10/19 09:44:03 [INFO] raft: Election won. Tally: 1
	2017/10/19 09:44:03 [INFO] raft: Node at 127.0.0.1:8300 [Leader] entering Leader state
	2017/10/19 09:44:03 [INFO] consul: cluster leadership acquired
	2017/10/19 09:44:03 [INFO] consul: New leader elected: crawler
	2017/10/19 09:44:03 [INFO] consul: member 'crawler' joined, marking health alive
	2017/10/19 09:44:03 [INFO] agent: Synced node info
```

=> '-ui' interface web monitoring: http://localhost:8500/ui


# PostGRESQL - PostGIS

- https://hub.docker.com/r/mdillon/postgis/

One shot (option '--rm'):
```bash
┗ docker run --rm --name postgis -e POSTGRES_PASSWORD=password -e POSTGRES_USER=user -p 5432:5432 -d mdillon/postgis

5a45393db4ba3820031df06ab43a8f75e8f04b128705897f08244627bb2ec283
┗ docker ps                                                                                                         
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                      NAMES
5a45393db4ba        mdillon/postgis     "docker-entrypoint..."   35 seconds ago      Up 33 seconds       0.0.0.0:5432->5432/tcp     postgis
┗ docker logs -f postgis                                                                       
The files belonging to this database system will be owned by user "postgres".                  
This user must also own the server process.
...
LOG:  MultiXact member wraparound protections are now enabled                                  
LOG:  database system is ready to accept connections                                           
LOG:  autovacuum launcher started              
```

- https://dba.stackexchange.com/questions/1285/how-do-i-list-all-databases-and-tables-using-psql
```bash
┗ psql -h 127.0.0.1 -U user -l
Mot de passe pour l'utilisateur user : 
                                     Liste des bases de données
       Nom        | Propriétaire | Encodage | Collationnement | Type caract. |    Droits d'accès     
------------------+--------------+----------+-----------------+--------------+-----------------------
 postgres         | postgres     | UTF8     | en_US.utf8      | en_US.utf8   | 
 template0        | postgres     | UTF8     | en_US.utf8      | en_US.utf8   | =c/postgres          +
                  |              |          |                 |              | postgres=CTc/postgres
 template1        | postgres     | UTF8     | en_US.utf8      | en_US.utf8   | =c/postgres          +
                  |              |          |                 |              | postgres=CTc/postgres
 template_postgis | user         | UTF8     | en_US.utf8      | en_US.utf8   | 
 test             | user         | UTF8     | en_US.utf8      | en_US.utf8   | 
 user             | postgres     | UTF8     | en_US.utf8      | en_US.utf8   | 
(6 lignes)
```

## Create database and install PostGIS extension

```bash
$ psql -h 127.0.0.1 -p 5432 --user user -c "CREATE DATABASE test;\c test; CREATE EXTENSION postgis"
$ psql test -h 127.0.0.1 -p 5432 --user user -c "CREATE EXTENSION postgis";
```

- https://stackoverflow.com/questions/28803651/how-to-execute-multiple-queries-using-psql-command-from-bash-shell
```bash
┗ psql -h 127.0.0.1 -p 5432 --user user -c "CREATE DATABASE test;"
┗ psql test -h 127.0.0.1 -p 5432 --user user -c "CREATE EXTENSION postgis";
Mot de passe pour l'utilisateur user :         
CREATE EXTENSION   
```

# Graphite
- https://github.com/hopsoft/docker-graphite-statsd

```bash
┗ docker run -d --name graphite --restart=always -p 80:80 -p 2003-2004:2003-2004 -p 2023-2024:2023-2024 -p 8125:8125/udp -p 8126:8126 hopsoft/graphite-statsd                                 
361d1e44bfd89a2d041d9bfec552e21291435a3baf8aa960b730c5e5fc98768e

┗ docker logs -f graphite    
*** Running /etc/my_init.d/00_regen_ssh_host_keys.sh...
*** Running /etc/my_init.d/01_conf_init.sh...
*** Running /etc/rc.local...
*** Booting runit daemon...
*** Runit started as PID 15
Oct 19 09:52:11 361d1e44bfd8 syslog-ng[32]: syslog-ng starting up; version='3.5.3'
```

# MicroService

## Server

- http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
- http://docs.sqlalchemy.org/en/latest/orm/extensions/declarative/table_config.html

```bash
┗ PYTHONPATH=proto/build/proto python src/search_server.py
2017-10-19 11:58:06,934 INFO sqlalchemy.engine.base.Engine select version()                    
2017-10-19 11:58:06,934 INFO sqlalchemy.engine.base.Engine {}                                  
2017-10-19 11:58:06,935 INFO sqlalchemy.engine.base.Engine select current_schema()             
2017-10-19 11:58:06,935 INFO sqlalchemy.engine.base.Engine {}                                  
2017-10-19 11:58:06,936 INFO sqlalchemy.engine.base.Engine SELECT CAST('test plain returns' AS VARCHAR(60)) AS anon_1
2017-10-19 11:58:06,936 INFO sqlalchemy.engine.base.Engine {}                                  
2017-10-19 11:58:06,936 INFO sqlalchemy.engine.base.Engine SELECT CAST('test unicode returns' AS VARCHAR(60)) AS anon_1
2017-10-19 11:58:06,936 INFO sqlalchemy.engine.base.Engine {}                                  
2017-10-19 11:58:06,937 INFO sqlalchemy.engine.base.Engine show standard_conforming_strings    
2017-10-19 11:58:06,937 INFO sqlalchemy.engine.base.Engine {}                                  
2017-10-19 11:58:06,937 INFO sqlalchemy.engine.base.Engine select relname from pg_class c join pg_namespace n on n.oid=c.relnamespace where pg_catalog.pg_table_is_visible(c.oid) and relname=%(name)s
2017-10-19 11:58:06,938 INFO sqlalchemy.engine.base.Engine {'name': 'thing'}                   
2017-10-19 11:58:06,938 INFO sqlalchemy.engine.base.Engine                                     
CREATE TABLE thing (   
	    id SERIAL NOT NULL,                    
	    name VARCHAR,  
	    geom geometry(POLYGON,-1),             
	    PRIMARY KEY (id)                       
)                      


2017-10-19 11:58:06,938 INFO sqlalchemy.engine.base.Engine {}                                  
2017-10-19 11:58:06,976 INFO sqlalchemy.engine.base.Engine COMMIT                              
2017-10-19 11:58:06,978 INFO sqlalchemy.engine.base.Engine CREATE INDEX "idx_thing_geom" ON "public"."thing" USING GIST ("geom")
2017-10-19 11:58:06,978 INFO sqlalchemy.engine.base.Engine {}                                  
2017-10-19 11:58:06,979 INFO sqlalchemy.engine.base.Engine COMMIT                              
2017-10-19 11:58:06,980 - root - INFO - register started                                       
2017-10-19 11:58:06,982 - urllib3.connectionpool - DEBUG - Starting new HTTP connection (1): 127.0.0.1
2017-10-19 11:58:06,989 - urllib3.connectionpool - DEBUG - http://127.0.0.1:8500 "PUT /v1/agent/service/register HTTP/1.1" 200 0
2017-10-19 11:58:06,990 - urllib3.connectionpool - DEBUG - http://127.0.0.1:8500 "GET /v1/agent/services HTTP/1.1" 200 184
2017-10-19 11:58:06,990 - root - INFO - services: {'search-service-54054': {'EnableTagOverride': False, 'Service': 'search-service', 'CreateIndex': 0, 'Port': 54054, 'Address': '127.0.0.1', 'Tags': [], 'ModifyIndex': 0, 'ID': 'search-service-54054'}}
2017-10-19 11:58:06,993 - root - INFO - server started            
```

Log de Consul:
```bash
2017/10/19 09:58:06 [INFO] agent: Synced service 'search-service-54054'                    
2017/10/19 09:58:09 [INFO] agent: Synced check 'service:search-service-54054'    
```

## Client

Ré-écriture du client.

Utilisation d'argparse pour les paramètres/controles des paramètres.

# Docs/Liens

- http://andrewjesaitis.com/2016/08/25/streaming-comparison/
- https://github.com/grpc/grpc-go/issues/414

## Asynchronous Multiplexing HTTP2/DBO Requests
- https://pypi.python.org/pypi/aquests
- https://stackoverflow.com/questions/34969446/grpc-image-upload

