# 🏭 Otimiza Fábrica - Guia de Uso

## 📋 O que você tem

Este projeto é um **solver de Programação Linear** para otimizar produção em múltiplas fábricas (ENADE 2021).

### 📦 Arquivos Gerados

```
otimiza-fabrica/
│
├── otimiza-fabrica.html          ⭐ ARQUIVO PRINCIPAL (abrir no navegador)
├── solver_producao.py             (Script Python avançado)
├── relatorio_solucao.txt          (Relatório em texto)
├── grafico_regiao_viavel.png      (Gráfico da solução)
│
└── GUIA_DE_USO.md                 (Este arquivo)
```

---

## 🚀 Como Usar

### **Opção 1: Abrir Direto no Navegador (Mais Fácil)**

1. **Localize o arquivo** `otimiza-fabrica.html`
2. **Clique duas vezes** nele (ele abrirá no seu navegador padrão)
3. **Pronto!** Use a interface para resolver o problema

**Ou:**
- Clique com botão direito → "Abrir com" → Escolha seu navegador (Chrome, Firefox, Edge, Safari, etc.)

---

### **Opção 2: Usar o Script Python (Para Análise Avançada)**

Se você quer executar o solver via linha de comando:

#### **Requisitos:**
```bash
pip install numpy scipy matplotlib pandas
```

#### **Executar:**
```bash
python3 solver_producao.py
```

Isto irá:
- ✓ Calcular a solução ótima
- ✓ Gerar um gráfico (`grafico_regiao_viavel.png`)
- ✓ Criar um relatório em texto (`relatorio_solucao.txt`)

---

## 🖥️ Estrutura de Pasta Recomendada

Se você quer colocar em um servidor ou pasta do seu computador:

```
meu-projeto-otimizacao/
│
├── index.html                    (renomear otimiza-fabrica.html para isto)
├── README.md                     (documentação)
├── solver_producao.py            (opcional)
└── relatorio_solucao.txt         (opcional)
```

---

## 📱 Acessar de Qualquer Lugar

### **Localmente (seu computador):**
1. Coloque os arquivos em uma pasta qualquer
2. Abra `otimiza-fabrica.html` no navegador

### **Via GitHub Pages (Grátis e Online):**

1. **Crie um repositório GitHub** chamado `seu-username.github.io`
2. **Faça upload** do arquivo `otimiza-fabrica.html` como `index.html`
3. **Acesse** em: `https://seu-username.github.io/`

### **Via Servidor Web (Apache, Nginx, etc):**

1. Coloque `otimiza-fabrica.html` na pasta `public_html` ou `www`
2. Acesse via seu domínio

---

## 🔧 Estrutura do Projeto

### **otimiza-fabrica.html**
- Interface completa em uma **única página HTML**
- Contém **CSS e JavaScript integrados**
- Usa **Chart.js** via CDN (não precisa instalar)
- **Totalmente responsivo** (mobile, tablet, desktop)

### **solver_producao.py**
- Implementação em Python puro
- Usa `scipy.optimize` para resolver
- Gera gráfico com `matplotlib`
- Cria relatório em texto

---

## 🎯 O Que o Solver Faz

**Problema:** Uma empresa tem 2 fábricas e precisa produzir 3 produtos com demandas específicas. 

**Objetivo:** Encontrar os **dias operacionais de cada fábrica** que **minimizam custos** mantendo a demanda.

**Entrada:**
- Dados de produção por fábrica
- Custos diários
- Demandas de produtos

**Saída:**
- ✓ Dias ótimos de operação (x₁, x₂)
- ✓ Custo mínimo
- ✓ Verificação de restrições
- ✓ Gráfico da região viável
- ✓ Detalhamento de produção

---

## 💡 Exemplo de Uso

### **Via navegador:**
1. Abra `otimiza-fabrica.html`
2. Mantenha precisão em "4 casas decimais"
3. Clique em "🚀 Resolver Problema"
4. Veja:
   - **x₁ = 2.8000** (dias Manaus)
   - **x₂ = 3.2000** (dias Sul)
   - **Custo = 1.092.000** (R$)

### **Via Python:**
```bash
$ python3 solver_producao.py

████████████████████████████████████
█   LINEAR PROGRAMMING SOLVER       █
████████████████████████████████████

Vértices encontrados: 2
Vértice 1: x₁ = 2.8000, x₂ = 3.2000 | Z = 1.092.000

✓ Gráfico salvo em: grafico_regiao_viavel.png
✓ Relatório salvo em: relatorio_solucao.txt
```

---

## 🌐 Hospedagem Online (Gratuita)

### **Opção 1: Vercel**
1. Crie conta em https://vercel.com
2. Faça upload do arquivo
3. Receba um link público

### **Opção 2: GitHub Pages**
1. Crie repositório: `seu-username.github.io`
2. Faça upload do `otimiza-fabrica.html` como `index.html`
3. Acesse em: `https://seu-username.github.io/`

### **Opção 3: Netlify**
1. Vá em https://app.netlify.com
2. Drag & drop do arquivo HTML
3. Receba URL pública

---

## 📊 Dados do Problema (Hardcoded)

Os dados estão **embutidos no código**:

```javascript
const problem = {
    costManaus: 150,           // R$ 150 mil/dia
    costSul: 210,              // R$ 210 mil/dia
    prodManaus: [8, 1, 2],     // Desktop, Notebook, Netbook
    prodSul: [2, 1, 7],        // Desktop, Notebook, Netbook
    demand: [16, 6, 28],       // Demandas em milhares
    products: ['Desktops', 'Notebooks', 'Netbooks']
};
```

Para **mudar os dados**, edite diretamente no código HTML.

---

## 🎓 Modelo Matemático

### **Variáveis:**
- x₁ = dias operação Fábrica Manaus
- x₂ = dias operação Fábrica Sul

### **Objetivo (Minimizar):**
```
Z = 150.000·x₁ + 210.000·x₂
```

### **Restrições:**
```
8.000·x₁ + 2.000·x₂ ≥ 16.000  (Desktops)
1.000·x₁ + 1.000·x₂ ≥ 6.000   (Notebooks)
2.000·x₁ + 7.000·x₂ ≥ 28.000  (Netbooks)
x₁, x₂ ≥ 0 (não-negatividade)
```

---

## ⚙️ Requisitos Técnicos

### **Para HTML (Mínimo):**
- ✓ Um navegador web moderno
- ✓ Conexão com internet (para CDN do Chart.js)

### **Para Python (Opcional):**
- ✓ Python 3.7+
- ✓ pip
- ✓ Pacotes: numpy, scipy, matplotlib, pandas

---

## 🐛 Troubleshooting

### **Problema:** Arquivo não abre no navegador
**Solução:** Clique direito → "Abrir com" → Escolha um navegador

### **Problema:** Gráfico não aparece
**Solução:** Verifique conexão de internet (precisa do CDN)

### **Problema:** Script Python dá erro
**Solução:** Instale as dependências:
```bash
pip install --upgrade numpy scipy matplotlib pandas
```

---

## 📝 Créditos

**Desenvolvido por:** Ana Clara Mendes Amim  
**Desafio:** ENADE 2021 - Programação Linear  
**Instituição:** UFPB - Campus IV  
)
---

## 📞 Suporte

Dúvidas sobre como usar?
- Verifique se o arquivo `otimiza-fabrica.html` está intacto
- Teste em diferentes navegadores
- Certifique-se de ter conexão com internet

---

**Aproveite! 🚀**
