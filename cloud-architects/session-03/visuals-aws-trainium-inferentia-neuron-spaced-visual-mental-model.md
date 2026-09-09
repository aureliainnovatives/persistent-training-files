# AWS Trainium, Inferentia & Neuron --- Spaced Visual Mental Model

> **Purpose:** Trainer reference for Module 2. This uses wide ASCII
> visuals, like the Bedrock reference, to explain the hardware families,
> the Neuron software stack, runtime/compiler flow, deployment options,
> and major features.

# 1. Complete Mental Model

``` text
                                   AWS AI ACCELERATOR STACK
                                              │
                ┌─────────────────────────────┴─────────────────────────────┐
                │                                                           │
                ▼                                                           ▼
          AWS TRAINIUM                                                AWS INFERENTIA
                │                                                           │
                │                                                           │
        Purpose-built AWS                                           Purpose-built AWS
        AI accelerator family                                      inference accelerator family
                │                                                           │
                └─────────────────────────────┬─────────────────────────────┘
                                              │
                                              ▼
                                         AWS NEURON
                                              │
       ┌──────────────────────┬───────────────┼───────────────┬──────────────────────┐
       │                      │               │               │                      │
       ▼                      ▼               ▼               ▼                      ▼
   FRAMEWORKS             COMPILER          RUNTIME       LIBRARIES / NKI        DEV TOOLS
       │                      │               │               │                      │
       ├── PyTorch            │               │               ├── Training           ├── Neuron Explorer
       ├── JAX                │               │               ├── Inference          ├── Profiling
       ├── Hugging Face       │               │               ├── NKI                ├── Monitoring
       ├── vLLM               │               │               └── Kernel Library     └── Debugging
       └── Others             │               │
                              ▼               ▼
                      Neuron Graph       Neuron Runtime
                        Compiler              │
                              │               ├── Load model
                              │               ├── Device allocation
                              │               ├── Memory management
                              │               ├── Scheduling
                              │               └── Collective communication
                              │
                              ▼
                    NEFF Executable Artifact
                              │
                              └───────────────────┐
                                                  │
                                                  ▼
                                             NEURONCORES
                                                  │
                           ┌──────────────────────┴──────────────────────┐
                           │                                             │
                           ▼                                             ▼
                     Trainium Devices                              Inferentia Devices
```

# 2. The Key Relationship

``` text
TRAINIUM / INFERENTIA
        =
      HARDWARE

AWS NEURON
        =
 SOFTWARE DEVELOPMENT STACK

NEURON COMPILER
        =
 MODEL / GRAPH → OPTIMIZED EXECUTABLE

NEURON RUNTIME
        =
 LOAD + EXECUTE + MANAGE MODEL ON NEURONCORES
```

> **Trainer memory line:** Trainium and Inferentia are the accelerator
> hardware families. Neuron is the software stack that makes those
> accelerators usable from AI frameworks and serving libraries.

# 3. Trainium --- Expanded View

``` text
                                          AWS TRAINIUM
                                               │
               ┌───────────────────────────────┼───────────────────────────────┐
               │                               │                               │
               ▼                               ▼                               ▼
          AI TRAINING                    AI INFERENCE                    SCALE-OUT AI
               │                               │                               │
               ├── Pre-training                ├── LLM serving                 ├── Multiple chips
               ├── Fine-tuning                 ├── vLLM                        ├── Multiple nodes
               ├── Post-training               ├── Agentic workloads           ├── Distributed training
               ├── Reinforcement learning      └── High-scale serving          └── Collective communication
               └── Frontier-model workloads

                                               │
                                               ▼
                                         NEURON SOFTWARE
                                               │
                   ┌───────────────────────────┼────────────────────────────┐
                   │                           │                            │
                   ▼                           ▼                            ▼
              FRAMEWORKS                    NKI                      DEV / PERF TOOLS
                   │                           │                            │
                   ├── PyTorch                 ├── Custom kernels           ├── Neuron Explorer
                   ├── JAX                     ├── Memory control           ├── Profiling
                   ├── TorchTitan              ├── Scheduling control       ├── Debugging
                   └── Hugging Face            └── ISA-level control        └── Performance analysis
```

## Trainium Features to Recognize

-   Purpose-built AWS AI accelerator family.
-   Strong focus on large-scale training, but modern Trainium is **not
    training-only**.
-   Supports training and inference through the Neuron stack.
-   PyTorch and JAX integrations.
-   Distributed training support.
-   FSDP, DDP and DTensor support in current Neuron workflows.
-   vLLM-based inference support.
-   Custom kernel development through NKI.
-   Scale-out through Neuron device/interconnect and distributed
    communication mechanisms.
-   Trainium generations currently represented in AWS Neuron
    documentation include Trainium, Trainium2 and Trainium3.

# 4. Inferentia --- Expanded View

``` text
                                        AWS INFERENTIA
                                              │
             ┌────────────────────────────────┼────────────────────────────────┐
             │                                │                                │
             ▼                                ▼                                ▼
        MODEL SERVING                    PERFORMANCE                         ECONOMICS
             │                                │                                │
             ├── LLM inference                ├── Low latency                   ├── Cost per request
             ├── Embeddings                   ├── High throughput               ├── Cost per token
             ├── Vision / DL models           ├── Concurrency                   ├── Utilization
             └── Production inference         └── Batching                      └── Scale efficiency
                                              │
                                              ▼
                                         AWS NEURON
                                              │
                ┌─────────────────────────────┼─────────────────────────────┐
                │                             │                             │
                ▼                             ▼                             ▼
             COMPILER                      RUNTIME                      SERVING
                │                             │                             │
                ├── Optimize graph            ├── Load NEFF                  ├── vLLM
                ├── Hardware mapping          ├── Allocate devices           ├── Framework integration
                └── Generate NEFF             ├── Manage memory              └── Production endpoints
                                              ├── Schedule execution
                                              └── Device communication
```

## Inferentia Features to Recognize

-   AWS purpose-built inference accelerator family.
-   Designed around production inference price/performance.
-   Supports deep-learning and Generative AI inference.
-   Neuron software stack provides framework integration, compilation,
    runtime and tooling.
-   Current Neuron supports large-scale inference patterns including
    vLLM integration.
-   Modern inference features in the Neuron ecosystem include
    optimizations such as speculative decoding, expert parallelism and
    disaggregated inference where supported.
-   Inferentia generations commonly encountered are Inf1 and Inf2.

# 5. Training vs Inference --- Architect View

``` text
                 TRAINING                                      INFERENCE
                    │                                              │
                    ▼                                              ▼
                  DATA                                           REQUEST
                    │                                              │
                    ▼                                              ▼
              FORWARD PASS                                   FORWARD PASS
                    │                                              │
                    ▼                                              ▼
                  LOSS                                      TOKEN / PREDICTION
                    │                                              │
                    ▼                                              ▼
              BACKWARD PASS                                   RESPONSE
                    │
                    ▼
             UPDATE WEIGHTS


Primary concerns:                                  Primary concerns:

Compute intensity                                  Latency
Memory capacity                                    Time to first token
Memory bandwidth                                   Tokens / second
Distributed communication                         Throughput
Checkpointing                                      Concurrency
Training time                                      Batching
Cost to train                                      Cost per request/token
```

# 6. AWS Neuron --- Complete Feature Map

``` text
                                             AWS NEURON
                                                  │
        ┌─────────────────┬───────────────────────┼───────────────────────┬─────────────────┐
        │                 │                       │                       │                 │
        ▼                 ▼                       ▼                       ▼                 ▼
    FRAMEWORK          COMPILER                RUNTIME                KERNELS           TOOLING
   INTEGRATION             │                       │                       │                 │
        │                  │                       │                       │                 │
        ├── PyTorch        ├── Graph compile       ├── Load NEFF           ├── NKI           ├── Neuron Explorer
        ├── JAX            ├── Optimization        ├── Device allocation   ├── NKI Library   ├── Profiling
        ├── Hugging Face   ├── Hardware mapping    ├── Memory management   ├── Custom ops    ├── Monitoring
        ├── vLLM           └── NEFF generation     ├── Scheduling          └── Optimized     └── Debugging
        ├── TorchTitan                             └── Collectives             kernels
        └── PyTorch Lightning
```

# 7. Neuron Compiler --- What Actually Happens?

``` text
                                      PYTORCH / JAX MODEL
                                               │
                                               ▼
                                         MODEL GRAPH
                                               │
                                               ▼
                                    NEURON GRAPH COMPILER
                                               │
                         ┌─────────────────────┼─────────────────────┐
                         │                     │                     │
                         ▼                     ▼                     ▼
                   Analyze Graph         Optimize Ops        Hardware Mapping
                         │                     │                     │
                         └─────────────────────┼─────────────────────┘
                                               │
                                               ▼
                                      EXECUTION SCHEDULE
                                               │
                                               ▼
                                              NEFF
                               Neuron Executable File Format
                                               │
                                               ▼
                                        NEURON RUNTIME
```

## NEFF Mental Model

A NEFF is the compiled executable artifact that the Neuron Runtime loads
onto Neuron devices.

Think:

``` text
Python / Framework Model
          ↓
     Neuron Compiler
          ↓
         NEFF
          ↓
     Neuron Runtime
          ↓
      NeuronCore
```

# 8. Neuron Runtime --- Expanded View

``` text
                                         NEURON RUNTIME
                                               │
           ┌───────────────────────────────────┼───────────────────────────────────┐
           │                                   │                                   │
           ▼                                   ▼                                   ▼
       MODEL EXECUTION                    DEVICE MANAGEMENT                  DISTRIBUTED EXECUTION
           │                                   │                                   │
           ├── Load NEFF                       ├── Device allocation                ├── Neuron Collectives
           ├── Launch execution                ├── Memory management                ├── Core-to-core communication
           └── Return results                  ├── Scheduling                       └── Multi-device workloads
                                               └── Host/device interaction
```

The current NeuronX Runtime consists of a kernel driver and C/C++
libraries that expose access to Trainium and Inferentia devices.
Framework integrations use the runtime to load and execute compiled
models on NeuronCores.

## Runtime Memory Line

> **Compiler prepares the workload. Runtime operates the workload.
> Hardware executes the workload.**

# 9. Neuron Kernel Interface --- NKI

Most architects do not need to write kernels, but they should know why
NKI exists.

``` text
                                         STANDARD PATH
                                              │
                                     PyTorch / JAX / vLLM
                                              │
                                              ▼
                                         AWS NEURON
                                              │
                                              ▼
                                          HARDWARE


                                      ADVANCED PATH
                                              │
                                              ▼
                                              NKI
                                              │
                     ┌────────────────────────┼────────────────────────┐
                     │                        │                        │
                     ▼                        ▼                        ▼
               Memory Control         Execution Scheduling      Hardware / ISA
                     │                        │                        │
                     └────────────────────────┼────────────────────────┘
                                              │
                                              ▼
                                        CUSTOM KERNEL
                                              │
                                              ▼
                                         NEURONCORE
```

## NKI Features

-   Python-based low-level programming interface.
-   Direct control of Neuron device capabilities.
-   Memory allocation and tensor placement.
-   Execution scheduling.
-   Custom operators/kernels.
-   Higher-level `nki.language` APIs.
-   Lower-level `nki.isa` access for instruction-level control.
-   NKI Library provides optimized kernels so developers do not always
    need to write their own.
-   Current NKI tooling includes a CPU Simulator for
    developing/debugging supported kernels without requiring accelerator
    hardware.

# 10. Neuron Explorer & Developer Tooling

``` text
                                          AI WORKLOAD
                                               │
                                               ▼
                                        NEURON DEVICES
                                               │
                                               ▼
                                      NEURON EXPLORER
                                               │
                       ┌───────────────────────┼───────────────────────┐
                       │                       │                       │
                       ▼                       ▼                       ▼
                    PROFILE                 DEBUG                  ANALYZE
                       │                       │                       │
                 Device behavior        Performance issues      System / device
                 Execution timeline     Bottlenecks             utilization
                 Distributed work       Code correlation        optimization
```

Neuron Explorer is the current profiling/debugging suite in the Neuron
ecosystem.

# 11. Deployment Mental Model

``` text
                                  MODEL / APPLICATION
                                           │
                                           ▼
                                       AWS NEURON
                                           │
          ┌────────────────────────────────┼────────────────────────────────┐
          │                                │                                │
          ▼                                ▼                                ▼
         EC2                              EKS                              ECS
          │                                │                                │
          └────────────────────────────────┼────────────────────────────────┘
                                           │
                                           ▼
                                      SAGEMAKER AI
                                           │
                                           ▼
                              TRAINIUM / INFERENTIA INSTANCES
```

Neuron also provides preconfigured Deep Learning AMIs and Deep Learning
Containers to simplify setup.

# 12. Modern LLM Inference Features

``` text
                                      LLM INFERENCE
                                            │
             ┌──────────────────────────────┼──────────────────────────────┐
             │                              │                              │
             ▼                              ▼                              ▼
           vLLM                       PARALLELISM                   OPTIMIZATION
             │                              │                              │
             ├── Standard APIs              ├── Expert Parallelism         ├── Speculative Decoding
             ├── LLM serving                ├── Context Parallelism        ├── Optimized Kernels
             └── Production use             └── Data / model patterns      └── Disaggregated Inference
```

Exact support depends on hardware generation, Neuron version and model.
Treat this as a **feature-recognition map**, not a guarantee for every
combination.

# 13. Trainium vs Inferentia --- Decision View

``` text
                                  AI WORKLOAD
                                       │
                         ┌─────────────┴─────────────┐
                         │                           │
                         ▼                           ▼
                 TRAIN / POST-TRAIN?           PRIMARILY SERVE?
                         │                           │
                         ▼                           ▼
                    TRAINIUM                    INFERENTIA
                         │                           │
                         │                           │
                 Also benchmark for            Optimized around
                 inference where               inference economics
                 appropriate
                         │                           │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                                  BENCHMARK FIRST
                                       │
                         ┌─────────────┼─────────────┐
                         ▼             ▼             ▼
                     QUALITY        PERFORMANCE      TCO
                                     / LATENCY
```

Do not make the decision only from the product name.

Validate:

-   model compatibility
-   framework compatibility
-   latency SLO
-   throughput
-   memory requirements
-   sequence lengths
-   concurrency
-   engineering migration effort
-   distributed architecture
-   utilization
-   cost

# 14. Trainium / Inferentia vs GPU

``` text
                                ACCELERATOR DECISION
                                        │
               ┌────────────────────────┴────────────────────────┐
               │                                                 │
               ▼                                                 ▼
              GPU                                         AWS AI CHIPS
               │                                                 │
       Broad ecosystem / CUDA                         Trainium / Inferentia
       High portability                                    │
       Mature tooling                                      │
               │                                      AWS Neuron stack
               │                                      AWS optimization
               │                                      Potential TCO benefit
               │                                                 │
               └────────────────────────┬────────────────────────┘
                                        │
                                        ▼
                                BENCHMARK REAL WORKLOAD
```

Questions before migration:

1.  Is the model supported?
2.  Are required operators supported?
3.  Are CUDA-specific custom kernels involved?
4.  What changes are required?
5.  What is compilation/optimization effort?
6.  What is the actual throughput?
7.  What latency is achieved?
8.  What is the end-to-end TCO?

# 15. The Most Important Architect Metrics

``` text
                                      AI ACCELERATOR
                                            │
            ┌───────────────────────────────┼───────────────────────────────┐
            │                               │                               │
            ▼                               ▼                               ▼
        PERFORMANCE                       MEMORY                           COST
            │                               │                               │
            ├── Latency                     ├── Model size                   ├── Instance cost
            ├── TTFT                        ├── HBM capacity                 ├── Cost / request
            ├── Tokens/sec                  ├── Memory bandwidth            ├── Cost / token
            ├── Throughput                  ├── KV cache                    └── Utilization
            └── Concurrency                 └── Batch / sequence impact
```

# 16. Five Common Misconceptions

``` text
1. "Trainium can only train."
   → Too simplistic. Modern Trainium supports inference workloads too.

2. "Inferentia is an LLM."
   → No. It is accelerator hardware.

3. "Neuron is hardware."
   → No. Neuron is the software stack.

4. "Neuron Runtime compiles my model."
   → Compiler and Runtime are separate concepts:
     compiler produces executable artifacts;
     runtime loads and executes them.

5. "Cheaper instance = cheaper AI."
   → Not necessarily. Compare throughput, utilization,
     migration effort, latency and total cost.
```

# 17. Five-Minute Whiteboard Version

``` text
                          PYTORCH / JAX / vLLM
                                   │
                                   ▼
                              AWS NEURON
                                   │
             ┌─────────────────────┼─────────────────────┐
             │                     │                     │
             ▼                     ▼                     ▼
          COMPILER               RUNTIME                NKI
             │                     │                     │
        Model → NEFF         Load / Execute        Custom Kernels
             │                     │                     │
             └─────────────────────┼─────────────────────┘
                                   │
                                   ▼
                              NEURONCORES
                                   │
                       ┌───────────┴───────────┐
                       │                       │
                       ▼                       ▼
                    TRAINIUM               INFERENTIA
                       │                       │
                 Training +              Inference-focused
                 inference              production serving
```

# 18. Trainer Memory Lines

> **Trainium = AWS purpose-built AI accelerator family strongly
> associated with training and high-scale AI compute.**

> **Inferentia = AWS purpose-built accelerator family optimized around
> inference economics.**

> **Neuron = the software stack connecting frameworks and AI workloads
> to Trainium and Inferentia.**

> **Neuron Compiler = converts/optimizes model graphs into executable
> artifacts for Neuron devices.**

> **Neuron Runtime = loads and executes those compiled workloads while
> managing devices, memory, scheduling and communication.**

> **NKI = lower-level programming interface for developers who need
> custom kernels and deeper hardware control.**

# 19. Trainer Checkpoint

You should be able to answer:

1.  What is Trainium?
2.  What is Inferentia?
3.  Why does AWS need Neuron?
4.  What is a NeuronCore?
5.  What does the Neuron Compiler do?
6.  What is NEFF?
7.  What does Neuron Runtime do?
8.  What is NKI?
9.  Why would someone use NKI instead of only PyTorch?
10. What is Neuron Explorer?
11. Can Trainium perform inference?
12. Why might Inferentia improve inference economics?
13. Why is hourly instance price not enough for comparison?
14. How do vLLM and Neuron relate?
15. What should an architect benchmark before choosing an accelerator?

# 20. One-Line Complete Mental Model

``` text
AI FRAMEWORK
    ↓
AWS NEURON
    ↓
COMPILER → NEFF → RUNTIME
    ↓
NEURONCORES
    ↓
TRAINIUM / INFERENTIA
    ↓
TRAINING + INFERENCE AT AWS SCALE
```
