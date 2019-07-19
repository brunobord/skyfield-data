download:
	python3 download.py

clean:
	rm -f skyfield_data/data/*

package:
	python3 setup.py sdist
