import sys
import urllib.request as request
import xml.etree.ElementTree as ET

def cria_url(ano, dtInicio, dtFim):
    url = 'http://www.camara.leg.br/SitCamaraWS/Proposicoes.asmx/ListarProposicoes?sigla=PL&numero=&ano={}&datApresentacaoIni={}&datApresentacaoFim={}&parteNomeAutor=&idTipoAutor=&siglaPartidoAutor=&siglaUFAutor=&generoAutor=&codEstado=&codOrgaoEstado=&emTramitacao='
    url.format(ano, dtInicio, dtFim)

def abre_url(url):
    req = request.urlopen(url)
    if req.getcode() == 200:
        return req.read()
    else:
        return None

def percorre(dados):
    proposicoes = ET.fromstring(dados)
    filtro = sys.argv[1]
    proposicoes_filtradas = []

    for proposicao in proposicoes:
        obj = extrai_texto(proposicao)
        if filtro in obj['txtEmenta']:
            proposicoes_filtradas.append(obj)

    for proposicao in proposicoes_filtradas:
        print(proposicao)

def extrai_texto(proposicao):
    attrs = ('txtEmenta', 'nome')
    prop_dict = {}
    for tag_filha in proposicao:
        if tag_filha.tag in attrs:
            prop_dict[tag_filha.tag] = tag_filha.text.strip()
    return prop_dict


ano = int(input("Ano:"))
dtInicio = input("Data de início:")
dtFim = input("Data de término:")

url = cria_url(ano, dtInicio, dtFim)
percorre(abre_url(url))