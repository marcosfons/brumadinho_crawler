import os
from PIL import Image

filename='vitimas.pdf'
local_dir = os.getcwd()

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

# Cut Images
def CutImages(filename):
    os.chdir(local_dir + '/imgs/' + filename)
    os.mkdir(local_dir + '/cortadas')
    for arq in os.listdir():
        print(arq)
        if(arq.find('.jpg') != -1):
            name = arq[:arq.rindex('.')]
            img = Image.open(arq)
            area = (220, 495, 2265, 3300)
            cropped_img = img.crop(area)
            cropped_img.save(local_dir + '/cortadas/' + name + '.jpg')

# Extract text

def ExtractText(filename):
    import pytesseract
    os.chdir(local_dir + '/cortadas/')
    os.mkdir(local_dir + '/txts')
    for arq in os.listdir():
        if(arq.find('.jpg') != -1):
            print(arq)
            name = arq[:arq.rindex('.')]
            with open(local_dir + '/txts/' + name + '.txt', 'w') as file:
                file.write(pytesseract.image_to_string(Image.open(arq), lang='por', config='--psm 6'))

def organizeData():
    os.chdir(local_dir + '/txts')
    data = []
    for arq in os.listdir():
        with open(arq, 'r') as file:
            lista = file.read().replace('Préprios', 'Próprios').split('\n')
            cats = ['Próprios', 'Terceiro/Comunidade']
            status = [' Localizado', ' Óbito confirmado pelo IML', ' Sem Contato']
            for pessoa in lista:
                for cat in cats:
                    if(pessoa.find(cat) != -1):
                        teste = pessoa.split(cat)
                        teste.append(cat)
                        for stat in status:
                            if(teste[1].find(stat) != -1 and len(teste[1]) != len(stat)):
                                teste.append(teste[1][len(stat):])
                                teste[1] = teste[1][:len(stat)]
                        data.append(teste)
    with open(local_dir + r'\resultado.json', 'w') as file:
        file.write(str(data))
    print(data)
    print(len(data))

#download('http://www.vale.com/brasil/PT/aboutvale/servicos-para-comunidade/minas-gerais/atualizacoes_brumadinho/Documents/PDFs/290120192000.pdf', filename)
#toImages(filename)
#CutImages(filename)
#ExtractText(filename)
organizeData()

