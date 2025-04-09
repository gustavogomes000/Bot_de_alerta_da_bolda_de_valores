# 📈 Bot de Alerta da Bolsa de Valores

Este projeto é um **bot inteligente**, desenvolvido em Python, que monitora ações da bolsa de valores e envia **alertas automáticos via E-mail** sempre que os preços atingirem os valores definidos para **compra** ou **venda**.

Com a interface o usuário pode:
- Cadastrar ações manualmente;
- Definir valores de alerta para compra e venda;
- Ver a lista de ações monitoradas;
- Receber alertas.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter** – Interface gráfica
- **yfinance** – Consulta de preços em tempo real
- **smtplib** – Envio de e-mails via Gmail
- **requests** – Envio de mensagens via Telegram
- **ConfigParser** – Gerenciamento de configurações (INI)
- **Threading** – Execução paralela para monitoramento contínuo
- **JSON** – Armazenamento local dos dados
- **PyInstaller** – Geração de executável `.exe`

---

🛠️ Passo a Passo para Instalação e Configuração
1️⃣ Clonar o Repositório
git clone https://github.com/gustavogomes000/Bot_de_alerta_da_bolda_de_valores.git
cd Bot_de_alerta_da_bolda_de_valores


2️⃣ Instalar as Dependências
pip install -r requirements.txt

3️⃣ Configurar o Arquivo config.ini
Crie ou edite o arquivo em:
config/config.ini
Preencha com suas informações do Gmail:

🔹 Senha do Gmail (Senha de App)

Acesse: https://myaccount.google.com/security

Ative a verificação em duas etapas

Vá em "Senhas de app"

Crie uma nova senha para o app (ex: "Bot Python")

Copie e use no config.ini

4️⃣ Executar o Bot
python botvalores.py
A interface será aberta para você cadastrar ações e definir os preços de alerta.

5️⃣ Criar Executável .exe
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed botvalores.py
O arquivo .exe será gerado dentro da pasta dist/.

6️⃣ Adicionar na Inicialização do Windows para funcionar em tempo real em segundo plano.
Pressione Win + R

Digite shell:startup e pressione Enter

Cole um atalho do seu .exe (da pasta dist/) nessa pasta

Pronto! O bot será iniciado automaticamente sempre que o computador ligar.


