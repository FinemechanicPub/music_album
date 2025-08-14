FROM python:3.13-slim
 
RUN groupadd -r appgroup
RUN useradd -r -g appgroup appuser
RUN mkdir /app
RUN chown appuser:appgroup /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=appuser:appuser . .
USER appuser
EXPOSE 8000 

CMD ["gunicorn", "music_album.wsgi:application", "--bind", "0.0.0.0:8000"]