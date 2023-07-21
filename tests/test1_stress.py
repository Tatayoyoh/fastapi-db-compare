from timeit import default_timer as timer

student = {
    "fullname": "John Doe",
    "email": "jdoe@x.edu.ng",
    "course_of_study": "Water resources engineering",
    "year": 2,
    "gpa": "3.0",
}

import httpx
import statistics

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
        r = httpx.get(URL+url_path)
        stats.append(round(timer() - start2, 2))
        if r.status_code != 200:
            print(r.status_code, r.content)
            errors += 1
    print("GET x%s on %s in %s seconds (request average %s)"%(AMOUNT, url_path, round(timer() - start, 2), round(statistics.fmean(stats),2)))
    print('Errors %s'%(errors))


if __name__ == '__main__':
    test_write('/test1/mongo')
    test_write('/test1/pgsql')
    test_write('/test1/redis')

    test_read('/test1/mongo')
    test_read('/test1/pgsql')
    test_read('/test1/redis')


