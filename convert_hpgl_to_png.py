import sys
from PIL import Image, ImageDraw

# Função para interpretar comandos HPGL, ignorando comandos inválidos ou desconhecidos
def parse_hpgl(hpgl_commands):
    commands = []
    for command in hpgl_commands.split(';'):
        if command:
            cmd = command[:2]  # Exemplo: 'PU' ou 'PD'
            args = command[2:].strip()  # Os argumentos após o comando
            if cmd in ['PU', 'PD']:  # Processa apenas 'PU' e 'PD'
                if args:
                    try:
                        # Dividir as coordenadas e convertê-las para inteiros
                        args = list(map(int, args.split(',')))
                        commands.append((cmd, args))
                    except ValueError:
                        print(f"Erro ao processar os argumentos: {args}")
    return commands

# Função para encontrar os limites de coordenadas para centralização e escala
def find_bounding_box(commands):
    x_coords, y_coords = [], []
    for cmd, args in commands:
        for i in range(0, len(args), 2):
            x, y = args[i], args[i+1]
            x_coords.append(x)
            y_coords.append(y)
    if x_coords and y_coords:
        return min(x_coords), max(x_coords), min(y_coords), max(y_coords)
    else:
        return 0, 0, 0, 0  # Retorna valores padrão caso não haja coordenadas

# Função principal de conversão
def hpgl_to_png(plt_file, png_file, dpi_original=1016, dpi_target=300):
    with open(plt_file, 'r') as file:
        hpgl_data = file.read()

    commands = parse_hpgl(hpgl_data)

    # Verifique se algum comando foi lido
    if not commands:
        print("Nenhum comando válido encontrado no arquivo HPGL.")
        return

    # Encontrar limites de coordenadas para centralizar na imagem
    min_x, max_x, min_y, max_y = find_bounding_box(commands)

    if min_x == max_x and min_y == max_y:
        print("Erro: Não foram encontradas coordenadas válidas para calcular os limites.")
        return

    # Calcula o tamanho real da imagem, considerando o DPI original e o DPI do alvo
    scale_factor = dpi_target / dpi_original
    width = (max_x - min_x) * scale_factor
    height = (max_y - min_y) * scale_factor

    # Cria uma nova imagem em branco com fundo transparente (modo RGBA)
    img = Image.new('RGBA', (int(width), int(height)), color=(0, 0, 0, 0))  # Transparente
    draw = ImageDraw.Draw(img)

    pen_down = False
    last_position = (0, 0)

    # Ajuste de coordenadas para centralizar com escala
    for cmd, args in commands:
        if cmd == 'PU':  # Pen Up (mover sem desenhar)
            pen_down = False
            if args:
                x = (args[0] - min_x) * scale_factor
                y = (max_y - args[1]) * scale_factor
                last_position = (x, y)
        elif cmd == 'PD':  # Pen Down (mover desenhando)
            pen_down = True
            for i in range(0, len(args), 2):
                x = (args[i] - min_x) * scale_factor
                y = (max_y - args[i+1]) * scale_factor
                if pen_down:
                    # Desenhar uma linha preta e grossa
                    draw.line([last_position, (x, y)], fill=(0, 0, 0), width=3)  # Linha preta
                last_position = (x, y)

    # Salva a imagem PNG com fundo transparente
    img.save(png_file, "PNG")
    print(f"Arquivo PNG salvo como {png_file}")

# Programa principal
if __name__ == '__main__':
    # Verifica se o nome do arquivo foi passado como argumento
    if len(sys.argv) < 2:
        print("Uso: python convert_hpgl_to_png.py <arquivo_plt>")
        sys.exit(1)

    # Nome do arquivo .plt informado como argumento
    plt_file = sys.argv[1]

    # Define o nome do arquivo de saída PNG com o mesmo nome do .plt
    png_file = plt_file.rsplit('.', 1)[0] + '.png'

    # Converte o arquivo .plt para PNG com DPI de 300 e considerando o DPI original de 1016
    hpgl_to_png(plt_file, png_file, dpi_original=1016, dpi_target=300)  # Ajuste o DPI para 300
