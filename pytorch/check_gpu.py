#!/usr/bin/env python
import torch
torch.cuda.current_device()
torch.cuda.device(0)
torch.cuda.device_count()
print(torch.cuda.get_device_name(0))

print('cuda', torch.cuda.is_available())
