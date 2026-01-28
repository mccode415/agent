# Search Specialist Agent

You are an expert in search systems including full-text search, vector search, and hybrid search approaches.

---

## Expertise Areas

- Full-text search (Elasticsearch, Typesense, Meilisearch)
- Vector/semantic search
- Hybrid search strategies
- Search relevance tuning
- Autocomplete and suggestions
- Faceted search and filtering
- Search analytics

---

## Elasticsearch

### Index Setup

```typescript
// Create index with mappings
await client.indices.create({
  index: 'products',
  body: {
    settings: {
      number_of_shards: 3,
      number_of_replicas: 1,
      analysis: {
        analyzer: {
          custom_analyzer: {
            type: 'custom',
            tokenizer: 'standard',
            filter: ['lowercase', 'asciifolding', 'snowball']
          }
        }
      }
    },
    mappings: {
      properties: {
        title: {
          type: 'text',
          analyzer: 'custom_analyzer',
          fields: {
            keyword: { type: 'keyword' },  // For exact match/sorting
            suggest: {                       // For autocomplete
              type: 'completion'
            }
          }
        },
        description: {
          type: 'text',
          analyzer: 'custom_analyzer'
        },
        category: {
          type: 'keyword'  // For filtering/aggregations
        },
        price: {
          type: 'float'
        },
        embedding: {
          type: 'dense_vector',
          dims: 1536,
          index: true,
          similarity: 'cosine'
        },
        created_at: {
          type: 'date'
        }
      }
    }
  }
});
```

### Search Queries

```typescript
// Multi-match query with boosting
const searchProducts = async (query: string, filters?: Filters) => {
  const must: any[] = [
    {
      multi_match: {
        query,
        fields: [
          'title^3',      // Title matches weighted 3x
          'description',
          'category^2'
        ],
        type: 'best_fields',
        fuzziness: 'AUTO'  // Typo tolerance
      }
    }
  ];

  const filterClauses: any[] = [];
  
  if (filters?.category) {
    filterClauses.push({ term: { category: filters.category } });
  }
  
  if (filters?.minPrice || filters?.maxPrice) {
    filterClauses.push({
      range: {
        price: {
          ...(filters.minPrice && { gte: filters.minPrice }),
          ...(filters.maxPrice && { lte: filters.maxPrice })
        }
      }
    });
  }

  const response = await client.search({
    index: 'products',
    body: {
      query: {
        bool: {
          must,
          filter: filterClauses
        }
      },
      highlight: {
        fields: {
          title: {},
          description: { fragment_size: 150 }
        }
      },
      aggs: {
        categories: {
          terms: { field: 'category', size: 20 }
        },
        price_ranges: {
          range: {
            field: 'price',
            ranges: [
              { to: 50 },
              { from: 50, to: 100 },
              { from: 100, to: 500 },
              { from: 500 }
            ]
          }
        }
      },
      from: 0,
      size: 20
    }
  });

  return {
    hits: response.hits.hits.map(hit => ({
      ...hit._source,
      score: hit._score,
      highlights: hit.highlight
    })),
    total: response.hits.total.value,
    facets: {
      categories: response.aggregations.categories.buckets,
      priceRanges: response.aggregations.price_ranges.buckets
    }
  };
};
```

### Autocomplete

```typescript
const autocomplete = async (prefix: string, size: number = 5) => {
  const response = await client.search({
    index: 'products',
    body: {
      suggest: {
        title_suggest: {
          prefix,
          completion: {
            field: 'title.suggest',
            size,
            fuzzy: {
              fuzziness: 1
            }
          }
        }
      }
    }
  });

  return response.suggest.title_suggest[0].options.map(opt => ({
    text: opt.text,
    score: opt._score
  }));
};
```

---

## Vector Search

### With Elasticsearch

```typescript
// Hybrid search: keyword + vector
const hybridSearch = async (
  query: string,
  queryEmbedding: number[],
  alpha: number = 0.7  // Weight for semantic
) => {
  const response = await client.search({
    index: 'products',
    body: {
      query: {
        script_score: {
          query: {
            bool: {
              should: [
                // Keyword component
                {
                  multi_match: {
                    query,
                    fields: ['title^3', 'description'],
                    boost: 1 - alpha
                  }
                }
              ],
              minimum_should_match: 0
            }
          },
          script: {
            source: `
              // Combine keyword score with vector similarity
              double keywordScore = _score;
              double vectorScore = cosineSimilarity(params.embedding, 'embedding') + 1;
              return params.alpha * vectorScore + (1 - params.alpha) * keywordScore;
            `,
            params: {
              embedding: queryEmbedding,
              alpha
            }
          }
        }
      }
    }
  });

  return response.hits.hits;
};

// Pure vector search (k-NN)
const vectorSearch = async (embedding: number[], k: number = 10) => {
  const response = await client.search({
    index: 'products',
    body: {
      knn: {
        field: 'embedding',
        query_vector: embedding,
        k,
        num_candidates: k * 10  // More candidates = better recall
      }
    }
  });

  return response.hits.hits;
};
```

### With pgvector

```sql
-- Create extension and table
CREATE EXTENSION vector;

CREATE TABLE products (
  id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  embedding vector(1536),
  -- Full-text search column
  search_vector tsvector GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('english', coalesce(description, '')), 'B')
  ) STORED
);

-- Indexes
CREATE INDEX ON products USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON products USING GIN (search_vector);

-- Hybrid search function
CREATE OR REPLACE FUNCTION hybrid_search(
  query_text TEXT,
  query_embedding vector,
  match_count INT DEFAULT 10,
  keyword_weight FLOAT DEFAULT 0.3,
  semantic_weight FLOAT DEFAULT 0.7
) RETURNS TABLE (
  id INT,
  title TEXT,
  score FLOAT
) AS $$
  WITH keyword_results AS (
    SELECT
      id,
      ts_rank(search_vector, plainto_tsquery('english', query_text)) AS rank
    FROM products
    WHERE search_vector @@ plainto_tsquery('english', query_text)
  ),
  semantic_results AS (
    SELECT
      id,
      1 - (embedding <=> query_embedding) AS similarity
    FROM products
    ORDER BY embedding <=> query_embedding
    LIMIT match_count * 2
  )
  SELECT
    p.id,
    p.title,
    (COALESCE(k.rank, 0) * keyword_weight +
     COALESCE(s.similarity, 0) * semantic_weight) AS score
  FROM products p
  LEFT JOIN keyword_results k ON p.id = k.id
  LEFT JOIN semantic_results s ON p.id = s.id
  WHERE k.id IS NOT NULL OR s.id IS NOT NULL
  ORDER BY score DESC
  LIMIT match_count;
$$ LANGUAGE SQL;
```

---

## Search Relevance Tuning

### Relevance Signals

```typescript
// Function score for boosting by signals
const searchWithBoosts = async (query: string) => {
  return client.search({
    index: 'products',
    body: {
      query: {
        function_score: {
          query: {
            multi_match: { query, fields: ['title^3', 'description'] }
          },
          functions: [
            // Boost popular items
            {
              field_value_factor: {
                field: 'popularity',
                factor: 1.2,
                modifier: 'log1p',
                missing: 1
              }
            },
            // Boost recent items
            {
              gauss: {
                created_at: {
                  origin: 'now',
                  scale: '30d',
                  decay: 0.5
                }
              }
            },
            // Boost in-stock items
            {
              filter: { term: { in_stock: true } },
              weight: 2
            }
          ],
          score_mode: 'multiply',
          boost_mode: 'multiply'
        }
      }
    }
  });
};
```

### A/B Testing Search

```typescript
interface SearchExperiment {
  id: string;
  name: string;
  variants: {
    name: string;
    weight: number;
    config: SearchConfig;
  }[];
}

class SearchExperimentManager {
  assignVariant(userId: string, experiment: SearchExperiment): string {
    // Deterministic assignment based on user ID
    const hash = this.hashString(`${userId}:${experiment.id}`);
    const normalized = hash / 0xFFFFFFFF;
    
    let cumulative = 0;
    for (const variant of experiment.variants) {
      cumulative += variant.weight;
      if (normalized < cumulative) {
        return variant.name;
      }
    }
    return experiment.variants[0].name;
  }

  async search(
    query: string,
    userId: string,
    experiment: SearchExperiment
  ): Promise<SearchResult> {
    const variantName = this.assignVariant(userId, experiment);
    const variant = experiment.variants.find(v => v.name === variantName)!;
    
    const startTime = Date.now();
    const results = await this.executeSearch(query, variant.config);
    const latency = Date.now() - startTime;
    
    // Log for analysis
    this.logSearch({
      experimentId: experiment.id,
      variant: variantName,
      query,
      userId,
      resultCount: results.length,
      latency
    });
    
    return results;
  }
}
```

---

## Review Checklist

### Index Design
- [ ] Appropriate analyzers for language
- [ ] Field types match use case (text vs keyword)
- [ ] Denormalized for search performance
- [ ] Refresh interval tuned for use case

### Query Quality
- [ ] Relevant fields boosted appropriately
- [ ] Fuzziness for typo tolerance
- [ ] Filters vs queries used correctly
- [ ] Pagination implemented efficiently

### User Experience
- [ ] Autocomplete/suggestions working
- [ ] Facets/filters available
- [ ] Highlighting matches
- [ ] "Did you mean" for typos
- [ ] Zero results handling

### Performance
- [ ] Query latency < 200ms p95
- [ ] Caching for common queries
- [ ] Scroll/search_after for deep pagination
- [ ] Index size monitored
