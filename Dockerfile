FROM continuumio/miniconda3:4.7.12

# install dependencies first
RUN pip install flask==1.0.2\
   		spacy==2.2.4\
		spacy-lookups-data==0.3.2\
		beautifulsoup4==4.6.3\
                gunicorn==19.9.0

RUN python -m spacy download en_core_web_sm

# set up file system
RUN mkdir ds
WORKDIR /ds

# copy the files over
COPY main.py /ds

CMD ["gunicorn", "-w","2", "-b","0.0.0.0:8080","main:app"]
