// Teste simples de JavaScript para debug
console.log('=== TESTE DE DEBUG ===');
console.log('Document ready state:', document.readyState);

// Aguardar DOM estar pronto
function testarBusca() {
    console.log('Testando busca...');
    
    const buscaInput = document.getElementById('busca-peca');
    const resultados = document.getElementById('resultados-busca');
    
    console.log('Input encontrado:', buscaInput);
    console.log('Resultados encontrado:', resultados);
    
    if (buscaInput) {
        console.log('Adicionando event listener...');
        buscaInput.addEventListener('input', function(e) {
            console.log('INPUT DETECTADO:', e.target.value);
        });
        
        buscaInput.addEventListener('keyup', function(e) {
            console.log('KEYUP DETECTADO:', e.target.value);
        });
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', testarBusca);
} else {
    testarBusca();
}

// Testar após 2 segundos também
setTimeout(testarBusca, 2000);