import tkinter as tk
from tkinter import messagebox, Listbox
import threading
import time
import yfinance as yf
import smtplib
from email.message import EmailMessage
import json
import os

ARQUIVO_DADOS = 'dados.json'

def enviar_email(destinatario, assunto, corpo, copia_oculta=None):
    try:
        email = EmailMessage()
        email['Subject'] = assunto
        email['From'] = entry_gmail.get()
        email['To'] = destinatario
        if copia_oculta:
            email['Bcc'] = copia_oculta
        email.set_content(corpo)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(entry_gmail.get(), entry_senha.get())
            smtp.send_message(email)
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

def testar_envio():
    sucesso = enviar_email(entry_email.get(), "Teste de Alerta", "Seu alerta de ações está funcionando corretamente.")
    if sucesso:
        messagebox.showinfo("Teste de E-mail", "E-mail enviado com sucesso!")
    else:
        messagebox.showerror("Erro", "Erro ao enviar o e-mail. Verifique o Gmail e a senha.")

def carregar_dados():
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, 'r') as f:
            return json.load(f)
    return []

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w') as f:
        json.dump(dados, f, indent=4)

dados_monitoramento = carregar_dados()

def monitorar_acoes():
    while True:
        for item in dados_monitoramento:
            try:
                dados = yf.Ticker(item['acao'])
                preco_atual = dados.history(period='1d', interval='1m').tail(1)['Close'].iloc[0]

                if preco_atual <= item['compra']:
                    mensagem = f"O valor de {item['acao']} caiu para R$ {preco_atual:.2f}. Hora de COMPRAR!"
                    enviar_email(item['email'], "Alerta de COMPRA", mensagem)

                elif preco_atual >= item['venda']:
                    mensagem = f"O valor de {item['acao']} subiu para R$ {preco_atual:.2f}. Hora de VENDER!"
                    enviar_email(item['email'], "Alerta de VENDA", mensagem)

            except Exception as e:
                print(f"Erro ao monitorar {item['acao']}: {e}")
        time.sleep(60)

def adicionar_monitoramento():
    try:
        acao = entry_acao.get()
        compra = float(entry_compra.get())
        venda = float(entry_venda.get())
        email = entry_email.get()

        if not all([acao, compra, venda, email]):
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        novo = {
            'acao': acao,
            'compra': compra,
            'venda': venda,
            'email': email
        }

        dados_monitoramento.append(novo)
        salvar_dados(dados_monitoramento)
        atualizar_lista()

        # Enviar e-mail com os dados cadastrados, com cópia oculta para o remetente
        mensagem = (
            f"Ação cadastrada com sucesso!\n\n"
            f"Nome da Ação: {acao}\n"
            f"Valor definido para COMPRA: R$ {compra:.2f}\n"
            f"Valor definido para VENDA: R$ {venda:.2f}"
        )
        enviar_email(email, "Nova Ação Cadastrada", mensagem, copia_oculta=entry_gmail.get())

        messagebox.showinfo("Sucesso", "Ação cadastrada com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar: {e}")

def atualizar_lista():
    listbox.delete(0, tk.END)
    for i, item in enumerate(dados_monitoramento):
        texto = f"{item['acao']} - Compra: {item['compra']} / Venda: {item['venda']}"
        listbox.insert(tk.END, texto)

def remover_selecionado():
    try:
        index = listbox.curselection()[0]
        del dados_monitoramento[index]
        salvar_dados(dados_monitoramento)
        atualizar_lista()
        messagebox.showinfo("Sucesso", "Cadastro removido.")
    except:
        messagebox.showerror("Erro", "Selecione um item para remover.")

def iniciar_monitoramento():
    thread = threading.Thread(target=monitorar_acoes, daemon=True)
    thread.start()

# Interface
janela = tk.Tk()
janela.title("Bot de Ações - botvalores")
janela.geometry("400x650")
janela.configure(bg='white')

tk.Label(janela, text="Nome da Ação (ex: PETR4.SA):", bg='white').pack()
entry_acao = tk.Entry(janela)
entry_acao.pack()

tk.Label(janela, text="Valor para Comprar:", bg='white').pack()
entry_compra = tk.Entry(janela)
entry_compra.pack()

tk.Label(janela, text="Valor para Vender:", bg='white').pack()
entry_venda = tk.Entry(janela)
entry_venda.pack()

tk.Label(janela, text="E-mail que receberá o alerta:", bg='white').pack()
entry_email = tk.Entry(janela)
entry_email.pack()

tk.Label(janela, text="Seu Gmail (remetente):", bg='white').pack()
entry_gmail = tk.Entry(janela)
entry_gmail.pack()

tk.Label(janela, text="Senha do app (Gmail):", bg='white').pack()
entry_senha = tk.Entry(janela, show="*")
entry_senha.pack()

tk.Button(janela, text="Cadastrar Ação", command=adicionar_monitoramento, bg='green', fg='white').pack(pady=10)
tk.Button(janela, text="Testar Envio de E-mail", command=testar_envio, bg='blue', fg='white').pack(pady=5)

tk.Label(janela, text="Ações Cadastradas:", bg='white').pack()
listbox = Listbox(janela, width=50, height=10)
listbox.pack(pady=5)

tk.Button(janela, text="Remover Selecionada", command=remover_selecionado, bg='red', fg='white').pack(pady=5)

atualizar_lista()
iniciar_monitoramento()
janela.mainloop()
