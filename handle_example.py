#/usr/bin/python
# -*- coding: utf-8 -*-
from piston.handler import BaseHandler
from nfe.models import NFe
from piston.utils import rc, throttle
from nfe.forms import NFeUploadFileForm

# custom status for piston
rc.CODES.update(SUCCESS=('SUCCESS', 201))  # 201 Created
rc.CODES.update(ERROR=('ERROR', 203))  # 203 Non-Authoritative Information


class NFeHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
    model = NFe
    fields = ('zipfile', 'creation_date', 'updated_date', 'number', 'serie', 'portal_protocol')

    def read(self, request, nfe_id):
        try:
            nfe = NFe.objects.get(id=nfe_id)
        except NFe.DoesNotExist, e:
            resp = rc.ERROR
            resp.write(': ' + e.message)
            return resp
        return nfe

    @throttle(60, 60)
    def create(self, request):
        nfe_id = request.POST.get('id', None)
        if nfe_id:  # update item
            try:
                nfe = NFe.objects.get(id=nfe_id)
            except NFe.DoesNotExist, e:
                resp = rc.ERROR
                resp.write(': ' + e.message)
                return resp
            form = NFeUploadFileForm(request.POST, request.FILES, instance=nfe)
        else:
            form = NFeUploadFileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
            except Exception, e:
                resp = rc.ERROR
                resp.write(': ' + repr(e))
                return resp

            return rc.SUCCESS

        resp = rc.ERROR
        resp.write(': ' + repr(form.errors))
        return resp
