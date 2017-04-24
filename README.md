# ptc



#base on django1.10.3,  simplejson, jpush, django-celery
django:pip install django==1.10.3
simplejson: pip install simplejson
pip install jpush
pip install django-celery




#run server
python manage.py runserver 192.168.*.*:8000
#run celery
python manage.py celery beat