O methodology_script.sh gera um arquivo fastq para um modelo e tem como argumentos, primeiro o arquivo do modelo.csv e segundo o tamanho do arquivo fastq que deseja gerar
O get_all_fastq.py gera os arquivos fastq para todos os modelos de todas as plataformas, tem como argumentos primeiro o diretorio onde esses arquivos estao e em segundo o tamanho do arquivo que deseja gerar para cada modelo
EX:
./methodology_script.sh [file].csv [tamanho em MB]
python3 get_all_fastq.py [diretorio] [tamanho em MB]

Para rodar o methodology sozinho tenha na mesma pasta que ele o modelo que deseja gerar o aquivo fastq
Para rodar o get_all_fastq tenha o methodology e o diretorio na mesma pasta que o script
