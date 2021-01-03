from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime
import json
from .models import Plan,Path,Subject,Subtopic,Method
from .forms import PlanForm, SubjectForm, SubtopicForm, PathForm, MethodForm, EditPlanForm, EditSubjectForm, EditSubtopicForm, EditPathForm, EditMethodForm

# Create your views here.

def home(request):
	plans = Plan.objects.filter(is_completed=False,archived=False)
	return render(request, 'studyplanner/index.html', {'plans':plans})

def my_plans(request):
	plans = Plan.objects.filter(archived=False)
	return render(request, 'studyplanner/my_plans.html', {'plans':plans})

def archived_plans(request):
	plans = Plan.objects.filter(archived=True)
	return render(request, 'studyplanner/archived_plans.html', {'plans':plans})

def create_plan(request):
	if request.method == 'POST':
		form = PlanForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			if cd['deadline'] < datetime.date.today():
				messages.error(request, "Geçersiz tamamlanma tarihi. Lütfen geçerli tarih giriniz.")
				return redirect('studyplanner:create-plan')
			else:
				new_plan = Plan.objects.create(name=cd['name'])
				new_plan.deadline = cd['deadline']
				new_plan.description = cd['description']
				new_plan.save()
				messages.success(request, "Çalışma planı başarılı şekilde eklendi. Uygulama yönteminizi ekleyebilirisniz")
				return redirect('studyplanner:plan-detail', pk=new_plan.pk)
	else:
		form = PlanForm()
	return render(request, 'studyplanner/forms/create_plan.html', {'form':form})

def edit_plan(request,pk):
	plan = get_object_or_404(Plan, pk=pk)
	title = plan.name
	if not plan.is_completed:
		if request.method == 'POST':
			form = EditPlanForm(request.POST,instance=plan)
			if form.is_valid():
				cd = form.cleaned_data
				if cd['deadline'] < datetime.date.today():
					messages.error(request, "Geçersiz tamamlanma tarihi. Lütfen geçerli tarih giriniz.")
					return redirect('studyplanner:edit-plan', pk=pk)
				else:
					plan.name = cd['name']
					plan.deadline = cd['deadline']
					plan.description = cd['description']
					plan.save()
					messages.success(request, "Çalışma Planı başarılı şekilde güncellendi.")
					return redirect('studyplanner:plan-detail', pk=pk)
		else:
			form = EditPlanForm(instance=plan)
		return render(request, 'studyplanner/forms/edit_form.html', {'form':form,'title':title})
	else:
		messages.info(request, "Tamamlanmış planlarızı günceleyemezsiniz.")
	return redirect('studyplanner:plan-detail',pk=plan.pk)

def plan_detail(request,pk):
	plan = get_object_or_404(Plan, pk=pk)
	paths = Path.objects.filter(plan=plan)
	if plan.archived:
		messages.error(request, "Plan mevcut değil")
		return redirect('home')
	subject_form = SubjectForm()
	subtopic_form = SubtopicForm()
	path_form = PathForm()
	method_form = MethodForm()
	return render(request, 'studyplanner/plan_detail.html', {'plan':plan,'paths':paths,'subject_form':subject_form,'subtopic_form':subtopic_form,'path_form':path_form,'method_form':method_form})

def archive_plan(request,pk):
	plan = get_object_or_404(Plan, pk=pk)
	if plan.archived:
		messages.info(request, "Planınız zaten kayıtlı")
	else:
		plan.archived = True
		plan.save()
		messages.success(request, "Planınız arşivlendi")
	return redirect('home')

def unarchive_plan(request,pk):
	plan = get_object_or_404(Plan, pk=pk)
	if not plan.archived:
		messages.info(request, "Arşivlenmemiş Plan")
	else:
		plan.archived = False
		plan.save()
		messages.success(request, "Arşivlenmemiş Plan")
	return redirect('home')

def complete_plan(request,pk):
	plan = get_object_or_404(Plan, pk=pk)
	if not plan.is_completed:
		plan.is_completed = True
		plan.completed_on = datetime.date.today()
		plan.save()
		messages.success(request, "{} Başarılı şekilde tamamlandı".format(plan))
	else:
		messages.error(request, "{} Zaten tamamlanmış {}".format(plan,plan.completed_on))
	return redirect('studyplanner:plan-detail',pk=plan.pk)

def print_plan(request,pk):
	plan = get_object_or_404(Plan,pk=pk)
	paths = Path.objects.filter(plan=plan)
	if plan.archived:
		messages.error(request, "Plan mevcut değil")
		return redirect('home')
	subject_form = SubjectForm()
	subtopic_form = SubtopicForm()
	path_form = PathForm()
	method_form = MethodForm()
	return render(request, 'studyplanner/print_plan.html', {'plan':plan,'paths':paths,'subject_form':subject_form,'subtopic_form':subtopic_form,'path_form':path_form,'method_form':method_form})

def add_subject(request,pk):
	plan = get_object_or_404(Plan, pk=pk)
	if not plan.archived:
		if not plan.is_completed:
			if request.method == 'POST':
				if request.is_ajax():
					dt = request.POST.get('deadline')
					dt=dt.split(" ")
					deadline = datetime.date(int(dt[0]),int(dt[1]),int(dt[2]))
					if (deadline < datetime.date.today()) and (deadline <= plan.deadline):
						messages.error(request, "Geçersiz tamamlanma tarihi. Lütfen geçerli tarih giriniz.")
					else:
						new_subject = Subject.objects.create(name=request.POST.get('name'),plan=plan)
						new_subject.description = request.POST.get('description')
						new_subject.deadline = deadline
						new_subject.save()
						messages.success(request, "{} başarılı şekilde eklendi".format(request.POST.get('name')))
		else:
			messages.error(request, "Plan zaten tamamlanmış {}".format(plan.completed_on))
	else:
		messages.error(request, "Plan mevcut değil")
	return JsonResponse({
		'success':True
	})

def edit_subject(request,pk):
	subject = get_object_or_404(Subject, pk=pk)
	title = subject.name
	if not subject.plan.archived:
		if (not subject.plan.is_completed) or (not subject.is_completed):
			if request.method == 'POST':
				form = EditSubjectForm(request.POST,instance=subject)
				if form.is_valid():
					cd = form.cleaned_data
					if (cd['deadline'] < datetime.date.today()) and (cd['deadline'] < subject.plan.deadline):
						messages.error(request, "Geçersiz bitiş tarihi. Lütfen geçerli tarih giriniz.")
						return redirect('studyplanner:edit-subject', pk=pk)
					else:
						subject.name = cd['name']
						subject.description = cd['description']
						subject.deadline = cd['deadline']
						subject.save()
						messages.success(request, "{} güncelleme başarılı".format(cd['name']))
						return redirect('studyplanner:plan-detail', pk=subject.plan.pk)
			else:
				form = EditSubjectForm(instance=subject)
			return render(request, 'studyplanner/forms/edit_form.html', {'form':form,'title':title})
		else:
			messages.error(request, "Konu/Plan zaten tamamlanmış.")
	else:
		messages.error(request, "Plan/Konu mevcut değil")
	return redirect('home')

def complete_subject(request,pk):
	subject = get_object_or_404(Subject,pk=pk)
	if not subject.plan.archived:
		if subject.is_completed:
			messages.info(request, "{} zaten tamamlanmış {}".format(subject,subject.completed_on))
		else:
			subject.is_completed = True
			subject.completed_on = datetime.date.today()
			plan = subject.plan
			plan.completed_subjects += 1
			plan.save()
			subject.save()
			messages.success(request, "{} Başarılı şekilde tamamlandı".format(subject))
		return redirect('studyplanner:plan-detail',pk=subject.plan.pk)
	else:
		messages.error(request,"Plan arşivlendi")
	return redirect('home')

def add_subtopic(request,pk):
	subject = get_object_or_404(Subject, pk=pk)
	if not subject.plan.archived:
		if not subject.is_completed:
			if request.method == 'POST':
				if request.is_ajax():
					dt = request.POST.get('deadline')
					dt=dt.split(" ")
					deadline = datetime.date(int(dt[0]),int(dt[1]),int(dt[2]))
					if (deadline < datetime.date.today()) and (deadline <= subject.deadline):
						messages.error(request, "Geçersiz bitiş tarihi. Lütfen geçerli tarih giriniz.")
					else:
						new_subtopic = Subtopic.objects.create(name=request.POST.get('name'),subject=subject)
						new_subtopic.description = request.POST.get('description')
						new_subtopic.deadline = deadline
						new_subtopic.save()
						messages.success(request, "{} başarılı şekilde eklendi".format(request.POST.get('name')))
		else:
			messages.error(request, "Konu zaten kayıtlı {}".format(subject.completed_on))
	else:
		messages.error(request, "Plan mevcut değil")
	return JsonResponse({
		'success':True
	})

def edit_subtopic(request,pk):
	subtopic = get_object_or_404(Subtopic, pk=pk)
	title = subtopic.name
	if not subtopic.subject.plan.archived:
		if not subtopic.is_completed:
			if request.method == 'POST':
				form = EditSubtopicForm(request.POST,instance=subtopic)
				if form.is_valid():
					cd = form.cleaned_data
					if (cd['deadline'] < datetime.date.today()) and (cd['deadline'] < subtopic.subject.deadline):
						messages.error(request, "Geçersiz bitiş tarihi. Lütfen geçerli tarih giriniz.")
						return redirect('studyplanner:edit-subtopic', pk=pk)
					else:
						subtopic.name = cd['name']
						subtopic.description = cd['description']
						subtopic.deadline = cd['deadline']
						subtopic.save()
						messages.success(request, "{} güncelleme başarılı".format(cd['name']))
						return redirect('studyplanner:plan-detail', pk=subtopic.subject.plan.pk)
			else:
				form = EditSubtopicForm(instance=subtopic)
			return render(request, 'studyplanner/forms/edit_form.html', {'form':form,'title':title})
		else:
			messages.error(request, "Altkonu zaten tamamlanmış. Güncelleyemezsiniz.")
	else:
		messages.error(request, "Plan/Altkonu mevcut değil")
	return redirect('home')

def complete_subtopic(request,pk):
	subtopic = get_object_or_404(Subtopic,pk=pk)
	if not subtopic.subject.plan.archived:
		if subtopic.is_completed:
			messages.info(request, "{} zaten tamamlanmış {}".format(subtopic,subtopic.completed_on))
		else:
			subtopic.is_completed = True
			subtopic.completed_on = datetime.date.today()
			subtopic.save()
			messages.success(request, "{} tamamlanma başarılı".format(subtopic))
		return redirect('studyplanner:plan-detail',pk=subtopic.subject.plan.pk)
	else:
		messages.error(request,"Plan arşivlendi")
	return redirect('home')

def add_path(request,pk):
	plan = get_object_or_404(Plan, pk=pk)
	if not plan.archived:
		if not plan.is_completed:
			if request.method == 'POST':
				if request.is_ajax():
					dt = request.POST.get('deadline')
					dt=dt.split(" ")
					deadline = datetime.date(int(dt[0]),int(dt[1]),int(dt[2]))
					if (deadline < datetime.date.today()) and (deadline <= plan.deadline):
						messages.error(request, "Geçersiz tamamlanma tarihi. Lütfen geçerli bir tarih giriniz.")
					else:
						new_path = Path.objects.create(name=request.POST.get('name'),plan=plan)
						new_path.description = request.POST.get('description')
						new_path.deadline = deadline
						new_path.save()
						messages.success(request, "{} başarılı şekilde eklendi".format(request.POST.get('name')))
		else:
			messages.error(request, "Zaten tamamlanmış plan.")
	else:
		messages.error(request, "Plan mevcut değil")
	return JsonResponse({
		'success':True
	})

def edit_path(request,pk):
	path = get_object_or_404(Path, pk=pk)
	title = path.name
	if not path.plan.archived:
		if not path.plan.is_completed:
			if request.method == 'POST':
				form = EditPathForm(request.POST,instance=path)
				if form.is_valid():
					cd = form.cleaned_data
					if (cd['deadline'] < datetime.date.today()) and (cd['deadline'] < path.plan.deadline):
						messages.error(request, "Geçersiz tamamlanma tarihi. Lütfen geçerli bir tarih giriniz.")
						return redirect('studyplanner:edit-path', pk=pk)
					else:
						path.name = cd['name']
						path.deadline = cd['deadline']
						path.description = cd['description']
						path.save()
						messages.success(request, "{} güncelleme başarılı".format(cd['name']))
						return redirect('studyplanner:plan-detail', pk=path.plan.pk)
			else:
				form = EditPathForm(instance=path)
		else:
			messages.error(request, "Plan zaten tamamlanmış düzenleme yapamazsınız.")
		return render(request, 'studyplanner/forms/edit_form.html', {'form':form,'title':title})
	else:
		messages.error(request, "Plan/Yol mevcut değil")
	return redirect('home')

def complete_path(request,pk):
	path = get_object_or_404(Path,pk=pk)
	if not path.plan.archived:
		if path.is_completed:
			messages.info(request, "{} zaten tamamlanmış {}".format(path,path.completed_on))
		else:
			path.is_completed = True
			path.completed_on = datetime.date.today()
			path.save()
			messages.success(request, "{} başarılı şekilde tamamlanmış".format(path))
		return redirect('studyplanner:plan-detail',pk=path.plan.pk)
	else:
		messages.error(request,"Plan arşivlendi")
	return redirect('home')

def add_method(request,pk,pathpk,flag):
	plan = ''
	path = get_object_or_404(Path,pk=pathpk)
	if request.method == 'POST':
		if request.is_ajax():
			dt = request.POST.get('deadline')
			dt=dt.split(" ")
			deadline = datetime.date(int(dt[0]),int(dt[1]),int(dt[2]))
			if (deadline < datetime.date.today()) and (deadline <= path.deadline):
				messages.error(request, "Geçersiz tamamlanma tarihi. Lütfen geçerli bir tarih giriniz.")
			else:
				if flag == 'sb':
					subject = get_object_or_404(Subject, pk=pk)
					plan = subject.plan
					new_method = Method.objects.create(name=request.POST.get('name'),subject=subject,path=path)
				elif flag == 'st':
					subtopic = get_object_or_404(Subtopic, pk=pk)
					plan = subtopic.subject.plan
					new_method = Method.objects.create(name=request.POST.get('name'),subtopic=subtopic,path=path)
				else:
					messages.error(request, "Yöntem eklenirken hata!")
					return JsonResponse({
						'success':True
					})
				new_method.deadline = deadline
				new_method.description = request.POST.get('description')
				new_method.save()
				if path.is_completed:
					path.is_completed = False
					path.save()
				messages.success(request, "Yöntem başarılı şekilde eklendi.")
	return JsonResponse({
		'success':True
	})

def edit_method(request,pk):
	method = get_object_or_404(Method, pk=pk)
	title = method.name
	if request.method == 'POST':
		form = EditMethodForm(request.POST,instance=method)
		if form.is_valid():
			cd = form.cleaned_data
			if (cd['deadline'] < datetime.date.today()) and (cd['deadline'] < method.path.deadline):
				messages.error(request, "Geçersiz tamamlanma tarihi. Lütfen geçerli bir tarih giriniz.")
				return redirect('studyplanner:edit-method', pk=pk)
			else:
				method.name = cd['name']
				method.deadline = cd['deadline']
				method.description = cd['description']
				method.save()
				messages.success(request, "{} tanımlanma başarılı".format(cd['name']))
				return redirect('studyplanner:plan-detail', pk=method.path.plan.pk)
	else:
		form = EditMethodForm(instance=method)
	return render(request, 'studyplanner/forms/edit_form.html', {'form':form,'title':title})

def complete_method(request,pk,flag):
	method = get_object_or_404(Method,pk=pk)
	if method.is_completed:
		messages.info(request, "{} zaten tamamlandı {}".format(method,method.completed_on))
	else:
		methods = Method.objects.filter(pk=method.pk)
		complete_methods(methods,flag)
		messages.success(request, "{} Başarılı şekilde tamamlandı".format(method))
	return redirect('studyplanner:plan-detail',pk=method.path.plan.pk)

class DeleteSubject(DeleteView):
    model = Subject
    success_url = reverse_lazy('home')

class DeleteSubtopic(DeleteView):
    model = Subtopic
    success_url = reverse_lazy('home')

class DeletePath(DeleteView):
    model = Path
    success_url = reverse_lazy('home')

class DeleteMethod(DeleteView):
    model = Method
    success_url = reverse_lazy('home')

def complete_methods(methods,flag=''):
	for method in methods:
		if not method.is_completed:
			path = method.path
			subtopic = ''
			subject = ''
			if flag == 'st':
				subtopic = method.subtopic
			elif flag == 'sb':
				subject = method.subject
			else:
				print("sadece bir yol")
			method.is_completed = True
			method.completed_on = datetime.date.today()
			method.save()
			path.completed_methods += 1
			path.save()
			if subtopic:
				subtopic.completed_methods += 1
				subtopic.save()
			if subject:
				subject.completed_methods += 1
				subject.save()
			path_complete(path)
	return 1

def path_complete(path):
	if not path.is_completed:
		methods = Method.objects.filter(path=path)
		if path.completed_methods == methods.count():
			path.is_completed = True
			path.completed_on = datetime.date.today()
			path.save()
			plan = Plan.objects.get(pk=path.plan.pk)
			plan.completed_paths += 1
			plan.save()
	return 1




