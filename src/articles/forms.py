from django import forms
from articles.models import Articulos

class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields = ['title', 'subtitle', 'content', 'opcional_content', 'category']
        widgets ={
            'title': forms.TextInput(attrs={'class':'form-control','placeholder':'Titulo de la Noticia'}),
            'subtitle':forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control','rows':8}),
            'opcional_content':forms.Textarea(attrs={'class':'form-control','rows':4}),
            'category':forms.Select(attrs={'class':'form-select'}),
        }

        labels ={
            'title':'Titulo',
            'subtitle':'Subtitulo',
            'content':'Contenido',
            'opcional_content':'Contenido Opcional',
            'category':'Categoria',
        }
        
        

