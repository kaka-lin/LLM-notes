from vllm import LLM, SamplingParams


def main():
    # initialize the LLM with the desired model
    llm = LLM(
        model="google/gemma-3-4b-it",
        dtype="auto",
    )

    # Sample prompts for chating
    prompts = [
        "Explain what vLLM is in one paragraph.",
        "Give me three use cases of vLLM.",
    ]

    # Create a sampling params.
    sampling_params = SamplingParams(
        temperature=0.8,
        top_p=0.95,
        max_tokens=256,
    )

    outputs = llm.generate(prompts, sampling_params)

    for i, out in enumerate(outputs):
        print(f"\n=== Prompt {i} ===")
        print("Prompt:", prompts[i])
        print("Output:", out.outputs[0].text)


if __name__ == "__main__":
    main()
