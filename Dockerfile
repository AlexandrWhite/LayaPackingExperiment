FROM sergeypotemkin/blackwell_cuda12.8_pytorch2.8.0_py3.10_ubuntu22.04:latest
RUN pip install tabulate
RUN pip install huggingface-hub
RUN pip install datasets
RUN pip install transformers
RUN pip install laya 
CMD g++ timus-best.cpp -o grounded_truth
CMD ["bash"]