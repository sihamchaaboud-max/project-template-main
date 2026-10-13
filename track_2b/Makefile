.PHONY: run ingest eval down

# Lance Jisr dans Docker : http://localhost:7860
run:
	@test -f .env || (cp .env.example .env && echo "Fichier .env cree. Remplis les valeurs (voir README), puis relance make run." && exit 1)
	docker compose up --build

# Indexer les documents sources
ingest:
	docker compose run --rm jisr python -m src.ingest

# Lancer le benchmark
eval:
	docker compose run --rm jisr python eval/run_eval.py

down:
	docker compose down