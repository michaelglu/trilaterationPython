from django.http import HttpResponse
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
@csrf_exempt
def index(request):
    if request.method == "POST":
        body = json.loads(request.body)
        point1=body["point1"]
        point2=body["point2"]
        point3=body["point3"]
        point4=body["point4"]
        print(point1)
        print(point2)
        print(point3)
        print(point4)
        jsonResponse=trilaterate(point1,point2,point3,point4)
        print(jsonResponse)
        return HttpResponse(jsonResponse)
    else: return HttpResponse(status=404)
def trilaterate(point1,point2,point3,point4):
    np.set_printoptions(precision=3)
    x1,x2,x3,x4=[point1["x"],point2["x"],point3["x"],point4["x"]]
    y1,y2,y3,y4=[point1["y"],point2["y"],point3["y"],point4["y"]]
    z1,z2,z3,z4=[point1["z"],point2["z"],point3["z"],point4["z"]]
    d1=point1["rad"]
    d2=point2["rad"]
    d3=point3["rad"]
    d4=point4["rad"]

    coeffs=2*np.array([[x2-x1, y2-y1,z2-z1],[x3-x1, y3-y1,z3-z1],[x4-x1, y4-y1,z4-z1]])
    print("Coeffs")
    print(coeffs)
    soln=np.array([[(d1*d1-d2*d2)-(x1*x1-x2*x2)-(y1*y1-y2*y2)-(z1*z1-z2*z2)],
    [(d1*d1-d3*d3)-(x1*x1-x3*x3)-(y1*y1-y3*y3)-(z1*z1-z3*z3)]
    ,[(d1*d1-d4*d4)-(x1*x1-x4*x4)-(y1*y1-y4*y4)-(z1*z1-z4*z4)]])
    print("Soln")
    print(soln)
    [x,y,z]=np.dot(np.linalg.inv(coeffs),soln)
    print("x: ",x[0].astype(str),"\ny: ",y[0].astype(str),"\nz: "+z[0].astype(str))
    data={};
    data["x"]=np.round(x[0],3);
    data["y"]=np.round(y[0],3);
    data["z"]=np.round(z[0],3);
    return json.dumps(data)
