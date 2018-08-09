

# ===========================================================================================================
# phony targets
# ===========================================================================================================
# exécuter l'exécutable (utile pour utiliser F5 dans vim)
.PHONY : make
make :
	@ cd $(RUN_DIR); ./$(EXEC)

# supprimer les fichiers objet et l'exécutable s'ils existent
.PHONY : clean
clean :
	rm -f $(OBJ_DIR)/*.mod $(OBJ_DIR)/*.o $(RUN_DIR)/$(EXEC)

# effacer le contenu des dossiers d'entrees et de sorties
.PHONY : del
del :
	rm -f sorties/*.dat graphes/*.eps graphes/*.ps graphes/*.png

# ouvrir les fichiers du projet dans des onglets de vim
.PHONY : open
open :
	@ vim $(SOURCES) $(OTHER)

# tout compiler et lancer gdb (segmentation fault)
.PHONY : gdb
gdb :
	$(FC) -g $(SOURCES) -o $(EXEC) && (cd $(RUN_DIR); gdb ./$(EXEC))

# clean et tarer le dossier
.PHONY : tar
tar :
	make clean
	cd ..; tar -zcvf $(PROJECT).tar.gz $(PROJECT)

# sauvegarder ancienne version
.PHONY : save
save :
	make clean
	cd ..; cp -r $(PROJECT) old_$(PROJECT)

.PHONY : pdf
pdf :
	@ xdg-open $(PDF)

#
.PHONY : clean
coffe :
	@ echo "  (\n   )\n c[]"
