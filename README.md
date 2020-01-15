# Projeto
Um programa para otimizar o download dos filmes 
e legendas presentes no site [Filmes Cult](https://filmestorrentshd.org/cult/)

## Pré-requisitos:

É necessário ter instalado o programa [qBittorrent](https://www.qbittorrent.org/) 
para realizar o download de filmes.

## Como Funciona?

O projeto possui um único arquivo capaz de realizar pesquisas 
bem como o download dos arquivos do site.

Para realizar pesquisas, basta rodar o comando:

```bash
$ python filmes_cult.py -p 'minha pesquisa'
```

Após isso, você receberá via terminal a lista dos filmes 
presentes na plataforma que batem com sua pesquisa.

Para fazer o download de um determinado filme:

```bash
$ python filmes_cult.py -d 'nome do filme e ano'
```

No comando acima você pode usar apenas letras minúsculas e números, 
caso seja adicionado algum outro carácter o programa realiza uma 
normalização antes de procurar pela legenda e o magnet link.

Após isso, um novo diretório com o nome do filme será criado onde 
estarão as legendas (em formato srt) e o filme (assim que o download 
no qBittorrent tenha sido finalizado).
