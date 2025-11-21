#!/bin/bash
# Run both Scalene and non-Scalene optimizations for 5 iterations and compare

set -e

DATASET="${1:-EffiBench}"
MODEL="${2:-gpt-4o}"
OUTPUT_DIR="${3:-results}"
SAMPLE_SIZE="${4:-20}"

echo "=================================================================================="
echo "Running 5-iteration optimization comparison: Scalene vs Non-Scalene"
echo "=================================================================================="
echo "Dataset: $DATASET"
echo "Model: $MODEL"
echo "Output Directory: $OUTPUT_DIR"
echo "Sample Size: $SAMPLE_SIZE"
echo "Iterations: 5 for each profiler"
echo "=================================================================================="
echo ""

# Step 1: Check for generation file
GEN_FILE="$OUTPUT_DIR/generation/${DATASET}_${MODEL}_none.json"
if [ ! -f "$GEN_FILE" ]; then
    echo "⚠️  Generation file not found: $GEN_FILE"
    echo "   Please generate baseline code first using:"
    echo "   python src/gpt_generation.py"
    echo "   or use an existing generation file"
    echo ""
    echo "   Checking for legacy generation files..."
    # Check for legacy location
    if [ -f "./${DATASET}_${MODEL}.json" ]; then
        echo "   Found legacy file: ./${DATASET}_${MODEL}.json"
        GEN_FILE="./${DATASET}_${MODEL}.json"
        echo "   Using: $GEN_FILE"
    else
        echo "   ✗ No generation file found. Exiting."
        exit 1
    fi
    echo ""
else
    echo "✓ Found generation file: $GEN_FILE"
    echo ""
fi

# Step 2: Run non-Scalene optimization (5 epochs)
echo "=================================================================================="
echo "Step 1: Running Non-Scalene optimization (5 epochs)"
echo "=================================================================================="
python src/RunSmallEffi.py \
    --dataset "$DATASET" \
    --checkpoint "$MODEL" \
    --epoch 5 \
    --output_dir "$OUTPUT_DIR" \
    --input_file "$GEN_FILE" \
    --sample_size "$SAMPLE_SIZE" \
    --no_shuffle \
    --batch_size 8

NONE_OUTPUT="$OUTPUT_DIR/optimization/${DATASET}_${MODEL}_none_5.json"
echo "✓ Non-Scalene optimization complete"
echo "  Output: $NONE_OUTPUT"
echo ""

# Step 3: Run Scalene optimization (5 epochs)
echo "=================================================================================="
echo "Step 2: Running Scalene optimization (5 epochs)"
echo "=================================================================================="
python src/RunSmallEffi.py \
    --dataset "$DATASET" \
    --checkpoint "$MODEL" \
    --epoch 5 \
    --output_dir "$OUTPUT_DIR" \
    --input_file "$GEN_FILE" \
    --sample_size "$SAMPLE_SIZE" \
    --no_shuffle \
    --batch_size 8 \
    --use_scalene \
    --scalene_runs 1

SCALENE_OUTPUT="$OUTPUT_DIR/optimization/${DATASET}_${MODEL}_scalene_5.json"
echo "✓ Scalene optimization complete"
echo "  Output: $SCALENE_OUTPUT"
echo ""

# Step 4: Compare results
echo "=================================================================================="
echo "Step 3: Comparing results after 5 iterations"
echo "=================================================================================="
python src/compare_scalene_vs_none.py \
    --dataset "$DATASET" \
    --model "$MODEL" \
    --output_dir "$OUTPUT_DIR" \
    --epoch 5

echo ""
echo "=================================================================================="
echo "Comparison complete!"
echo "=================================================================================="
echo ""
echo "Results saved to:"
echo "  Non-Scalene: $NONE_OUTPUT"
echo "  Scalene: $SCALENE_OUTPUT"
echo ""

