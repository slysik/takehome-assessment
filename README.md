## Multi-Agent Research & Analysis System 

## Welcome

You're about to build a multi-agent orchestration system using LangGraph that analyzes company earnings reports. This assignment will showcase your ability to design, implement, and containerize a production-ready multi-agent workflow.

## Your Mission

You'll create an automated system that processes quarterly earnings reports using multiple specialized agents that work together. Think of it as building a team of AI specialists, each with their own expertise, working together to analyze financial documents.

## Requirements

### 1. Multi-Agent System Architecture (60 minutes)

You'll implement the following agents using LangGraph:

#### **Coordinator Agent**
- Manages the overall workflow
- Routes tasks to appropriate agents
- Handles state management between agents
- Implements retry logic for failed agent tasks

#### **Data Extraction Agent**
- Extracts key financial metrics (revenue, profit, EPS, etc.)
- Identifies year-over-year changes
- Structures data in a consistent format

#### **Sentiment Analysis Agent**
- Analyzes management commentary tone
- Identifies positive/negative indicators
- Flags risk factors mentioned

#### **Summary Agent**
- Consolidates all agent findings
- Generates an executive summary
- Produces structured output (JSON format)

### 2. Implementation Requirements

You should:
- Use LangGraph for agent orchestration
- Implement proper state management between agents
- Include error handling and fallback mechanisms
- Use environment variables for configuration
- Implement logging for debugging

### 3. Containerization (20 minutes)

You'll need to:
- Complete the Dockerfile for your application
- Ensure all dependencies are properly managed
- Make your application accessible via REST API endpoint
- Include a working health check endpoint

### 4. Documentation (10 minutes)

Create a `SOLUTION.md` file where you'll explain:

1. **Architecture Overview** (200 words max)
   - Why you chose your specific agent design
   - How agents communicate and share state
   - Key design decisions

2. **Production Considerations** (300 words max)
   - How would you scale this to handle 1000+ documents/hour?
   - What monitoring/observability would you implement?
   - Cost optimization strategies for LLM usage
   - Security considerations for handling sensitive financial data

3. **Improvements** (100 words max)
   - What additional agents would you add given more time?
   - How would you implement agent memory/learning?

## What We've Provided for You

### Sample Data
- `data/earnings_report_sample.txt` - A sample earnings report you'll process
- `data/expected_output.json` - Shows what your output should look like

### Starter Code
- `src/agents/base.py` - Base agent template to extend
- `src/main.py` - Main application entry point with TODOs for you
- `requirements.txt` - All the Python dependencies you'll need
- `Dockerfile.template` - Docker template for you to complete

## How to Submit Your Solution

1. Complete your implementation in the provided structure
2. Make sure your Docker container builds and runs successfully
3. Test with the provided sample data
4. Write your `SOLUTION.md` documentation
5. Create a ZIP file with your entire solution
6. Include a `run.sh` script that demonstrates your solution working

### Expected Deliverables

```
takehome-submission/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── coordinator.py
│   │   ├── data_extractor.py
│   │   ├── sentiment.py
│   │   └── summary.py
│   ├── workflow/
│   │   └── graph.py
│   └── main.py
├── data/
│   ├── earnings_report_sample.txt
│   └── expected_output.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── SOLUTION.md
└── run.sh
```

## Testing Your Solution

Here's how you can test your implementation:

```bash
# Build your Docker container
docker build -t earnings-analyzer .

# Run your container
docker run -p 8000:8000 earnings-analyzer

# Test your endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"report_path": "/app/data/earnings_report_sample.txt"}'
```

## Important Notes

- You can use OpenAI, Anthropic, or any open-source LLM (just tell us which one)
- We're more interested in your architecture and orchestration skills than perfect prompts
- The sample data is synthetic - don't worry about actual financial accuracy
- Feel free to mock LLM APIs if you're testing locally
- We value clean, production-ready code over complex features

## Tips for Success

- Start by understanding the provided base code
- Think about how your agents will communicate and share state
- Consider error cases - what happens when an agent fails?
- Keep your code modular and easy to test
- Document your design decisions clearly

## Questions?

If something isn't clear, document your assumptions in `SOLUTION.md` and proceed with your best interpretation. We'd rather see how you think through ambiguity than have you stuck.



