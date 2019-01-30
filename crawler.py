import os
from PIL import Image

filename='vitimas.pdf'
local_dir = os.getcwd()

encoding = 'utf-8'

# Download pdf
def download(url, filename):
    import requests
    r = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(r.content)

# To images
def toImages(filename, outPath=local_dir + r"\imgs"):
    from pdf2jpg import pdf2jpg
    result = pdf2jpg.convert_pdf2jpg(filename, outPath, pages="ALL")
    print(result)

# Extract text

def ExtractText(filename):
    import pytesseract
    #os.chdir(local_dir + '/cortadas/')
    os.chdir(local_dir + '/imgs/' + filename)
    os.mkdir(local_dir + '/txts')
    for arq in os.listdir():
        if(arq.find('.jpg') != -1):
            name = arq[:arq.rindex('.')]
            img = Image.open(arq)
            area = (220, 495, 2265, 3300)
            img = img.crop(area).convert('L')
            img = img.resize([img.width*2,img.height*2], Image.ANTIALIAS)
            name = arq[:arq.rindex('.')]
            with open(local_dir + '/txts/' + name + '.txt', 'w', -1, encoding) as file:
                dados = pytesseract.image_to_string(img, config='--psm 6')
                print(dados)
                file.write(dados)

def organizeData():
    os.chdir(local_dir + '/txts')
    data = []
    for arq in os.listdir():
        with open(arq, 'r', -1, encoding) as file:
            lista = file.read().replace('Prdaprios', 'Próprios').replace('Préprios', 'Próprios').replace('Prdéprios', 'Próprios').replace('Prdoprios', 'Próprios').replace('Proprios', 'Próprios').replace('Prdprios', 'Próprios').replace('Prdprios', 'Próprios').replace('Obito', 'Óbito').split('\n')
            cats = ['Próprios', 'Terceiro/Comunidade']
            status = [' Localizado', ' Óbito confirmado pelo IML', ' Sem Contato']
            for pessoa in lista:
                for cat in cats:
                    if(pessoa.find(cat) != -1):
                        info = pessoa.split(cat)
                        info.append(cat)
                        for stat in status:
                            if(info[1].find(stat) != -1 and len(info[1]) != len(stat)):
                                info.append(info[1][len(stat):])
                                info[1] = info[1][:len(stat)]
                        data.append(info)
    with open(local_dir + r'\resultado.json', 'w', -1, 'utf-8') as file:
        file.write(str(data).replace("'", '"'))
    print(data)
    print(len(data))

download('http://www.vale.com/brasil/PT/aboutvale/servicos-para-comunidade/minas-gerais/atualizacoes_brumadinho/Documents/PDFs/290120192000.pdf', filename)
toImages(filename)
ExtractText(filename)
organizeData()

# Format of result data
# ['Nome', 'Category', 'Status', 'Hospital']