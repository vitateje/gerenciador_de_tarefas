from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..forms import TarefaForm
from ..entidades.tarefa import Tarefa
from ..services import tarefa_service

# Create your views here.

@login_required()
def listar_tarefas(request):
    tarefas = tarefa_service.listar_tarefas(request.user)
    nome = "Assistir Semana Python" # teste para renderizar infos da View
    #ctx = { 'materia': "anothercase"}
    #msg = "ola"
    return render(request, 'tarefas/listar_tarefas.html', {'nome': nome, 'tarefas': tarefas}) # Noº parametro, pode adicionar quantos variaveis/dicionarios quiser, desde que dentro de um Dic {}

@login_required()
def cadastrar_tarefa(request):
    if request.method == "POST":
        form_tarefa = TarefaForm(request.POST)
        if form_tarefa.is_valid():
        #return redirect('listar_tarefas')
            titulo = form_tarefa.cleaned_data['titulo']
            descricao = form_tarefa.cleaned_data['descricao']
            data_expiracao = form_tarefa.cleaned_data['data_expiracao']
            prioridade = form_tarefa.cleaned_data['prioridade']
            tarefa_nova = Tarefa(titulo=titulo, descricao=descricao,
                                 data_expiracao=data_expiracao,
                                 prioridade=prioridade, usuario=request.user)
        tarefa_service.cadastrar_tarefa(tarefa_nova)
            #form_tarefa = TarefaForm()
        return redirect('listar_tarefas')    
            
    else:
        form_tarefa = TarefaForm()
    #return redirect('listar_tarefas') 
    return render(request, 'tarefas/form_tarefa.html', {"form_tarefa": TarefaForm(request.POST)})

@login_required()
def editar_tarefa(request, id):
    tarefa_bd = tarefa_service.listar_tarefa_id(id)
    if tarefa_bd.usuario != request.user:
        return HttpResponse('Não Permitido')
    form_tarefa = TarefaForm(request.POST or None, instance=tarefa_bd)
    if form_tarefa.is_valid():
        #return redirect('listar_tarefas')
        titulo = form_tarefa.cleaned_data['titulo']
        descricao = form_tarefa.cleaned_data['descricao']
        data_expiracao = form_tarefa.cleaned_data['data_expiracao']
        prioridade = form_tarefa.cleaned_data['prioridade']
        tarefa_nova = Tarefa(titulo=titulo, descricao=descricao,
                                 data_expiracao=data_expiracao,
                                 prioridade=prioridade, usuario=request.user)    
        tarefa_service.editar_tarefa(tarefa_bd, tarefa_nova)
            #form_tarefa = TarefaForm()
        return redirect('listar_tarefas')
    return render(request, 'tarefas/form_tarefa.html', {"form_tarefa": form_tarefa})

@login_required()
def remover_tarefa(request, id):
    tarefa_bd = tarefa_service.listar_tarefa_id(id)
    if tarefa_bd.usuario != request.user:
        return HttpResponse('Não Permitido')
    if request.method == "POST":
        tarefa_service.remover_tarefa(tarefa_bd)
        return redirect('listar_tarefas')
    return render(request, 'tarefas/confirma_exclusao.html', {"tarefa": tarefa_bd})
