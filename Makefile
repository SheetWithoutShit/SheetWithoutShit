lint:
	pylint --rcfile=.pylintrc ./collector/app/;\
    pylint --rcfile=.pylintrc ./telegram/app/;\
    pylint --rcfile=.pylintrc ./server/app/
