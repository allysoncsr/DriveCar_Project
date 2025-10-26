// Teste simples para verificar se o sino funciona
console.log('🚀 Script de teste carregado');

// Função de teste mais simples
function testarSino(pecaId) {
    console.log('🔔 TESTE FUNÇÃO CHAMADA - ID:', pecaId);
    
    var sino = document.getElementById('sino-' + pecaId);
    if (!sino) {
        console.error('❌ Sino não encontrado');
        alert('❌ Sino não encontrado!');
        return;
    }
    
    console.log('✅ Sino encontrado:', sino);
    
    // Alternar classe ativo
    if (sino.classList.contains('ativo')) {
        sino.classList.remove('ativo');
        console.log('🔕 Classe REMOVIDA');
        alert('🔕 Sino DESATIVADO');
    } else {
        sino.classList.add('ativo');
        console.log('🔔 Classe ADICIONADA');
        alert('🔔 Sino ATIVADO');
    }
    
    console.log('🔔 Classes finais:', sino.className);
}

// Teste direto
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM carregado - testando sinos...');
    
    var sinos = document.querySelectorAll('.sino-alerta');
    console.log('🔔 Encontrados', sinos.length, 'sinos');
    
    sinos.forEach(function(sino, index) {
        console.log('🔔 Sino', index + 1, ':', sino.id, '- Classes:', sino.className);
    });
});