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
    from .models import Marca, Modelo, Versao
    
    if request.method == 'POST':
        marca_id = request.POST['marca']
        modelo_id = request.POST['modelo']
        versao_id = request.POST.get('versao')
        ano = int(request.POST['ano'])
        placa = request.POST.get('placa', '')
        combustivel = request.POST['combustivel']
        km_atual = int(request.POST['km_atual']) if request.POST['km_atual'] else 0
        
        # Obter instâncias dos objetos
        marca = get_object_or_404(Marca, id=marca_id)
        modelo = get_object_or_404(Modelo, id=modelo_id)
        versao = get_object_or_404(Versao, id=versao_id) if versao_id else None
        
        veiculo = Veiculo.objects.create(
            usuario=request.user,
            marca=marca,
            modelo=modelo,
            versao=versao,
            ano=ano,
            placa=placa,
            combustivel=combustivel,
            km_atual=km_atual
        )
        
        messages.success(request, f'Veículo {marca.nome} {modelo.nome} cadastrado com sucesso!')
        return redirect('drivecar:index')
    
    # Buscar marcas ativas para o template
    marcas = Marca.objects.filter(ativo=True).order_by('nome')
    
    context = {
        'marcas': marcas,
    }
    return render(request, 'drivecar/cadastrar_veiculo.html', context)

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
    from .models import Servico, LocalLavagem
    from django.core.paginator import Paginator
    from django.db import models
    
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    pecas = Peca.objects.all()
    servicos = Servico.objects.all()
    locais_lavagem = LocalLavagem.objects.filter(usuario=request.user, ativo=True).order_by('nome')
    
    # Filtros
    filtro_tipo = request.GET.get('tipo', '')
    filtro_troca = request.GET.get('troca', '')
    filtro_categoria = request.GET.get('categoria', '')
    filtro_periodo = request.GET.get('periodo', '')
    filtro_data_inicio = request.GET.get('data_inicio', '')
    filtro_data_fim = request.GET.get('data_fim', '')
    
    # Query base
    registros_qs = RegistroManutencao.objects.filter(veiculo=veiculo)
    
    # Aplicar filtros
    if filtro_tipo:
        registros_qs = registros_qs.filter(tipo=filtro_tipo)
    
    if filtro_troca == 'sim':
        registros_qs = registros_qs.filter(troca=True)
    elif filtro_troca == 'nao':
        registros_qs = registros_qs.filter(troca=False)
    
    if filtro_categoria:
        registros_qs = registros_qs.filter(
            models.Q(peca__categoria=filtro_categoria) | 
            models.Q(servico__categoria=filtro_categoria) |
            models.Q(tipo='lavagem')  # Lavagem sempre na categoria "Lavagem"
        )
    
    # Filtros de data/período
    from datetime import datetime, timedelta
    from django.utils import timezone
    
    if filtro_periodo:
        hoje = timezone.now().date()
        
        if filtro_periodo == 'ultimo_mes':
            data_inicio = hoje - timedelta(days=30)
            registros_qs = registros_qs.filter(data__gte=data_inicio)
        elif filtro_periodo == 'ultimos_3_meses':
            data_inicio = hoje - timedelta(days=90)
            registros_qs = registros_qs.filter(data__gte=data_inicio)
        elif filtro_periodo == 'ultimos_6_meses':
            data_inicio = hoje - timedelta(days=180)
            registros_qs = registros_qs.filter(data__gte=data_inicio)
        elif filtro_periodo == 'ultimo_ano':
            data_inicio = hoje - timedelta(days=365)
            registros_qs = registros_qs.filter(data__gte=data_inicio)
        elif filtro_periodo == 'personalizado':
            if filtro_data_inicio:
                registros_qs = registros_qs.filter(data__gte=filtro_data_inicio)
            if filtro_data_fim:
                registros_qs = registros_qs.filter(data__lte=filtro_data_fim)
    
    registros_qs = registros_qs.order_by('-data', '-km')
    
    # Paginação
    paginator = Paginator(registros_qs, 5)  # 5 registros por página
    page_number = request.GET.get('page', 1)
    registros = paginator.get_page(page_number)
    
    # Organizar peças por categoria
    categorias_pecas = {}
    for peca in pecas:
        categoria_nome = peca.get_categoria_display()
        if categoria_nome not in categorias_pecas:
            categorias_pecas[categoria_nome] = []
        categorias_pecas[categoria_nome].append(peca)
    
    # Organizar serviços por categoria
    categorias_servicos = {}
    for servico in servicos:
        categoria_nome = servico.get_categoria_display()
        if categoria_nome not in categorias_servicos:
            categorias_servicos[categoria_nome] = []
        categorias_servicos[categoria_nome].append(servico)
    
    if request.method == 'POST':
        tipo_item = request.POST['tipo_item']  # 'peca' ou 'servico'
        quilometragem = int(request.POST['quilometragem'])
        custo = float(request.POST['custo'].replace(',', '.'))
        observacoes = request.POST.get('observacoes', '')
        data_realizacao = request.POST['data_realizacao']
        troca = request.POST.get('troca') == 'on'
        garantia_meses = request.POST.get('garantia_meses')
        
        # Criar registro baseado no tipo
        if tipo_item == 'peca':
            peca_id = request.POST['peca']
            peca = get_object_or_404(Peca, id=peca_id)
            
            registro = RegistroManutencao.objects.create(
                veiculo=veiculo,
                tipo='peca',
                peca=peca,
                km=quilometragem,
                preco=custo,
                observacoes=observacoes,
                data=datetime.strptime(data_realizacao, '%Y-%m-%d').date(),
                troca=troca,
                garantia_meses=int(garantia_meses) if garantia_meses else None,
            )
            messages.success(request, f'Peça "{peca.nome}" registrada com sucesso!')
            
        elif tipo_item == 'servico':
            servico_id = request.POST['servico']
            servico = get_object_or_404(Servico, id=servico_id)
            
            registro = RegistroManutencao.objects.create(
                veiculo=veiculo,
                tipo='servico',
                servico=servico,
                km=quilometragem,
                preco=custo,
                observacoes=observacoes,
                data=datetime.strptime(data_realizacao, '%Y-%m-%d').date(),
                troca=troca,
                garantia_meses=int(garantia_meses) if garantia_meses else None,
            )
            messages.success(request, f'Serviço "{servico.nome}" registrado com sucesso!')
            
        elif tipo_item == 'lavagem':
            tipo_lavagem = request.POST['tipo_lavagem']
            local_lavagem = request.POST.get('local_lavagem')
            
            # Se foi selecionado "novo local", criar o local e usar seu valor
            if local_lavagem == 'novo_local':
                novo_local_nome = request.POST.get('novo_local', '')
                if novo_local_nome:
                    # Criar novo local personalizado
                    local_obj, created = LocalLavagem.objects.get_or_create(
                        usuario=request.user,
                        nome=novo_local_nome,
                        defaults={'ativo': True}
                    )
                    local_lavagem = novo_local_nome
                    if created:
                        messages.info(request, f'Novo local "{novo_local_nome}" adicionado à sua lista!')
                else:
                    messages.error(request, 'Por favor, informe o nome do novo local.')
                    return redirect('drivecar:manutencao', veiculo_id=veiculo.id)
            
            registro = RegistroManutencao.objects.create(
                veiculo=veiculo,
                tipo='lavagem',
                tipo_lavagem=tipo_lavagem,
                local_lavagem=local_lavagem,
                km=quilometragem,
                preco=custo,
                observacoes=observacoes,
                data=datetime.strptime(data_realizacao, '%Y-%m-%d').date(),
                troca=False,  # Lavagem não tem troca
                garantia_meses=None,  # Lavagem não tem garantia
            )
            # Obter o nome do tipo de lavagem para a mensagem
            tipo_nome = dict(RegistroManutencao.TIPO_LAVAGEM_CHOICES).get(tipo_lavagem, tipo_lavagem)
            messages.success(request, f'Lavagem "{tipo_nome}" registrada com sucesso!')
        
        # Atualizar quilometragem do veículo se necessário
        if quilometragem > veiculo.km_atual:
            veiculo.km_atual = quilometragem
            veiculo.save()
        
        return redirect('drivecar:manutencao', veiculo_id=veiculo.id)
    
    # Obter todas as categorias únicas para o filtro
    categorias_filtro = set()
    for peca in pecas:
        categorias_filtro.add((peca.categoria, peca.get_categoria_display()))
    for servico in servicos:
        categorias_filtro.add((servico.categoria, servico.get_categoria_display()))
    
    # Adicionar categoria "Lavagem" se houver registros de lavagem
    if RegistroManutencao.objects.filter(veiculo=veiculo, tipo='lavagem').exists():
        categorias_filtro.add(('lavagem', 'Lavagem'))
    
    categorias_filtro = sorted(list(categorias_filtro), key=lambda x: x[1])
    
    context = {
        'veiculo': veiculo,
        'pecas': pecas,
        'servicos': servicos,
        'registros': registros,
        'categorias_pecas': categorias_pecas,
        'categorias_servicos': categorias_servicos,
        'categorias_filtro': categorias_filtro,
        'locais_lavagem': locais_lavagem,
        'filtro_tipo': filtro_tipo,
        'filtro_troca': filtro_troca,
        'filtro_categoria': filtro_categoria,
        'filtro_periodo': filtro_periodo,
        'filtro_data_inicio': filtro_data_inicio,
        'filtro_data_fim': filtro_data_fim,
        'total_registros': paginator.count if 'paginator' in locals() else 0,
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

# APIs para select cascateado
@login_required
def api_modelos(request, marca_id):
    """API para buscar modelos de uma marca"""
    from django.http import JsonResponse
    from .models import Modelo
    
    try:
        modelos = Modelo.objects.filter(marca_id=marca_id, ativo=True).order_by('nome')
        data = {
            'modelos': [
                {
                    'id': modelo.id,
                    'nome': modelo.nome
                }
                for modelo in modelos
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required  
def excluir_local_lavagem(request, local_id):
    """View para excluir um local de lavagem personalizado"""
    from .models import LocalLavagem
    
    local = get_object_or_404(LocalLavagem, id=local_id, usuario=request.user)
    
    if request.method == 'POST':
        nome_local = local.nome
        local.delete()
        messages.success(request, f'Local "{nome_local}" removido com sucesso!')
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)  
def api_versoes(request, modelo_id):
    """API para buscar versões de um modelo"""
    from django.http import JsonResponse
    from .models import Versao
    
    try:
        versoes = Versao.objects.filter(modelo_id=modelo_id, ativo=True).order_by('nome')
        data = {
            'versoes': [
                {
                    'id': versao.id,
                    'nome': versao.nome,
                    'motor': versao.motor or '',
                    'combustivel': versao.combustivel or ''
                }
                for versao in versoes
            ]
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required  
def excluir_local_lavagem(request, local_id):
    """View para excluir um local de lavagem personalizado"""
    from .models import LocalLavagem
    
    local = get_object_or_404(LocalLavagem, id=local_id, usuario=request.user)
    
    if request.method == 'POST':
        nome_local = local.nome
        local.delete()
        messages.success(request, f'Local "{nome_local}" removido com sucesso!')
        return JsonResponse({'success': True})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)