from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, CreateView, UpdateView
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .forms import *

from .models import GRPMST, GRPINFO, ACCOUNT

# Group List
class GRPListView(View):

    def get(self, request, *args, **kwargs):
        grpinfo = GRPMST.objects.all()

        context = {
            'grp_info': grpinfo,
        }
        return render(request, 'kent/grplist.html', context)

grplist = GRPListView.as_view()

# Add Group
class CreateGRPView(View):

    def get(self, request, *args, **kwargs):
        accinfo = ACCOUNT.objects.all()
        grpinfo = GRPINFO.objects.all()

        context = {
            'acc_info': accinfo,
            'grp_info': grpinfo,
            'form'    : CreateGroupForm(),
        }
        return render(request, 'kent/creategrp.html', context)

    def post(self, request, *args, **kwargs):

        #grpname = request.POST['grpname']
        #q = GRPMST(grpname = grpname)
        #q.save()
        #del q

        return redirect(reverse('kent:grplist'))
        #return HttpResponse(reverse('kent:grplist'))

creategrp = CreateGRPView.as_view()

# Detail Group
class DetailGRPView(View):

    def get(self, request, *args, **kwargs):
        grpname = GRPMST.objects.get(id=kwargs['grpid'])
        grpacclist = GRPINFO.objects.filter(grpname = kwargs['grpid'])
        context = {
            'grpname'   : grpname,
            'grpacclist': grpacclist,
        }
        return render(request, 'kent/detailgrp.html', context)


detailgrp = DetailGRPView.as_view()

# Index
class IndexView(View):

    def get(self, request, *args, **kwargs):
        accinfo = ACCOUNT.objects.all

        context = {
            'acc_info': accinfo,
        }
        return render(request, 'kent/index.html', context)

    def post(self, request, *args, **kwargs):

        return redirect(reverse('kent:index'))

index = IndexView.as_view()

def sendmbr(request):

    if request.method == 'POST':
        grpname = request.POST.get('grpname')
        grpmember = request.POST.get('grpmbr[]')
        print("-- grpname --")
        print(grpname)
        print("-- grpmember --")
        accid = grpmember.split(",")
        for i in accid: print(i.replace("\"",""))

        res  = {'result'   : 'success',
                'messeage' : 'post to sendmbr successfully',
                'errmsg'   : 'post to sendmbr failed',
               }
        resp = "success"
        #return HttpResponse("success")
        return JsonResponse(res)

def sendchk(request):

    if request.method == 'POST':
        all  = request.POST.getlist("all[]")
        chkd = request.POST.getlist("chkd[]")
        print(all)
        print(chkd)

        for recid in all:
            if recid in chkd:
                q = ACCOUNT(id=int(recid))
                q.cstatus = True 
                q.save(update_fields = ["cstatus",])
                del q
            else:
                q = ACCOUNT(id=int(recid))
                q.cstatus = False 
                q.save(update_fields = ["cstatus",])
                del q

        return HttpResponse(all)

# Update
class UpdateView(View):

    def get(self, request, accid, *args, **kwargs):
        accinfo = ACCOUNT.objects.get(pk=accid)
        context = {
            'form': UpdateInfoForm(initial={'selected_dbid':accinfo.dbname_id}),
        }
        return render(request, 'kent/update.html', context)

    def post(self, request, accid, *args, **kwargs):
        accinfo = ACCOUNT.objects.get(pk=accid)
        accinfo.dbname_id = request.POST['selected_dbid']
        accinfo.save()
        del accinfo
        return redirect(reverse('kent:index'))

update = UpdateView.as_view()
