# Autores:
# Darlan de Castro Silva Filho
# Marcos Henrique Fernandes Marcone


from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Funções de estilização e opções das bibliotecas utilizadas
plt.style.use('classic')
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Função para o path das bases de dados
# Entrada: nome = string
# Saida: path = string


def path(nome):
    return './'+nome+'.csv'


# Importa os arquivos (bases de dados) utilizados
unidades = pd.read_csv(path('unidades'), sep=';')
docentes = pd.read_csv(path('docentes'), sep=';')
avaliacao = pd.read_csv(path('avaliacaoDocencia'), sep=';')

# Filtra os docentes que trabalham em Natal e que tenham a categoria de Professor do Magistério Superior
unidadesFiltradas = unidades.loc[:, [
    'id_unidade', 'municipio', 'unidade_responsavel']]
docentesComUnidadeAcademica = pd.merge(
    docentes, unidadesFiltradas, left_on="id_unidade_lotacao", right_on="id_unidade").drop('id_unidade', axis=1)
docentesNatalUnidadeAcademica = docentesComUnidadeAcademica[
    docentesComUnidadeAcademica['municipio'] == 'NATAL']
docentesNatalMSUnidadeAcademica = docentesNatalUnidadeAcademica[
    docentesNatalUnidadeAcademica['categoria'] == 'PROFESSOR DO MAGISTERIO SUPERIOR']

# Filtra as unidades_dirigentes não aceitas pela aplicação
docentesNatalMSUnidadeAcademica['unidade_dirigente'] = np.where(docentesNatalMSUnidadeAcademica['unidade_responsavel'] == 'UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE', (
    docentesNatalMSUnidadeAcademica['lotacao']), (docentesNatalMSUnidadeAcademica['unidade_responsavel']))
unidadesNaoAceitas = ['PRÓ-REITORIA DE EXTENSÃO UNIVERSITÁRIA', 'MUSEU CÂMARA CASCUDO', 'UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE', 'EDITORA UNIVERSITÁRIA', 'EMPRESA BRASILEIRA DE SERVICOS HOSPITALARES',
                      'REITORIA', 'INSTITUTO DE MEDICINA TROPICAL - IMT-RN', 'SECRETARIA DE EDUCAÇÃO A DISTÂNCIA', 'GABINETE DO REITOR', 'SUPERINTENDENCIA DE COMUNICACAO', 'PRÓ-REITORIA DE ADMINISTRAÇÃO (PROAD)']
docentesNatalMSUnidadeAcademica = docentesNatalMSUnidadeAcademica[~docentesNatalMSUnidadeAcademica['unidade_dirigente'].isin(
    unidadesNaoAceitas)]

# Gráfico de barras da distribuição dos docentes da UFRN por unidade acadêmica
quantidadeDocentesUnidadeDirigente = docentesNatalMSUnidadeAcademica['unidade_dirigente'].value_counts(
)
barraDocentesUnidadeDirigente = go.Bar(x=quantidadeDocentesUnidadeDirigente.index,
                                       y=quantidadeDocentesUnidadeDirigente.values, text=quantidadeDocentesUnidadeDirigente.values, textposition='auto')
layoutDocentesUnidadeDirigente = go.Layout(title='Gráfico de docentes por unidade responsável (UFRN 2021 - Unidades de Natal - Magistério Superior)', xaxis={
                                           'title': 'Unidade responsável'}, yaxis={'title': 'Número de docentes'})
figuraDocentesUnidadeDirigente = go.Figure(
    data=[barraDocentesUnidadeDirigente], layout=layoutDocentesUnidadeDirigente)

# Gráfico de pizza da distribuição dos docentes da UFRN por sexo
quantidadeDocentesSexo = docentesNatalMSUnidadeAcademica['sexo'].value_counts()
piechartSexo = go.Pie(labels=['Masculino', 'Feminino'], values=quantidadeDocentesSexo.values, text=quantidadeDocentesSexo.values, marker={
                      'colors': ['#665FD1', '#FFFF7E'], 'line': dict(color='#000000', width=2)})
layoutDocentesSexo = go.Layout(title='Gráfico de docentes por sexo (UFRN 2021 - Unidades de Natal - Magistério Superior)',
                               xaxis={'title': 'Docentes'}, yaxis={'title': 'Número de docentes'}, barmode='stack')
figuraDocentesSexo = go.Figure(data=piechartSexo, layout=layoutDocentesSexo)

# Gráfico de pizza da distribuição dos docentes da UFRN por formação acadêmica
quantidadeDocentesFormacao = docentesNatalMSUnidadeAcademica['formacao'].value_counts(
)
piechartFormacao = go.Pie(labels=quantidadeDocentesFormacao.index, values=quantidadeDocentesFormacao.values, text=quantidadeDocentesFormacao.values, marker={
                          'colors': ['#665FD1', '#FFFF7E', '#F5054F', '#3F012C'], 'line': dict(color='#000000', width=2)})
layoutDocentesFormacao = go.Layout(title='Gráfico de docentes por formação (UFRN 2021 - Unidades de Natal - Magistério Superior)',
                                   xaxis={'title': 'Formação'}, yaxis={'title': 'Número de docentes'})
figuraDocentesFormacao = go.Figure(
    data=[piechartFormacao], layout=layoutDocentesFormacao)

# Gráfico de pizza da distribuição dos docentes da UFRN por classe funcional
quantidadeDocentesClasseFuncional = docentesNatalMSUnidadeAcademica['classe_funcional'].value_counts(
).sort_index()
piechartClasseFuncional = go.Pie(labels=quantidadeDocentesClasseFuncional.index, values=quantidadeDocentesClasseFuncional.values,
                                 text=quantidadeDocentesClasseFuncional.values, marker={'colors': px.colors.qualitative.Dark24, 'line': dict(color='#000000', width=2)})
barraDocentesClasseFuncional = go.Bar(x=quantidadeDocentesClasseFuncional.index, y=quantidadeDocentesClasseFuncional.values,
                                      text=quantidadeDocentesClasseFuncional.values, textposition='auto', marker={'color': '#5D21D0'})
layoutDocentesClasseFuncional = go.Layout(title='Gráfico de docentes por classe funcional (UFRN 2021 - Unidades de Natal - Magistério Superior)', xaxis={
                                          'title': 'Classe funcional'}, yaxis={'title': 'Número de docentes'}, height=450)
figuraDocentesClasseFuncional = go.Figure(
    data=[piechartClasseFuncional], layout=layoutDocentesClasseFuncional)

# Cria gráfico para ressaltar os dados de classe funcional dos docentes agrupados por unidade_dirigente
filtroClasseFuncional = ['unidade_dirigente', 'classe_funcional']
docentesClasseGroupBy = docentesNatalMSUnidadeAcademica.groupby(
    filtroClasseFuncional).count().reset_index().loc[:, filtroClasseFuncional + ['nome']]
docentesClasseGroupBy['quantidade'] = docentesClasseGroupBy['nome']
del docentesClasseGroupBy['nome']
figClasseDetalhe = px.bar(docentesClasseGroupBy, x="unidade_dirigente", y="quantidade", color="classe_funcional",
                          text='quantidade', color_discrete_sequence=px.colors.qualitative.Bold, height=800)

# Cria gráfico para ressaltar os dados de sexo dos docentes agrupados por unidade_dirigente
filtroSexo = ['unidade_dirigente', 'sexo']
docentesSexoGroupBy = docentesNatalMSUnidadeAcademica.groupby(
    filtroSexo).count().reset_index().loc[:, filtroSexo + ['nome']]
docentesSexoGroupBy['quantidade'] = docentesSexoGroupBy['nome']
del docentesSexoGroupBy['nome']
figSexoDetalhe = px.bar(docentesSexoGroupBy, x="unidade_dirigente", y="quantidade",
                        color="sexo", text='quantidade', color_discrete_sequence=px.colors.qualitative.Bold)

# Cria gráfico para ressaltar os dados de formação acadêmica dos docentes agrupados por unidade_dirigente
filtroFormacao = ['unidade_dirigente', 'formacao']
docentesFormacaoGroupBy = docentesNatalMSUnidadeAcademica.groupby(
    filtroFormacao).count().reset_index().loc[:, filtroFormacao + ['nome']]
docentesFormacaoGroupBy['quantidade'] = docentesFormacaoGroupBy['nome']
del docentesFormacaoGroupBy['nome']
figFormacaoDetalhe = px.bar(docentesFormacaoGroupBy, x="unidade_dirigente",
                            y="quantidade", color="formacao", text='quantidade', range_y=[0, 400])

# Cria um dicionário com os dados indexados por unidade_dirigente
unidadesDirigentes = docentesNatalMSUnidadeAcademica['unidade_dirigente'].unique(
)
unidadesDirigentes
dfUnidadesDirigentes = {}
for unidadeDirigente in unidadesDirigentes:
    df = docentesNatalMSUnidadeAcademica[docentesNatalMSUnidadeAcademica['unidade_dirigente'] == unidadeDirigente]
    dfUnidadesDirigentes[unidadeDirigente] = df

# Função utilizada na filtragem de um dataFrame agrupando os dados por uma propriedade e o filtrando por outras duas
# Entradas: df = DataFrame, title = string, x = string, y = string, cor = ['rgb(a,b,c)','rgb(d,e,f)'...]
# Saídas: figAdmissao = Gráfico de barras


def filtrarDFPorUnidadeDirigente(df, title, x, y, cor=px.colors.qualitative.Bold):
    dfFinal = df[title]
    filtro = [x, y]
    docentesFiltroGroupBy = dfFinal.groupby(
        filtro).count().reset_index().loc[:, filtro + ['nome']]
    docentesFiltroGroupBy['quantidade'] = docentesFiltroGroupBy['nome']
    del docentesFiltroGroupBy['nome']
    figAdmissao = px.bar(docentesFiltroGroupBy, x=x, y="quantidade", color=y,
                         text='quantidade', color_discrete_sequence=cor, title=title)
    return figAdmissao


# Cria e formata um dataFrame geral com todos os professores e os atributos necessários para a geração dos gráficos e da tabela por média
avaliacaoDocentesFiltro = avaliacao[avaliacao['nome_docente'].isin(
    docentesNatalMSUnidadeAcademica['nome'])]
avaliacaoDocentesFiltro['total_postura'] = avaliacaoDocentesFiltro['postura_profissional_media'] * \
    avaliacaoDocentesFiltro['qtd_discentes']
avaliacaoDocentesFiltro['total_atuacao'] = avaliacaoDocentesFiltro['atuacao_profissional_media'] * \
    avaliacaoDocentesFiltro['qtd_discentes']
docentesMedias = avaliacaoDocentesFiltro.loc[:, [
    'nome_docente', 'qtd_discentes', 'total_postura', 'total_atuacao']]
docentesMediasGroupBy = docentesMedias.groupby(['nome_docente']).sum()
docentesMediasGroupBy['media_postura'] = docentesMediasGroupBy['total_postura'] / \
    docentesMediasGroupBy['qtd_discentes']
docentesMediasGroupBy['media_atuacao'] = docentesMediasGroupBy['total_atuacao'] / \
    docentesMediasGroupBy['qtd_discentes']
docentesMediasGroupBy['media_alunos'] = avaliacaoDocentesFiltro.groupby(
    ['nome_docente']).mean().loc[:, 'autoavaliacao_aluno_media']
docentesMediasNatalMSUnidadeAcademica = pd.merge(
    docentesNatalMSUnidadeAcademica, docentesMediasGroupBy, left_on="nome", right_on="nome_docente").round(3)

# Exclui os campos não necessários para a geração da tabela de notas e assinala os campos restantes para um novo dataFrame
docenteParaTabelaNotas = docentesMediasNatalMSUnidadeAcademica.loc[:, [
    'nome', 'media_postura', 'media_atuacao', 'media_alunos', 'unidade_dirigente', 'lotacao', 'qtd_discentes']]

# Faz a filtragem e formatação de um dataFrame para agrupas os dados da media_postura, media_atuacao e media_alunos por undade_dirigente
docentesMediaUnidadeDirigente = docentesMediasNatalMSUnidadeAcademica.groupby(
    'unidade_dirigente').mean().loc[:, ['media_postura', 'media_atuacao', 'media_alunos']]
docentesMediaUnidadeDirigente['unidade_dirigente'] = docentesMediaUnidadeDirigente.index

# Faz a filtragem e formatação de um dataFrame para conter as informações da media_postura, media_atuacao e media_alunos a serem apresentas no gráfico de linha por evolução temporal
docentesMediasAno = avaliacaoDocentesFiltro.loc[:, [
    'nome_docente', 'qtd_discentes', 'total_postura', 'total_atuacao', 'ano']]
docentesMediasAnoGroupBy = docentesMediasAno.groupby(['ano']).sum()
docentesMediasAnoGroupBy['media_postura'] = docentesMediasAnoGroupBy['total_postura'] / \
    docentesMediasAnoGroupBy['qtd_discentes']
docentesMediasAnoGroupBy['media_atuacao'] = docentesMediasAnoGroupBy['total_atuacao'] / \
    docentesMediasAnoGroupBy['qtd_discentes']
docentesMediasAnoGroupBy['media_alunos'] = avaliacaoDocentesFiltro.groupby(
    ['ano']).mean().loc[:, 'autoavaliacao_aluno_media']
docentesMediasAnoGroupBy['ano'] = docentesMediasAnoGroupBy.index

# Cria o gráfico de linhas da evolução temporal da media_postura, media_atuacao e media_alunos
figuraMediasAnoGroupBy = go.Figure()
figuraMediasAnoGroupBy.add_trace(go.Scatter(x=docentesMediasAnoGroupBy['ano'], y=docentesMediasAnoGroupBy['media_postura'],
                                            mode='lines',
                                            name='media_postura'))
figuraMediasAnoGroupBy.add_trace(go.Scatter(x=docentesMediasAnoGroupBy['ano'], y=docentesMediasAnoGroupBy['media_atuacao'],
                                            mode='lines',
                                            name='media_atuacao'))
figuraMediasAnoGroupBy.add_trace(go.Scatter(x=docentesMediasAnoGroupBy['ano'], y=docentesMediasAnoGroupBy['media_alunos'],
                                            mode='lines',
                                            name='media_alunos'))
figuraMediasAnoGroupBy.update_layout(
    title='Evolução da avaliação dos discentes e docentes do magistério superior da UFRN nos anos de 2013 à 2019')

# Define as opções de unidades dirigentes que serão mostradas no 'dropdown-1'
indicadoresDropdown1 = [
    'GERAL'] + list(docentesNatalMSUnidadeAcademica['unidade_dirigente'].unique())

# Estilos das divs dos gráficos iniciais
estilosDivGraficosIniciais = {'width': '95%',
                              'display': 'inline-block', 'padding': '0 20'}

# Cria a variável app e escolhe os stylesheets da aplicação
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define o layout a ser apresentado na página web
app.layout = html.Div([
    html.H1(children='Análise dos dados dos docentes do magistério superior da UFRN das unidades de Natal no ano de 2021'),
    html.Div([
        dcc.Markdown('''
Trabalho referente à disciplina DCA-0131, Ciência de Dados, ministrada pelo professor Luiz Affonso Hederson Guedes de Oliveira.

Plataforma desenvolvida pelos discentes Darlan de Castro e Marcos Henrique, alunos do curso de Engenharia Computação da UFRN.

A aplicação web desenvolvida consiste em uma análise exploratória dos dados sobre os docentes do magistério superior das unidades de Natal da Universidade Federal do Rio Grande do Norte (UFRN) no ano de 2021.

Os dados utilizados aqui podem ser acessados pelo seguinte site: [http://dados.ufrn.br](http://dados.ufrn.br)

As principais tecnologias usadas para o desenvolvimento da plataforma foram:

* Linguagem Python;
* Pacotes Pandas, Plotly e Dash;
* Heroku (deploy da aplicação).
''')
    ]),
    html.H2(
        children='Divisão dos docentes do magistério superior da UFRN no ano de 2021'),
    html.Div([

        html.Div([
            dcc.Markdown('''
            Nesta seção da aplicação pode-se acompanhar a divisão dos docentes através de difentes categorias, como sexo, formação e classe funcional, assim como ver como eles estão distribuídos por cada unidade responsável na UFRN.

            Na primeira caixa de seleção pode-se escolher qual unidade responsável deseja-se analisar. Assim, são atualizados os três primeiros gráficos com informações das divisões dos decentes referentes a cada lotação que compõe aquela unidade responsável.

            Se a opção for escolhida for "GERAL", então pode-se mostar gráficos gerais sobre toda as unidades de Natal da UFRN, ou gráficos detalhados mostrando a divisão por unidades responsáveis.
            '''),
            dcc.Dropdown(
                id='dropdown-1',
                options=[{'label': i, 'value': i}
                         for i in indicadoresDropdown1],
                value='GERAL'
            ),
            dcc.RadioItems(
                id='radioitems-1',
                options=[{'label': i, 'value': i}
                         for i in ['GERAL', 'DETALHADA']],
                value='GERAL',
                labelStyle={'display': 'inline-block'}
            )
        ],
            style={'width': '80%', 'display': 'inline-block'}),


        html.Div([
            dcc.Graph(
                id='grafico-sexo')
        ], style=estilosDivGraficosIniciais),
        html.Div([
            dcc.Graph(
                id='grafico-formacao')
        ], style=estilosDivGraficosIniciais),
        html.Div([
            dcc.Graph(
                id='grafico-classe')
        ], style=estilosDivGraficosIniciais),
        html.Div([
            dcc.Graph(
                id='grafico-sobra',
                figure=figuraDocentesUnidadeDirigente)
        ], style=estilosDivGraficosIniciais, id='div-grafico-sobra'),
    ]),

    html.H2(children='Estatísticas das avaliações dos docentes do magistério superior da UFRN (campus Natal) nos anos de 2013 à 2019'),
    dcc.Markdown('''
    Nesta seção da aplicação pode-se acompanhar dados sobre as avaliações dos docentes da UFRN e da autoavalição dos alunos feita a cada fim de semestre. Os dados disponibilizados constam do período de 2013 à 2019.

    Ao todo são três dados importantes a serem considerados a média de postura dos docentes, a média de atuação dos docentes e autoavaliação dos alunos.

    No primeiro gráfico pode-se acompanhar a média desses três quesitos por cada unidade responsável.
    '''),
    html.Div([
        dcc.Graph(
            id='grafico-nota-1')
    ], style={'width': '95%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Slider(
            id='slider-grafico-nota-1',
            min=1,
            max=3,
            value=1,
            marks={str(i): str(i) for i in [1, 2, 3]},
            step=None)],
        style={'width': '80%', 'padding': '0px 15px 15px 15px'}),

    dcc.Markdown('''
    * Opção 1 - Média de atuação dos docentes;
    * Opção 2 - Média de postura dos docentes;
    * Opção 3 - Média da autoavaliação dos discentes.
    '''),

    dcc.Markdown('''
    No segundo gráfico há dados sobre a evolução das médias de postura e atuação dos docentes e autoavaliação dos discentes ao longo dos anos. 
            '''),

    html.Div([
        dcc.Graph(
            id='grafico-nota-2',
            figure=figuraMediasAnoGroupBy)
    ], style={'width': '95%', 'display': 'inline-block', 'padding': '0 20'}),

    dcc.Markdown('''
    No terceito gráfico pode-se ver um histograma com a frequência das médias de postura e atuação dos docentes dividida por sexo.
            '''),

    html.Div([
        dcc.Graph(
            id='grafico-histograma')
    ], style={'width': '95%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Slider(
            id='slider-grafico-histograma',
            min=1,
            max=2,
            value=1,
            marks={str(i): str(i) for i in [1, 2]},
            step=None)],
        style={'width': '80%', 'padding': '0px 15px 15px 15px'}),

    dcc.Markdown('''
        * Opção 1 - Média de atuação dos docentes;
        * Opção 2 - Média de postura dos docentes.
            '''),

    dcc.Markdown('''
    Nesta parte, pode-se selecionar uma unidade responsável (primeira caixa de seleção) e a partir dela escolher uma lotação (segunda caixa de seleção) para verificar a média de atuação e postura de cada profressor, assim como da autoavaliação dos discentes das turmas desses docentes e quantidade de discentes que passaram por eles, para cada departamento da UFRN.
    '''),
    html.Div([
        dcc.Dropdown(
            id='dropdown-2',
            options=[{'label': i, 'value': i}
                     for i in docenteParaTabelaNotas['unidade_dirigente'].unique()],
            value=docenteParaTabelaNotas['unidade_dirigente'].iloc[0]
        )],
        style={'width': '80%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='dropdown-3',
        )],
        style={'width': '80%', 'display': 'inline-block'}),

    html.Div([
        dash_table.DataTable(
            id='table-nota',
            columns=[{"name": i, "id": i} for i in [
                'nome', 'media_postura', 'media_atuacao', 'media_alunos', 'qtd_discentes']],
            style_cell={'textAlign': 'left'},
        )
    ], style={'width': '95%', 'display': 'inline-block', 'padding': '0 20'}),

])

# Callback para atualização do estilo dos gráfico de barras (quatantidadeDocente x unidade_dirigente)
# Entradas: 'value' - 'dropdown-1', 'value' - 'radioitems-1'
# Saída: 'figure' - 'grafico-classe'


@app.callback(
    dash.dependencies.Output('div-grafico-sobra', 'style'),
    [dash.dependencies.Input('dropdown-1', 'value'),
     dash.dependencies.Input('radioitems-1', 'value')])
def visibility_graficoSobra(dropValue, radioValue):
    if(radioValue == 'GERAL' and dropValue == 'GERAL'):
        estilosDivGraficosIniciais['display'] = 'inline-block'
        return estilosDivGraficosIniciais
    estilosDivGraficosIniciais['display'] = 'none'
    return estilosDivGraficosIniciais

# Callback para atualização da 'figure' no gráfico por sexo.
# Entradas: 'value' - 'dropdown-1', 'value' - 'radioitems-1'
# Saída: 'figure' - 'grafico-sexo'


@app.callback(
    dash.dependencies.Output('grafico-sexo', 'figure'),
    [dash.dependencies.Input('dropdown-1', 'value'),
     dash.dependencies.Input('radioitems-1', 'value')])
def att_sexo(dropValue, radioValue):
    if(radioValue == 'GERAL' and dropValue == 'GERAL'):
        return figuraDocentesSexo
    elif(radioValue == 'DETALHADA' and dropValue == 'GERAL'):
        return figSexoDetalhe
    return filtrarDFPorUnidadeDirigente(dfUnidadesDirigentes, dropValue, 'lotacao', 'sexo')

# Callback para atualização da 'figure' no gráfico por formação
# Entradas: 'value' - 'dropdown-1', 'value' - 'radioitems-1'
# Saída: 'figure' - 'grafico-formacao'


@app.callback(
    dash.dependencies.Output('grafico-formacao', 'figure'),
    [dash.dependencies.Input('dropdown-1', 'value'),
     dash.dependencies.Input('radioitems-1', 'value')])
def att_formacao(dropValue, radioValue):
    if(radioValue == 'GERAL' and dropValue == 'GERAL'):
        return figuraDocentesFormacao
    elif(radioValue == 'DETALHADA' and dropValue == 'GERAL'):
        return figFormacaoDetalhe
    return filtrarDFPorUnidadeDirigente(dfUnidadesDirigentes, dropValue, 'lotacao', 'formacao')

# Callback para atualização da 'figure' no gráfico por classe
# Entradas: 'value' - 'dropdown-1', 'value' - 'radioitems-1'
# Saída: 'figure' - 'grafico-classe'


@app.callback(
    dash.dependencies.Output('grafico-classe', 'figure'),
    [dash.dependencies.Input('dropdown-1', 'value'),
     dash.dependencies.Input('radioitems-1', 'value')])
def att_classe(dropValue, radioValue):
    if(radioValue == 'GERAL' and dropValue == 'GERAL'):
        return figuraDocentesClasseFuncional
    elif(radioValue == 'DETALHADA' and dropValue == 'GERAL'):
        return figClasseDetalhe
    return filtrarDFPorUnidadeDirigente(dfUnidadesDirigentes, dropValue, 'lotacao', 'classe_funcional')

# Callback para atualização da 'figure' no gráfico por nota
# Entradas: 'value' - 'slider-grafico-nota-1'
# Saída: 'figure' - 'grafico-nota-1'


@app.callback(
    dash.dependencies.Output('grafico-nota-1', 'figure'),
    [dash.dependencies.Input('slider-grafico-nota-1', 'value')])
def att_nota1(sliderValue):
    var = 'media_atuacao'
    if sliderValue == 2:
        var = 'media_postura'
    elif sliderValue == 3:
        var = 'media_alunos'
    return px.scatter(docentesMediaUnidadeDirigente, x="unidade_dirigente", y=var,
                      size=var, hover_name="unidade_dirigente", color="unidade_dirigente")

# Callback para atualização da 'figure' no histograma
# Entradas: 'value' - 'slider-grafico-histograma'
# Saída: 'figure' - 'grafico-histograma'


@app.callback(
    dash.dependencies.Output('grafico-histograma', 'figure'),
    [dash.dependencies.Input('slider-grafico-histograma', 'value')])
def att_histograma(sliderValue):
    var = 'media_atuacao'
    if sliderValue == 2:
        var = 'media_postura'
    return px.histogram(docentesMediasNatalMSUnidadeAcademica, x=var, color="sexo", title='Histograma da avaliação dos docentes do magistério superior da UFRN nos anos de 2013 à 2019')

# Callback para atualização das 'options' no dropdown por lotação da tabela
# Entradas: 'value' - 'dropdown-2'
# Saída: 'options' - 'dropdown-3'


@app.callback(
    dash.dependencies.Output('dropdown-3', 'options'),
    [dash.dependencies.Input('dropdown-2', 'value')])
def att_dropdown3Options(dropValue):
    df = docenteParaTabelaNotas[docenteParaTabelaNotas['unidade_dirigente'] == dropValue]
    del df['unidade_dirigente']
    return [{'label': 'GERAL', 'value': 'GERAL'}] + [{'label': i, 'value': i} for i in df['lotacao'].unique()]

# Callback para atualização do 'value' no dropdown por lotação da tabela
# Entradas: 'value' - 'dropdown-2'
# Saída: 'value' - 'dropdown-3'


@app.callback(
    dash.dependencies.Output('dropdown-3', 'value'),
    [dash.dependencies.Input('dropdown-2', 'value')])
def att_dropdown3Value(dropValue):
    return 'GERAL'

# Callback para atualização da 'data' na tabela de exposição das notas dos professores por unidade_dirigente e lotação
# Entradas: 'value' - 'dropdown-2', value' - 'dropdown-3'
# Saída: 'data' - 'table-nota'


@app.callback(
    dash.dependencies.Output('table-nota', 'data'),
    [dash.dependencies.Input('dropdown-2', 'value'),
     dash.dependencies.Input('dropdown-3', 'value')])
def att_table(dropValue2, dropValue3):
    df = docenteParaTabelaNotas[docenteParaTabelaNotas['unidade_dirigente'] == dropValue2]
    del df['unidade_dirigente']
    if dropValue3 == 'GERAL':
        del df['lotacao']
        return df.to_dict("records")
    df = docenteParaTabelaNotas[docenteParaTabelaNotas['lotacao'] == dropValue3]
    del df['lotacao']
    return df.to_dict("records")


# Atribui o servidor da aplicação a variável server
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
