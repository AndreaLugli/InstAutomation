from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from social_auth.models import UserSocialAuth

from .models import ListaTag
from .forms import TagForm

MIOIP = settings.IP_LOCALE
CLIENT_SECRET = settings.INSTAGRAM_CLIENT_SECRET

@login_required(login_url='/login')
def aggiungi_tag(request):
	instance = UserSocialAuth.objects.get(user=request.user, provider='instagram')
	tag_form = TagForm(request.POST)
	if tag_form.is_valid():
		testo_tag = tag_form.cleaned_data['keyword']
		testo_tag = testo_tag.replace("#","")
		
		esistenza_tag = ListaTag.objects.filter(keyword = testo_tag, utente = instance).exists()
		
		if esistenza_tag is False:
			nuovo_tag = ListaTag(keyword = testo_tag, utente = instance)
			nuovo_tag.save()
			
			return HttpResponse()
		else:
			return HttpResponseRedirect('/')
 
@login_required(login_url='/login') 
def rimuovi_tag(request):
	instance = UserSocialAuth.objects.get(user=request.user, provider='instagram')
	
	nome_tag = request.POST['keyword']
	
	tag_da_eliminare = ListaTag.objects.get(keyword = nome_tag, utente = instance)
	tag_da_eliminare.delete()

	return HttpResponse()
	

 


