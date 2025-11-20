# ADW Spec Generator Guide

## Overview

The **ADW Spec Generator** is a tool that transforms markdown documents (like README.md) into detailed implementation specifications using AI-powered planning. It integrates with the ADW (AI Developer Workflow) system to automatically:

1. Create a unique ADW ID for tracking
2. Generate comprehensive implementation specifications
3. Save specifications to the `/specs/` directory
4. Output structured state for workflow integration

## What It Does

The spec generator takes input documents and produces detailed specifications including:

- **Project Overview**: Purpose, features, target users, use cases
- **Architecture & Design**: System components, technology stack, design patterns, data models
- **Implementation Requirements**: Features with acceptance criteria, technical requirements
- **Development Phases**: Structured phases from foundation to release
- **Testing Strategy**: Unit, integration, E2E, and performance testing approaches
- **Success Criteria**: Definition of done, performance benchmarks, quality metrics
- **Known Risks & Mitigation**: Technical and scheduling risks with mitigation strategies
- **References**: Links to documentation and related projects

## Quick Start

### Prerequisites

```bash
# Ensure environment is configured
export ANTHROPIC_API_KEY="your-api-key"
export CLAUDE_CODE_PATH="/path/to/claude"  # Optional, defaults to 'claude'
```

### Basic Usage

```bash
# Navigate to ADW directory
cd /Users/slysik/tac/steve/adws

# Generate spec from README
uv run adw_spec_generator.py /Users/slysik/tac/steve/README.md

# Generate spec with custom output name
uv run adw_spec_generator.py /Users/slysik/tac/steve/README.md "my-spec-name"
```

### Output

The tool generates:

1. **Specification File**: Saved in `/specs/` directory
   - Format: `{output-name}.md` or `spec-{adw_id}.md`
   - Size: Typically 15-30KB for comprehensive specs

2. **Execution Log**: Saved in `agents/{adw_id}/adw_spec_generator/execution.log`
   - Contains detailed timing and processing information

3. **ADW ID**: Unique 8-character identifier for the workflow
   - Example: `740c587d`
   - Used for tracking and resuming workflows

4. **JSON Output**: Structured state for chaining with other ADW tools
   ```json
   {
     "adw_id": "740c587d",
     "spec_file": "/Users/slysik/tac/steve/specs/readme-specification.md",
     "output_name": "readme-specification.md"
   }
   ```

## Example: Generate Spec for README.md

```bash
$ cd /Users/slysik/tac/steve/adws
$ uv run adw_spec_generator.py /Users/slysik/tac/steve/README.md "readme-specification"

Created ADW ID: 740c587d
ADW Logger initialized - ID: 740c587d
ADW Spec Generator started
Input file: /Users/slysik/tac/steve/README.md
Output name: readme-specification
Read 7831 characters from input file
Specs directory ensured: /Users/slysik/tac/steve/specs
Generating specification with Claude Code agent
Output saved to: spec_740c587d.md
Created JSON file: spec_740c587d.md
Specification generated successfully
Specification saved: /Users/slysik/tac/steve/specs/readme-specification.md

======================================================================
SPECIFICATION GENERATION COMPLETE
======================================================================
ADW ID:       740c587d
Spec File:    /Users/slysik/tac/steve/specs/readme-specification.md
Relative:     ../specs/readme-specification.md
======================================================================
{
  "adw_id": "740c587d",
  "spec_file": "/Users/slysik/tac/steve/specs/readme-specification.md",
  "output_name": "readme-specification.md"
}
```

## Spec Content Structure

Generated specifications follow this structure:

### 1. Project Overview
- Project title and purpose
- Key features and capabilities
- Target users and use cases

### 2. Architecture & Design
- System component diagram
- Technology stack breakdown
- Design patterns employed
- Data models and schemas

### 3. Implementation Requirements
- Individual features with acceptance criteria
- Technical requirements for each feature
- Dependencies and prerequisites

### 4. Development Phases
- Phase 1: Foundation work
- Phase 2: Core features
- Phase 3: Integration
- Phase 4: Testing & refinement
- Phase 5: Documentation & release

### 5. Testing Strategy
- Unit testing approach
- Integration testing requirements
- E2E test scenarios
- Performance and security testing

### 6. Success Criteria
- Definition of done
- Performance benchmarks
- Quality metrics
- User acceptance criteria

### 7. Risks & Mitigation
- Technical risks and solutions
- Scheduling risks and contingencies
- Resource and dependency risks

### 8. References
- Documentation links
- External resources
- Related projects

## Integration with ADW Workflow

The spec generator output can be piped to other ADW tools:

```bash
# Generate spec and chain with implementation
uv run adw_spec_generator.py /path/to/input.md | jq '.adw_id' | \
  xargs -I {} uv run adw_build.py 123 {}
```

## Input File Requirements

### Supported Formats
- Markdown (.md)
- Plain text (.txt)
- Any UTF-8 encoded text file

### Content Guidelines
- Clear project description
- Feature lists and requirements
- Architecture or design diagrams (in text format)
- Technology choices with rationale
- Any existing documentation or specs

### File Size
- Recommended: 2KB - 100KB
- Tested with files up to 1MB
- Larger files generate more detailed specifications

## Logging and Debugging

All execution is logged to: `agents/{adw_id}/adw_spec_generator/execution.log`

Check logs for:
- File read operations
- Spec directory validation
- Agent communication details
- File save status
- Overall timing

## Troubleshooting

### Error: "ANTHROPIC_API_KEY not set"
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Error: "Claude Code CLI is not installed"
```bash
# Set correct path
export CLAUDE_CODE_PATH="/path/to/claude"

# Or install Claude Code
# See: https://docs.anthropic.com/en/docs/claude-code
```

### Error: "Input file not found"
- Verify the file path is correct
- Use absolute paths for reliability
- Check file permissions (must be readable)

### Error: "Specs directory creation failed"
- Verify you have write permissions in the project root
- Check disk space
- Ensure parent directories exist

### Spec file is incomplete or empty
- Check the execution log: `agents/{adw_id}/adw_spec_generator/execution.log`
- Agent response might have been cut off
- Try with a smaller input file to narrow down the issue

## Advanced Usage

### Generate Multiple Specs

```bash
# Create specs from multiple files
for file in *.md; do
  echo "Generating spec for $file..."
  uv run adw_spec_generator.py "$file" "spec-${file%.md}"
done
```

### Batch Processing with State

```bash
# Generate and store state
STATE=$(uv run adw_spec_generator.py /path/to/input.md "output-name")

# Use the ADW ID from state
ADW_ID=$(echo "$STATE" | jq -r '.adw_id')
SPEC_FILE=$(echo "$STATE" | jq -r '.spec_file')

echo "Generated spec: $SPEC_FILE"
echo "ADW ID: $ADW_ID"
```

### Viewing Generated Specs

```bash
# List all generated specs
ls -lh /Users/slysik/tac/steve/specs/

# View a spec
cat /Users/slysik/tac/steve/specs/readme-specification.md

# Search specs
grep -r "implementation" /Users/slysik/tac/steve/specs/
```

## Architecture of the Tool

```
adw_spec_generator.py
├── Imports
│   ├── File system operations
│   ├── Logging utilities
│   └── Agent execution
├── Input Validation
│   ├── File existence check
│   ├── Readability verification
│   └── Content validation
├── ADW ID Creation
│   └── Unique 8-character identifier
├── Specification Generation
│   ├── Prompt construction
│   ├── Agent execution via Claude Code
│   └── Response parsing
└── Output Handling
    ├── File system persistence
    ├── Log file creation
    └── JSON state output
```

## Performance Characteristics

- **Input Read**: < 100ms for typical files
- **Spec Generation**: 60-120 seconds (depends on LLM)
- **File Writing**: < 500ms
- **Total Time**: ~2-3 minutes

## Environment Variables

| Variable | Purpose | Required | Default |
|----------|---------|----------|---------|
| `ANTHROPIC_API_KEY` | API authentication | Yes | None |
| `CLAUDE_CODE_PATH` | Claude Code CLI path | No | `claude` |
| `PYTHONPATH` | Python module path | No | Auto-set |

## Output Directory Structure

```
/Users/slysik/tac/steve/
├── specs/
│   ├── readme-specification.md          ← Generated spec
│   └── patch/                           ← Existing patch specs
└── agents/
    └── 740c587d/                        ← ADW ID directory
        ├── adw_state.json               ← Workflow state
        └── adw_spec_generator/
            └── execution.log             ← Detailed log
```

## Best Practices

1. **Use Descriptive Output Names**: `uv run adw_spec_generator.py input.md "clear-descriptive-name"`

2. **Preserve Generated Specs**: Keep specs in version control for reference

3. **Reference ADW IDs**: Save the ADW ID if you plan to resume or chain workflows

4. **Check Logs**: Always review the execution log for detailed processing information

5. **Validate Generated Specs**: Review generated specifications for accuracy before using for implementation

## Related Tools

- **adw_plan.py**: GitHub issue planning
- **adw_build.py**: Implementation execution
- **adw_test.py**: Test execution
- **adw_review.py**: Code review
- **adw_document.py**: Documentation generation

## Support

For issues or questions:
1. Check the execution log: `agents/{adw_id}/adw_spec_generator/execution.log`
2. Verify environment variables are set correctly
3. Ensure input file is valid and readable
4. Check that Claude Code CLI is installed and working
