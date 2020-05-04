lint:
	pylint --rcfile=.pylintrc ./collector/app/ --init-hook='sys.path.extend(["./collector/app/"])';\
    pylint --rcfile=.pylintrc ./telegram/app/ --init-hook='sys.path.extend(["./telegram/app/"])';\
    pylint --rcfile=.pylintrc ./server/app/ --init-hook='sys.path.extend(["./server/app/"])';\
    pylint --rcfile=.pylintrc ./tasker/app/ --init-hook='sys.path.extend(["./tasker/app/"])'
