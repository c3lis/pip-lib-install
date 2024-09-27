#!/usr/bin/python
import subprocess
import argparse
import os
import site

if os.geteuid() != 0:
    print("[!] Este script debe ser ejecutado como root.")
    exit(1) 


log = """
       _       _ _ _     
 _ __ (_)_ __ | (_) |__  
| '_ \| | '_ \| | | '_ \ 
| |_) | | |_) | | | |_) |
| .__/|_| .__/|_|_|_.__/ 
|_|     |_|              
"""

def venv(libraries):
    print("\n[+] Creando entorno virtual.")
    
    # Crear el entorno virtual
    virtual = subprocess.run(["python3", "-m", "venv", "piplib"], capture_output=True, text=True)
    if virtual.stderr:
        print("[!] Error al crear el entorno virtual:", virtual.stderr)
        quit()

    print("     * Entorno virtual creado.")
    
    # Activar el entorno virtual e instalar librerías
    print("\n[+] Instalando las dependencias.")
    for install in libraries:
        install_cmd = subprocess.run([f"./piplib/bin/pip", "install", install], capture_output=True, text=True)
        if install_cmd.stderr:
            print(f"[!] Error al instalar {install}:", install_cmd.stderr)
            quit()
        print(f"     * Dependencia {install} instalada.")
    
   

    # Extraer rutas de las librerías instaladas
    print("\n[+] Extrayendo rutas.")
    for install in libraries:
        os.system(f'find . | grep -i "{install}" >> rutas.tmp' )
        print(f"    * ruta : {install} extraida.")
    
    print("\n[+] Moviendo archivos al sistema base.") 
    sited = site.getsitepackages()[1]
    os.system(f'for x in $(seq 1 $(cat rutas.tmp | wc -l)); do cp -r $(cat rutas.tmp | awk "NR==$x") {sited}/; done')
    
    print("     * Elementos movidos.")
      
    print("     * Limpiando instalación.")
    os.system('deactivate 2>/dev/null; rm -rf piplib rutas.tmp')
    print("\n[+] Limpieza terminada.")
    print("\n\n     * OK.")

def main():
    parser = argparse.ArgumentParser(description="Instalación de librerías Python.")
    parser.add_argument('-m', '--library', nargs='+', help="Librerías que desea instalar")  # Corrección aquí
    args = parser.parse_args()

    if args.library:
        for install in args.library:
            print(f"Instalando: {install}")
        venv(args.library)
    else:
        print("[!] No se proporcionaron librerías.\nuse = sudo python ./piplibinstall.py -m {libreria}\n")
        
if __name__ == "__main__":
    print(log)
    main()
