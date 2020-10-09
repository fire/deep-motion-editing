import torch
from torch import optim

class DeepMotionTargeting(torch.nn.Module):
    def __init__(self, N, M):
        super(DeepMotionTargeting, self).__init__()
        self.weight = torch.nn.Parameter(torch.rand(N, M))

    def forward(self, input):
        if input.sum() > 0:
          output = self.weight.mv(input)
        else:
          output = self.weight + input
        return output

module = DeepMotionTargeting(10,20)
sm = torch.jit.script(module)
print(sm.code)