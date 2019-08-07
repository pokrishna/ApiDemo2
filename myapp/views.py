from django.shortcuts import render
from django.views.generic import View
from myapp.models import Employee
import json
from django.http import HttpResponse
from django.core.serializers import serialize
from myapp.mixins import SerializeMixin,HttpResponseMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from myapp.utils import is_json
from myapp.forms import EmployeeForm

@method_decorator(csrf_exempt,name='dispatch')
class EmployeeCBV(HttpResponseMixin,SerializeMixin,View):
    def get_object_by_id(self,id):
        try:
            emp=Employee.objects.get(id=id)
        except Emploee.DoesNotExist:
            emp=None
        return emp

    def get(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':"pls send valid json data only"}),status=400)
        data=json.loads(request.body)
        id=data.get('id',None)
        if id is not None:
            obj=self.get_object_by_id(id)
            if obj is None:
                return self.render_to_http_response(json.dumps({"msg":
                "No Matched Record found with specified id"}),status=404)
            json_data=self.serialize([obj,])
            return self.render_to_http_response(json_data)
        qs=Employee.objects.all()
        json_data=self.serialize(qs)
        return self.render_to_http_response(json_data)

    def post(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':'pls send me json_data only'}),status=400)
        empdata=json.loads(request.body)
        print(empdata)
        form =EmployeeForm(empdata)
        if form.is_valid():
            obj=form.save(commit=True)
            return self.render_to_http_response(json.dumps({'msg':'resource created successfully'}))
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=400)

    def put(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':'pleas send me json data'}),status=400)
        pdata=json.loads(request.body)
        id=pdata.get('id',None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg':"Id is required"}),status=400)
        obj=self.get_object_by_id(id)
        if obj is None:
            json_data=json.dumps({'msg':'Object not exist'})
            return self.render_to_http_response(json_data,status=404)
        new_data=pdata
        old_data={
        'eno':obj.eno,
        'ename':obj.ename,
        'esal':obj.esal,
        'eaddr':obj.eaddr,
        }
        old_data.update(new_data)
        form=EmployeeForm(old_data,instance=obj)
        if form.is_valid():
            form.save(commit=True)
            json_data=json.dumps({'msg':'updated successfully'})
            return self.render_to_http_response(json_data,status=201)
        if form.errors:
            json_data=json.dumps(form.errors)
            return self.render_to_http_response(json_data,status=400)
    def delete(self,request,*args,**kwargs):
        data=request.body
        if not is_json(data):
            return self.render_to_http_response(json.dumps({'msg':'pls send me dalid data'}),status=400)
        data=json.loads(request.body)
        id=data.get('id',None)
        if id is None:
            return self.render_to_http_response(json.dumps({'msg':'pls send me id'}),status=400)
        obj=self.get_object_by_id(id)
        if obj is None:
            json_data=json.dumps({"msg":'No matching id found'})
            return self.render_to_http_response(json_data,status=404)
        status,deleted_item=obj.delete()
        if status==1:
            json_data=json.dumps({'msg':'Resource Deleted successfully'})
            return self.render_to_http_response(json_data,status=201)
        json_data=json.dumps({'msg':'unable to delete '})
        return self.render_to_http_response(json_data,status=500)
