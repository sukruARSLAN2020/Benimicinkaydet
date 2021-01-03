from django import forms
import datetime
from .models import Plan, Subject, Subtopic, Path, Method

class PlanForm(forms.Form):
	name =  forms.CharField(max_length=100,label="Plan Adı")
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))

class SubjectForm(forms.Form):
	name =  forms.CharField(max_length=100,label="Konu İsmi",widget=forms.TextInput(attrs={'class':'subjectname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))

class SubtopicForm(forms.Form):
	name =  forms.CharField(max_length=100,label="Alt Konuu Ekle",widget=forms.TextInput(attrs={'class':'subtopicname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))

class PathForm(forms.Form):
	name =  forms.CharField(max_length=100,label="Yöntem İsmi",widget=forms.TextInput(attrs={'class':'pathname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.CharField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))

class MethodForm(forms.Form):
	name =  forms.CharField(max_length=100,label="Uygulama Biçimi",widget=forms.TextInput(attrs={'class':'methodname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))

class EditPlanForm(forms.ModelForm):
	name =  forms.CharField(max_length=100,label="Plan Adı")
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))
	class Meta:
		model = Plan
		fields = ['name','deadline','description']

class EditSubjectForm(forms.ModelForm):
	name =  forms.CharField(max_length=100,label="Konu Adı",widget=forms.TextInput(attrs={'class':'subjectname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))
	class Meta:
		model = Subject
		fields = ['name','deadline','description']

class EditSubtopicForm(forms.ModelForm):
	name =  forms.CharField(max_length=100,label="Alt Konu İsmi",widget=forms.TextInput(attrs={'class':'subtopicname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))
	class Meta:
		model = Subtopic
		fields = ['name','deadline','description']

class EditPathForm(forms.ModelForm):
	name =  forms.CharField(max_length=100,label="Uygulama Biçimi",widget=forms.TextInput(attrs={'class':'pathname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.CharField(label="Bitiş Tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))
	class Meta:
		model = Path
		fields = ['name','deadline','description']

class EditMethodForm(forms.ModelForm):
	name =  forms.CharField(max_length=100,label="Yöntem İsmi",widget=forms.TextInput(attrs={'class':'methodname'}))
	description = forms.CharField(label='Tanım',widget=forms.Textarea(attrs={'placeholder':'Tanımlama Ekle','class':'description'}))
	deadline = forms.DateField(label="Bitiiş tarihi",widget=forms.SelectDateWidget(years=range(2018,2031),attrs={'placeholder':datetime.date.today}))
	class Meta:
		model = Method
		fields = ['name','deadline','description']