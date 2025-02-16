# depuradordecamaratrampa

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Programa para filtrar imagenes de camaras trampa en donde se haya detectado un objeto usando [Ultralytics YOLO AI](https://github.com/ultralytics/ultralytics) y [ONNX Runtime](https://github.com/microsoft/onnxruntime)

Construido con [Toga](https://github.com/beeware/toga) y [Briefcase](https://github.com/beeware/briefcase)

# Build on Linux

1. Crea un entorno virtual:
```
mkdir dct
cd dct
python3 -m venv dct-venv
source dct-venv/bin/activate
```
2. Clona este repositorio:
```
git clone https://github.com/antruc/depuradordecamaratrampa.git
cd depuradordecamaratrampa
```
3. Instala las dependencias:
```
pip install briefcase ultralytics onnx onnxruntime
```
4. Construye la aplicación:
```
briefcase create
briefcase build
briefcase package
```
Y por ultimo instala el programa

Para crear un instalador para otros sistemas operativos se puede seguir el tutorial en la pagina de [BeeWare](https://docs.beeware.org/es/latest/tutorial/tutorial-0.html)
