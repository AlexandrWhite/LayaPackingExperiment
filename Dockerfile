FROM sergeypotemkin/blackwell_cuda12.8_pytorch2.8.0_py3.10_ubuntu22.04:latest
RUN pip install laya 
RUN pip install tabulate
CMD g++ timus-best.cpp -o grounded_truth
CMD ["bash"]