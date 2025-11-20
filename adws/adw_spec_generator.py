#!/usr/bin/env -S uv run
# /// script
# dependencies = ["python-dotenv", "pydantic"]
# ///

"""
ADW Spec Generator - Create specifications from markdown input files

Usage:
  uv run adw_spec_generator.py <input-file> [output-name]

This script:
1. Reads a markdown/text input file (e.g., README.md)
2. Creates an ADW ID
3. Generates a detailed implementation specification
4. Saves the spec to specs/ directory
5. Outputs the ADW ID and spec file path

Example:
  uv run adw_spec_generator.py /path/to/README.md
  uv run adw_spec_generator.py /path/to/README.md "my-project-spec"
"""

import sys
import os
import json
import logging
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from adw_modules.utils import make_adw_id, setup_logger, parse_json
from adw_modules.data_types import AgentPromptRequest
from adw_modules.agent import prompt_claude_code
from adw_modules.state import ADWState


def validate_input_file(file_path: str, logger: logging.Logger) -> bool:
    """Validate that input file exists and is readable."""
    if not os.path.exists(file_path):
        logger.error(f"Input file not found: {file_path}")
        return False

    if not os.path.isfile(file_path):
        logger.error(f"Path is not a file: {file_path}")
        return False

    if not os.access(file_path, os.R_OK):
        logger.error(f"File is not readable: {file_path}")
        return False

    return True


def read_input_file(file_path: str, logger: logging.Logger) -> Optional[str]:
    """Read input file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"Read {len(content)} characters from input file")
        return content
    except Exception as e:
        logger.error(f"Failed to read input file: {e}")
        return None


def ensure_specs_directory(logger: logging.Logger) -> bool:
    """Ensure specs directory exists in project root."""
    try:
        # Get project root (parent of adws directory)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        specs_dir = os.path.join(project_root, "specs")

        os.makedirs(specs_dir, exist_ok=True)
        logger.info(f"Specs directory ensured: {specs_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to create specs directory: {e}")
        return False


def generate_specification(
    input_content: str,
    adw_id: str,
    logger: logging.Logger
) -> Optional[str]:
    """Generate implementation specification using Claude Code agent."""

    # Prepare the prompt for the planner agent
    prompt = f"""You are an expert software architecture and specification writer.

Analyze the following document and create a comprehensive implementation specification:

<document>
{input_content}
</document>

Generate a detailed specification that includes:

1. **Project Overview**
   - Clear project title and purpose
   - Key features and capabilities
   - Target users/use cases

2. **Architecture & Design**
   - System components and modules
   - Technology stack decisions
   - Design patterns and principles
   - Data models and schemas

3. **Implementation Requirements**
   - Core features with acceptance criteria
   - Dependencies and prerequisites
   - Integration points with existing systems
   - API/Interface specifications (if applicable)

4. **Development Phases**
   - Phase 1: Foundation
   - Phase 2: Core Features
   - Phase 3: Integration
   - Phase 4: Testing & Refinement
   - Phase 5: Documentation & Release

5. **Testing Strategy**
   - Unit testing approach
   - Integration testing requirements
   - E2E/Acceptance test scenarios
   - Performance/Security testing needs

6. **Success Criteria**
   - Definition of done
   - Performance benchmarks
   - Quality metrics
   - User acceptance criteria

7. **Known Risks & Mitigation**
   - Technical risks
   - Scheduling risks
   - Mitigation strategies

8. **References**
   - Links to relevant documentation
   - External resources
   - Related projects

Format your response as a clean, well-structured markdown document suitable for implementation planning.
The specification should be detailed enough for a developer to understand exactly what to build.
"""

    logger.info("Generating specification with Claude Code agent")

    request = AgentPromptRequest(
        prompt=prompt,
        adw_id=adw_id,
        agent_name="sdlc_planner",
        output_file=f"spec_{adw_id}.md"
    )

    try:
        response = prompt_claude_code(request)

        if not response.success:
            logger.error(f"Agent failed to generate specification: {response.output}")
            return None

        logger.info("Specification generated successfully")
        return response.output

    except Exception as e:
        logger.error(f"Error generating specification: {e}")
        return None


def save_specification(
    spec_content: str,
    adw_id: str,
    output_name: Optional[str],
    logger: logging.Logger
) -> Optional[str]:
    """Save specification to specs/ directory."""
    try:
        # Get project root
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        specs_dir = os.path.join(project_root, "specs")

        # Determine filename
        if output_name:
            # Use provided output name
            if not output_name.endswith('.md'):
                output_name = f"{output_name}.md"
            filename = output_name
        else:
            # Use ADW ID-based filename
            filename = f"spec-{adw_id}.md"

        spec_path = os.path.join(specs_dir, filename)

        # Write specification to file
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)

        logger.info(f"Specification saved: {spec_path}")
        return spec_path

    except Exception as e:
        logger.error(f"Failed to save specification: {e}")
        return None


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()

    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: uv run adw_spec_generator.py <input-file> [output-name]")
        print("Example: uv run adw_spec_generator.py /path/to/README.md")
        sys.exit(1)

    input_file = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else None

    # Create ADW ID
    adw_id = make_adw_id()
    print(f"Created ADW ID: {adw_id}")

    # Set up logger
    logger = setup_logger(adw_id, "adw_spec_generator")
    logger.info("ADW Spec Generator started")
    logger.info(f"Input file: {input_file}")
    if output_name:
        logger.info(f"Output name: {output_name}")

    # Validate environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        logger.error("ANTHROPIC_API_KEY not set")
        sys.exit(1)

    if not os.getenv("CLAUDE_CODE_PATH"):
        logger.warning("CLAUDE_CODE_PATH not set, using default 'claude'")

    # Validate input file
    if not validate_input_file(input_file, logger):
        sys.exit(1)

    # Read input file
    input_content = read_input_file(input_file, logger)
    if not input_content:
        sys.exit(1)

    # Ensure specs directory exists
    if not ensure_specs_directory(logger):
        sys.exit(1)

    # Generate specification
    spec_content = generate_specification(input_content, adw_id, logger)
    if not spec_content:
        sys.exit(1)

    # Save specification
    spec_path = save_specification(spec_content, adw_id, output_name, logger)
    if not spec_path:
        sys.exit(1)

    # Output summary
    print("\n" + "=" * 70)
    print("SPECIFICATION GENERATION COMPLETE")
    print("=" * 70)
    print(f"ADW ID:       {adw_id}")
    print(f"Spec File:    {spec_path}")
    print(f"Relative:     {os.path.relpath(spec_path)}")
    print("=" * 70)

    # Output state JSON for chaining
    state = {
        "adw_id": adw_id,
        "spec_file": spec_path,
        "output_name": output_name or f"spec-{adw_id}.md"
    }
    print(json.dumps(state, indent=2))

    logger.info("ADW Spec Generator completed successfully")


if __name__ == "__main__":
    main()
