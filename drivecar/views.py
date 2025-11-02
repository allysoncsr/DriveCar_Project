from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from .models import Veiculo, RegistroManutencao, Peca

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('drivecar:index')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    return render(request, 'drivecar/login.html')

def user_logout(request):
    logout(request)
    return redirect('drivecar:login')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password != password_confirm:
            messages.error(request, 'As senhas não coincidem.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já está em uso.')
        elif len(password) < 6:
            messages.error(request, 'A senha deve ter pelo menos 6 caracteres.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Conta criada com sucesso! Faça login.')
            return redirect('drivecar:login')
    return render(request, 'drivecar/register.html')

@login_required
def index(request):
    veiculos = Veiculo.objects.filter(usuario=request.user)
    
    context = {
        'veiculos': veiculos,
        'total_veiculos': veiculos.count(),
    }
    return render(request, 'drivecar/index.html', context)

@login_required
def cadastrar_veiculo(request):
    if request.method == 'POST':
        marca = request.POST['marca']
        modelo = request.POST['modelo']
        ano = int(request.POST['ano'])
        cor = request.POST['cor']
        combustivel = request.POST['combustivel']
        quilometragem = int(request.POST['quilometragem'])
        
        veiculo = Veiculo.objects.create(
            usuario=request.user,
            marca=marca,
            modelo=modelo,
            ano=ano,
            cor=cor,
            combustivel=combustivel,
            km_atual=quilometragem
        )
        
        messages.success(request, f'Veículo {marca} {modelo} cadastrado com sucesso!')
        return redirect('drivecar:index')
    
    return render(request, 'drivecar/cadastrar_veiculo.html')

@login_required
def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    
    if request.method == 'POST':
        veiculo.marca = request.POST['marca']
        veiculo.modelo = request.POST['modelo']
        veiculo.ano = int(request.POST['ano'])
        veiculo.cor = request.POST['cor']
        veiculo.combustivel = request.POST['combustivel']
        veiculo.km_atual = int(request.POST['quilometragem'])
        veiculo.save()
        
        messages.success(request, 'Veículo atualizado com sucesso!')
        return redirect('drivecar:index')
    
    return render(request, 'drivecar/editar_veiculo.html', {'veiculo': veiculo})

@login_required
def excluir_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    
    if request.method == 'POST':
        veiculo.delete()
        messages.success(request, 'Veículo excluído com sucesso!')
        return redirect('drivecar:index')
    
    return render(request, 'drivecar/confirmar_exclusao.html', {'veiculo': veiculo})

@login_required
def manutencao(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    pecas = Peca.objects.all()
    registros = RegistroManutencao.objects.filter(veiculo=veiculo).order_by('-data')
    
    # Organizar peças por categoria
    categorias = {}
    for peca in pecas:
        categoria_nome = peca.get_categoria_display()
        if categoria_nome not in categorias:
            categorias[categoria_nome] = []
        categorias[categoria_nome].append(peca)
    
    if request.method == 'POST':
        peca_id = request.POST['peca']
        quilometragem = int(request.POST['quilometragem'])
        custo = float(request.POST['custo'].replace(',', '.'))
        observacoes = request.POST.get('observacoes', '')
        data_realizacao = request.POST['data_realizacao']
        troca = request.POST.get('troca') == 'on'
        garantia_meses = request.POST.get('garantia_meses')
        
        # Obter peça
        peca = get_object_or_404(Peca, id=peca_id)
        
        registro = RegistroManutencao.objects.create(
            veiculo=veiculo,
            peca=peca,
            km=quilometragem,
            preco=custo,
            observacoes=observacoes,
            data=datetime.strptime(data_realizacao, '%Y-%m-%d').date(),
            troca=troca,
            garantia_meses=int(garantia_meses) if garantia_meses else None,
        )
        
        # Atualizar quilometragem do veículo se necessário
        if quilometragem > veiculo.km_atual:
            veiculo.km_atual = quilometragem
            veiculo.save()
        
        messages.success(request, 'Registro de manutenção adicionado com sucesso!')
        return redirect('drivecar:manutencao', veiculo_id=veiculo.id)
    
    context = {
        'veiculo': veiculo,
        'pecas': pecas,
        'registros': registros,
        'categorias': categorias,
        'categorias_com_alerta': [],  # Sistema de alertas desabilitado
        'categorias_tipo_alerta': {},  # Sistema de alertas desabilitado
        'pecas_com_alerta': [],  # Sistema de alertas desabilitado
    }
    return render(request, 'drivecar/manutencao.html', context)



@login_required
def excluir_registro(request, registro_id):
    registro = get_object_or_404(RegistroManutencao, id=registro_id, veiculo__usuario=request.user)
    veiculo_id = registro.veiculo.id
    
    if request.method == 'POST':
        registro.delete()
        messages.success(request, 'Registro excluído com sucesso!')
        return redirect('drivecar:manutencao', veiculo_id=veiculo_id)
    
    return render(request, 'drivecar/confirmar_exclusao_registro.html', {'registro': registro})