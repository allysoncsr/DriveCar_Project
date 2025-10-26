#!/usr/bin/env python3
"""
Script de Teste Automático do Sistema de Alertas DriveCar
Executa automaticamente:
1. Criação de dados de teste
2. Início do servidor Django
3. Abertura do navegador para visualização
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def print_header():
    print("=" * 70)
    print("🚗 TESTE AUTOMÁTICO - SISTEMA DE ALERTAS DRIVECAR")
    print("=" * 70)

def print_step(step_num, description):
    print(f"\n📋 PASSO {step_num}: {description}")
    print("-" * 50)

def run_command(command, description, check_success=True):
    """Executa um comando e mostra o resultado"""
    print(f"⚙️  Executando: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✅ Sucesso: {description}")
            if result.stdout.strip():
                # Mostrar apenas as linhas importantes
                lines = result.stdout.split('\n')
                important_lines = [line for line in lines if any(marker in line for marker in ['✅', '🚗', '🔴', '🟡', '🟢', 'SUCESSO', 'Total de alertas'])]
                for line in important_lines[-10:]:  # Últimas 10 linhas importantes
                    if line.strip():
                        print(f"   {line}")
            return True
        else:
            print(f"❌ Erro: {description}")
            if result.stderr:
                print(f"   Erro: {result.stderr[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ Exceção: {str(e)}")
        return False

def main():
    print_header()
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('manage.py'):
        print("❌ ERRO: manage.py não encontrado!")
        print("   Execute este script do diretório do projeto Django")
        sys.exit(1)
    
    print("📍 Diretório atual:", os.getcwd())
    
    # PASSO 1: Criar dados de teste
    print_step(1, "Criando dados de teste para alertas")
    success = run_command(
        "python manage.py teste_alertas",
        "Executando comando de criação de dados de teste"
    )
    
    if not success:
        print("\n❌ ERRO: Falha ao criar dados de teste")
        print("   Verifique se o banco de dados está configurado")
        sys.exit(1)
    
    # PASSO 2: Iniciar servidor (em background)
    print_step(2, "Iniciando servidor Django")
    print("⚙️  Iniciando servidor em background...")
    
    # Iniciar servidor em processo separado
    try:
        server_process = subprocess.Popen(
            ["python", "manage.py", "runserver"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        print("✅ Servidor iniciado em background")
        
        # Aguardar um pouco para o servidor inicializar
        print("⏳ Aguardando servidor inicializar...")
        time.sleep(3)
        
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)
    
    # PASSO 3: Abrir navegador
    print_step(3, "Abrindo navegador para visualização")
    
    url = "http://127.0.0.1:8000/"
    print(f"🌐 Abrindo: {url}")
    
    try:
        webbrowser.open(url)
        print("✅ Navegador aberto")
    except Exception as e:
        print(f"❌ Erro ao abrir navegador: {e}")
        print(f"   Abra manualmente: {url}")
    
    # PASSO 4: Instruções para o usuário
    print_step(4, "Instruções de Login e Visualização")
    
    print("🎯 DADOS DE LOGIN:")
    print("   👤 Usuário: teste_alertas")
    print("   🔑 Senha: 123456")
    
    print("\n📋 O QUE VOCÊ DEVE VER:")
    print("   1. Painel 'Alertas Ativos' na tela principal")
    print("   2. Cards vermelhos (urgente) e amarelos (atenção)")
    print("   3. Informações como: 'Óleo do motor: VENCIDO'")
    print("   4. Ao clicar em um veículo -> Manutenção:")
    print("      • Seção 'Alertas deste Veículo' no topo")
    print("      • Detalhes específicos com recomendações")
    
    print("\n🔍 CENÁRIOS DE TESTE CRIADOS:")
    print("   🔴 URGENTE - Óleo do motor: VENCIDO")
    print("   🔴 URGENTE - Filtro combustível: 500 km restantes")
    print("   🟡 ATENÇÃO - Filtro de ar: 2.000 km restantes")
    
    print("\n⌨️  CONTROLES:")
    print("   • Pressione Ctrl+C para parar o servidor")
    print("   • O servidor continuará rodando até você parar")
    
    print("\n" + "=" * 70)
    print("🎉 TESTE INICIADO COM SUCESSO!")
    print("   Verifique o navegador para ver os alertas funcionando")
    print("=" * 70)
    
    # Manter o script rodando e monitorar o servidor
    try:
        print("\n⏳ Servidor rodando... (Pressione Ctrl+C para parar)")
        server_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Parando servidor...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()
        print("✅ Servidor parado")
    except Exception as e:
        print(f"\n❌ Erro no servidor: {e}")
        server_process.terminate()

if __name__ == "__main__":
    main()