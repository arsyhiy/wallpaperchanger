.PHONY: run service test format lint clean

run:
	python -m wallpaperchanger.Gui.main

service:
	python -m wallpaperchanger.Service.main

test:
	pytest

format:
	ruff format .

lint:
	ruff check .

clean:
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf *.egg-info

# TODO: переписать этот вариант неочень 
