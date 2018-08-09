import os
import sys
import re



def writeSpaces(fichier, n) :
    for i in range(0, n) :
        fichier.write(" ")
    #}
#}



class Makefile :

    # =======================================================================================================
    # Constructeur.
    # =======================================================================================================
    def __init__(self) :
        """Constructeur."""

        # ---------------------------------------------------------------------------------------------------
        # attributs
        # ---------------------------------------------------------------------------------------------------
        # location de ce programme
        self.location = '/home/vmagda/.bin/make'

        # balises commentées pour structurer le code
        self.delim1 = ''
        self.delim2 = ''

        # type des sources (extension)
        self.filetype = sys.argv[1].split('.')[1]

        # nom des fichier sources, modules et objets
        self.sources = list(sys.argv[1:])
        self.modules = list(' ')
        self.objects = list()

        # nombre de fichiers et contenu
        self.nbfiles = len(self.sources)
        self.filestxt = list()
        self.use = list()

        # ---------------------------------------------------------------------------------------------------
        # affectations
        # ---------------------------------------------------------------------------------------------------
        self.delim1 = '# '
        for i in range(1, 108) :
            self.delim1 += '='
        #}
        self.delim1 += '\n'

        self.delim2 = '# '
        for i in range(1, 108) :
            self.delim2 += '-'
        #}
        self.delim2 += '\n'

        for i in range(0, len(self.sources)) :
            # self.modules.append(self.sources[i].split('.')[0] + '.mod')
            self.objects.append(self.sources[i].split('.')[0] + '.o')
        #}

        for file_name in self.sources :
            with open(file_name, 'r') as temp_sources :
                self.filestxt.append(temp_sources.read())
            #}
        #}

        for i in range(1, self.nbfiles) :
            modules = re.search('(\\n\s*MODULE) (\w*)', self.filestxt[i]).group(2)
            self.modules.append(modules + '.mod')
        #}

        for i in range(0, self.nbfiles) :
            use = re.findall('\\n\s*use (\w*)', self.filestxt[i])
            # supprime les doublons
            use = list(set(use))
            self.use.append(use)
        #}
    #}



    # =======================================================================================================
    # Tronc commun, début du makefile
    # =======================================================================================================
    def head(self) :
        """En tête du Makefile, ce qui ne dépend pas du langage."""

        with open('Makefile', 'a') as makefile :
            makefile.write(self.delim1)
            makefile.write('# Variables.\n')
            makefile.write(self.delim1)

            makefile.write('# Project name.\n')
            makefile.write('PROJECT = ' + os.getcwd().split('/')[-1] + '\n')

            makefile.write('\n')
            makefile.write('# Structure.\n')
            makefile.write('OBJ_DIR = objects\n')
            makefile.write('RUN_DIR = run\n')
            makefile.write('EXEC    = truc\n')

            makefile.write('\n')
            makefile.write('# Files to edit.\n')
            makefile.write('SOURCES = ' + ' '.join(self.sources) + '\n')
            makefile.write('MODULES = ' + ' '.join(self.modules[1:]) + '\n')
            makefile.write('OBJECTS = ' + ' '.join(self.objects) + '\n')
            makefile.write('OTHER   = Makefile\n')
            makefile.write('PDF     =\n')
        #}
    #}



    # =======================================================================================================
    # partie spécifique au fortran
    # =======================================================================================================
    def fortran(self) :
        """Si sources fortran."""

        with open('Makefile', 'a') as makefile :
            makefile.write('\n')
            makefile.write('# Compilator informations.\n')
            makefile.write('FC      = gfortran\n')
            makefile.write('FLAGS   = -fbounds-check -J $(OBJ_DIR)\n')

            makefile.write('\n\n\n')
            makefile.write(self.delim1)
            makefile.write('# Compilationrules.\n')
            makefile.write(self.delim1)

            # -----------------------------------------------------------------------------------------------
            # Exécutable
            # -----------------------------------------------------------------------------------------------
            makefile.write('# Exécutable\n')
            makefile.write('$(RUN_DIR)/$(EXEC) : ')
            makefile.write('$(OBJ_DIR)/' + self.objects[0] + ' \\\n')
            for i in range(1, self.nbfiles) :
                writeSpaces(makefile, 21)
                makefile.write('$(OBJ_DIR)/' + self.objects[i])
                if i < self.nbfiles - 1 :
                    makefile.write(' \\')
                #}
                makefile.write('\n')
            #}
            makefile.write('\t$(FC) $(FLAGS) $(OBJ_DIR)/*.o -o $(RUN_DIR)/$(EXEC)\n')

            # -----------------------------------------------------------------------------------------------
            # Programme principal
            # -----------------------------------------------------------------------------------------------
            makefile.write('\n\n')
            makefile.write('# Programme principal\n')
            makefile.write('$(OBJ_DIR)/' + self.objects[0] + ' : ' + self.sources[0])
            if len(self.use[0]) > 0 :
                makefile.write(' \\')
            #}
            makefile.write('\n')
            for j, depend in enumerate(self.use[0]) :
                writeSpaces(makefile, 14 + len(self.objects[0]))
                makefile.write('$(OBJ_DIR)/' + depend + '.mod')
                if j < len(self.use[0]) - 1 :
                    makefile.write(' \\')
                #}
                makefile.write('\n')
            #}
            makefile.write('\t$(FC) $(FLAGS) -c ' + self.sources[0] +
                ' -o $(OBJ_DIR)/' + self.objects[0] + '\n')

            # -----------------------------------------------------------------------------------------------
            # Modules
            # -----------------------------------------------------------------------------------------------
            makefile.write('\n\n')
            makefile.write('# Modules\n')
            for i in range(1, self.nbfiles) :
                makefile.write('$(OBJ_DIR)/' + self.objects[i] + ' ')
                makefile.write('$(OBJ_DIR)/' + self.modules[i] + ' : ' + self.sources[i])
                if len(self.use[i]) > 0 :
                    makefile.write(' \\')
                #}
                makefile.write('\n')
                for j, depend in enumerate(self.use[i]) :
                    writeSpaces(makefile, 26 + len(self.objects[i]) + len(self.modules[i]))
                    makefile.write('$(OBJ_DIR)/' + depend + '.mod')
                    if j < len(self.use[i]) - 1 :
                        makefile.write(' \\')
                    #}
                    makefile.write('\n')
                #}
                makefile.write('\t$(FC) $(FLAGS) -c ' + self.sources[i] +
                    ' -o $(OBJ_DIR)/' + self.objects[i] + '\n\n')
            #}
        #}
    #}



    # =======================================================================================================
    # tronc commun, fin du makefile
    # =======================================================================================================
    def tail(self) :
        with open(self.location + '/Makefile', 'r') as fichier :
            temp = fichier.read()
        #}

        with open('Makefile', 'a') as makefile :
            makefile.write(temp)
        #}
    #}
#}
