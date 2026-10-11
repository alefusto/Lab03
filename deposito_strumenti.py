from strumento import Strumento
from prestito import Prestito

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""

        self.nome = nome
        self.__responsabile = responsabile

        self.lista_strumenti = [] # E' attributo del deposito, va definita qui, altrimenti si cancella ogni volta
        self.lista_prestiti = [] # Idem per questa

    @property # Metodi per modificare il responsabile
    def responsabile(self):
        return self.__responsabile  # Qui per riferirsi all'attributo responsabile ci va il dunder

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        if nuovo_responsabile == self.__responsabile: # Aggiungo controllo sull'esistenza del responsabile
            print("E' già responsabile")
        else:
            self.__responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""

        from csv import reader
        with open(file_path, "r") as infile:
            csvReader = reader(infile, delimiter=',')

        for riga in csvReader:
            codice = riga[0]
            tipo = riga[1]
            marca = riga[2]
            anno_acquisto = riga[3]
            valore = riga[4]
            s = Strumento(codice, tipo, marca, anno_acquisto, valore)
            self.lista_strumenti.append(s)


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""

        if len(self.lista_strumenti) == 0: # Algoritmo per creazione codice
            codice_aggiornato = "S1"
        else:
            ultimo_codice = self.lista_strumenti[-1].codice
            parte_numerica = int(ultimo_codice[1:])
            nuova_parte_numerica = str(parte_numerica + 1)
            codice_aggiornato = "S" + nuova_parte_numerica

        s = Strumento(codice_aggiornato,tipo, marca, anno_acquisto, valore)
        self.lista_strumenti.append(s)

        return s


    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""

        from operator import attrgetter
        attributo_chiave = attrgetter('marca')

        return sorted(self.lista_strumenti, key = attributo_chiave)

    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""

        # Controllo se lo strumento è presente nel database
        codici_esistenti = [s.codice for s in self.lista_strumenti] # Estrae tutti i codici degli strumenti presenti nel database
        if id_strumento not in codici_esistenti:
            raise Exception("Lo strumento non è presente nel sistema")

        # Controllo se lo strumento è già stato prestato
        strumenti_in_prestito = [p.id_strumento for p in self.lista_prestiti] # Estrae tutti i codici degli strumenti in prestito
        if id_strumento in strumenti_in_prestito:
            raise Exception("Lo strumento è già in prestito")

        if len(self.lista_prestiti) == 0: # Algoritmo per creazione codice
            codice_prestito = "P1"

        else:
            ultimo_codice = self.lista_prestiti[-1].codice_prestito
            parte_numerica = int(ultimo_codice[1:])
            nuova_parte_numerica = str(parte_numerica + 1)
            codice_prestito = "P" + nuova_parte_numerica

        p = Prestito(codice_prestito, data, id_strumento, cognome_allievo)
        self.lista_prestiti.append(p)

        return p

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""

        # Controllo se il prestito è presente nel database
        codici_esistenti = [s.codice_prestito for s in self.lista_prestiti]  # Estrae tutti i codici dei prestiti presenti nel database
        if id_prestito not in codici_esistenti:
            raise Exception("Il prestito non è presente nel sistema")

        self.lista_prestiti = [p for p in self.lista_prestiti if p.codice_prestito != id_prestito]
