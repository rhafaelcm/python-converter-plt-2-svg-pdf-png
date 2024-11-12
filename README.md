# Conversor de arquivos .plt (HPGL) em Python
Criei esses conversores pois precisava abrir arquivos em plt gerado para impressão em plotter de corte e não conseguia abrir em nenhum programa de edição com o Inkscape ou outro CAD gratuíto disponível para linux.

### Como utilizar:
Para utilizar basta apenas executar o seguinte comando:

```bash
python seu_conversor.py seu_arquivo_para_converter.plt
```
* onde seu_conversor.py pode ser
    * convert_hpgl_to_svg.py
    * convert_hpgl_to_pdf.py
    * convert_hpgl_to_png.py
* onde seu_arquivo_para_converter.plt é o nome do seu arquivo