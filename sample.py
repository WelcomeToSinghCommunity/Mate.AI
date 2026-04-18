import torch

print(torch.cuda.is_available())
print(torch.cuda.get_device_name(0))

#I was check whether GPU power was getting consumed