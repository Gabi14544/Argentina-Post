from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from accounts.forms import RegistroForm
    
def Registro (request:HttpRequest) ->HttpResponse:
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('accounts:login')
    else:
        form =RegistroForm()
    return render(request, 'accounts/registro.html', {"form":form})