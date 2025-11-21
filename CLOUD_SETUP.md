# Cloud Setup Guide for EffiLearner

## Quick Start: Using API-Based Models (Recommended)

### Option 1: Together AI (Cheapest for Open Models)

1. **Sign up**: https://together.ai
2. **Get API key**: https://api.together.xyz/settings/api-keys
3. **Set environment variable**:
   ```bash
   export TOGETHER_API_KEY="your-api-key-here"
   ```
4. **Run EffiLearner**:
   ```bash
   python src/EffiLearner_API.py \
     --model "meta-llama/Llama-3-8b-chat-hf" \
     --api_base "https://api.together.xyz/v1" \
     --dataset MBPP \
     --epoch 5
   ```

**Pricing**: ~$0.20-0.50 per 1M tokens (very cheap!)

**Recommended models on Together AI**:
- `meta-llama/Llama-3-8b-chat-hf` - Good quality, fast
- `Qwen/Qwen2.5-7B-Instruct` - Excellent for code
- `mistralai/Mixtral-8x7B-Instruct-v0.1` - High quality
- `meta-llama/Llama-3-70b-chat-hf` - Best quality (more expensive)

### Option 2: OpenAI API

```bash
export OPENAI_API_KEY="your-key"
python src/EffiLearner_API.py \
  --model "gpt-4o-mini" \
  --dataset MBPP \
  --epoch 5
```

**Pricing**: 
- GPT-4o-mini: $0.15/$0.60 per 1M tokens (input/output)
- GPT-4o: $2.50/$10 per 1M tokens

### Option 3: Replicate API

```bash
export REPLICATE_API_TOKEN="your-token"
python src/EffiLearner_API.py \
  --model "meta/llama-3-8b-instruct" \
  --api_base "https://api.replicate.com/v1" \
  --api_key "$REPLICATE_API_TOKEN" \
  --dataset MBPP
```

## Option 2: GPU Cloud Instances (For Local Model Loading)

### RunPod (Recommended)

1. **Sign up**: https://www.runpod.io
2. **Create GPU pod**:
   - Choose: RTX 3090 (24GB) or A100 (40GB)
   - Template: PyTorch
   - Spot pricing: ~$0.20-0.50/hour
3. **Upload your code** and run:
   ```bash
   python src/EffiLearner.py --checkpoint Qwen/Qwen2.5-7B-Instruct --dataset MBPP
   ```

**Pricing**: 
- RTX 3090: ~$0.29/hour (spot)
- A100 40GB: ~$1.10/hour (spot)

### Vast.ai (Cheapest)

1. **Sign up**: https://vast.ai
2. **Rent GPU**: Often 50% cheaper than RunPod
3. **Same usage** as RunPod

**Pricing**: 
- RTX 3090: ~$0.15-0.25/hour
- A100: ~$0.60-0.90/hour

### Google Colab (Free, Limited)

1. **Open**: https://colab.research.google.com
2. **Enable GPU**: Runtime → Change runtime type → GPU (T4)
3. **Upload code** and run

**Limitations**: 
- 12-hour session limit
- May disconnect
- T4 GPU (slower than RTX 3090)

## Cost Comparison

| Service | Model Size | Cost per Hour | Cost for 100 samples |
|---------|-----------|---------------|---------------------|
| **Together AI** | 8B | $0.20-0.50/1M tokens | ~$0.10-0.50 |
| **OpenAI GPT-4o-mini** | - | $0.15/1M tokens | ~$0.50-2.00 |
| **RunPod RTX 3090** | Any | $0.29/hour | ~$0.30-1.00 |
| **Vast.ai RTX 3090** | Any | $0.15-0.25/hour | ~$0.15-0.50 |
| **Colab** | Any | FREE | FREE (with limits) |

## Recommendation

**For your use case (limited disk space)**: Use **Together AI API** with `EffiLearner_API.py`

**Why**:
- ✅ No disk space needed
- ✅ No GPU needed
- ✅ Very cheap (~$0.10-0.50 per 100 samples)
- ✅ Easy setup (just API key)
- ✅ Good model quality (Llama-3, Qwen, etc.)

## Example Usage

```bash
# 1. Set API key
export TOGETHER_API_KEY="your-key-here"

# 2. Generate code (if needed)
python src/gpt_generation.py \
  --dataset MBPP \
  --model "meta-llama/Llama-3-8b-chat-hf" \
  --num_samples 10 \
  --output_dir results

# 3. Run optimization
python src/EffiLearner_API.py \
  --model "meta-llama/Llama-3-8b-chat-hf" \
  --api_base "https://api.together.xyz/v1" \
  --dataset MBPP \
  --epoch 5
```

## Troubleshooting

**API errors**: Check your API key and rate limits
**Rate limits**: Together AI allows 1000 requests/minute (usually enough)
**Cost tracking**: Check your Together AI dashboard for usage

