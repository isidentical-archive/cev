.PHONY: clean

hookify.so: hookify.c lpyhook.c
	gcc `python-config --cflags` `python-config --includes` -Wl,--export-dynamic -fPIC -shared -o $@ $^ -ldl `python-config --libs`

lpyhook.c:
	python lpyhook.py
	
clean:
	rm hookify.so lpyhook.c lpyhook.h
