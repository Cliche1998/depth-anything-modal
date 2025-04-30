# DepthAnything Service

We aim to deploy a web API using FastAPI on Modal that processes videos to generate depth images for frames using the DepthAnything V2 model.

## Part 1: Pick a Model

### Candidate Model
- **DepthAnything V2** - [GitHub](#) | [Huggingface](#)

Conduct a lightweight trade study to identify the best open-source model for this use case. DepthAnything V2 is among the most performant models, but feel free to suggest alternatives if you have strong preferences. Document the factors considered for this decision. Additionally, analyze the tradeoffs between different model sizes within DepthAnything V2 and summarize them in a table.

## Part 2: Host the Model Inference on Modal

Deploy the model inference as an app on Modal. This involves:
1. A GPU app for running the model inference.
2. A REST endpoint to:
    - Trigger inference on the GPU app.
    - Provide a status endpoint for monitoring.

This setup allows asynchronous inference execution and monitoring for a web frontend. Modal provides FastAPI examples that can be leveraged. Use the $30 monthly credits provided by Modal for experimentation. If additional credits are required, notify me.

## Part 3: Test Script and Benchmark Runtime

1. Select a few video examples not included in the training set (e.g., recent or self-recorded videos).
2. Test the depth estimation performance qualitatively.
3. Measure inference runtime and analyze how it varies based on:
    - GPU choice on Modal.
    - Model size selected in Step 1.

Document these findings in a Python script.

## Part 4: Evaluation & Documentation

1. Propose effective methods for evaluating depth maps. Use existing metrics or suggest new ones, noting the tradeoffs between them. This is a discussion-only task; no implementation is required.
2. Provide the complete code and create a README or slide deck explaining:
    - The model deployment process.
    - Libraries/tools used.

Prepare to present this in a 30-minute call.
# DepthAnything Service

We aim to deploy a web API using FastAPI on Modal that processes videos to generate depth images for frames using the DepthAnything V2 model.

## Part 1: Pick a Model

### Candidate Model
- **DepthAnything V2** - [GitHub](#) | [Huggingface](#)

Conduct a lightweight trade study to identify the best open-source model for this use case. DepthAnything V2 is among the most performant models, but feel free to suggest alternatives if you have strong preferences. Document the factors considered for this decision. Additionally, analyze the tradeoffs between different model sizes within DepthAnything V2 and summarize them in a table.

## Part 2: Host the Model Inference on Modal

Deploy the model inference as an app on Modal. This involves:
1. A GPU app for running the model inference.
2. A REST endpoint to:
    - Trigger inference on the GPU app.
    - Provide a status endpoint for monitoring.

This setup allows asynchronous inference execution and monitoring for a web frontend. Modal provides FastAPI examples that can be leveraged. Use the $30 monthly credits provided by Modal for experimentation. If additional credits are required, notify me.

## Part 3: Test Script and Benchmark Runtime

1. Select a few video examples not included in the training set (e.g., recent or self-recorded videos).
2. Test the depth estimation performance qualitatively.
3. Measure inference runtime and analyze how it varies based on:
    - GPU choice on Modal.
    - Model size selected in Step 1.

Document these findings in a Python script.

## Part 4: Evaluation & Documentation

1. Propose effective methods for evaluating depth maps. Use existing metrics or suggest new ones, noting the tradeoffs between them. This is a discussion-only task; no implementation is required.
2. Provide the complete code and create a README or slide deck explaining:
    - The model deployment process.
    - Libraries/tools used.

