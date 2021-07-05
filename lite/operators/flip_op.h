// Copyright (c) 2019 PaddlePaddle Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#pragma once
#include <string>
#include <vector>
#include "lite/core/op_lite.h"
#include "lite/core/scope.h"
#include "lite/utils/all.h"

namespace paddle {
namespace lite_metal {
namespace operators {

class FlipOp : public OpLite {
 public:
  FlipOp() {}
  explicit FlipOp(const std::string &op_type) : OpLite(op_type) {}

  bool CheckShape() const override;

  bool InferType() override {
    param_.Out->set_precision(param_.X->precision());
    return true;
  }

  bool InferShapeImpl() const override;

  bool AttachImpl(const cpp::OpDesc &opdesc, lite_metal::Scope *scope) override;

  void AttachKernel(KernelBase *kernel) override { kernel->SetParam(param_); }
  std::string DebugString() const override { return "flip"; }

 protected:
  mutable FlipParam param_;
  int axis_;
};

}  // namespace operators
}  // namespace lite
}  // namespace paddle