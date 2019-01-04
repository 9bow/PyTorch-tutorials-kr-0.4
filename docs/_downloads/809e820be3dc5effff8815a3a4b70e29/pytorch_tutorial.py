# -*- coding: utf-8 -*-
r"""
PyTorch 소개
***********************

Torch의 텐서(Tensor) 라이브러리 소개
======================================

모든 딥러닝은 2차원 이상으로 색인될 수 있는 행렬의 일반화인
텐서의 연산입니다. 이것이 무엇을 의미하지 나중에 정확히
알게 될 것입니다. 먼저, 텐서로 무엇을 할 수 있는지 살펴 봅시다.
"""
# Author: Robert Guthrie

import torch
import torch.autograd as autograd
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

torch.manual_seed(1)


######################################################################
# 텐서 생성하기
# ~~~~~~~~~~~~~~~~
#
# 텐서는 파이썬 리스트에서 torch.Tensor() 함수로 생성될 수 있습니다.
#

# torch.tensor(data) 는 주어진 데이터로 torch.Tensor 객체를 생성합니다.
V_data = [1., 2., 3.]
V = torch.tensor(V_data)
print(V)

# 행렬 생성
M_data = [[1., 2., 3.], [4., 5., 6]]
M = torch.tensor(M_data)
print(M)

# 2x2x2 크기의 3D 텐서 생성.
T_data = [[[1., 2.], [3., 4.]],
          [[5., 6.], [7., 8.]]]
T = torch.tensor(T_data)
print(T)


######################################################################
# 어쨌든 3D 텐서가 무엇입니까? 이렇게 생각해 보십시오. 만약 벡터가 있다면
# 벡터에 주소를 입력하면 스칼라를 줍니다. 만약 행렬을 가지고 있다면 행렬에
# 주소를 입력하면 벡터를 줍니다. 만약 3D 텐서를 가지고 있다면 텐서에 주소를
# 입력하면 행렬을 줍니다.
#
# 용어에 대한 주석:
# 이 튜토리얼에서 "텐서"를 언급 할 때 그것은 어떤 torch.Tensor 객체를 말합니다.
# 행렬과 벡터는 각각 차원이 1과 2인 torch.Tensors 의 특별한 케이스 입니다.
# 3D 텐서를 말할 때는 "3D 텐서"라고 명시적으로 사용하겠습니다.
#

# Index into V and get a scalar (0 dimensional tensor)
print(V[0])
# Get a Python number from it
print(V[0].item())

# Index into M and get a vector
print(M[0])

# Index into T and get a matrix
print(T[0])


######################################################################
# 다른 데이터 유형의 텐서를 생성 할 수도 있습니다. 보시다시피 기본값은
# Float입니다. 정수형의 텐서를 만들려면 torch.LongTensor ()를 사용하십시오.
# 더 많은 데이터 유형에 대해서는 설명서를 확인하십시오.
# 그러나 Float 및 Long이 가장 일반적입니다.
#


######################################################################
# torch.randn ()을 사용하여 랜덤 데이터와 제공된 차원으로 텐서를
# 만들 수 있습니다.
#

x = torch.randn((3, 4, 5))
print(x)


######################################################################
# 텐서로 작업하기
# ~~~~~~~~~~~~~~~~~~~~~~~
#
# 기대하는 방식으로 텐서로 작업할 수 있습니다.

x = torch.tensor([1., 2., 3.])
y = torch.tensor([4., 5., 6.])
z = x + y
print(z)


######################################################################
# 사용 가능한 방대한 작업의 전체 목록은
# `문서 <http://pytorch.org/docs/torch.html>`__ 를 참고하십시오. 단순한
# 수학적 연산 이상으로 확장됩니다.
#
# 나중에 사용하게 될 유용한 작업 중 하나는 연결입니다.
#

# 기본으로 첫번째 축(가로 연결)을 따라 연결합니다.
x_1 = torch.randn(2, 5)
y_1 = torch.randn(3, 5)
z_1 = torch.cat([x_1, y_1])
print(z_1)

# 세로 연결:
x_2 = torch.randn(2, 3)
y_2 = torch.randn(2, 5)
# 두번째 변수는 연결될 축을 결정합니다.
z_2 = torch.cat([x_2, y_2], 1)
print(z_2)

# 텐서가 호환되지 않으면 Torch가 오류 메시지를 출력 합니다. 주석 처리를 제거하여 오류를 확인하십시오.
# torch.cat([x_1, x_2])


######################################################################
# 텐서 재구성
# ~~~~~~~~~~~~~~~~~
#
# .view() 메서드를 사용해서 텐서를 재구성합니다.
# 이 메서드는 많은 신경망 구성 요소가 입력을 특정 모양으로 예상하기
# 때문에 많이 사용됩니다. 데이터를 구성 요소로 전달하기 전에 종종 모양을
# 변경해야합니다.
#

x = torch.randn(2, 3, 4)
print(x)
print(x.view(2, 12))  # 가로 2 , 세로 12로 재구성
# 위와 같이 하나의 차원이 -1이면 그 것의 크기는 유추될 수 있습니다.
print(x.view(2, -1))


######################################################################
# 연산 그래프(Computation Graph)와 자동 미분(Automatic Differentiation)
# =======================================================================
#
# 연산 그래프의 개념은 역전파 그라디언트를 직접 작성할 필요가 없게 해주기 때문에
# 효율적인 딥러닝 프로그래밍에 필수적입니다.
# 연산 그래프는 데이터를 결합하여 출력을 제공하는 방법의 간단한 특징입니다.
# 그래프는 어떤 연산과 어떤 매개 변수가 연관되는지를 완전하게 특정하기 때문에
# 도함수(derivative)를 계산하기에 충분한 정보를 포함합니다.
# 아마 모호하게 들릴지도 모르니, 근본적인 플래그``requires_grad`` 를 사용하는데
# 어떤 일이 일어나는지 살펴봅시다.
#
# 먼저 프로그래머 관점에서 생각해 보세요.
# torch 에 무엇이 저장되있나요.
# 위에서 생성한 텐서의 객체는 무엇입니까? 분명히 데이터와 형태, 그리고
# 아마 몇몇 다른 것들 입니다. 그러나 우리가 두개의 텐서를 더할 때
# 출력 텐서를 얻습니다. 이 모든 출력 텐서는 그것의 데이터와 형태를 알고 있습니다.
# 하지만 그것이 두 텐서의 합이 었는지는 알지 못합니다.(파일에서 읽었을 수도
# 있고 다른 연산의 결과일 수도 있음)
#
# 만일 ``requires_grad=True`` 라면, 텐서 객체는 것이 어떻게 생성되었는지 추적합니다.
# 실제로 그것을 확인해 봅시다.
#

# 텐서 공장 메소드에 ``requires_grad`` 플래그가 있습니다.
x = torch.tensor([1., 2., 3], requires_grad=True)

# requires_grad=True 으로 이전에 있었던 모든 작업을 여전히 할 수 있습니다.
y = torch.tensor([4., 5., 6], requires_grad=True)
z = x + y
print(z)

# 그러나 z 는 몇가지를 추가로 알고 있습니다.
print(z.grad_fn)


######################################################################
# 그래서 텐서는 무엇이 그들을 생성했는지를 알고 있습니다.
# z 는 그것이 파일에서 읽어온 것이 아니고 곱셈 지수승 또는 다른 어떤 것의
# 결과가 아니라는 것을 알고 있습니다. 그리고 만약 z.grad_fn 를 따라 간다면
# x 와 y 를 찾을 것 입니다.
#
# 그러나 그것이 기울기(gradient)를 계산하는데 어떻게 도움이 될까요?
#

# z 의 모든 요소를 합해 봅시다.
s = z.sum()
print(s)
print(s.grad_fn)


######################################################################
# 이제 x의 첫번째 구성요소에 해당하는 이 합계의 도함수가 무엇입니까?
# 우리가 원하는 수식은 다음과 같습니다.
#
# .. math::
#
#    \frac{\partial s}{\partial x_0}
#
#
#
# 그럼 s 는 텐서 z 의 합으로 생성되었다는 것을 알고 있습니다.
# z 는 x + y 합이 었다는 것을 알고 있습니다. 따라서
#
# .. math::  s = \overbrace{x_0 + y_0}^\text{$z_0$} + \overbrace{x_1 + y_1}^\text{$z_1$} + \overbrace{x_2 + y_2}^\text{$z_2$}
#
# 그리고 따라서 s 는 우리가 원하는 도함수가 1인 것을 결정하는데 충분한 정보를 가지고 있습니다.
#
# 물론 이것은 그 도함수를 실제로 계산법에 대한 도전에 대해 해설하고 있습니다.
# 여기서 핵심은 s 가 그것을 계산 할 수 있는 충분한 정보를 가지고 있다는 것 입니다.
# 실제로 Pytorch 개발자는 기울기를 계산하는 방법을 알고 sum() 과 + 연산을 프로그램하고
# 역전파 알고리즘을 실행합니다. 이 알고리즘에 대한 자세한 설명은 이 튜토리얼의
# 범위를 벗어납니다.
#


######################################################################
# Pytorch가 기울기를 계산하게 하고, 우리가 옳았다는 것을 확인하십시오
# ( 만약 이 블럭을 여러번 실행한다면 기울기가 증가할 것입니다.
# 그것은 Pytorch 가 .grad 속성에 기울기를 누적하기 때문이고,
# 이것은 많은 모델에서 매우 편리합니다.
#

# 어떤 변수에서 .backward() 호출은 그것에서 시작하는 역전파를 실행합니다.
s.backward()
print(x.grad)


######################################################################
# 아래 블록에서 진행되는 작업을 이해하는 것은 딥러닝의 성공적인
# 프로그래머가 되는데 중요합니다.
#

x = torch.randn(2, 2)
y = torch.randn(2, 2)
# 기본적으로 사용자가 생성한 텐서는 ``requires_grad=False`` 로 설정됩니다.
print(x.requires_grad, y.requires_grad)
z = x + y
# 따라서 z 를 통하는 역전파를 계산할 수 없습니다.
print(z.grad_fn)

# ``.requires_grad_( ... )`` 는 기존 텐서의 ``requires_grad`` 플래그를 변경합니다.
# 입력 플래그는 주어지지 않을 경우 기본적으로 ``True`` 설정됩니다.
x = x.requires_grad_()
y = y.requires_grad_()
# 위에서 본대로 z 는 기울기를 계산하는데 충분한 정보를 가지고 있습니다.
z = x + y
print(z.grad_fn)
# 만일 연산의 어떤 입력이 ``requires_grad=True`` 를 가지면, 그 출력도 동일합니다.
print(z.requires_grad)

# 이제 z는 x와 y와 관련이 있는 연산 이력을 가집니다.
# 그것의 값만 취해서 그것의 이력에서 **분리** 할 수 있을 까요?
new_z = z.detach()

# ... new_z는 x와 y에 역전파하기 위한 정보를 가지고 있습니까?
# 아닙니다!
print(new_z.grad_fn)
# 어떻게 그럴 수 있을까요?  ``z.detach()`` 는 ``z`` 와 같은 저장 공간을 공유하지만
# 계산 이력을 잊어버린 텐서를 반환합니다. 그것은 그것이 어떻게 계산되었는지
# 아무 것도 모릅니다.
# 기본적으로 우리는 과거의 이력에서 Tensor를 분리했습니다.

###############################################################
# requires_grad=True 를 가진 텐서를 ``with torch.no_grad():`` 으로
# 둘러싸서 이력 추적의 자동미분(autograd)을 멈출 수 있습니다.
print(x.requires_grad)
print((x ** 2).requires_grad)

with torch.no_grad():
	print((x ** 2).requires_grad)


