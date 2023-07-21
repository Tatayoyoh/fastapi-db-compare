# FastAPI DB Compare

Comparatifs de performances pour BDD

Candidates :
* `Redis` (DB mode)
* `PostgreSQL`
* `MongoDB`

Databases visualisation tools :
* RedisInsight http://localhost:9901
* MongoExpress http://localhost:9902
* pgAdmin4     http://localhost:9903

## Test 1

Test conditions :
* One uniq model to write (Student)
* A list of models to read (many Students)

> 👉 You should proceed FastAPI DB tests on a hosted VM for a more realistic results
> 👉 Tests results where realized on an OVH VM (Debian server)

```bash
python3 tests/stress.py
```

> POST x100 /test/mongo in 25.59 seconds (request average 0.26)<br>
> Errors 0<br>
> POST x100 /test/mongo in 25.64 seconds (request average 0.26)<br>
> Errors 0<br>
> POST x100 /test/pgsql in 24.89 seconds (request average 0.25)<br>
> Errors 0<br>
> GET x100 /test/pgsql in 29.23 seconds (request average 0.29)<br>
> Errors 0<br>
> GET x100 /test/pgsql in 27.19 seconds (request average 0.27)<br>
> Errors 0<br>
> GET x100 /test/pgsql in 28.82 seconds (request average 0.29)<br>
> Errors 0<br>

## Test 2

`Redis` a été retiré des candidates car la BDD est stockée en mémoire vive, et donc prendre potentiellement trop de ressources sur le projet TripyMap3. Elle est d'un autre côté très bien pour les petites BDD (sans stockage de médias par exemple).

Même cas de figure que Test 1 mais avec plusieurs relations supplémentaires liées à l'entitée principale (Student)

### résultat

Postgres + Ormar est plus performant d'environ 20%
MAIS la création du modèle est bien plus complexe, ainsi que sa migration.

Article intéressant : https://www.algoo.fr/fr/actualites/article/fastapi-et-sqlalchemy-un-duo-puissant-mais-attention-aux-transactions

MongoDB est donc choisi comme Database. Maintenant reste à choisir l'ODM (Test 3)

FastAPI utils
https://github.com/mjhea0/awesome-fastapi

ORM SQL Postgres
https://github.com/piccolo-orm/piccolo
https://collerek.github.io/ormar/
https://github.com/Ignisor/FastAPIwee
https://github.com/RobertCraigie/prisma-client-py

ODM NoSQL MongoDB
https://github.com/art049/odmantic
https://github.com/roman-right/beanie
    example  https://github.com/roman-right/beanie-fastapi-demo




## Test 3

ODMantic VS Beanie

Beanie grand gagnant !! Grâce à ses relations 'Link' et baward relation 'BackLink'

Il peut aussi facilement récupérer les relations avec `Model.all(fetch_links=True)`

### PC local

>POST x10 on /test3/odmantic in 2.62 seconds (request average 0.26)
>Errors 0
>POST x10 on /test3/beanie in 2.58 seconds (request average 0.26)
>Errors 0
>GET x10 on /test3/odmantic in 3.44 seconds (request average 0.34)
>Errors 0
>GET x10 on /test3/beanie in 2.21 seconds (request average 0.22)
>Errors 0

Beanie est aussi 40% plus rapide sur les opérations de lecture, alors que odmantic n'a pas de récupération des Relations sur ce test

