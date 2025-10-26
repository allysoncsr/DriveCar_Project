from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Veiculo, RegistroManutencao, Peca
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

# Formulários simples em português
class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ["marca", "modelo", "versao", "ano", "placa", "km_atual", "combustivel"]


class RegistroForm(forms.ModelForm):
    class Meta:
        model = RegistroManutencao
        fields = ["data", "km", "preco", "troca", "garantia_meses", "observacoes"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date", "class": "input"}),
            "km": forms.NumberInput(attrs={"class": "input", "min": "0"}),
            "preco": forms.NumberInput(attrs={"class": "input", "step": "0.01", "min": "0"}),
            "troca": forms.CheckboxInput(attrs={"class": "checkbox"}),
            "garantia_meses": forms.NumberInput(attrs={"class": "input", "min": "0"}),
            "observacoes": forms.Textarea(attrs={"class": "textarea", "rows": 2}),
        }


@login_required
def manutencao(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    # agrupar peças por categoria para exibição
    pecas = Peca.objects.all().order_by("categoria", "nome")
    categorias = {}
    for p in pecas:
        categorias.setdefault(p.get_categoria_display(), []).append(p)
    
    # Obter alertas específicos deste veículo e criar mapeamento por peça
    alertas_veiculo = veiculo.get_alertas_ativos()
    alertas_por_peca = {}
    categorias_com_alerta = set()
    categorias_tipo_alerta = {}  # Mapear categoria -> tipo de alerta mais crítico
    pecas_com_alerta = []
    
    # Hierarquia de criticidade dos alertas
    criticidade = {'urgente': 3, 'atencao': 2, 'baixo': 1}
    
    for alerta in alertas_veiculo:
        # Encontrar a peça correspondente ao alerta
        peca_nome = alerta['item']
        peca_completa = alerta.get('peca_completa', peca_nome)
        
        # Tentar encontrar pela peça completa primeiro, depois pela simplificada
        peca = None
        try:
            # Para óleo, priorizar a categoria Motor
            if 'óleo' in peca_nome.lower() or 'oleo' in peca_nome.lower():
                peca = Peca.objects.filter(nome=peca_completa, categoria='motor').first()
            
            if not peca:
                peca = Peca.objects.filter(nome=peca_completa).first()
        except:
            pass
            
        if not peca:
            try:
                # Buscar por nome que contenha a palavra-chave
                if 'óleo' in peca_nome.lower() or 'oleo' in peca_nome.lower():
                    peca = Peca.objects.filter(nome__icontains=peca_nome, categoria='motor').first()
                
                if not peca:
                    peca = Peca.objects.filter(nome__icontains=peca_nome).first()
            except:
                pass
        
        if peca:
            alertas_por_peca[peca.id] = alerta
            categoria = peca.get_categoria_display()
            categorias_com_alerta.add(categoria)
            pecas_com_alerta.append(peca.id)
            
            # Determinar o tipo de alerta mais crítico para a categoria
            tipo_atual = alerta['urgencia']  # Corrigido: usar 'urgencia' em vez de 'tipo'
            if categoria not in categorias_tipo_alerta:
                categorias_tipo_alerta[categoria] = tipo_atual
            else:
                if criticidade.get(tipo_atual, 0) > criticidade.get(categorias_tipo_alerta[categoria], 0):
                    categorias_tipo_alerta[categoria] = tipo_atual
    
    return render(request, "drivecar/manutencao.html", {
        "veiculo": veiculo, 
        "categorias": categorias,
        "alertas_por_peca": alertas_por_peca,
        "categorias_com_alerta": categorias_com_alerta,
        "categorias_tipo_alerta": categorias_tipo_alerta,
        "pecas_com_alerta": pecas_com_alerta
    })


@login_required
def buscar_pecas(request):
    """Busca rápida de peças por nome via AJAX"""
    if request.method == 'GET':
        termo = request.GET.get('q', '').strip()
        veiculo_id = request.GET.get('veiculo_id')
        
        if not termo or len(termo) < 2:
            return JsonResponse({'pecas': []})
        
        # Buscar peças que contenham o termo no nome
        pecas = Peca.objects.filter(
            nome__icontains=termo
        ).order_by('categoria', 'nome')[:10]  # Limitar a 10 resultados
        
        resultados = []
        for peca in pecas:
            resultados.append({
                'id': peca.id,
                'nome': peca.nome,
                'categoria': peca.get_categoria_display(),
                'url': reverse('drivecar:registros_peca', args=[veiculo_id, peca.id])
            })
        
        return JsonResponse({'pecas': resultados})
    
    return JsonResponse({'error': 'Método não permitido'}, status=405)

@login_required  
def registros_peca(request, veiculo_id, peca_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    peca = get_object_or_404(Peca, id=peca_id)
    saved = False
    if request.method == "POST":
        print(f"[DEBUG] ===== INICIANDO PROCESSAMENTO =====")
        print(f"[DEBUG] POST original: {dict(request.POST)}")
        
        # Processar dados formatados antes de criar o form
        post_data = request.POST.copy()
        
        # Processar KM formatado (ex: "123,456" -> 123.456)
        if 'km' in post_data:
            km_valor = post_data['km']
            print(f"[DEBUG] KM original: '{km_valor}'")
            if km_valor:
                try:
                    # Remove pontos e vírgulas e converte para número
                    km_limpo = km_valor.replace('.', '').replace(',', '.')
                    km_float = float(km_limpo)
                    post_data['km'] = str(int(km_float))  # KM deve ser inteiro
                    print(f"[DEBUG] KM convertido: '{km_valor}' -> '{post_data['km']}'")
                except ValueError as e:
                    print(f"[DEBUG] Erro ao converter KM: {km_valor} - {e}")
        
        # Processar Preço formatado (ex: "R$ 1.234,56" -> 1234.56)
        if 'preco' in post_data:
            preco_valor = post_data['preco']
            print(f"[DEBUG] Preço original: '{preco_valor}'")
            if preco_valor:
                try:
                    # Limpar e converter preço
                    preco_limpo = preco_valor.replace('R$', '').replace(' ', '').strip()
                    
                    # Se tem formato brasileiro (pontos para milhares, vírgula para decimal)
                    if ',' in preco_limpo:
                        if '.' in preco_limpo:
                            # Formato: 1.234,56 (brasileiro)
                            preco_limpo = preco_limpo.replace('.', '').replace(',', '.')
                        else:
                            # Formato: 1234,56 (vírgula apenas para decimal)
                            preco_limpo = preco_limpo.replace(',', '.')
                    # Se só tem ponto, assumir decimal americano (1234.56)
                    
                    preco_float = float(preco_limpo)
                    post_data['preco'] = str(preco_float)
                    print(f"[DEBUG] Preço convertido: '{preco_valor}' -> '{post_data['preco']}'")
                except ValueError as e:
                    print(f"[DEBUG] Erro ao converter preço: {preco_valor} - {e}")
        
        print(f"[DEBUG] Dados finais para formulário: {dict(post_data)}")
        
        form = RegistroForm(post_data)
        print(f"[DEBUG] Formulário criado. Validando...")
        
        if form.is_valid():
            print(f"[DEBUG] Formulário VÁLIDO. Salvando...")
            reg = form.save(commit=False)
            reg.veiculo = veiculo
            reg.peca = peca
            reg.save()
            saved = True
            print(f"[DEBUG] Registro salvo com ID: {reg.id}, Preço: {reg.preco}")
            # após salvar, limpar o formulário para que o fragmento retornado mostre campos vazios
            form = RegistroForm()
        else:
            print(f'[DEBUG] Formulário INVÁLIDO. Erros: {form.errors}')
            print(f'[DEBUG] Dados limpos do form: {form.cleaned_data if hasattr(form, "cleaned_data") else "N/A"}')
    else:
        form = RegistroForm()

    registros = RegistroManutencao.objects.filter(veiculo=veiculo, peca=peca).order_by("-data")
    
    # Verificar se há alerta para esta peça
    alertas_veiculo = veiculo.get_alertas_ativos()
    alerta_peca = None
    for alerta in alertas_veiculo:
        if alerta['item'] == peca.nome:
            alerta_peca = alerta
            break
    
    return render(request, "drivecar/registros_peca_fragment.html", {
        "veiculo": veiculo, 
        "peca": peca, 
        "registros": registros, 
        "form": form, 
        "saved": saved,
        "alerta_peca": alerta_peca
    })


@csrf_exempt
@login_required
def api_registro_create(request, veiculo_id, peca_id):
    """API simples para criar um RegistroManutencao via JSON POST.
    Espera JSON com chaves: data (YYYY-MM-DD), km (int), preco (decimal), troca (bool), garantia_meses (int|null), observacoes (string)
    Retorna JSON com sucesso e id do registro criado ou erros.
    """
    if request.method != 'POST':
        return HttpResponseBadRequest('Esperado POST')
    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        return HttpResponseBadRequest(f'JSON inválido: {e}')

    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    peca = get_object_or_404(Peca, id=peca_id)

    # mapear campos
    data = payload.get('data')
    km = payload.get('km')
    preco = payload.get('preco')
    troca = payload.get('troca', False)
    garantia_meses = payload.get('garantia_meses')
    observacoes = payload.get('observacoes', '')

    # validações simples
    errors = {}
    if not data:
        errors['data'] = 'Campo obrigatório'
    if km is None:
        errors['km'] = 'Campo obrigatório'
    if preco is None:
        errors['preco'] = 'Campo obrigatório'

    if errors:
        return JsonResponse({'success': False, 'errors': errors}, status=400)

    # criar registro
    try:
        reg = RegistroManutencao.objects.create(
            veiculo=veiculo,
            peca=peca,
            data=data,
            km=int(km),
            preco=preco,
            troca=bool(troca),
            garantia_meses=(int(garantia_meses) if garantia_meses not in (None, '') else None),
            observacoes=observacoes,
        )
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'success': True, 'id': reg.id})

@login_required
def index(request):
    # Filtrar apenas os veículos do usuário logado
    veiculos = Veiculo.objects.filter(usuario=request.user)
    
    # Coletar alertas de todos os veículos
    alertas_urgentes = []
    for veiculo in veiculos:
        alertas_veiculo = veiculo.get_alertas_ativos()
        # Adicionar apenas os 2 primeiros alertas mais urgentes por veículo
        for alerta in alertas_veiculo[:2]:
            alerta['veiculo'] = veiculo
            alertas_urgentes.append(alerta)
    
    # Ordenar todos os alertas por urgência
    alertas_urgentes.sort(key=lambda x: (x['urgencia'] != 'urgente', x['km_restante']))
    
    # Limitar a 4 alertas na tela principal
    alertas_urgentes = alertas_urgentes[:4]
    
    return render(request, "drivecar/index.html", {
        "veiculos": veiculos,
        "alertas_urgentes": alertas_urgentes
    })

@login_required
def cadastrar_veiculo(request):
    from .models import Marca, Modelo, Versao
    
    if request.method == "POST":
        # Processar dados do formulário manualmente para lidar com os ForeignKeys
        marca_id = request.POST.get('marca')
        modelo_id = request.POST.get('modelo')
        versao_id = request.POST.get('versao')
        ano = request.POST.get('ano')
        placa = request.POST.get('placa')
        km_atual = request.POST.get('km_atual')
        combustivel = request.POST.get('combustivel')
        
        # Validação básica
        errors = []
        if not marca_id:
            errors.append("Marca é obrigatória")
        if not modelo_id:
            errors.append("Modelo é obrigatório")
        if not ano:
            errors.append("Ano é obrigatório")
        if not placa:
            errors.append("Placa é obrigatória")
            
        if not errors:
            try:
                # Buscar as instâncias dos ForeignKeys
                marca = Marca.objects.get(id=marca_id) if marca_id else None
                modelo = Modelo.objects.get(id=modelo_id) if modelo_id else None
                versao = Versao.objects.get(id=versao_id) if versao_id else None
                
                # Criar o veículo
                veiculo = Veiculo.objects.create(
                    usuario=request.user,
                    marca=marca,
                    modelo=modelo,
                    versao=versao,
                    ano=int(ano),
                    placa=placa.upper(),
                    km_atual=int(km_atual) if km_atual else 0,
                    combustivel=combustivel
                )
                
                messages.success(request, f"Veículo {marca.nome} {modelo.nome} cadastrado com sucesso!")
                
                # Se a requisição vier via HTMX, retorne um HX-Redirect header
                if request.headers.get("HX-Request") == "true":
                    resp = HttpResponse()
                    resp["HX-Redirect"] = reverse("drivecar:index")
                    return resp
                return redirect("drivecar:index")
                
            except (Marca.DoesNotExist, Modelo.DoesNotExist, Versao.DoesNotExist) as e:
                errors.append("Erro ao processar seleção de veículo")
            except ValueError as e:
                errors.append("Dados inválidos fornecidos")
        
        # Se há erros, mostrar na página
        for error in errors:
            messages.error(request, error)
    
    # Carregar marcas para o dropdown
    marcas = Marca.objects.filter(ativo=True).order_by('nome')
    
    return render(request, "drivecar/cadastrar_veiculo.html", {
        "marcas": marcas
    })



@login_required
def registros_veiculo(request, veiculo_id):
    # Garantir que o usuário só acesse seus próprios veículos
    veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
    registros = RegistroManutencao.objects.filter(veiculo=veiculo).select_related("peca").order_by("-data")
    # este template pode ser retornado como fragmento HTMX
    return render(request, "drivecar/registros_fragment.html", {"veiculo": veiculo, "registros": registros})



@login_required
def excluir_veiculo(request, veiculo_id):
    """Exclui um veículo e todos os seus registros associados"""
    if request.method == "POST":
        veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
        # Os registros serão excluídos automaticamente devido ao CASCADE no modelo
        veiculo.delete()
        
        # Se a requisição vier via HTMX, retorne um HX-Redirect header
        if request.headers.get("HX-Request") == "true":
            resp = HttpResponse()
            resp["HX-Redirect"] = reverse("drivecar:index")
            return resp
        return redirect("drivecar:index")
    else:
        # GET request - página de confirmação
        veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
        return render(request, "drivecar/confirmar_exclusao.html", {"veiculo": veiculo})

@login_required
def excluir_registro(request, veiculo_id, peca_id, registro_id):
    """Exclui um registro de manutenção específico - Exclusão Direta"""
    if request.method == "POST":
        try:
            veiculo = get_object_or_404(Veiculo, id=veiculo_id, usuario=request.user)
            peca = get_object_or_404(Peca, id=peca_id)
            registro = get_object_or_404(RegistroManutencao, id=registro_id, veiculo=veiculo, peca=peca)
            
            print(f"🗑️ Excluindo registro {registro_id} da peça {peca.nome}")
            
            # Excluir o registro
            registro.delete()
            
            print(f"✅ Registro {registro_id} excluído com sucesso!")
            
            # Debug: verificar headers HTMX
            hx_request = request.headers.get('HX-Request')
            has_htmx_attr = hasattr(request, 'htmx') and request.htmx
            print(f"🔍 Headers de debug:")
            print(f"   HX-Request: {hx_request}")
            print(f"   X-Requested-With: {request.headers.get('X-Requested-With')}")
            print(f"   Content-Type: {request.headers.get('Content-Type')}")
            print(f"   request.htmx: {has_htmx_attr}")
            print(f"   User-Agent: {request.headers.get('User-Agent', 'N/A')[:50]}...")
            
            # Para HTMX/AJAX: retornar resposta vazia (200 OK)
            if hx_request == 'true' or has_htmx_attr or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print("⚡ HTMX/AJAX detectado - linha será removida automaticamente")
                return HttpResponse("", status=200)
            
            # Requisição normal: redirecionar para a página de manutenção
            print("↩️ Requisição normal - redirecionando para página de manutenção...")
            return redirect("drivecar:manutencao", veiculo_id=veiculo_id)
            
        except Exception as e:
            print(f"❌ ERRO ao excluir registro: {e}")
            if request.headers.get("HX-Request") == "true":
                return HttpResponse(f"Erro: {e}", status=500)
            return HttpResponse(f"Erro ao excluir registro: {e}", status=500)
    
    return HttpResponseBadRequest("❌ Método não permitido")


# =================================== 
# VIEWS DE AUTENTICAÇÃO
# ===================================

def login_view(request):
    """View de login personalizada"""
    if request.user.is_authenticated:
        return redirect('drivecar:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Mensagem será mostrada na página principal, não aqui
                return redirect('drivecar:index')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    return render(request, 'drivecar/login.html')


def logout_view(request):
    """View de logout"""
    user_name = request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f'Até logo, {user_name}!')
    return redirect('drivecar:login')


def register_view(request):
    """View de cadastro de usuário"""
    if request.user.is_authenticated:
        return redirect('drivecar:index')
    
    if request.method == 'POST':
        # Verificar se é uma requisição AJAX (do modal)
        is_ajax = (request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
                  'application/json' in request.headers.get('Accept', ''))
        
        if is_ajax:
            # Processar dados do modal
            usuario = request.POST.get('usuario')
            email = request.POST.get('email')
            senha = request.POST.get('senha')
            repetir_senha = request.POST.get('repetir_senha')
            
            errors = {}
            
            # Validações AJAX
            if not usuario:
                errors['usuario'] = 'Campo obrigatório'
            elif User.objects.filter(username=usuario).exists():
                errors['usuario'] = 'Este usuário já existe'
            
            if not email:
                errors['email'] = 'Campo obrigatório'
            elif User.objects.filter(email=email).exists():
                errors['email'] = 'Este email já está cadastrado'
            
            if not senha:
                errors['senha'] = 'Campo obrigatório'
            elif len(senha) < 6:
                errors['senha'] = 'A senha deve ter pelo menos 6 caracteres'
            
            if not repetir_senha:
                errors['repetir_senha'] = 'Campo obrigatório'
            elif senha != repetir_senha:
                errors['repetir_senha'] = 'As senhas não coincidem'
            
            if errors:
                return JsonResponse({
                    'success': False,
                    'errors': errors
                })
            
            # Criar usuário
            try:
                user = User.objects.create_user(
                    username=usuario,
                    email=email,
                    password=senha,
                    first_name=usuario
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Conta criada com sucesso! Você será redirecionado para fazer login.'
                })
                
            except Exception as e:
                return JsonResponse({
                    'success': False,
            'errors': {'general': f'Erro ao criar conta: {str(e)}'}
        })


@login_required
def get_modelos_by_marca(request, marca_id):
    """API para buscar modelos de uma marca específica"""
    try:
        from .models import Modelo
        modelos = Modelo.objects.filter(marca_id=marca_id, ativo=True).values('id', 'nome')
        return JsonResponse({'modelos': list(modelos)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required  
def get_versoes_by_modelo(request, modelo_id):
    """API para buscar versões de um modelo específico"""
    try:
        from .models import Versao
        versoes = Versao.objects.filter(modelo_id=modelo_id, ativo=True).values('id', 'nome', 'motor', 'combustivel')
        return JsonResponse({'versoes': list(versoes)})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

