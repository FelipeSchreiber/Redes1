from flask import Flask, render_template, request, redirect, session, flash, abort
import datetime
# -*- coding: utf-8 -*-
import qrcode
app = Flask(__name__)

app.secret_key = 'aula'

class Usuario:
    def __init__(self, dre, cpf, senha, nome, curso, nasc, profile_img, validade):
        self.dre = dre
        self.cpf = cpf
        self.senha = senha
        self.nome = nome
        self.curso = curso
        self.nasc = nasc
        self.profile_img = profile_img;#nome do arquivo que esta na pasta static correspondente ao usuario
        self.validade = validade;#campo que define a data limite da validade da carteirinha

currentTime = datetime.datetime.now()#obtem a data atual para comparar com a validade

usuario1 = Usuario('118025293', '99999999999', '123456','Joao Pedro Brandao','ECI','DD/MM/AA',"","Jun 1 2005")
usuario2 = Usuario('116206990', '00000000000', '123456', 'Felipe Schreiber', 'ECI','16/05/1998',"Felipe Schreiber.jpg","Dec 1 2018")
usuario3 = Usuario('115171922', '11111111111', '123456','JJ', 'ECI','DD/MM/AA',"Felipe Schreiber.jpg","Dec 1 2018")

usuarios = {usuario1.cpf : usuario1 , usuario2.cpf : usuario2, usuario3.cpf : usuario3}


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuariocpf'] in usuarios:#checa se o usuario existe no banco de dados
        if usuarios[request.form['usuariocpf']].senha == request.form['senha']:#checa se a senha esta correta
            if usuarios[request.form['usuariocpf']].dre != "":
                if usuarios[request.form['usuariocpf']].nome != "":
                    if usuarios[request.form['usuariocpf']].curso != "":
                        if usuarios[request.form['usuariocpf']].nasc != "":
                            if usuarios[request.form['usuariocpf']].profile_img != "":       
                                if datetime.datetime.strptime(usuarios[request.form['usuariocpf']].validade, "%b %d %Y") > currentTime :
                                 #converte a string correspondente a validade no objeto "datetime" e compara com a data atual   
                                 session['usuario_logado'] = request.form['usuariocpf']  # cria uma sessao com o usuario preenchido no login
                                 return redirect('/carteirinha')
                                else:
                                 flash('Validade venceu em:'+ usuarios[request.form['usuariocpf']].validade)
                                 session['usuario_logado'] = None
                                 return redirect('/') 	   
                            else: 
                             flash('Sem foto!')
                             session['usuario_logado'] = None
                             return redirect('/')                             
                        else:
                         flash('Data de nascimento faltando!')
                         session['usuario_logado'] = None
                         return redirect('/')                             
                    else: 
                     flash('Curso faltando!')
                     session['usuario_logado'] = None
                     return redirect('/')                             
                else: 
                 flash('Nome faltando!')
                 session['usuario_logado'] = None
                 return redirect('/')                             
            else: 
             flash('DRE faltando')
             session['usuario_logado'] = None
             return redirect('/')                             
        else: 
         flash('Senha incorreta!')
         session['usuario_logado'] = None
         return redirect('/')
    else: 
     flash('Usuario Incorreto!')
     session['usuario_logado'] = None
     return redirect('/')

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    return redirect('/')

@app.route('/carteirinha')
def carteirinha():
    if session['usuario_logado'] == None:
        abort(503)
    qr = qrcode.QRCode(
            version = 1,
            error_correction = qrcode.constants.ERROR_CORRECT_H,
            box_size = 3,
            border = 4,)
    data = session['usuario_logado'] #cria um QRCODE com o CPF do usuario
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image() #cria a imagem do QRCODE
    img.save("./static/Qr_image.png")#salva a imagem no diretorio static
    x = usuarios[session['usuario_logado']]
    return render_template('carteirinha.html',x=x)
app.run(host='0.0.0.0', port=5000, debug=True) # com debug true vai bastar salvar ao inves de ficar rodando diversas vezes

