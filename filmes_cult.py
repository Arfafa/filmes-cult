import argparse
import io
import re
import os
import unicodedata
import zipfile
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('-p',
                    '--pesquisa',
                    nargs='+',
                    default=None,
                    help='Item procurado')

parser.add_argument('-d',
                    '--download',
                    nargs='+',
                    default=None,
                    help='Título para download')

args = parser.parse_args()


def search(pesquisa):
    url = 'https://filmescult.net/?s='

    page = requests.get(url+pesquisa)
    soup = BeautifulSoup(page.content, 'html.parser')

    filmes = []

    for filme in soup.find_all('h2', class_='entry-title'):
        movie = filme.find('a').text

        if re.search(r'\(+4*[0-9]+\)', movie):
            filmes.append(movie)

    return filmes


def download(filme):
    url = 'https://filmescult.net/'

    page = requests.get(url+filme)
    soup = BeautifulSoup(page.content, 'html.parser')

    magnet_link = ''
    legenda = ''

    for link in soup.find_all('a'):

        if link.get('href').startswith('magnet'):
            magnet_link = link.get('href')

        elif link.get('href').endswith('.zip'):
            legenda = link.get('href')

    if filme not in os.listdir():
        os.mkdir(filme)

    if legenda:
        download_legenda(legenda, filme)

    else:
        print('Legenda não encontrada')

    if magnet_link:
        download_torrent(magnet_link, filme)

    else:
        print('Magnet Link não encontrado')


def download_legenda(legenda_link, name_dir):
    page = requests.get(legenda_link)

    if page.ok:
        zfile = zipfile.ZipFile(io.BytesIO(page.content))
        zfile.extractall(name_dir)


def download_torrent(magnet_link, name_dir):
    path = os.path.abspath(name_dir)

    command = f'qbittorrent --save-path={path} '
    command += '--skip-dialog=true '
    command += f'{magnet_link} &'

    os.system(command)


def tratamento_flags(flag, sep):
    if len(flag) == 1:
        nome = sep.join(flag[0].split())

    else:
        nome = sep.join(flag)

    return nome


def normalize_name(data):
    nome = data.lower()
    nome = unicodedata.normalize('NFKD', nome)
    nome = nome.encode('ASCII', 'ignore')
    nome = nome.decode('utf-8')

    nome = re.sub("[^a-z0-9\-]+", "", nome)

    nome_list = [w for w in nome.split('-') if w]

    nome = '-'.join(nome_list)

    return nome


def main():
    if args.pesquisa:
        nome = tratamento_flags(args.pesquisa, '+')

        filmes = search(nome)

        for filme in filmes:
            print(filme)

        if not filmes:
            nome = ' '.join(nome.split('+'))
            print(f'Nenhum filme encontrado com: {nome}')

    elif args.download:
        nome = tratamento_flags(args.download, '-')
        nome = normalize_name(nome)

        download(nome)


if __name__ == '__main__':
    main()
