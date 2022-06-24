# Makefile for invoking KiBot documentation and fabrication generation.
# KiBot scripts go in the .kibot directory.

docs:
	kibot -b ./kicad_6/*.kicad_pcb -c ./.kibot/doc_gen.kibot.yaml
	mkdir ./docs/reports
	mv *-erc.txt ./docs/reports/
	mv *-drc.txt ./docs/reports/

clean:
	rm -r ./docs
	rm -f index.html