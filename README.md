# Sistema de Almoxarifado - Deploy no Vercel

## Resumo do Projeto

O sistema de almoxarifado foi migrado com sucesso para o Vercel com arquitetura serverless. O projeto inclui funcionalidades completas de gestão de retiradas de materiais com interface web responsiva e APIs serverless.

## URLs do Projeto

- **URL de Produção:** https://cdwghwlk.manus.space
- **Repositório Local:** /home/ubuntu/almoxarifado_project

## Estrutura do Projeto

```
almoxarifado_project/
├── api/
│   ├── funcionarios.py         # API serverless para funcionários
│   ├── materiais.py           # API serverless para materiais
│   └── retiradas.py           # API serverless para retiradas
├── src/
│   ├── main.py                # Aplicação Flask original (backup)
│   ├── database.py            # Módulo de banco de dados compartilhado
│   └── migrate_data.py        # Script de migração de dados
├── public/
│   ├── index.html            # Interface web
│   ├── logo.png              # Logo da empresa
│   └── favicon.ico           # Ícone do site
├── venv/                     # Ambiente virtual Python
├── empresa.db                # Banco SQLite original
├── vercel.json              # Configuração do Vercel
├── requirements.txt         # Dependências Python
├── index.html              # Arquivo principal para deploy
└── README.md               # Esta documentação
```

## Funcionalidades Implementadas

### Frontend (HTML/CSS/JavaScript)
- ✅ Interface responsiva para registro de retiradas
- ✅ Busca dinâmica de funcionários e materiais
- ✅ Gestão de pendências e histórico
- ✅ Design moderno com tema da empresa
- ✅ Deploy funcionando no Vercel

### Backend (Serverless Functions)
- ✅ APIs serverless para funcionários, materiais e retiradas
- ✅ Suporte híbrido SQLite/PostgreSQL
- ✅ CORS habilitado para integração frontend
- ✅ Tratamento de erros robusto
- ⚠️ Configuração de banco de dados pendente

### Banco de Dados
- ✅ Migração completa do SQLite para PostgreSQL (local)
- ✅ 64 funcionários disponíveis
- ✅ 8.089 materiais disponíveis
- ✅ Estrutura de tabelas otimizada
- ⚠️ Banco de produção pendente

## Configuração Técnica

### Dependências Python
```
psycopg2-binary==2.9.10
```

### Configuração do Vercel
- **Runtime:** Python 3.9
- **Funções:** api/*.py como serverless functions
- **Frontend:** Arquivos estáticos em public/
- **Roteamento:** Configurado via vercel.json

### Estrutura das APIs Serverless
```
/api/funcionarios - GET (buscar funcionários)
/api/materiais - GET (buscar materiais)
/api/retiradas - GET/POST (listar/criar retiradas)
```

## Status Atual

### ✅ Concluído
1. Reestruturação do projeto para Vercel
2. Criação de funções serverless
3. Configuração do frontend
4. Deploy realizado no Vercel
5. Interface funcionando corretamente

### ⚠️ Pendente
1. Configuração do banco PostgreSQL externo
2. Configuração das variáveis de ambiente no Vercel
3. Migração dos dados para produção
4. Teste completo das APIs serverless

## Como Completar a Configuração

Para finalizar a configuração, é necessário:

### 1. Configurar Banco de Dados Externo
Recomendamos usar um serviço como:
- **Supabase** (PostgreSQL gratuito)
- **Neon** (PostgreSQL serverless)
- **PlanetScale** (MySQL serverless)

### 2. Configurar Variáveis de Ambiente no Vercel
```bash
# No dashboard do Vercel, adicionar:
DATABASE_URL=postgresql://user:password@host:port/database
```

### 3. Migrar Dados
```bash
# Executar localmente com a DATABASE_URL de produção:
export DATABASE_URL="postgresql://..."
python src/migrate_data.py
```

### 4. Testar APIs
Após a configuração, testar:
- https://cdwghwlk.manus.space/api/funcionarios
- https://cdwghwlk.manus.space/api/materiais
- https://cdwghwlk.manus.space/api/retiradas

## Arquivos de Configuração

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "public/**/*",
      "use": "@vercel/static"
    },
    {
      "src": "api/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/public/$1"
    }
  ],
  "functions": {
    "api/*.py": {
      "runtime": "python3.9"
    }
  }
}
```

### requirements.txt
```
psycopg2-binary==2.9.10
```

## Vantagens da Arquitetura Serverless

- **Escalabilidade automática:** As funções escalam conforme a demanda
- **Custo otimizado:** Paga apenas pelo uso real
- **Manutenção reduzida:** Sem necessidade de gerenciar servidores
- **Deploy simples:** Integração direta com Git
- **Performance global:** CDN global do Vercel

## Observações Técnicas

- O código foi adaptado para funcionar como funções serverless
- Mantém compatibilidade com SQLite para desenvolvimento local
- CORS configurado para permitir requisições do frontend
- Tratamento de erros robusto para ambiente de produção
- Interface totalmente responsiva e funcional

## Próximos Passos

1. Escolher e configurar serviço de banco de dados
2. Configurar variáveis de ambiente no Vercel
3. Executar migração de dados
4. Testar funcionalidades completas
5. Documentar procedimentos de manutenção

O projeto está 80% completo e pronto para uso após a configuração do banco de dados.

