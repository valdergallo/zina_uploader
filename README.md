ZinaUploader
============

Comando para upload de arquivos em linha de comando.


Como funciona
-------------

Deve existir uma URL Rest que recebe o arquivo e retorna o registro da informação por padrão.

Upload:

```bash
zina_uploader <filename> <api_url>
```

Validar:

```bash
zina_uploader <zina_id> <api_url>
```

Verificar conexão:

```bash
zina_uploader 0 <api_url>
```

Configurar Login Bash Auth
--------------------------

As configurações de login para o upload caso, a API utilize Base Auth estão ligadas no flowbot.json que fica no mesmo diretório do comando zina_uploader.

flowbot.ini

```
[user]
username=vgallo
password=password

[config]
http = 87.254.212.121:8080
https= 87.254.212.121:8080
debug= 1

```


Utilizando com o Flowbot
------------------------

O Flowbot (Resources) verifica antes de começar um processo se a URL existe, para isso ele bate na API com um ID indefinido. A mesma deve retorna algum conteúdo para ele sem conter a palavra ***ERRO*** em qualquer parte do  JSON. Lembrando sempre que o retorno é lido como texto pelo Flowbot e não uma lista de itens como esperado por um parser de um JSON.


--------------------------------------------------------------------

- Nos exemplos estou utlizando PISTON com Django para API Rest

Exemplo de handle.py

```python
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
```
--------------------------------------------------------------------

Exemplo de urls.py

```python
	# base rest authentication
	auth = HttpBasicAuthentication(realm="MyRealm")
	ad = {'authentication': auth}
	nfe_resource = Resource(handler=NFeHandler, **ad)

	urlpatterns += patterns('',
   		url(r'^api/(?P<nfe_id>\d+)/$', nfe_resource, name='api_nfe'),
   		url(r'^api/$', nfe_resource, name='api_nfe'),
	)
```
