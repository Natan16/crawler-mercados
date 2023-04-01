# qualidade de código
format: 
	isort --old-finders --profile black --line-length 120 .
	black --line-length 120 .

mypy: 
	mypy --ignore-missing-imports --follow-imports=skip --strict-optional optools/remanejamento.py
	mypy --ignore-missing-imports --follow-imports=skip --strict-optional optools/models.py
	mypy --ignore-missing-imports --follow-imports=skip --strict-optional optools/forms.py
	mypy --ignore-missing-imports --follow-imports=skip --strict-optional optools/errors.py

ruff: 
	ruff --line-length 120 .

# deploy
all: build get-login retag push

build:
	@echo building image...
	docker build -t crawlers .
	@echo

get-login:
	@echo aws login...
	aws ecr get-login-password --region sa-east-1 | docker login --username AWS --password-stdin 415395292850.dkr.ecr.sa-east-1.amazonaws.com
	@echo

retag: build
	@echo retag docker image...
	docker tag crawlers:latest 415395292850.dkr.ecr.sa-east-1.amazonaws.com/crawlers:latest
	@echo

push: retag get-login
	@echo push new image...
	docker push 415395292850.dkr.ecr.sa-east-1.amazonaws.com/crawlers:latest
	@echo

# crawlear
crawl:
	scrapy crawl spani
	scrapy crawl shibata
	scrapy crawl carrefour
	scrapy crawl pao_de_acucar