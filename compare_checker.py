#!/usr/bin/env python3
"""Comparison checker for earnings analyzer output"""

import json
import sys

def normalize_for_comparison(obj):
    """Remove timestamp and runtime-specific fields for comparison"""
    if isinstance(obj, dict):
        normalized = {}
        for key, value in obj.items():
            # Skip runtime-specific fields
            if key in ['timestamp', 'analysis_id', 'errors']:
                continue
            if key == 'metadata':
                meta = {}
                if isinstance(value, dict):
                    for k, v in value.items():
                        if k not in ['processing_time_seconds']:
                            meta[k] = v
                normalized[key] = meta
            else:
                normalized[key] = normalize_for_comparison(value)
        return normalized
    elif isinstance(obj, list):
        return [normalize_for_comparison(item) for item in obj]
    else:
        return obj

try:
    with open('/tmp/actual_response.json', 'r') as f:
        actual = json.load(f)
    with open('/app/data/expected_output.json', 'r') as f:
        expected = json.load(f)

    actual_norm = normalize_for_comparison(actual)
    expected_norm = normalize_for_comparison(expected)

    print("\n📊 OUTPUT COMPARISON REPORT")
    print("=" * 60)

    print("\n1. STRUCTURE CHECK:")
    actual_keys = set(actual_norm.keys())
    expected_keys = set(expected_norm.keys())

    if actual_keys == expected_keys:
        print("✓ All required sections present")
        print(f"  Sections: {', '.join(sorted(actual_keys))}")
    else:
        missing = expected_keys - actual_keys
        extra = actual_keys - expected_keys
        if missing:
            print(f"✗ Missing sections: {missing}")
        if extra:
            print(f"✗ Extra sections: {extra}")

    print("\n2. DATA CONTENT CHECK:")
    if actual_norm == expected_norm:
        print("✓ All data matches expected output")
    else:
        print("✗ Data differences found:")
        for key in expected_keys:
            if key in actual:
                if actual_norm.get(key) != expected_norm.get(key):
                    print(f"\n  {key}:")
                    exp_str = json.dumps(expected_norm.get(key), indent=6)[:100]
                    act_str = json.dumps(actual_norm.get(key), indent=6)[:100]
                    print(f"    Expected: {exp_str}...")
                    print(f"    Actual:   {act_str}...")

    print("\n3. METADATA CHECK:")
    actual_meta = actual.get('metadata', {})
    expected_meta = expected.get('metadata', {})

    if 'data_quality_score' in actual_meta and 'data_quality_score' in expected_meta:
        actual_quality = actual_meta['data_quality_score']
        expected_quality = expected_meta['data_quality_score']
        match = "✓" if actual_quality == expected_quality else "✗"
        print(f"  {match} Data Quality Score: {actual_quality} (expected: {expected_quality})")

    if 'agents_coordination_success' in actual_meta and 'agents_coordination_success' in expected_meta:
        actual_success = actual_meta['agents_coordination_success']
        expected_success = expected_meta['agents_coordination_success']
        match = "✓" if actual_success == expected_success else "✗"
        print(f"  {match} Agents Coordination Success: {actual_success} (expected: {expected_success})")

    print("\n4. TOKEN USAGE CHECK:")
    if 'llm_tokens_used' in actual_meta:
        actual_tokens = actual_meta['llm_tokens_used']
        expected_tokens = expected_meta.get('llm_tokens_used', 'N/A')
        print(f"  Actual tokens used: {actual_tokens}")
        print(f"  Expected tokens used: {expected_tokens}")
        print(f"  Note: Using Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)")

    print("\n5. PROCESSING TIME:")
    if 'processing_time_seconds' in actual_meta:
        actual_time = actual_meta['processing_time_seconds']
        print(f"  Processing time: {actual_time} seconds")
        print(f"  Note: This will vary based on system performance")

    print("\n6. TIMESTAMP CHECK:")
    if 'timestamp' in actual:
        print(f"  Actual timestamp: {actual['timestamp']}")
        print(f"  Expected timestamp: {expected['timestamp']}")
        print(f"  Note: Timestamps naturally differ per run")

    print("\n" + "=" * 60)
    print("\n📝 SUMMARY:")
    if actual_norm == expected_norm:
        print("✓ OUTPUT MATCHES EXPECTED FORMAT (ignoring timestamps and runtime)")
    else:
        print("⚠️  OUTPUT HAS DIFFERENCES - Review details above")
    print()

except Exception as e:
    print(f"Error during comparison: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
