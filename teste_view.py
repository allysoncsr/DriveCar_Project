from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Peca
from django.urls import reverse

def teste_busca_simples(request):
    """Teste simples sem autenticação"""
    termo = request.GET.get('q', '').strip()
    veiculo_id = request.GET.get('veiculo_id', '1')
    
    if not termo:
        return JsonResponse({'status': 'erro', 'msg': 'Termo não fornecido'})
    
    # Buscar peças
    pecas = Peca.objects.filter(nome__icontains=termo)[:5]
    
    resultados = []
    for peca in pecas:
        resultados.append({
            'nome': peca.nome,
            'categoria': peca.get_categoria_display(),
            'url': f'/veiculo/{veiculo_id}/peca/{peca.id}/registros/'
        })
    
    return JsonResponse({
        'status': 'ok',
        'termo': termo,
        'veiculo_id': veiculo_id,
        'total': len(resultados),
        'pecas': resultados
    })