#encoding: utf-8
import os
import re
import subprocess
import configparser
import unicodedata
import csv
from collections import namedtuple

def lista_ssids_no_windows():
    #  pega os SSIDS salvos no windows:
    saida_crua = subprocess.check_output("netsh wlan show profiles").decode("utf-8", "ignore")
    lista_ssids = []
    redes = re.findall(r":(.*)", saida_crua)
    for rede in redes:
        ssid = rede.strip().encode('utf-8').decode('unicode_escape') # remove espaços e escapa caracteres especiais
        if ssid:            
            lista_ssids.append(ssid) # Se existir, adiciona à lista
    return lista_ssids

def collect_saved_passwords_windows():
    ssids = lista_ssids_no_windows()
    Rede = namedtuple("Rede", ["ssid", "ciphers", "key"])
    redes = []
    # print(ssids)
    for ssid in ssids:
        ssid_details = subprocess.check_output(f"""netsh wlan show profile "{ssid}" key=clear""").decode('unicode_escape')                
        modos_criptografia = re.findall(r"Cipher\s(.*)|Codifica\x87Æo\s(.*)", ssid_details) # achar os protocolos de criptografia  da rede        
        criptografia = "/".join([c[1].strip().strip(":").strip() for c in modos_criptografia]) # limpar o output        
        senha = re.findall(r"Key Content\s(.*)|da Chave\s(.*)", ssid_details) # achar a senha do Wi-Fi        
        try:
            senha = senha[0][1].strip().strip(":").strip() # limpando a senha   
        except IndexError:
            senha = "None"            
        rede = Rede(ssid=ssid, ciphers=criptografia, key=senha)
        print(f"{rede.ssid:25}{rede.ciphers:15}{rede.key:50}") # Imprime as informacoes da rede
        redes.append(rede)

    export = input('\n >> Would you like to save the results(Y/N)?')
    if export == 'Y' or export == 'y':                
        f = open('./wifi_passwords.csv', 'w')
        writer = csv.writer(f)
        writer.writerow(["SSID","Cipher(s)","Key"])
        for r in redes:
            writer.writerow(r)
        f.close()

    return redes

def mostrar_redes_windows():
    print("SSID"+(' '*21)+"CIPHER(S)"+(' '*7)+"KEY")
    print("="*75)
    collect_saved_passwords_windows()    

mostrar_redes_windows()    