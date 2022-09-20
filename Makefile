test:
	python manage.py test

test-cover:
	coverage run --omit="**/tests.py,monapi/settings.py,manage.py" manage.py test
	coverage report -m
