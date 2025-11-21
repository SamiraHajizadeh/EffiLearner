#!/bin/bash
# Script to run both Scalene and non-Scalene optimizations on the same samples
# for a fair comparison

set -e

DATASET="${1:-EffiBench}"
MODEL="${2:-gpt-4o}"
EPOCH="${3:-1}"
OUTPUT_DIR="${4:-results}"
SAMPLE_SIZE="${5:-20}"

echo "=================================================================================="
echo "Running Scalene and Non-Scalene optimizations on the SAME samples"
echo "=================================================================================="
echo "Dataset: $DATASET"
echo "Model: $MODEL"
echo "Epochs: $EPOCH"
echo "Output Directory: $OUTPUT_DIR"
echo "Sample Size: $SAMPLE_SIZE"
echo "=================================================================================="
echo ""

# Step 1: Generate baseline if it doesn't exist
GEN_FILE="$OUTPUT_DIR/generation/${DATASET}_${MODEL}_none.json"
if [ ! -f "$GEN_FILE" ]; then
    echo "Step 1: Generating baseline code..."
    python src/gpt_generation.py \
        --dataset "$DATASET" \
        --checkpoint "$MODEL" \
        --output_dir "$OUTPUT_DIR" \
        --sample_size "$SAMPLE_SIZE" \
        --no_shuffle
    echo "✓ Baseline generation complete"
    echo ""
else
    echo "✓ Baseline file already exists: $GEN_FILE"
    echo ""
fi

# Step 2: Run non-Scalene optimization
echo "Step 2: Running non-Scalene optimization..."
python src/RunSmallEffi.py \
    --dataset "$DATASET" \
    --checkpoint "$MODEL" \
    --epoch "$EPOCH" \
    --output_dir "$OUTPUT_DIR" \
    --input_file "$GEN_FILE" \
    --sample_size "$SAMPLE_SIZE" \
    --no_shuffle \
    --batch_size 8
echo "✓ Non-Scalene optimization complete"
echo ""

# Step 3: Run Scalene optimization (using same input file)
echo "Step 3: Running Scalene optimization (same samples)..."
python src/RunSmallEffi.py \
    --dataset "$DATASET" \
    --checkpoint "$MODEL" \
    --epoch "$EPOCH" \
    --output_dir "$OUTPUT_DIR" \
    --input_file "$GEN_FILE" \
    --sample_size "$SAMPLE_SIZE" \
    --no_shuffle \
    --batch_size 8 \
    --use_scalene \
    --scalene_runs 1
echo "✓ Scalene optimization complete"
echo ""

# Step 4: Compare results
echo "=================================================================================="
echo "Step 4: Comparing results..."
echo "=================================================================================="
python src/compare_scalene_vs_none.py \
    --dataset "$DATASET" \
    --model "$MODEL" \
    --output_dir "$OUTPUT_DIR" \
    --epoch "$EPOCH"

echo ""
echo "=================================================================================="
echo "Comparison complete!"
echo "=================================================================================="

