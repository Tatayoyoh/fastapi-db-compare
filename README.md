# FastAPI DB Compare

Comparatifs de performances pour BDD

Poste Github : https://github.com/pydantic/pydantic/issues/857#issuecomment-1644311858

Voir le code dans `github_post`

## Test 1

Candidats :
* `Redis` (DB mode)
* `PostgreSQL`
* `MongoDB`

Conditions de test :
* Une unique entitée (Student) à écrire
* La liste de ces entitées à lire


Résultats procédés sur une VM d'un serveur OVH (jet.tripy.be)

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

`Redis` a été retiré des candidats car la BDD est stockée en mémoire vive, et donc prendre potentiellement trop de ressources sur le projet TripyMap3. Elle est d'un autre côté très bien pour les petites BDD (sans stockage de médias par exemple).

Candidats :
* `PostgreSQL`
* `MongoDB`

Même cas de figure que Test 1 mais avec plusieurs relations supplémentaires liées à l'entitée principale (Student)

```python
class StudentMongo(Model):
    # 1 - via modèle direct
    friends: List[StudentFriendMongo]
    parents: List[ParentMongo]
    # OU 
    # 2 - via référence
    friends: List[ObjectId]
    parents: List[ObjectId]
```

Pro/Con 1 - via modèle direct
* 💚 création des sous-entitées en liste à la volée
* 💔 pas de possibilité de les récupérer séparément (voir test2.py GET /mongo/parent)
* 💔 création des sous-entitées séparément impossible

Pro/Con 1 - via référence
* 💛 la création des sous-entitées doit être faite séparément
* 💚 possibilité de les récupérer séparément (voir test2.py GET /mongo/parent)
* 💔 pas d'affichage des champs des sous-entitées de façon naturelle dans le corp de l'entité parent (seulement les IDs apparaissent)

## Test 3

Voir facilités de migration face à un changement de modèle