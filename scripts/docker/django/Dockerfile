FROM debian
RUN apt-get upgrade && apt-get update
ADD Django-prepare.sh /Homepage-scripts/Django-prepare.sh
RUN chmod +x /Homepage-scripts/Django-prepare.sh
RUN /Homepage-scripts/Django-prepare.sh
ADD Django-run.sh /Homepage-scripts/Django-run.sh
RUN chmod +x /Homepage-scripts/Django-run.sh
RUN /Homepage-scripts/Django-run.sh
RUN chmod +x /Homepage/manage.py
CMD cd /Homepage && python3 manage.py runserver 0.0.0.0:8000