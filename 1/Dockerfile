FROM python:3.9.6-buster

COPY switch_to_full_release.py /plugin_script/switch_to_full_release.py
COPY requirements.txt /plugin_script/requirements.txt
RUN python -m pip install -r /plugin_script/requirements.txt
CMD ["python", "/plugin_script/switch_to_full_release.py"]
