#!/usr/bin/env python3
"""Compare actual analysis output against expected output"""

import json
import sys

def normalize_for_comparison(obj):
    """Remove timestamp and runtime-specific fields for comparison"""
    if isinstance(obj, dict):
        normalized = {}
        for key, value in obj.items():
            # Skip dynamic fields
            if key in ['timestamp', 'analysis_id']:
                continue
            if key == 'metadata':
                # Keep metadata structure but skip dynamic values
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

def compare_jsons(actual_path, expected_path):
    """Compare actual output with expected output"""
    try:
        with open(actual_path, 'r') as f:
            actual = json.load(f)
        with open(expected_path, 'r') as f:
            expected = json.load(f)

        # Normalize both for comparison
        actual_norm = normalize_for_comparison(actual)
        expected_norm = normalize_for_comparison(expected)

        print("\033[94m📊 OUTPUT COMPARISON REPORT\033[0m")
        print("=" * 60)

        # Check basic structure
        print("\n\033[94m1. STRUCTURE CHECK:\033[0m")
        actual_keys = set(actual_norm.keys())
        expected_keys = set(expected_norm.keys())

        if actual_keys == expected_keys:
            print(f"\033[92m✓ All required sections present\033[0m")
            print(f"  Sections: {', '.join(sorted(actual_keys))}")
        else:
            missing = expected_keys - actual_keys
            extra = actual_keys - expected_keys
            if missing:
                print(f"\033[91m✗ Missing sections: {missing}\033[0m")
            if extra:
                print(f"\033[91m✗ Extra sections: {extra}\033[0m")

        # Check data content
        print("\n\033[94m2. DATA CONTENT CHECK:\033[0m")
        if actual_norm == expected_norm:
            print("\033[92m✓ All data matches expected output\033[0m")
        else:
            print("\033[91m✗ Data differences found:\033[0m")

            # Find specific differences
            for key in expected_keys:
                if key in actual:
                    if actual_norm.get(key) != expected_norm.get(key):
                        print(f"\n  {key}:")
                        print(f"    Expected: {json.dumps(expected_norm.get(key), indent=6)[:100]}...")
                        print(f"    Actual:   {json.dumps(actual_norm.get(key), indent=6)[:100]}...")

        # Check metadata and tokens
        print("\n\033[94m3. METADATA CHECK:\033[0m")
        actual_meta = actual.get('metadata', {})
        expected_meta = expected.get('metadata', {})

        # Check data quality
        if 'data_quality_score' in actual_meta and 'data_quality_score' in expected_meta:
            actual_quality = actual_meta['data_quality_score']
            expected_quality = expected_meta['data_quality_score']
            match = "✓" if actual_quality == expected_quality else "✗"
            print(f"  {match} Data Quality Score: {actual_quality} (expected: {expected_quality})")

        # Check agents coordination
        if 'agents_coordination_success' in actual_meta and 'agents_coordination_success' in expected_meta:
            actual_success = actual_meta['agents_coordination_success']
            expected_success = expected_meta['agents_coordination_success']
            match = "✓" if actual_success == expected_success else "✗"
            print(f"  {match} Agents Coordination Success: {actual_success} (expected: {expected_success})")

        # Check tokens (estimate should be reasonable)
        print("\n\033[94m4. TOKEN USAGE CHECK:\033[0m")
        if 'llm_tokens_used' in actual_meta:
            actual_tokens = actual_meta['llm_tokens_used']
            expected_tokens = expected_meta.get('llm_tokens_used', 'N/A')
            print(f"  Actual tokens used: {actual_tokens}")
            print(f"  Expected tokens used: {expected_tokens}")
            print(f"  ℹ️  Note: Using Claude 3.5 Sonnet (claude-3-5-sonnet-20241022)")

        # Check processing time
        print("\n\033[94m5. PROCESSING TIME:\033[0m")
        if 'processing_time_seconds' in actual_meta:
            actual_time = actual_meta['processing_time_seconds']
            print(f"  Processing time: {actual_time} seconds")
            print(f"  ℹ️  This will vary based on system performance")

        # Check timestamp
        print("\n\033[94m6. TIMESTAMP CHECK:\033[0m")
        if 'timestamp' in actual:
            print(f"  Actual timestamp: {actual['timestamp']}")
            print(f"  Expected timestamp: {expected['timestamp']}")
            print(f"  ℹ️  Timestamps naturally differ per run")

        print("\n" + "=" * 60)
        print("\n\033[94m📝 SUMMARY:\033[0m")
        if actual_norm == expected_norm:
            print("\033[92m✓ OUTPUT MATCHES EXPECTED FORMAT (ignoring timestamps and runtime)\033[0m")
        else:
            print("\033[93m⚠️  OUTPUT HAS DIFFERENCES - Review details above\033[0m")

    except FileNotFoundError as e:
        print(f"\033[91m✗ Error: {e}\033[0m")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\033[91m✗ JSON Error: {e}\033[0m")
        sys.exit(1)

if __name__ == "__main__":
    compare_jsons('/tmp/actual_response.json', '/app/data/expected_output.json')
