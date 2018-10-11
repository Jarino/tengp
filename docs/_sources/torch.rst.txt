Using PyTorch
=============

`PyTorch <https://pytorch.org/>`_ is an deep learning framework, providing many useful features, including tensor computation with GPU if available.

Since API of PyTorch is designed to be similar to NumPy, not much is needed to execute TenGP individual using GPU::
  
  # define function set with operation from torch library, instead of numpy
  torch_funset = tengp.FunctionSet()
  torch_funset.add(torch.add, 2)
  torch_funset.add(torch.sub, 2)
  torch_funset.add(torch.mul, 2)

  # specify, that we want to use tensors, so the output is aligned
  torch_params = tengp.Parameters(9, 1, 1, 50, torch_funset, use_tensors=True)

  # create a random individual
  torch_individual = tengp.individual.IndividualBuilder(torch_params).create()

  # convert numpy array to tensor
  x_train_tensor = torch.from_numpy(x_train)

  # copy tensor to GPU (should check before whether its available)
  x_train_tensor = x_train_tensor.to(torch.device('cuda'))

  # transform works the same way
  output = torch_individual.transform(x_train_tensor)
