FROM lighting-base-image

# Set working directory
WORKDIR /lighting/integration_tests

# Add sources
ADD . .

# Install requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

#Run tests
# CMD tail -f /dev/null
ENTRYPOINT pytest -v -s tests/main.py
# ENTRYPOINT python -m debugpy --listen 127.0.0.1:5678 --wait-for-client -m pytest -v -s tests/run.py
