from timeit import default_timer as timer

friends = [
        {
        "fullname": "friend1 Jack",
        "email": "friend1@gmail.com",
        "status": "super friend",
        "isfamily": "no",
        },
        {
        "fullname": "friend2 Bob",
        "email": "friend2@gmail.com",
        "status": "great friend",
        "isfamily": "no",
        },
        {
        "fullname": "big brother",
        "email": "bro@gmail.com",
        "status": "brother",
        "isfamily": "yes",
        }
]
parents = [
        {
            "fullname": "Maman",
            "email":"mama@gmail.com",
            "relation":"Mère",
        },
        {
            "fullname": "Papa",
            "email":"papa@gmail.com",
            "relation":"Père",
        }
]
student = {
    "fullname": "John Doe",
    "email": "jdoe@x.edu.ng",
    "course_of_study": "Water resources engineering",
    "year": 2,
    "gpa": "3.0",
    "friends": [
    ],
    "parents": [
    ],
    "school": {
        "name":"Ecole Toulon",
        "address":
        {
            "city": "Toulon",
            "street": "Liberté",
            "number": 155,
            "zipcode": "83000",
            "other": "Entrée #2",
        },
        "reputationscore":5,
        "note":"Très bonne école",
    },
    "address":
        {
            "city": "La Farlède",
            "street": "impasse de bob",
            "number": 15,
            "zipcode": 83210,
            "other": "fond de la rue",
        },  
}

import httpx
import statistics
import json
from pprint import pprint 

URL='http://localhost:9900'
AMOUNT=10
# URL='http://jet.tripy.be:9900'
# AMOUNT=100

def test_write(url_path):
    start = timer()
    stats = []
    errors = 0
    for i in range(0,AMOUNT):
        start2 = timer()
        student['fullname'] = 'John Doe %s'%(AMOUNT-i) 
        student['friends'] = friends # inside doc
        for parent in parents: # generate parents references separately
            r = httpx.post(URL+url_path+'/parent', json=parent)
            content = json.loads(r.content)
            if 'id' in content:
                pid = content['id'] # << Odmantic
            else:
                pid = content['_id'] # << Beanie
            student['parents'].append(pid)
        r = httpx.post(URL+url_path, json=student)
        stats.append(round(timer() - start2, 2))
        if r.status_code != 200:
            print(r.status_code, r.content)
            errors += 1
    print("POST x%s on %s in %s seconds (request average %s)"%(AMOUNT, url_path, round(timer() - start, 2), round(statistics.fmean(stats),2)))
    print('Errors %s'%(errors))
    
def test_read(url_path):
    start = timer()
    stats = []
    errors = 0
    for i in range(0,AMOUNT):
        start2 = timer()
        r = httpx.get(URL+url_path, timeout=30)
        stats.append(round(timer() - start2, 2))
        if r.status_code != 200:
            print(r.status_code, r.content)
            errors += 1
    print("GET x%s on %s in %s seconds (request average %s)"%(AMOUNT, url_path, round(timer() - start, 2), round(statistics.fmean(stats),2)))
    print('Errors %s'%(errors))


if __name__ == '__main__':
    test_write('/test3/odmantic')
    test_write('/test3/beanie')

    test_read('/test3/odmantic')
    test_read('/test3/beanie')


