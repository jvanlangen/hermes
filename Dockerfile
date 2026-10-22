FROM nousresearch/hermes-agent:latest

USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libcairo2 \
        libglib2.0-0 \
        libgomp1 \
        libxml2 \
        libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m ensurepip --upgrade \
    && python3 -m pip install --no-cache-dir \
    pandas \
    openpyxl \
    python-docx \
    python-pptx \
    odfpy \
    pymupdf \
    pdfplumber \
    pypdf \
    Pillow \
    opencv-python-headless \
    cairosvg \
    ezdxf \
    lxml \
    PyYAML \
    toml