FROM lighting-base-image

# Add sources
WORKDIR /lighting/core
ADD src/ src/
ADD __init__.py .

# Run the script
# CMD tail -f /dev/null
ENTRYPOINT [ "python", "/lighting/core/src/main.py" ]
