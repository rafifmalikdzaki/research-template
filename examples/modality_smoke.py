"""Local random-weight forward passes. No pretrained weights or dataset downloads."""

import argparse


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("modality", choices=["vision", "llm", "multimodal", "scientific"])
    args = parser.parse_args()
    if args.modality == "scientific":
        import numpy as np
        from scipy.integrate import solve_ivp

        result = solve_ivp(lambda t, y: -y, (0, 1), [1.0], rtol=1e-8, atol=1e-10)
        assert result.success
        assert abs(result.y[0, -1] - np.exp(-1)) < 1e-6
        print("Synthetic exponential-decay solver smoke passed")
        return

    import torch

    torch.manual_seed(42)
    if args.modality == "vision":
        from torchvision.models import resnet18

        model = resnet18(weights=None, num_classes=2).eval()
        with torch.inference_mode():
            output = model(torch.randn(2, 3, 64, 64))
        assert output.shape == (2, 2)
    elif args.modality == "llm":
        from transformers import GPT2Config, GPT2LMHeadModel

        model = GPT2LMHeadModel(
            GPT2Config(vocab_size=64, n_positions=16, n_embd=32, n_layer=1, n_head=2)
        ).eval()
        with torch.inference_mode():
            output = model(input_ids=torch.randint(0, 64, (2, 8))).logits
        assert output.shape == (2, 8, 64)
    else:
        from torchvision.models import resnet18

        image_encoder = resnet18(weights=None).eval()
        image_encoder.fc = torch.nn.Identity()
        tabular_encoder = torch.nn.Sequential(torch.nn.Linear(9, 16), torch.nn.ReLU())
        fusion = torch.nn.Linear(512 + 16, 2)
        with torch.inference_mode():
            output = fusion(
                torch.cat(
                    [
                        image_encoder(torch.randn(2, 3, 64, 64)),
                        tabular_encoder(torch.randn(2, 9)),
                    ],
                    dim=1,
                )
            )
        assert output.shape == (2, 2)
    assert torch.isfinite(output).all()
    print(f"{args.modality}: random-weight CPU smoke passed; shape={tuple(output.shape)}")


if __name__ == "__main__":
    main()
