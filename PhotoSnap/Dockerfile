FROM python:3

ENV PYTHONBUFFERED 1
RUN mkdir /PhotoSnap
WORKDIR /PhotoSnap
COPY . /PhotoSnap/
RUN pip install -r requirements.txt
CMD ["uvicorn", "PhotoSnap:app", "--host", "0.0.0.0", "--port", "8000"]