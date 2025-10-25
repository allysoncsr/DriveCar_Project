from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Veiculo, Alerta, RegistroManutencao, Peca
from django import forms
from django.urls import reverse
from django.http import HttpResponse
from django import forms
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

# Formulários simples em português
class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ["marca", "modelo", "ano", "placa", "km_atual", "combustivel"]


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


def manutencao(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    # agrupar peças por categoria para exibição
    pecas = Peca.objects.all().order_by("categoria", "nome")
    categorias = {}
    for p in pecas:
        categorias.setdefault(p.get_categoria_display(), []).append(p)
    return render(request, "drivecar/manutencao.html", {"veiculo": veiculo, "categorias": categorias})


def registros_peca(request, veiculo_id, peca_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    peca = get_object_or_404(Peca, id=peca_id)
    saved = False
    if request.method == "POST":
        form = RegistroForm(request.POST)
        # debug: log POST attempts to help troubleshooting local dev
        try:
            print(f"[DEBUG] registros_peca POST veiculo={veiculo_id} peca={peca_id} data_keys={list(request.POST.keys())}")
        except Exception:
            pass
        if form.is_valid():
            reg = form.save(commit=False)
            reg.veiculo = veiculo
            reg.peca = peca
            reg.save()
            saved = True
            # após salvar, limpar o formulário para que o fragmento retornado mostre campos vazios
            form = RegistroForm()
        else:
            # debug: mostrar erros do form no terminal
            try:
                print('[DEBUG] registro form errors:', form.errors)
            except Exception:
                pass
    else:
        form = RegistroForm()

    registros = RegistroManutencao.objects.filter(veiculo=veiculo, peca=peca).order_by("-data")
    return render(request, "drivecar/registros_peca_fragment.html", {"veiculo": veiculo, "peca": peca, "registros": registros, "form": form, "saved": saved})


@csrf_exempt
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

    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
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

def index(request):
    veiculos = Veiculo.objects.all()
    return render(request, "drivecar/index.html", {"veiculos": veiculos})

def cadastrar_veiculo(request):
    if request.method == "POST":
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            # Se a requisição vier via HTMX, retorne um HX-Redirect header
            if request.headers.get("HX-Request") == "true":
                resp = HttpResponse()
                resp["HX-Redirect"] = reverse("drivecar:index")
                return resp
            return redirect("drivecar:index")
    else:
        form = VeiculoForm()
    return render(request, "drivecar/cadastrar_veiculo.html", {"form": form})

def lista_alertas(request):
    alertas = Alerta.objects.select_related("veiculo").order_by("data_prevista", "km_previsto")
    return render(request, "drivecar/alertas.html", {"alertas": alertas})

def registros_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    registros = RegistroManutencao.objects.filter(veiculo=veiculo).select_related("peca").order_by("-data")
    # este template pode ser retornado como fragmento HTMX
    return render(request, "drivecar/registros_fragment.html", {"veiculo": veiculo, "registros": registros})
