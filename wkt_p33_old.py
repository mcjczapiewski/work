import os
import shutil
import regex
import datetime
import chardet
import io
from chardet.universaldetector import UniversalDetector
from natsort import natsorted, natsort_keygen

nkey = natsort_keygen()

count = 1

# # rozrzucenie wkt do folderow
# for subdir, _, files in os.walk(r"D:\_MACIEK_\python_proby\p33\do_operatow"):
#     for file in natsorted(files):
#         stad = os.path.join(subdir, file)
#         tutaj = os.path.join(
#             subdir,
#             file.split("__")[0],
#             (file.split("__")[1]).split(".wkt")[0],
#             file,
#         )
#         folder = os.path.join(
#             subdir, file.split("__")[0], (file.split("__")[1]).split(".wkt")[0]
#         )
#         if not os.path.exists(folder):
#             os.makedirs(folder)
#         try:
#             shutil.move(stad, tutaj)
#             print(count)
#             count += 1
#         except:
#             print(file)


# # dodanie nazwy obrebu do folderu
# for subdir, dirs, _ in os.walk(r"D:\_MACIEK_\python_proby\p33\do_operatow"):
#     dirs.sort(key=nkey)
#     if regex.match(r".*2\.00..$", subdir):
#         with open(
#             r"D:\_MACIEK_\python_proby\p33\slownik_obrebow.txt", "r"
#         ) as sl:
#             for line in sl:
#                 if (
#                     os.path.basename(subdir)
#                     == (line.split("\t")[1]).split("\n")[0]
#                 ):
#                     os.rename(subdir, subdir + "_" + line.split("\t")[0])


# # rozrzucenie wkt od plikow do folderow z wkt operatow
# for subdir, dirs, files in os.walk(
#     r"V:\P32_kopie_prac\Cyfryzacja_powiat inowroclawski\_MACIEK\oddanie_I-II\do_operatow"
# ):
#     dirs.sort(key=nkey)
#     for file in natsorted(files):
#         czesc = subdir
#         nazwa = file.split(".wkt")[0]
#         for subdir, _, files in os.walk(
#             r"V:\P32_kopie_prac\Cyfryzacja_powiat inowroclawski\_MACIEK\oddanie_I-II\do_plikow"
#         ):
#             for file in natsorted(files):
#                 nowa = regex.sub(r"^(.+)?(?=(_.-|_..-)|_...-).+", "\\1", file)
#                 if nowa.endswith(".wkt"):
#                     nowa = nowa.split(".wkt")[0]
#                 if nowa == nazwa:
#                     stad = os.path.join(subdir, file)
#                     tutaj = os.path.join(czesc, file)
#                     try:
#                         shutil.move(stad, tutaj)
#                         print(count)
#                         count += 1
#                     except:
#                         print(file)


# # usuniecie jednego nawiasu jak jest polygon a nie multi
for subdir, dirs, files in os.walk(
    r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III"
):
    for file in files:
        if file.endswith(".wkt"):
            temporary_lines = ""
            plik = os.path.join(subdir, file)
            with open(plik, "r", encoding='utf-8') as wkt:
                for line in wkt:
                    if regex.match(r"^POLYGON.+", line):
                        nowa = regex.sub(
                            r"(^.+)\((\(\(.+\)\))\)", "\\1\\2", line
                        )
                        temporary_lines += nowa
            if temporary_lines:
                print(plik)
                with open(plik, 'w', encoding='utf-8') as nowywkt:
                    nowywkt.write(temporary_lines)


# # dopasowanie folderow z wkt do folderow operatow
# with open(
#     r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\lista_wkt.txt",
#     "r",
#     encoding="utf-8",
# ) as stad:
#     for line in stad:
#         print(count)
#         count += 1
#         pelne = line.split("\n")[0]
#         nazwa = (
#             os.path.basename(os.path.dirname(os.path.dirname(pelne)))
#             + os.path.basename(os.path.dirname(pelne))
#             + os.path.basename(pelne)
#         )
#         with open(
#             r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\lista_pdf.txt",
#             "r",
#             encoding="utf-8",
#         ) as tutaj:
#             for line in tutaj:
#                 pelne1 = line.split("\n")[0]
#                 nazwa1 = (
#                     os.path.basename(os.path.dirname(os.path.dirname(pelne1)))
#                     + os.path.basename(os.path.dirname(pelne1))
#                     + os.path.basename(pelne1)
#                 )
#                 if nazwa1 == nazwa:
#                     print(nazwa)
#                     print("\t" + nazwa1)
#                     with open(
#                         r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",
#                        "a",
#                        encoding="utf-8",
#                     ) as cdc:
#                         cdc.write(pelne + "\t" + pelne1 + "\n")


# # dopasowanie po nazwie pliku a nie tylko folderu
# with open(
#     r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\wkt_bez_odpowiednika_pdf.txt", "r", encoding="utf-8"
# ) as stad:
#     for line in stad:
#         print(count)
#         count += 1
#         pelne = line.split("\n")[0]
#         nazwa = os.path.basename(pelne).split(".wkt")[0]
#         sciezka = os.path.basename(os.path.dirname(pelne))
#         with open(
#             r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\lista_plikow_p33.txt", "r", encoding="utf-8"
#         ) as tutaj:
#             for line in tutaj:
#                 pelne1 = line.split("\n")[0]
#                 nazwa1 = os.path.basename(pelne1).split(".PDF")[0]
#                 sciezka1 = os.path.basename(os.path.dirname(pelne1))
#                 if sciezka1 + nazwa1 == sciezka + nazwa:
#                     with open(
#                         r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt", "a"
#                     ) as cdc:
#                         cdc.write(pelne + "\t" + pelne1 + "\n")


# # czy wszystkie operaty z listy zostaly dopasowane
# dopasowane = set()
# with open(
#     r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",
#     "r",
#     encoding="utf-8",
# ) as cdc:
#     for line in cdc:
#         dopasowane.add(line.split("\t")[0])
# with open(
#     r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\lista_wkt.txt",
#     "r",
#     encoding="utf-8",
# ) as stad:
#     for line in stad:
#         if not line.split("\n")[0] in dopasowane:
#             with open(
#                 r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\niedopasowane_wkt.txt",
#                 "a",
#                 encoding="utf-8",
#             ) as niedopasowane:
#                 niedopasowane.write(line.split("\n")[0] + "\n")


# # z cdc wyodrebnij linijki powtarzajace sie
# poprzednia = pierwsza = ""
# with open(r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt", "r", encoding="utf-8") as cdc:
#     for line in cdc:
#         linia = line.split("\t")[0]
#         if poprzednia == "":
#             pierwsza = line
#             poprzednia = linia
#             czy1 = 1
#             continue
#         if linia != poprzednia:
#             pierwsza = line
#             czy1 = 1
#             poprzednia = linia
#             continue
#         elif poprzednia == linia:
#             if czy1 == 1:
#                 with open(
#                     r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt", "a"
#                 ) as kilka:
#                     kilka.write(pierwsza)
#                 czy1 = 0
#             with open(
#                 r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt", "a"
#             ) as kilka:
#                 kilka.write(line)


# # z cdc usun te co poszly do kilka dopasowan
# usunac = set()
# with open(r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt", "r", encoding="utf-8") as kilka:
#     for line in kilka:
#         usunac.add(line)
# with open(r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt", "r", encoding="utf-8") as cdc:
#     for line in cdc:
#         if line not in usunac:
#             with open(
#                 r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\n_co_do_czego.txt", "a"
#             ) as ncdc:
#                 ncdc.write(line)

# # kopiowanie wkt do odpowiadajacych folderow operatow
# with io.open(
#     r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\co_do_czego.txt",
#     "r",
#     encoding="utf-8",
# ) as cdc:
#     for line in cdc:
#         print(count)
#         count += 1
#         stad = line.split("\t")[0]
#         tutaj = (line.split("\t")[1]).split("\n")[0]
#         for _, _, files in os.walk(stad):
#             for file in natsorted(files):
#                 if file.upper().endswith(".WKT"):
#                     plik = os.path.join(stad, file)
#                     docelowe = os.path.join(tutaj, file)
#                     if not os.path.exists(docelowe):
#                         try:
#                             shutil.copy2(plik, docelowe)
#                             with io.open(
#                                 r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\mozna_usunac.txt",  # noqa
#                                 "a",
#                                 encoding="utf-8",
#                             ) as usun:
#                                 usun.write(plik + "\n")
#                         except:
#                             with io.open(
#                                 r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\bledy_kopiowania.txt",  # noqa
#                                 "a",
#                                 encoding="utf-8",
#                             ) as bledy:
#                                 bledy.write(plik + "\n")
#                     else:
#                         with io.open(
#                             r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\wkt_juz_istnieje.txt",  # noqa
#                             "a",
#                             encoding="utf-8",
#                         ) as istnieje:
#                             istnieje.write(plik + "\n")


# # usuwanie przerzuconych poprawnie
# with open(r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\mozna_usunac.txt", "r") as usun:
#     for line in usun:
#         print(count)
#         count += 1
#         try:
#             os.remove(line.split("\n")[0])
#         except:
#             with open(
#                 r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\nie_da_sie_usunac.txt", "a"
#             ) as nds:
#                 nds.write(line)


# # kilka dopasowan, przerzedzenie
# with open(r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\kilka_dopasowan.txt", "r") as kilka:
#     for line in kilka:
#         obreb = (
#             regex.sub(
#                 r"^.+do_operatow.+\.[0-9][0-9][0-9][0-9](.+?)\t.+", "\\1", line
#             )
#         ).split("\n")[0]
#         if obreb.upper() in (line.split("\t")[1]).upper():
#             with io.open(
#                 r"D:\_MACIEK_\python_proby\p33\wkt_rozrzucenie\wyczyszczone.txt",
#                 "a",
#                 encoding="utf-8",
#             ) as czyste:
#                 czyste.write(line)


# # przerzucanie ze struktura
# desti = r"D:\_MACIEK_\python_proby\p33\numer_p_do_xml\kopia"
# with open(
#     r"D:\_MACIEK_\python_proby\p33\numer_p_do_xml\lista.txt", "r"
# ) as pliki:
#     for line in pliki:
#         opis = line.split("\n")[0]
#         tutaj = os.path.join(desti, os.path.dirname(opis.split(":\\")[1]))
#         if not os.path.exists(tutaj):
#             os.makedirs(tutaj)
#         try:
#             shutil.copy2(opis, tutaj)
#         except:
#             print(opis)


# # czy do pliku wkt jest odpowiednik w pdf
# braki = 0
# sciezka = r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III"
# with open(
#     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt", "r", encoding="utf-8"
# ) as sciezki:
#     for line in sciezki:
#         sciezka = line.strip()
# for subdir, dirs, files in os.walk(sciezka):
#     dirs.sort(key=nkey)
#     for file in natsorted(files):
#         if file.endswith(".wkt"):
#             wkt = os.path.join(subdir, file)
#             print(str(count))
#             count += 1
#             if (
#                 not os.path.exists((wkt.split(".wkt")[0]) + ".PDF")
#                 and os.path.basename(subdir) != file.split(".wkt")[0]
#             ):
#                 # braki += 1
#                 # print("\t\t" + str(braki))
#                 with io.open(
#                     r"V:\P32_kopie_prac\Cyfryzacja_powiat inowroclawski\_MACIEK\oddanie_III\do_plikow\wkt_bez_odpowiednika_pdf.txt",  # noqa
#                     "a",
#                     encoding="utf-8",

#                 ) as brak:
#                     brak.write(wkt + "\n")


# # kiedy bledne wkt byly utworzone
# with open(
#     r"D:\_MACIEK_\python_proby\p33\wkt_bez_odpowiednika_pdf.txt", "r"
# ) as braki:
#     for line in braki:
#         sciezka = line.split("\n")[0]
#         data = (
#             str(datetime.datetime.fromtimestamp(os.path.getmtime(sciezka)))
#         ).split(" ")[0]
#         with open(r"D:\_MACIEK_\python_proby\p33\wkt_daty.txt", "a") as daty:
#             daty.write(sciezka + "\t" + data + "\n")


# # czy struktura wkt jest prawidlowa
# braki = 0
# for subdir, dirs, files in os.walk(
#     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\Zmiana_kodowania_test"
# ):
#     dirs.sort(key=nkey)
#     for file in natsorted(files):
#         if file.endswith(".wkt"):
#             zeruj = 0
#             print(count)
#             count += 1
#             wkt = os.path.join(subdir, file)
#             with open(wkt, "r") as sprawdz:
#                 for line in sprawdz:
#                     if zeruj == 0:
#                         zeruj = 1
#                         if not regex.match(r"^POLYGON|MULTI.*", line.upper()):
#                             braki += 1
#                             print("\t\t" + str(braki))
#                             with open(
#                                 r"D:\_MACIEK_\python_proby\p33\wkt_bledne_struktuaaary.txt",  # noqa
#                                 "a",
#                             ) as brak:
#                                 brak.write(wkt + "\n")
#                     else:
#                         continue


# # laczenie wkt ze zla struktura - przeglad
# with open(
#     r"D:\_MACIEK_\python_proby\p33\wkt_bledne_struktury.txt", "r"
# ) as braki:
#     for line in braki:
#         bb = 0
#         sciezka = line.split("\n")[0]
#         with open(sciezka, "r") as wkt:
#             for line in wkt:
#                 with open(
#                     r"D:\_MACIEK_\python_proby\p33\wkt_bledne_zlaczone.txt",
#                     "a",
#                 ) as bledne:
#                     if bb == 0:
#                         bledne.write(
#                             "\n~~~~~~~~~~~~~~~~~~~~~~~~~\n" + sciezka + "\n\n"
#                         )
#                         bb = 1
#                     bledne.write(line)


# # sprawdzanie kodowania plikow - 1 metoda
# for subdir, dirs, files in os.walk(r"W:\dla Maćka\przykłady wkt"):
#     dirs.sort(key=nkey)
#     for file in natsorted(files):
#         if file.endswith(".wkt"):
#             print(count)
#             count += 1
#             wkt = os.path.join(subdir, file)
#             rawdata = open(wkt, "rb").read()
#             result = chardet.detect(rawdata)
#             print(result)
#             charenc = result["encoding"]
#             with open(
#                 r"D:\_MACIEK_\python_proby\p33\kodowania_plikow.txt", "a"
#             ) as kodowanie:
#                 kodowanie.write(wkt + "\t" + charenc + "\n")


# # sprawdzanie kodowania plikow - 2 metoda
# detector = UniversalDetector()
# for subdir, dirs, files in os.walk(
#     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA\RADOJEWICE"
# ):
#     dirs.sort(key=nkey)
#     for file in natsorted(files):
#         if file.endswith(".xml"):
#             print(count)
#             count += 1
#             wkt = os.path.join(subdir, file)
#             detector.reset()
#             with open(wkt, "rb") as sprawdz:
#                 for line in sprawdz:
#                     detector.feed(line)
#                     if detector.done:
#                         break
#             detector.close()
#             if "utf-8" not in str(detector.result):
#                 with open(
#                     r"D:\_MACIEK_\python_proby\p33\numer_p_do_xml\kodowania_plikow.txt",  # noqa
#                     "a",
#                 ) as kodowanie:
#                     kodowanie.write(wkt + "\t" + str(detector.result) + "\n")


# # zapis plikow z nowym kodowaniem
# for subdir, dirs, files in os.walk(
#     r"W:\dla Maćka\przykłady wkt\P.0410.1999.241"
# ):
#     dirs.sort(key=nkey)
#     for file in natsorted(files):
#         stad = os.path.join(subdir, file)
#         with io.open(stad, "r", encoding="utf-16") as pobierz:
#             tresc = pobierz.read()
#         with io.open(
#             stad + ".new", "w", encoding="utf-8", errors="ignore"
#         ) as zapisz:
#             zapisz.write(tresc)

# # rozkopiowanie zakresow do szkiców polowych
# for subdir, dirs, files in os.walk(
#     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\INOWROCŁAW"
# ):
#     for file in files:
#         if file.endswith(".PDF") and "SZK-POL" in file:
#             if not os.path.exists(
#                 os.path.join(subdir, os.path.splitext(file)[0] + ".wkt")
#             ):
#                 plik = file
#                 if any(
#                     fname.endswith(".wkt") and "SZK-POL" in fname
#                     for fname in os.listdir(subdir)
#                 ):
#                     for file in files:
#                         if file.endswith(".wkt") and "SZK-POL" in file:
#                             wkt = os.path.join(subdir, file)
#                             new = os.path.join(
#                                 subdir, os.path.splitext(plik)[0] + ".wkt"
#                             )
#                             print(count)
#                             count += 1
#                             shutil.copy(wkt, new)

# rozkopiowanie wkt operatow na poszczegolne dokumenty
# sciezka = r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III"
# with open(
#     r"P:\cyfryzacja_powiat_inowroclawski\kontrole_2020-07-06\sciezki.txt", "r", encoding="utf-8"
# ) as sciezki:
#     for line in sciezki:
#         sciezka = line.strip()
# for subdir, dirs, files in os.walk(sciezka):
#     dirs.sort(key=nkey)
#     wkt_operatu = os.path.join(
#         subdir, os.path.basename(subdir) + ".wkt"
#     )
#     if os.path.exists(wkt_operatu):
#         for file in natsorted(files):
#             if regex.match(r".+((-M-)|(-SZK-)|(-Z-KAT-)|(-Z-POM-)|(-MPZP-)).+\.PDF", file.upper()):
#                 new_wkt = os.path.join(
#                     subdir, os.path.splitext(file)[0] + ".wkt"
#                 )
#                 if os.path.exists(new_wkt):
#                     continue
#                 else:
#                     try:
#                         shutil.copy(wkt_operatu, new_wkt)
#                         print(str(count) + "\t" + new_wkt)
#                         count += 1
#                     except:
#                         with open(
#                             r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\nie_udalo_sie_utworzyc_wkt.txt",  # noqa
#                             "a",
#                             encoding="utf-8",
#                         ) as bledy:
#                             bledy.write(new_wkt + "\n")
#     else:
#         if any(
#             fname.upper().endswith(".PDF")
#             for fname in os.listdir(subdir)
#         ):
#             with open(
#                 r"P:\cyfryzacja_powiat_inowroclawski\SKANY_III\brak_wkt_operatu.txt",
#                 "a",
#                 encoding="utf-8",
#             ) as bledy:
#                 bledy.write(subdir + "\n")

# czy wkt są tylko dla szkiców i map
# with open(
#     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",
#     "r",
#     encoding="utf-8",
# ) as sciezki:
#     for line in sciezki:
#         sciezka = line.strip()
# sciezka = r'P:\cyfryzacja_powiat_inowroclawski\SKANY_III'
# for subdir, dirs, files in os.walk(sciezka):
#     dirs.sort(key=nkey)
#     if not any(
#         fname.upper().endswith(".WKT") for fname in os.listdir(subdir)
#     ):
#         continue
#     wkt_operatu = os.path.join(
#         subdir, os.path.basename(subdir) + ".wkt"
#     )
#     print(count)
#     count += 1
#     for file in files:
#         if file.endswith(".wkt") and (
#             file != (os.path.basename(subdir) + ".wkt")
#             and "-M-" not in file
#             and "-SZK-" not in file
#             and "-Z-KAT-" not in file
#             and "-Z-POM-" not in file
#             and "-MPZP-" not in file
#         ):
#             with open(
#                 r"V:\P32_kopie_prac\Cyfryzacja_powiat inowroclawski\_MACIEK\oddanie_III\do_plikow\wkt_do_niewlasciwych_plikow.txt",
#                 "a",
#                 encoding="utf-8",
#             ) as bledy:
#                 bledy.write(os.path.join(subdir, file) + "\n")

# czy sa wkt dla plikow i operatow
# with open(
#     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt", "r", encoding="utf-8"
# ) as sciezki:
#     for line in sciezki:
#         sciezka = line.split("\n")[0]
#         for subdir, dirs, files in os.walk(sciezka):
#             dirs.sort(key=nkey)
#             if not any(
#                 fname.upper().endswith(".PDF") for fname in os.listdir(subdir)
#             ):
#                 continue
#             print(count)
#             count += 1
#             wkt_operatu = os.path.join(
#                 subdir, os.path.basename(subdir) + ".wkt"
#             )
#             for file in natsorted(files):
#                 if regex.match(
#                     r".+((-M-)|(-SZK-)|(-Z-KAT-)).+\.PDF", file.upper()
#                 ):
#                     new_wkt = os.path.join(
#                         subdir, os.path.splitext(file)[0] + ".wkt"
#                     )
#                     if not os.path.exists(new_wkt):
#                         with open(
#                             r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\brak_wkt_dla_plikow.txt",  # noqa
#                             "a",
#                             encoding="utf-8",
#                         ) as bledy:
#                             bledy.write(new_wkt + "\n")
#             if not os.path.exists(wkt_operatu):
#                 with open(
#                     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\brak_wkt_dla_operatu.txt",
#                     "a",
#                     encoding="utf-8",
#                 ) as bledy:
#                     bledy.write(subdir + "\n")

# czy jak nie ma wkt głównej to czy jest jakaś do pliku
# with open(
#     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\sciezki.txt",
#     "r",
#     encoding="utf-8",
# ) as sciezki:
#     for line in sciezki:
#         sciezka = line.strip()
#         for subdir, dirs, _ in os.walk(sciezka):
#             if any(
#                 fname.upper().endswith(".WKT") for fname in os.listdir(subdir)
#             ) and not os.path.exists(
#                 os.path.join(subdir, os.path.basename(subdir) + ".wkt")
#             ):
#                 with open(
#                     r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 4\kontrole_2020-07-06\brak_glownej_jest_do_pliku.txt",
#                     "a",
#                     encoding="utf-8",
#                 ) as bledy:
#                     bledy.write(subdir + "\n")
#                 print(count)
#                 count += 1

# # czy folder zawiera plik
# with open(
#     r"D:\_MACIEK_\python_proby\p33\brak_wkt_operatu_20190807.txt", "r"
# ) as braki:
#     for line in braki:
#         print(count)
#         count += 1
#         hamuj = 0
#         sciezka = line.split("\n")[0]
#         for _, _, files in os.walk(sciezka):
#             for file in natsorted(files):
#                 if file.endswith(".wkt"):
#                     with open(
#                         r"D:\_MACIEK_\python_proby\p33\ale_sa_dla_plikow.txt",
#                         "a",
#                     ) as asdp:
#                         asdp.write(line)
#                     hamuj = 1
#                     break
#             if hamuj == 1:
#                 break


# # spis plikow w lokalizacji
# with open(r"D:\_MACIEK_\python_proby\p33\spis.txt", "a") as spis:
#     for subdir, dirs, files in os.walk(
#         r"I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\DĄBROWA BISKUPIA"
#     ):
#         dirs.sort(key=nkey)
#         for file in natsorted(files):
#             if (file.upper()).endswith(".PDF"):
#                 print(count)
#                 count += 1
#                 spis.write(subdir + "\n")
#                 break


# # czy w folderze jest wkt glowna
# with open(r"D:\_MACIEK_\python_proby\p33\spis.txt", "r") as spis:
#     for line in spis:
#         sciezka = line.split("\n")[0]
# for subdir, dirs, _ in os.walk(r'I:\INOWROCŁAW\DANE_IRON_MOUNTAIN\20190614\ZADANIE 2\10.06.2020\INOWROCŁAW'):
#     if not os.path.exists(
#         os.path.join(subdir, os.path.basename(subdir) + ".wkt")
#     ):
#         print(subdir)


# # rozrzucanie wkt modernizacji
# for subdir, dirs, files in os.walk(
#     r"I:\INOWROCŁAW\DANE PODGiK\SKANY OPERATÓW\!modernizacja inowrocław"
# ):
#     dirs.sort(key=nkey)
#     if "-00" in subdir:
#         glowny = subdir
#         nrobr = subdir.split("\\")[5].split("-")[1]
#         for file in natsorted(files):
#             if file.upper().endswith(".PDF"):
#                 pdf = os.path.splitext(file)[0]
#                 for subdir, dirs, files in os.walk(
#                     r"D:\_MACIEK_\python_proby\p33\do_operatow"
#                 ):
#                     dirs.sort(key=nkey)
#                     if ".00" in subdir:
#                         obreb = subdir.split("\\")[5].split(".")[1]
#                         if nrobr == obreb:
#                             for file in natsorted(files):
#                                 if file.upper().endswith(".WKT"):
#                                     wkt = os.path.splitext(file)[0]
#                                     if wkt == pdf:
#                                         stad = os.path.join(subdir, file)
#                                         nowy = os.path.join(glowny, file)
#                                         try:
#                                             shutil.copy(stad, nowy)
#                                             print(
#                                                 str(count)
#                                                 + "\t"
#                                                 + obreb
#                                                 + "_"
#                                                 + file
#                                             )
#                                             count += 1
#                                         except:
#                                             raise
