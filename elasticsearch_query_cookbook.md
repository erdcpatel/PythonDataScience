# Elasticsearch Query Cookbook

*Practical examples from Basic to Advanced using the Shakespeare
dataset*

------------------------------------------------------------------------

## 📌 Overview

This document contains practical Elasticsearch queries organized from
**basic to advanced** levels.\
The queries use the **Shakespeare dataset**, which contains fields like
`speaker`, `text_entry`, `play_name`, and `line_number`.

------------------------------------------------------------------------

## 🔧 Basic Operations

### **Cluster and Index Inspection**

``` json
GET _cat/nodes?v
GET _cat/indices?v
```

**Purpose:** Check cluster health and list all indices.

------------------------------------------------------------------------

### **Basic Search**

``` json
GET _search
{
  "query": {
    "match_all": {}
  }
}
```

**Purpose:** Retrieve all documents from all indices.

------------------------------------------------------------------------

## 📊 Query Types

### **1. Term Query**

Use Case: Exact match searches on keyword fields.

``` json
GET shakespeare/_search
{
  "query": {
    "term": {
      "speaker.keyword": {
        "value": "ROMEO"
      }
    }
  }
}
```

💡 *Use `.keyword` for exact matches on analyzed text fields.*

------------------------------------------------------------------------

### **2. Terms Query (Multiple Values)**

``` json
GET shakespeare/_search
{
  "size": 25,
  "query": {
    "terms": {
      "play_name.keyword": [
        "Henry VI Part 1",
        "Henry VI Part 2",
        "Henry VI Part 3"
      ]
    }
  }
}
```

------------------------------------------------------------------------

### **3. Match Query**

``` json
GET shakespeare/_search
{
  "size": 5,
  "query": {
    "match": {
      "text_entry": "London"
    }
  }
}
```

------------------------------------------------------------------------

### **4. Match Phrase Query**

``` json
GET shakespeare/_search
{
  "query": {
    "match_phrase": {
      "text_entry": "O Romeo"
    }
  }
}
```

------------------------------------------------------------------------

## 🧩 Intermediate Queries

### **5. Boolean Query**

``` json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"speaker": "JULIET"}},
        {"match": {"text_entry": "love"}}
      ],
      "must_not": [
        {"match": {"text_entry": "death"}}
      ]
    }
  }
}
```

**Components:**\
- **must** → AND logic\
- **should** → OR logic\
- **must_not** → Exclusion\
- **filter** → Fast, no scoring

------------------------------------------------------------------------

### **6. Multi-field Search**

``` json
GET shakespeare/_search
{
  "query": {
    "multi_match": {
      "query": "king",
      "fields": ["text_entry", "speaker"]
    }
  }
}
```

------------------------------------------------------------------------

### **7. Prefix Query**

``` json
GET shakespeare/_search
{
  "query": {
    "prefix": {
      "speaker.keyword": "HEN"
    }
  }
}
```

------------------------------------------------------------------------

## 📈 Aggregations

### **8. Basic Aggregation --- Terms**

``` json
GET shakespeare/_search
{
  "size": 0,
  "aggs": {
    "speakers_line_count": {
      "terms": {
        "field": "speaker.keyword",
        "size": 10
      }
    }
  }
}
```

📌 *`"size": 0` hides document hits and returns only aggregations.*

------------------------------------------------------------------------

### **9. Nested Aggregations**

``` json
GET shakespeare/_search
{
  "size": 0,
  "aggs": {
    "plays": {
      "terms": {
        "field": "play_name.keyword",
        "size": 5
      },
      "aggs": {
        "speakers": {
          "terms": {
            "field": "speaker.keyword",
            "size": 3
          }
        }
      }
    }
  }
}
```

**Output:** For each play → top 3 speakers.

------------------------------------------------------------------------

## 🚀 Advanced Features

### **10. Phrase Search with Slop**

``` json
GET shakespeare/_search
{
  "query": {
    "match_phrase": {
      "text_entry": {
        "query": "to be or not to be",
        "slop": 3
      }
    }
  }
}
```

📌 *Slop = number of positions words can move.*

------------------------------------------------------------------------

### **11. Filter Context**

``` json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"text_entry": "ghost"}}
      ],
      "filter": [
        {"term": {"speaker.keyword": "HAMLET"}},
        {"term": {"play_name.keyword": "Hamlet"}}
      ]
    }
  }
}
```

⚡ *Filters are cached → fast & no scoring impact.*

------------------------------------------------------------------------

### **12. Highlighting**

``` json
GET shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": "blood"
    }
  },
  "highlight": {
    "fields": {
      "text_entry": {}
    }
  },
  "size": 5
}
```

------------------------------------------------------------------------

### **13. Complex Boolean Logic**

``` json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [
        {"match": {"text_entry": "night"}},
        {"term": {"play_name.keyword": "Romeo and Juliet"}}
      ],
      "should": [
        {"term": {"speaker.keyword": "ROMEO"}},
        {"term": {"speaker.keyword": "JULIET"}}
      ],
      "minimum_should_match": 1
    }
  }
}
```

------------------------------------------------------------------------

### **14. Field Existence Check**

``` json
GET shakespeare/_search
{
  "query": {
    "exists": {
      "field": "line_number"
    }
  }
}
```

------------------------------------------------------------------------

### **15. Script Fields**

``` json
GET shakespeare/_search
{
  "query": {
    "term": {
      "speaker.keyword": "HAMLET"
    }
  },
  "script_fields": {
    "text_length": {
      "script": {
        "source": "doc['text_entry.keyword'].value.length()"
      }
    }
  },
  "size": 5
}
```

------------------------------------------------------------------------

## ✅ End of Document

Happy querying! 🎭
