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
