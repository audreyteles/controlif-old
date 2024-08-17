# 
FROM python:3.11

# 
WORKDIR ./

# 
COPY ./requirements.txt ./requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN apt update && apt install libgl1 -y

# 
COPY ./ /

# 
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
