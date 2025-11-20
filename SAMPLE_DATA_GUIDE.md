# Sample Data Guide - Multi-Agent Earnings Analyzer

This guide documents the sample data files provided with the Multi-Agent Earnings Analyzer and explains how they're used for testing and demonstration purposes.

## Sample Data Files Location

```
app/client/data/
├── earnings_report_sample.txt    # Sample earnings report for input
└── expected_output.json          # Expected system output for testing
```

## Input Sample: `earnings_report_sample.txt`

### File Details
- **Location**: `app/client/data/earnings_report_sample.txt`
- **Format**: Plain text earnings report
- **Company**: TechCorp International
- **Period**: Q3 2024
- **Size**: ~3.5 KB

### Content Structure

The sample earnings report contains the following sections:

#### 1. Financial Highlights
Key metrics extracted by the Data Extractor Agent:
```
- Revenue: $15.2 billion, up 12% year-over-year
- Net Income: $3.8 billion, up 18% year-over-year  
- Earnings Per Share (EPS): $4.52, beating analyst estimates of $4.30
- Operating Margin: 28.5%, up from 26.2% in Q3 2023
- Free Cash Flow: $4.1 billion, up 22% year-over-year
```

**Mapping to AnalysisState**:
- `financial_metrics.revenue`: $15.2B with 12% YoY growth
- `financial_metrics.net_income`: $3.8B with 18% YoY growth
- `financial_metrics.eps`: $4.52 (beats $4.30 estimate)
- `financial_metrics.operating_margin`: 28.5% (up from 26.2%)
- `financial_metrics.free_cash_flow`: $4.1B with 22% YoY growth

#### 2. CEO Commentary
Management commentary analyzed by the Sentiment Analyzer Agent:
```
"We are thrilled to report another outstanding quarter that exceeded 
expectations across all key metrics..."
```

**Sentiment Indicators**:
- **Positive phrases**: "thrilled", "outstanding", "exceeded expectations", "remarkable strength"
- **Growth signals**: "35% year-over-year growth", "unprecedented demand", "2,000 new enterprise customers"
- **Tone**: Optimistic and confident

#### 3. Segment Performance
Business segment breakdown analyzed by the Data Extractor Agent:

| Segment | Revenue | Growth | Key Metrics |
|---------|---------|--------|------------|
| Cloud Services | $6.8B | +35% YoY | 2,000+ new customers, 98.5% retention |
| Software Products | $5.1B | +8% YoY | Enterprise security suite strong |
| Hardware | $3.3B | -2% YoY | Margin improvement despite decline |

**Mapping to AnalysisState**:
```python
segment_performance = {
    "cloud_services": {
        "revenue": 6.8,
        "growth_rate": 0.35,
        "operating_margin": 0.42,
        "metrics": {
            "new_customers": 2000,
            "retention_rate": 0.985
        }
    },
    "software_products": {
        "revenue": 5.1,
        "growth_rate": 0.08,
        "highlights": ["enterprise security suite performance"]
    },
    "hardware": {
        "revenue": 3.3,
        "growth_rate": -0.02,
        "notes": "margin improvement despite revenue decline"
    }
}
```

#### 4. Forward Guidance
Future projections analyzed by the Data Extractor Agent:
```
Q4 2024 Guidance:
- Revenue: $16.0-16.5 billion
- EPS: $4.70-4.85
- Full-year revenue growth: 14-15%
```

**Mapping to AnalysisState**:
```python
forward_guidance = {
    "q4_2024": {
        "revenue_range": [16.0, 16.5],
        "eps_range": [4.70, 4.85]
    },
    "full_year_growth": [0.14, 0.15]
}
```

#### 5. Risk Factors
Negative indicators and challenges identified by the Sentiment Analyzer:
```
- Increasing competition in cloud services market
- Regulatory scrutiny in international markets
- Foreign exchange volatility
- Potential economic slowdown
- Cybersecurity threats requiring continued investment
```

**Sentiment Impact**: Demonstrates balanced reporting with both opportunities and risks

#### 6. Capital Allocation
Shareholder return information:
```
- $5 billion share buyback program
- Dividend increased 10% to $0.88 per share
- $2 billion for strategic acquisitions in AI/ML
- R&D targeting 15% of revenue
```

## Expected Output: `expected_output.json`

### File Details
- **Location**: `app/client/data/expected_output.json`
- **Format**: JSON (structured analysis results)
- **Size**: ~3.5 KB
- **Purpose**: Reference output for validation and testing

### Output Structure

#### 1. Metadata
```json
{
  "analysis_id": "analysis_12345",
  "timestamp": "2024-10-15T10:30:00Z",
  "company": "TechCorp International",
  "period": "Q3 2024",
  "agents_executed": [
    "coordinator",
    "data_extractor",
    "sentiment_analyzer",
    "summary_generator"
  ]
}
```

#### 2. Financial Metrics (Data Extractor Output)
```json
{
  "financial_metrics": {
    "revenue": {
      "value": 15.2,
      "unit": "billion USD",
      "yoy_change": 0.12,
      "trend": "positive"
    },
    "net_income": {
      "value": 3.8,
      "unit": "billion USD",
      "yoy_change": 0.18,
      "trend": "positive"
    },
    "eps": {
      "value": 4.52,
      "analyst_estimate": 4.30,
      "beat_estimate": true
    },
    "operating_margin": {
      "current": 0.285,
      "previous": 0.262,
      "trend": "improving"
    },
    "free_cash_flow": {
      "value": 4.1,
      "unit": "billion USD",
      "yoy_change": 0.22
    }
  }
}
```

#### 3. Segment Performance (Data Extractor Output)
```json
{
  "segment_performance": {
    "cloud_services": {
      "revenue": 6.8,
      "growth_rate": 0.35,
      "operating_margin": 0.42,
      "metrics": {
        "new_customers": 2000,
        "retention_rate": 0.985
      }
    },
    "software_products": {
      "revenue": 5.1,
      "growth_rate": 0.08,
      "highlights": ["enterprise security suite performance"]
    },
    "hardware": {
      "revenue": 3.3,
      "growth_rate": -0.02,
      "notes": "margin improvement despite revenue decline"
    }
  }
}
```

#### 4. Sentiment Analysis (Sentiment Analyzer Output)
```json
{
  "sentiment_analysis": {
    "overall_sentiment": "positive",
    "confidence": 0.85,
    "management_tone": "optimistic_cautious",
    "key_positive_indicators": [
      "exceeded expectations across all key metrics",
      "remarkable strength in cloud services",
      "unprecedented demand for AI solutions",
      "strong balance sheet and cash generation"
    ],
    "key_negative_indicators": [
      "hardware division revenue decline",
      "potential market saturation concerns",
      "macroeconomic uncertainties"
    ],
    "risk_factors_identified": [
      "increasing cloud market competition",
      "regulatory scrutiny",
      "foreign exchange volatility",
      "potential economic slowdown",
      "cybersecurity threats"
    ]
  }
}
```

#### 5. Forward Guidance (Data Extractor Output)
```json
{
  "forward_guidance": {
    "q4_2024": {
      "revenue_range": [16.0, 16.5],
      "eps_range": [4.70, 4.85]
    },
    "full_year_growth": [0.14, 0.15]
  }
}
```

#### 6. Capital Allocation (Data Extractor Output)
```json
{
  "capital_allocation": {
    "share_buyback": 5.0,
    "dividend_per_share": 0.88,
    "dividend_increase": 0.10,
    "acquisition_budget": 2.0,
    "rd_target_percentage": 0.15
  }
}
```

#### 7. Executive Summary (Summary Agent Output)
```json
{
  "executive_summary": {
    "headline": "Strong Q3 Performance Driven by Cloud and AI Growth",
    "summary": "TechCorp International delivered exceptional Q3 2024 results with 12% revenue growth to $15.2B and 18% net income growth to $3.8B. The cloud services division led performance with 35% YoY growth, while AI solutions gained significant traction with 2,000+ new enterprise customers. Despite hardware segment challenges (-2% YoY), overall margins improved to 28.5%. Management maintains cautiously optimistic outlook with Q4 guidance of $16.0-16.5B revenue, though acknowledges risks from competition, regulation, and macroeconomic factors. Strong cash generation ($4.1B FCF) supports $5B buyback program and 10% dividend increase.",
    "recommendation": "BUY",
    "confidence_score": 0.82
  }
}
```

#### 8. Processing Metadata (Coordinator Output)
```json
{
  "metadata": {
    "processing_time_seconds": 3.2,
    "llm_tokens_used": 4500,
    "data_quality_score": 0.95,
    "agents_coordination_success": true
  }
}
```

## Agent-to-Output Mapping

### Coordinator Agent
- Validates input report existence and format
- Initializes workflow state
- Manages agent execution sequence
- Produces: `metadata`

### Data Extractor Agent
- Extracts financial metrics (revenue, net income, EPS, margins)
- Analyzes segment performance
- Identifies forward guidance
- Extracts capital allocation plans
- Produces: `financial_metrics`, `segment_performance`, `forward_guidance`, `capital_allocation`

### Sentiment Analysis Agent
- Analyzes CEO commentary tone
- Identifies positive indicators (growth signals, achievements)
- Identifies negative indicators (challenges, risks)
- Produces: `sentiment_analysis`

### Summary Agent
- Consolidates findings from all agents
- Generates executive summary headline
- Produces investment recommendation (BUY/HOLD/SELL)
- Calculates confidence score
- Produces: `executive_summary`

## Using Sample Data for Testing

### Docker Container Testing
When running in Docker, the sample data is available at `/app/data/`:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "report_path": "/app/data/earnings_report_sample.txt",
    "options": {}
  }'
```

### Local Development Testing
When running locally, reference the full path:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "report_path": "app/client/data/earnings_report_sample.txt",
    "options": {}
  }'
```

### Python Test Fixtures
```python
# tests/fixtures/sample_reports.py
import json
from pathlib import Path

def load_sample_report():
    report_path = Path(__file__).parent.parent.parent / "data" / "earnings_report_sample.txt"
    return report_path.read_text()

def load_expected_output():
    output_path = Path(__file__).parent.parent.parent / "data" / "expected_output.json"
    return json.loads(output_path.read_text())

# In tests
async def test_earnings_analysis():
    report = load_sample_report()
    expected = load_expected_output()
    
    result = await process_earnings_report(report, {})
    
    assert result["financial_metrics"]["revenue"]["value"] == expected["financial_metrics"]["revenue"]["value"]
    assert result["sentiment_analysis"]["overall_sentiment"] == expected["sentiment_analysis"]["overall_sentiment"]
```

## Validation Criteria

Use these criteria to validate that agents are processing sample data correctly:

### Financial Metrics Validation
- ✅ Revenue extracted as 15.2 billion USD
- ✅ Net income as 3.8 billion USD  
- ✅ EPS as 4.52 (beats 4.30 estimate)
- ✅ Operating margin as 28.5%
- ✅ All YoY growth rates calculated correctly

### Segment Performance Validation
- ✅ Cloud Services: $6.8B revenue with 35% growth
- ✅ Software Products: $5.1B revenue with 8% growth
- ✅ Hardware: $3.3B revenue with -2% growth
- ✅ Retention rates and customer counts extracted

### Sentiment Analysis Validation
- ✅ Overall sentiment identified as "positive"
- ✅ Confidence score >= 0.80
- ✅ At least 3 positive indicators identified
- ✅ At least 3 risk factors identified
- ✅ Management tone captured as "optimistic_cautious"

### Executive Summary Validation
- ✅ Headline captures key themes
- ✅ Recommendation in [BUY, HOLD, SELL]
- ✅ Confidence score between 0.0 and 1.0
- ✅ Summary mentions cloud and AI growth

## Extending Sample Data

To create additional test cases:

1. **Copy the sample files**:
   ```bash
   cp app/client/data/earnings_report_sample.txt app/client/data/earnings_report_q4_2024.txt
   ```

2. **Modify the report** with different metrics:
   - Different financial figures
   - Different sentiment indicators
   - Different risk factors
   - Different industry/company specifics

3. **Generate expected output** by running the full analysis:
   ```bash
   docker-compose exec earnings-analyzer curl -X POST http://localhost:8000/analyze \
     -H "Content-Type: application/json" \
     -d '{"report_path": "/app/data/earnings_report_q4_2024.txt"}'
   ```

4. **Save the output** as a reference:
   ```bash
   # Output will serve as your new expected_output.json
   ```

## Notes

- Sample data reflects realistic earnings report structure
- All financial values are illustrative (not based on real TechCorp data)
- Expected output demonstrates full multi-agent coordination
- Processing time shown (3.2 seconds) is typical for local execution
- Token usage (4500) is approximate and varies with LLM

