from flask import Flask, render_template, request, flash, redirect, url_for
from datetime import date

app = Flask(__name__)

app.secret_key = 'Throwback Thursday'
usuario = []

vet1 = "Bernardo"

vet2 = "Maitê"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/meuspets/<codigo>')
def meuspets(codigo):
    for usu in usuario:
        if usu['codigo'] == codigo:
            return render_template('meuspets.html', usuario=usu)
    flash("Usuário não encontrado.")
    return redirect(url_for('login'))

@app.route('/prelogin')
def prelogin():
    return render_template('prelogin.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        for i in usuario:
            if i['email'] == email and i['senha'] == senha:
                flash('🌟Login feito com sucesso!', 'sucesso')
                return redirect(url_for('usuarios', codigo=i['codigo']))
        flash('❗ Email ou senha inválidos', 'erro')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        codigo = str(len(usuario) + 1)
        nome = request.form['tutor']
        email = request.form['email']
        senha = request.form['senha']

        maiuscula = False
        minuscula = False
        numero = False
        pcd = False

        for t in senha:
            if t.isupper():
                maiuscula = True
            if t.islower():
                minuscula = True
            if t.isdigit():
                numero = True
            if not t.isalnum():
                pcd = True

        if maiuscula == True and minuscula == True and numero == True and pcd == True:
            cadastro_usuario = {
                'codigo': codigo,
                'nome': nome,
                'email': email,
                'senha': senha,
                'pets': {},
                'agendamentos': {}
            }
            usuario.append(cadastro_usuario)
            flash("🌟 Cadastro realizado com sucesso!", 'sucesso')
            return redirect(url_for('login'))
        else:
            flash("❗ Senha fraca use pelo menos 8 caracteres,letra maiúscula, minúscula, número e símbolo.", 'erro')
            return redirect(url_for('cadastro'))

    return render_template('cadastro.html')

@app.route('/usuarios/<codigo>')
def usuarios(codigo):
    for usu in usuario:
        if usu['codigo'] == codigo:
            return render_template('usuario.html', usuario=usu)
    flash("❗ Usuário não existente", 'erro')
    return redirect(url_for('login'))

@app.route('/abrir_editar/<codigo>')
def abrir_editar(codigo):
    for usu in usuario:
        if usu['codigo'] == codigo:
            return render_template('editar_login.html', usuario=usu)
    flash("❗ Usuário não encontrado.", 'erro')
    return redirect(url_for('login'))

@app.route('/editarpet/<codigo>/<codigopet>', methods=['GET'])
def abrir_editarpet(codigo, codigopet):
    for g in usuario:
        if g['codigo'] == codigo:
            pet = g['pets'].get(codigopet)
            if pet:
                return render_template('editarpet.html', codigo=codigo, codigopet=codigopet, pet=pet)
            else:
                flash('Pet não encontrado.')
                return redirect(url_for('meuspets', codigo=codigo))
    flash("Usuário não encontrado.")
    return redirect(url_for('login'))


@app.route('/editar', methods=['POST'])
def editar_login():
    if request.method == 'POST':
        codigo = request.form['codigo']
        novonome = request.form['nomenovo']
        novoemail = request.form['emailnovo']
        novasenha = request.form['senhanova']

        maiuscula = False
        minuscula = False
        numero = False
        pcd = False

        for x in novasenha:
            if x.isupper():
                maiuscula = True
            if x.islower():
                minuscula = True
            if x.isdigit():
                numero = True
            if not x.isalnum():
                pcd = True
        if maiuscula == True and minuscula == True and numero == True and pcd == True:
            for n in usuario:
                if n['codigo'] == codigo:
                    if n['nome'] == novonome and n['email'] == novoemail and n['senha'] == novasenha:
                        flash('❗ Sem alterações' , 'erro')
                    else:
                        n['nome'] = novonome
                        n['email'] = novoemail
                        n['senha'] = novasenha
                        flash('🌟 Dados atualizados com sucesso!', 'sucesso')
                        break
        return redirect(url_for('usuarios', codigo=codigo))

@app.route('/adicionarpet/<codigo>', methods=['GET', 'POST'])
def adicionarpet(codigo):
    for c in usuario:
        if c['codigo'] == codigo:
            if request.method == 'POST':
                nome = request.form['nome']
                raca = request.form['raca']
                especie = request.form['especie']
                peso = float(request.form['peso'])
                idade = request.form['idade']

                codigopet = str(len(c['pets']) + 1)

                pet = {
                    'nome': nome,
                    'raca': raca,
                    'especie': especie,
                    'peso': peso,
                    'idade': idade
                }

                c['pets'][codigopet] = pet
                print(usuario)
                flash('🌟 Pet cadastrado com sucesso!', 'sucesso')
                return redirect(url_for('meuspets', codigo=codigo))

            return render_template('adicionar_pet.html', codigo=codigo)

    flash('❗ Usuário não encontrado' , 'erro')
    return redirect(url_for('login'))


@app.route('/editarpet/<codigo>/<codigopet>', methods=['POST'])
def editarpet(codigo, codigopet):
    for b in usuario:
        if b['codigo'] == codigo:
            pet = b['pets'].get(codigopet)
            if pet:
                pet['nome'] = request.form['nomepet']
                pet['raca'] = request.form['racapet']
                pet['especie'] = request.form['especiepet']
                pet['peso'] = float(request.form['pesopet'])
                pet['idade'] = request.form['idadepet']
                flash('Pet editado com sucesso!')
                return redirect(url_for('meuspets', codigo=codigo))
            else:
                flash('❗ Pet não encontrado' , 'erro')
                return redirect(url_for('meuspets', codigo=codigo))
    flash('❗ Usuário não encontrado', 'erro')
    return redirect(url_for('login'))


@app.route('/excluirpet/<codigo>/<codigopet>', methods=['POST'])
def excluirpet(codigo, codigopet):
    for usu in usuario:
        if usu['codigo'] == codigo:
            if codigopet in usu['pets']:
                del usu['pets'][codigopet]
                flash('🌟 Pet excluído com sucesso!', 'sucesso')
                return redirect(url_for('meuspets', codigo=codigo))
            flash('❗ Pet não encontrado' , 'erro')
            return redirect(url_for('meuspets', codigo=codigo))
    flash('❗ Usuário não encontrado' , 'erro')
    return redirect(url_for('login'))


@app.route('/agendar/<codigo>', methods=['GET', 'POST'])
def agendar(codigo):
    for usu in usuario:
        if usu['codigo'] == codigo:
            if not usu['pets']:
                flash('❗ Você precisa cadastrar pelo menos um pet antes de agendar.', 'erro')
                return redirect(url_for('meuspets', codigo=codigo))

            if request.method == 'POST':
                pet_selecionado = request.form['pet']
                dia = request.form['data']
                partes = dia.split('-')
                dia_formatado = f"{partes[2]}/{partes[1]}/{partes[0]}"
                horario = request.form['hora']
                motivo = request.form['motivo']
                veterinario = request.form['veterinario']

                conflito = False
                for user in usuario:
                    for agendamento in user['agendamentos'].values():
                        if (agendamento['dia'] == dia_formatado and 
                            agendamento['horario'] == horario and 
                            agendamento['veterinario'] == veterinario):
                            
                            if agendamento['pet'] == pet_selecionado:
                                flash('❗ Este pet já tem uma consulta marcada com este veterinário no mesmo horário.', 'erro')
                            else:
                                flash('❗ Este veterinário já tem uma consulta marcada no mesmo horário com outro pet.', 'erro')
                            conflito = True
                            return redirect(url_for('agendar', codigo=codigo))

                if not conflito:
                    codigo_agendamento = str(len(usu['agendamentos']) + 1)
                    agendamento = {
                        'pet': pet_selecionado,
                        'dia': dia_formatado,
                        'horario': horario,
                        'motivo': motivo,
                        'veterinario': veterinario
                    }
                    usu['agendamentos'][codigo_agendamento] = agendamento
                    flash('🌟 Agendamento feito com sucesso!', 'sucesso')
                    return redirect(url_for('consultas', codigo=codigo))

            return render_template('agendar.html', usuario=usu, date=date)

@app.route('/consultas/<codigo>', methods=['GET', 'POST'])
def consultas(codigo):
    for usu in usuario:
        if usu['codigo'] == codigo:
            return render_template('seusagendamentos.html', usuario=usu)
    flash('❗ Usuário não encontrado', 'erro')
    return redirect(url_for('login'))


@app.route('/excluiragen/<codigo>/<cod_ag>')
def excluir_agendamento(codigo, cod_ag):
    for u in usuario:
        if u['codigo'] == codigo:
            if cod_ag in u['agendamentos']:
                del u['agendamentos'][cod_ag]
                flash("🗑️ Consulta excluída com sucesso!", "sucesso")
            else:
                flash("❗ Agendamento não encontrado.", "erro")
            return redirect(url_for('usuarios', codigo=codigo))
    flash("❗ Usuário não encontrado.", "erro")
    return redirect(url_for('login'))

@app.route('/editaragendamento/<codigo>/<cod_ag>')
def abrir_editar_agendamento(codigo, cod_ag):
    for u in usuario:
        if u['codigo'] == codigo:
            agendamento = u['agendamentos'].get(cod_ag)
            if agendamento:
                return render_template('editaragendamento.html', agendamento=agendamento, codigo=codigo, cod_ag=cod_ag, usuario=u)
    flash("❗ Agendamento não encontrado", "erro")
    return redirect(url_for('usuarios', codigo=codigo))

@app.route('/editarAgendamento/<codigo>/<cod_ag>', methods=['POST'])
def editarAgendamento(codigo, cod_ag):
    for usu in usuario:
        if usu['codigo'] == codigo:
            agendamento = usu['agendamentos'].get(cod_ag)
            if agendamento:
                # Formata a data para o padrão brasileiro
                dia = request.form['dia']
                partes = dia.split('-')
                dia_formatado = f"{partes[2]}/{partes[1]}/{partes[0]}"
                horario = request.form['horario']
                veterinario = agendamento['veterinario'] 
                conflito = False
                for user in usuario:
                    for ag_id, ag in user['agendamentos'].items():

                        if user['codigo'] == codigo and ag_id == cod_ag:
                            continue
                            
                        if (ag['dia'] == dia_formatado and 
                            ag['horario'] == horario and 
                            ag['veterinario'] == veterinario):
                            
                            if ag['pet'] == agendamento['pet']:
                                flash('❗ Este pet já tem uma consulta marcada com este veterinário no mesmo horário.', 'erro')
                            else:
                                flash('❗ Este veterinário já tem uma consulta marcada no mesmo horário com outro pet.', 'erro')
                            conflito = True
                            return redirect(url_for('abrir_editar_agendamento', codigo=codigo, cod_ag=cod_ag))

                if not conflito:
                    agendamento['dia'] = dia_formatado
                    agendamento['horario'] = horario
                    agendamento['motivo'] = request.form['motivo']
                    flash('🌟 Consulta editada com sucesso!', 'sucesso')
                    return redirect(url_for('usuarios', codigo=codigo))
            
            flash('❗ Agendamento não encontrado.', 'erro')
            return redirect(url_for('usuarios', codigo=codigo))
    flash('❗ Usuário não encontrado.', 'erro')
    return redirect(url_for('login'))

@app.route('/lognvet')
def lognvet():
    return render_template('lognvet.html')

@app.route('/usuariovet', methods=['POST'])
def usuariovet():
    codigo_vet = request.form['codigo']

    if codigo_vet in [vet1, vet2]:
        return redirect(url_for('contavet', codigo_vet=codigo_vet))
    else:
        flash('❗ Veterinário não encontrado.', 'erro')
        return redirect(url_for('lognvet'))

@app.route('/contavet')
def contavet():
    codigo_vet = request.args.get('codigo_vet') 
    
    if codigo_vet not in [vet1, vet2]:
        flash('❗ Acesso não autorizado', 'erro')
        return redirect(url_for('lognvet'))
    
    return render_template('contavet.html', codigo_vet=codigo_vet)


@app.route('/vet/consultas/<codigo_vet>')
def consultas_vet(codigo_vet):
    if codigo_vet not in [vet1, vet2]:
        flash('❗ Acesso não autorizado', 'erro')
        return redirect(url_for('lognvet'))

    consultas = []
    for user in usuario:
        for agendamento_id, agendamento in user['agendamentos'].items():
            if agendamento.get('veterinario') == codigo_vet:

                pet_nome = user['pets'][agendamento['pet']]['nome'] if agendamento['pet'] in user['pets'] else "Pet não encontrado"
                
                consultas.append({
                    'id': agendamento_id,
                    'user_id': user['codigo'],
                    'user_nome': user['nome'],
                    'pet_nome': pet_nome,
                    'data': agendamento['dia'],
                    'hora': agendamento['horario'],
                    'motivo': agendamento['motivo']
                })
    return render_template('consultas_vet.html', 
                         consultas=consultas,
                         codigo_vet=codigo_vet)

@app.route('/cal_dose', methods=['GET', 'POST'])
def calculadora_dose():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            dose = float(request.form['dose'])
            
            # Validação dos valores
            if peso <= 0 or dose <= 0:
                flash("Valores devem ser maiores que zero!", "erro")
            else:
                resultado = f"{(peso * dose):.2f} mg"
                
        except ValueError:
            flash("Valores inválidos! Use números positivos.", "erro")
        except Exception as e:
            flash(f"Ocorreu um erro: {str(e)}", "erro")
            
    return render_template('cal_dose.html', resultado=resultado)

@app.route('/cal_desitratacao', methods=['GET', 'POST'])
def calculadora_desitratacao():
    resultado = None
    if request.method == 'POST':
        try:
            peso = float(request.form['peso'])
            grau = request.form['grau'].lower()
            
            # Validação do peso
            if peso <= 0:
                flash("O peso deve ser maior que zero!", "erro")
                return render_template('cal_desitra.html', resultado=resultado)
            
            volumes = {'leve': 50, 'moderada': 75, 'grave': 100}
            if grau not in volumes:
                flash("Grau inválido! Use: leve, moderada ou grave", "erro")
            else:
                resultado = f"{(peso * volumes[grau]):.2f} ml"
                
        except ValueError:
            flash("Valor de peso inválido! Use números positivos.", "erro")
        except Exception as e:
            flash(f"Ocorreu um erro: {str(e)}", "erro")
            
    return render_template('cal_desitra.html', resultado=resultado)
if __name__ == '__main__':
    app.run(debug=True)