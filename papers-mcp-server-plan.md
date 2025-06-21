# Academic Papers MCP Server - Design Plan

## Overview
An MCP server that fetches relevant academic papers based on various criteria, functioning as a customized RSS feed for research. This server will integrate with Zotero for intelligent paper recommendations and collection management.

## Project Context
- **Target User:** Researcher in neuroscience + AI intersection
- **Problem:** Current RSS feeds (arXiv cs.LG, bioRxiv, Nature, etc.) are too broad and noisy
- **Goal:** Replace RSS feeds entirely with intelligent, personalized paper discovery
- **Key Innovation:** Leverage existing Zotero library to bootstrap personalization and identify knowledge gaps

## Requirements Gathered

### Data Sources ✓
**Primary Sources:**
- arXiv (focus on cs.LG and related AI/ML categories)
- bioRxiv (neuroscience papers)
- PubMed (medical/neuroscience literature)
- Semantic Scholar (cross-domain academic search)
- Google Scholar (comprehensive coverage)

**User Context:**
- Field: Neuroscience + AI intersection
- Current workflow: RSS feeds from broad sources (too much noise)
- Goal: Replace RSS feeds entirely with intelligent filtering

### Use Cases ✓
1. **Daily/Weekly Digests:** Curated recent papers relevant to user's interests
2. **Specific Queries:** Ad-hoc searches for:
   - Latest papers on specific topics
   - Review papers for understanding field evolution
   - Seminal/foundational papers in a domain
3. **Smart Filtering:** Reduce noise from broad journal subscriptions

## Remaining Questions for Design

### Smart Filtering Strategy
- **How would you define "relevant"?** 
  - Specific neuroscience subfields? (computational neuroscience, neuroimaging, etc.)
  - AI techniques of interest? (deep learning, reinforcement learning, etc.)
  - Intersection topics? (neural networks, brain-inspired AI, etc.)
- **Should we use citation metrics** to filter high-impact papers?
- **Author preferences?** Track papers from specific researchers you follow?

### Digest Configuration
- **Frequency:** Daily, weekly, or configurable?
- **Volume:** How many papers per digest? (5, 10, 20?)
- **Diversity vs Focus:** Mix of different topics or deep focus on core interests?

### Query Types & Intelligence
- **Historical/Review queries:** How should we identify and rank review papers vs original research?
- **Semantic understanding:** Should "neural plasticity" also surface "synaptic plasticity" papers?
- **Cross-domain connections:** Flag papers that bridge neuroscience and AI?

### Output & Integration ✓
- **Reference Manager:** Zotero integration (existing MCP available)
- **Zotero Enhancement Ideas:**
  - Analyze existing library to suggest missing key papers
  - Find related papers based on current collection
  - Identify citation gaps in research areas
  - Recommend foundational papers for topics you're exploring
- **Note-taking:** Potential Obsidian integration
- **Paper Recommendations:** Based on Zotero library analysis

## Technical Considerations
- **API Rate Limits:** arXiv (3 requests/sec), Semantic Scholar (100 requests/sec), PubMed (10 requests/sec)
- **Caching Strategy:** Store paper metadata locally to avoid repeated API calls
- **Relevance Scoring:** Combine keyword matching, citation metrics, and author reputation
- **Zotero Integration:** 
  - Use existing Zotero MCP or Zotero API for library analysis
  - Extract keywords, authors, journals from current collection
  - Build user interest profile from existing papers
  - **Present recommendations only** (no auto-adding to Zotero)
- **Citation Network Analysis:** Use Semantic Scholar's citation data to find gaps
- **Learning System:**
  - Track user feedback (accept/reject/ignore recommendations)
  - Adjust future suggestions based on patterns
  - Build negative preference model from rejected papers
- **Collection Intelligence:**
  - Analyze paper topics using NLP/embeddings
  - Suggest optimal collection organization
  - Handle cross-collection papers appropriately
- **Configurable Aggressiveness:** User-adjustable thresholds for recommendation sensitivity
- **Update Frequency:** Balance between freshness and API quota usage
- **Error Handling:** Graceful degradation when APIs are unavailable
- **Data Storage:** SQLite for paper metadata, user preferences, and Zotero analysis cache

## Proposed MCP Tools

### Core Search & Discovery
1. `search_papers` - Ad-hoc search with filters (query, authors, date range, paper type)
2. `get_digest` - Generate personalized daily/weekly paper digest
3. `get_reviews` - Find review papers for a topic
4. `get_seminal_papers` - Find foundational papers in a field

### Zotero-Enhanced Features
5. `analyze_zotero_library` - Analyze current Zotero collection for patterns/gaps
6. `suggest_missing_papers` - Recommend key papers missing from your collection (adjustable aggressiveness)
7. `find_related_papers` - Find papers related to specific items in your Zotero library
8. `identify_citation_gaps` - Find highly-cited papers you should know about in your field
9. `recommend_foundation_papers` - Suggest seminal papers for new topics you're exploring

### Smart Organization & Collections
10. `suggest_collections` - Recommend new Zotero collections based on paper topics
11. `categorize_paper` - Suggest which existing collections a paper belongs to
12. `organize_papers` - Sort papers across multiple collections intelligently
13. `detect_research_themes` - Identify emerging themes in your research for new collections

### Configuration & Learning
14. `configure_interests` - Set user preferences and aggressiveness levels
15. `mark_paper_status` - Mark papers as read/saved/rejected/interesting for learning system
16. `get_learning_insights` - Show what the system has learned about your preferences

## Implementation Workflow Examples

### Smart Collection Management
```
User: "I have a paper on 'neural plasticity in deep learning'"
System: 
- Suggests: "Neuroscience" + "Machine Learning" collections
- Detects emerging theme: "Bio-inspired AI" → suggests new collection
- Shows similar papers already in library for context
```

### Learning from Feedback
```
User rejects papers on "computational psychiatry" repeatedly
System learns: 
- Reduces clinical/medical neuroscience suggestions
- Focuses more on computational methods and theory
- Adjusts aggressiveness down for medical applications
```

### Adaptive Recommendations
```
Aggressiveness Settings:
- Conservative: Only highly-cited papers (>100 citations)
- Balanced: Mix of established + emerging work  
- Aggressive: Include recent preprints and niche topics
```

## Next Steps
1. **Initial Implementation Focus:**
   - Core search functionality (`search_papers`, `get_digest`)
   - Basic Zotero integration (`analyze_zotero_library`)
   - Simple learning system (`mark_paper_status`)

2. **Advanced Features (Phase 2):**
   - Collection management tools
   - Sophisticated learning algorithms
   - Cross-domain intelligence

3. **Technical Decisions:**
   - Choose primary API (Semantic Scholar recommended for citation data)
   - Design learning system architecture
   - Define MCP server interface schema

## Important Implementation Notes

### API Priorities & Rationale
1. **Semantic Scholar** - Primary API for citation networks and cross-references
2. **arXiv** - Essential for CS/ML preprints (cs.LG, cs.AI, cs.NE categories)
3. **bioRxiv** - Critical for neuroscience preprints
4. **PubMed** - Medical/biological literature
5. **Google Scholar** - Fallback for comprehensive coverage

### Zotero Integration Strategy
- **Existing MCP:** There's already a Zotero MCP server available
- **Enhancement Approach:** Build complementary server that analyzes Zotero data
- **API Access:** Use Zotero Web API for library analysis (requires user API key)
- **Privacy:** All analysis should be local; don't send full library to external services

### Learning System Architecture
```
User Feedback → Local SQLite DB → Preference Vectors → API Query Adjustment
                                ↓
                         Negative Preference Model (what to avoid)
```

### Critical Design Decisions Made
- **No auto-adding to Zotero** - Present recommendations only
- **Adjustable aggressiveness** - User controls recommendation sensitivity  
- **Multi-collection support** - Papers can belong to multiple collections
- **Learning from rejections** - Build negative preference model
- **Present-only workflow** - Don't automatically modify user's Zotero library

### Performance Considerations
- **Rate Limiting:** Respect API limits (arXiv: 3/sec, Semantic Scholar: 100/sec)
- **Caching Strategy:** Cache paper metadata locally to minimize API calls
- **Batch Processing:** Process multiple papers in single API calls when possible
- **Background Updates:** Run digest generation as background tasks

### Future Extension Points
- **Obsidian Integration:** Link to existing Obsidian MCP for note-taking workflow
- **Citation Alerts:** Notify when your papers get cited
- **Collaboration Features:** Share collections or recommendations with colleagues
- **Journal Impact Integration:** Include journal rankings in recommendations

## File Location
This document is located at: `/Users/hlee/Desktop/admin/playgrounds/obsidian_fastmcp/papers-mcp-server-plan.md`

Created: 2025-06-20
Last Updated: 2025-06-20