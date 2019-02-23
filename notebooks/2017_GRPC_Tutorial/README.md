# Données

## Découpage administratif communal français issu d'OpenStreetMap

https://www.data.gouv.fr/fr/datasets/decoupage-administratif-communal-francais-issu-d-openstreetmap/

`Exports du découpage administratif français au niveau communal (contours des communes) 
issu d'OpenStreetMap produit dans sa grande majorité à partir du cadastre.`

Export de janvier 2019 (geojson simplifié, 24Mo)
Fichier contenant les géométries simplifiées, format geojson
 zip (23.2Mo)   408  Disponible
https://www.data.gouv.fr/fr/datasets/r/07b7c9a2-d1e2-4da6-9f20-01a7b72d4b12

## Limites administratives simplifiées
http://prev.openstreetmap.fr/blogs/cquest/limites-administratives-simplifiees

`Depuis que l'ensemble des limites administratives des communes françaises ont été tracées dans OpenStreetMap, 
un besoin d'une version simplifiée de ces limites s'est fait sentir.`


## Contours des départements français issus d'OpenStreetMap
https://www.data.gouv.fr/fr/datasets/contours-des-departements-francais-issus-d-openstreetmap/

`Exports du découpage administratif français au niveau départemental (contours des départements) 
issu d'OpenStreetMap produit dans sa grande majorité à partir du cadastre.`

# Insertion en base

## Using ogr2ogr to convert data between GeoJSON, PostGIS and Esri Shapefile
https://morphocode.com/using-ogr2ogr-convert-data-formats-geojson-postgis-esri-geodatabase-shapefiles/

`Ogr2ogr is the swiss-army knife when it comes to conversion of GIS data. 
It is part of the Geospatial Data Abstraction Library and provides an easy way to convert 
data between common storage formats: GeoJSON, Shapefile, PostGIS and others.`

```bash
ogr2ogr -f "PostgreSQL" \
        PG:"host=localhost dbname=test user=docker password=docker port=2345" \
        "communes-20190101.json"
```

### documentation GDAL 1.10.0 » Les commandes et formats OGR »
https://gdal.gloobe.org/ogr/ogr2ogr.html

`Convertie des données simple features entre divers formats de fichiers.`