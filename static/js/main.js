// Arquivo JS mínimo para testar carregamento de estáticos
console.log('DriveCar static loaded');

// Accordion manager (categorias e peças)
(function(){
	function onDocClick(e){
		// Categoria toggle
		const catBtn = e.target.closest('.categoria-toggle');
		if(catBtn){
			e.preventDefault();
			const target = document.querySelector(catBtn.dataset.target);
			if(!target) return;

			// fechar outras categorias
			document.querySelectorAll('.categoria-body.open').forEach(function(el){
				if(el !== target){ el.style.maxHeight = null; el.classList.remove('open'); el.classList.add('collapse'); el.previousElementSibling?.setAttribute('aria-expanded','false'); }
			});

			// toggle atual
			if(target.classList.contains('open')){
				target.style.maxHeight = null;
				target.classList.remove('open');
				target.classList.add('collapse');
				catBtn.setAttribute('aria-expanded','false');
				return;
			}

			// abrir
			target.classList.remove('collapse');
			target.classList.add('open');
			catBtn.setAttribute('aria-expanded','true');
			target.style.maxHeight = '0px';
			requestAnimationFrame(function(){ target.style.maxHeight = target.scrollHeight + 'px'; });
			return;
		}

		// Peca link behavior
		const a = e.target.closest('.peca-link');
		if(!a) return;
		e.preventDefault();
		const targetSelector = a.dataset.target;
		const target = document.querySelector(targetSelector);
		if(!target) return;

		// fechar outros painéis de peça
		document.querySelectorAll('.peca-registros.open').forEach(function(el){
			if(el !== target){ el.style.maxHeight = null; el.innerHTML = ''; el.classList.remove('open'); el.classList.add('collapse'); }
		});

		// helper: ajustar altura do container da categoria para acomodar o painel
		function adjustCategoryHeight(elem){
			var cat = elem.closest('.categoria-body');
			if(!cat) return;
			if(cat.classList.contains('open')){
				// recalcula e define maxHeight para empurrar conteúdo abaixo
				cat.style.maxHeight = cat.scrollHeight + 'px';
				// remover o maxHeight inline após a transição para permitir layout responsivo
				var onCatEnd = function(e){
					if(e.propertyName === 'max-height'){
						try{ cat.style.maxHeight = ''; }catch(er){}
						cat.removeEventListener('transitionend', onCatEnd);
					}
				};
				cat.addEventListener('transitionend', onCatEnd);
				// garantir que categorias subsequentes preservem posição no fluxo
				var currentCategoria = cat.closest('.categoria');
				if(currentCategoria){
					var sib = currentCategoria.nextElementSibling;
					while(sib){
						// reset possíveis estilos que causem overlay
						sib.style.transform = '';
						sib.style.position = '';
						sib.style.zIndex = '';
						sib = sib.nextElementSibling;
					}
				}
			}
		}

		// se já aberto, fecha
		if(target.classList.contains('open')){
			target.style.maxHeight = null;
			target.innerHTML = '';
			target.classList.remove('open');
			target.classList.add('collapse');
			adjustCategoryHeight(target);
			return;
		}

		// carregar e abrir via fetch com header HTMX
		fetch(a.href, {headers: {'HX-Request': 'true'}})
			.then(function(resp){ if(!resp.ok) throw new Error('Network response was not ok: ' + resp.status); return resp.text(); })
			.then(function(html){
				try{
					// inserir fragmento no DOM
					target.innerHTML = html;
					// garantir que htmx processe o HTML recém-inserido (vital quando injetamos via fetch)
					if(window.htmx && typeof window.htmx.process === 'function'){
						htmx.process(target);
					}

					// --- fallback: se o formulário não estiver sendo gerenciado por htmx, anexar um handler via fetch
					(function(){
						var form = target.querySelector('form.registro-form');
						if(!form) return;
						// se htmx já estiver cuidando, não duplicar
						if(window.htmx && form.hasAttribute('hx-post')){ return; }

						form.addEventListener('submit', function(evt){
							evt.preventDefault();
							var url = form.getAttribute('hx-post') || form.getAttribute('action') || window.location.href;
							var fd = new FormData(form);
							// pegar CSRF do input se existir
							var csrfInput = form.querySelector('input[name="csrfmiddlewaretoken"]');
							var headers = {'X-Requested-With': 'XMLHttpRequest', 'HX-Request': 'true'};
							if(csrfInput && csrfInput.value){ headers['X-CSRFToken'] = csrfInput.value; }

							fetch(url, { method: 'POST', headers: headers, body: fd })
								.then(function(resp){ if(!resp.ok) throw new Error('Erro: ' + resp.status); return resp.text(); })
								.then(function(newHtml){
									// substituir o conteúdo do target pelo fragmento retornado (lista atualizada + formulário limpo)
									target.innerHTML = newHtml;
									// re-run htmx processing if available
									if(window.htmx && typeof window.htmx.process === 'function') htmx.process(target);
									// opcional: animar altura
									target.style.maxHeight = '0px';
									requestAnimationFrame(function(){ target.style.maxHeight = target.scrollHeight + 'px'; });
								}).catch(function(err){ console.error('Erro ao submeter registro via fallback fetch:', err); alert('Não foi possível enviar o registro: ' + err.message); });
						});
					})();
					target.classList.remove('collapse');
					target.classList.add('open');
					target.style.maxHeight = '0px';
					requestAnimationFrame(function(){ target.style.maxHeight = target.scrollHeight + 'px'; adjustCategoryHeight(target); });

					// remover maxHeight inline do painel de peça após a transição para permitir ajuste natural
					var onTargetEnd = function(e){
						if(e.propertyName === 'max-height'){
							try{ target.style.maxHeight = ''; }catch(err){}
							target.removeEventListener('transitionend', onTargetEnd);
						}
					};
					target.addEventListener('transitionend', onTargetEnd);
				}catch(inner){ console.error('Erro ao renderizar fragmento:', inner); }
			}).catch(function(err){ console.error('Erro ao carregar registros via fetch:', err); try{ window.location.href = a.href; }catch(e){ alert('Não foi possível carregar registros: ' + err.message); } });
	}

	document.addEventListener('click', onDocClick);
})();

// === BUSCA RÁPIDA DE PEÇAS (VERSÃO SIMPLIFICADA) ===
document.addEventListener('DOMContentLoaded', function() {
	console.log('DOM carregado, iniciando busca rápida...');
	
	const buscaInput = document.getElementById('busca-peca');
	const resultados = document.getElementById('resultados-busca');
	
	if (!buscaInput || !resultados) {
		console.log('Elementos de busca não encontrados');
		return;
	}
	
	console.log('Elementos encontrados, configurando eventos...');
	
	// Obter veiculo_id da URL
	const urlPath = window.location.pathname;
	const match = urlPath.match(/\/veiculo\/(\d+)\/manutencao\//);
	const veiculoId = match ? match[1] : null;
	
	console.log('Veiculo ID extraído:', veiculoId);
	
	let timeoutId = null;
	
	buscaInput.addEventListener('input', function(e) {
		const termo = e.target.value.trim();
		console.log('Input detectado:', termo);
		
		if (timeoutId) clearTimeout(timeoutId);
		
		if (termo.length < 2) {
			resultados.style.display = 'none';
			return;
		}
		
		timeoutId = setTimeout(() => {
			console.log('Fazendo busca...');
			buscarPecas(termo, veiculoId);
		}, 300);
	});
	
	// Função de busca simplificada
	function buscarPecas(termo, veiculoId) {
		resultados.innerHTML = '<div class="resultado-item">🔄 Buscando...</div>';
		resultados.style.display = 'block';
		
				const url = `/api/buscar-pecas/?q=${encodeURIComponent(termo)}&veiculo_id=${veiculoId}`;
		console.log('URL da busca:', url);
		
		fetch(url, {
			method: 'GET',
			headers: {
				'X-Requested-With': 'XMLHttpRequest'
			},
			credentials: 'same-origin'  // Incluir cookies de sessão
		})
		.then(response => {
			console.log('Status da resposta:', response.status);
			
			if (!response.ok) {
				throw new Error(`Erro ${response.status}: ${response.statusText}`);
			}
			
			return response.json();
		})
		.then(data => {
			console.log('Dados recebidos:', data);
			mostrarResultados(data.pecas || []);
		})
		.catch(error => {
			console.error('Erro na busca:', error);
			resultados.innerHTML = '<div class="busca-sem-resultados">Erro ao buscar peças</div>';
		});
	}
	
	function mostrarResultados(pecas) {
		if (pecas.length === 0) {
			resultados.innerHTML = '<div class="busca-sem-resultados">Nenhuma peça encontrada</div>';
			return;
		}
		
		let html = '';
		pecas.forEach(peca => {
			html += `
				<div class="resultado-item" onclick="abrirPeca('${peca.url}')">
					<span class="resultado-nome">${peca.nome}</span>
					<span class="resultado-categoria">${peca.categoria}</span>
				</div>
			`;
		});
		
		resultados.innerHTML = html;
	}
	
	// Função global para abrir peça
	window.abrirPeca = function(url) {
		console.log('🎯 Abrindo peça:', url);
		
		// Encontrar o link da peça pelo href
		const linkElement = document.querySelector(`a.peca-link[href="${url}"]`);
		console.log('🔍 Link encontrado:', linkElement);
		
		if (linkElement) {
			// Verificar se a categoria pai está fechada
			const categoriaBody = linkElement.closest('.categoria-body');
			console.log('📂 Categoria body:', categoriaBody);
			
			if (categoriaBody && categoriaBody.classList.contains('collapse')) {
				// Encontrar o botão toggle da categoria
				const categoriaToggle = categoriaBody.previousElementSibling;
				console.log('🔘 Toggle da categoria:', categoriaToggle);
				
				if (categoriaToggle && categoriaToggle.classList.contains('categoria-toggle')) {
					console.log('📖 Expandindo categoria primeiro...');
					
					// Simular clique no toggle da categoria
					const clickEvent = new MouseEvent('click', {
						bubbles: true,
						cancelable: true,
						view: window
					});
					categoriaToggle.dispatchEvent(clickEvent);
					
					// Aguardar expansão da categoria e então clicar na peça
					setTimeout(() => {
						console.log('🎯 Clicando na peça após expansão...');
						const pecaClickEvent = new MouseEvent('click', {
							bubbles: true,
							cancelable: true,
							view: window
						});
						linkElement.dispatchEvent(pecaClickEvent);
					}, 350); // Tempo suficiente para animação
				}
			} else {
				// Categoria já está aberta, clicar direto na peça
				console.log('✅ Categoria já aberta, clicando na peça...');
				const pecaClickEvent = new MouseEvent('click', {
					bubbles: true,
					cancelable: true,
					view: window
				});
				linkElement.dispatchEvent(pecaClickEvent);
			}
		} else {
			console.error('❌ Link da peça não encontrado:', url);
			console.log('🔄 Tentando fallback...');
			
			// Fallback: extrair ID da peça da URL e tentar encontrar de outra forma
			const pecaIdMatch = url.match(/\/peca\/(\d+)\//);
			if (pecaIdMatch) {
				const pecaId = pecaIdMatch[1];
				const alternativeLink = document.querySelector(`a.peca-link[data-target="#registros-${pecaId}"]`);
				console.log('🔍 Link alternativo encontrado:', alternativeLink);
				
				if (alternativeLink) {
					// Usar a função recursiva com a URL correta
					window.abrirPeca(alternativeLink.href);
					return;
				}
			}
			
			// Último recurso: navegar diretamente
			console.log('🌐 Navegando diretamente...');
			window.location.href = url;
		}
		
		// Limpar busca
		console.log('🧹 Limpando busca...');
		buscaInput.value = '';
		resultados.style.display = 'none';
	};
	
	// Ocultar ao clicar fora
	document.addEventListener('click', function(e) {
		if (!e.target.closest('.busca-container')) {
			resultados.style.display = 'none';
		}
	});
});
