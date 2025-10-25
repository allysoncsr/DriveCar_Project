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
