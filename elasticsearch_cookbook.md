# 📘 Elasticsearch Complete Query Cookbook

This document combines **all Elasticsearch query examples** you provided—Shakespeare dataset, Bank index operations, Employee index operations, CRUD, search, aggregations, update-by-query, and practice tasks.

Duplicates have been removed. Everything is organized cleanly.

---

# 🔧 Basic Operations

## Cluster and Index Inspection
```json
GET _cat/nodes?v
GET _cat/indices?v
```

## Basic Search
```json
GET _search
{
  "query": {
    "match_all": {}
  }
}
```

---

# 🎭 Shakespeare Dataset Queries

## Term Query (Exact Match)
```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "speaker.keyword": { "value": "ROMEO" }
    }
  }
}
```

## Terms Query (Multiple Values)
```json
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

## Match Query
```json
GET shakespeare/_search
{
  "size": 5,
  "query": { "match": { "text_entry": "London" } }
}
```

## Match Phrase Query
```json
GET shakespeare/_search
{
  "query": { "match_phrase": { "text_entry": "O Romeo" } }
}
```

## Boolean Query
```json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "speaker": "JULIET" }},
        { "match": { "text_entry": "love" }}
      ],
      "must_not": [
        { "match": { "text_entry": "death" }}
      ]
    }
  }
}
```

## Multi-field Search
```json
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

## Prefix Query
```json
GET shakespeare/_search
{
  "query": {
    "prefix": { "speaker.keyword": "HEN" }
    }
}
```

## Aggregation – Terms
```json
GET shakespeare/_search
{
  "size": 0,
  "aggs": {
    "speakers_line_count": {
      "terms": { "field": "speaker.keyword", "size": 10 }
    }
  }
}
```

## Aggregation – Nested
```json
GET shakespeare/_search
{
  "size": 0,
  "aggs": {
    "plays": {
      "terms": { "field": "play_name.keyword", "size": 5 },
      "aggs": {
        "speakers": {
          "terms": { "field": "speaker.keyword", "size": 3 }
        }
      }
    }
  }
}
```

## Phrase Query With Slop
```json
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

## Filter Context
```json
GET shakespeare/_search
{
  "query": {
    "bool": {
      "must": [{ "match": { "text_entry": "ghost" }}],
      "filter": [
        { "term": { "speaker.keyword": "HAMLET" }},
        { "term": { "play_name.keyword": "Hamlet" }}
      ]
    }
  }
}
```

## Highlighting
```json
GET shakespeare/_search
{
  "query": { "match": { "text_entry": "blood" }},
  "highlight": { "fields": { "text_entry": {} }},
  "size": 5
}
```

## Field Exists Query
```json
GET shakespeare/_search
{
  "query": { "exists": { "field": "line_number" }}
}
```

## Script Fields
```json
GET shakespeare/_search
{
  "query": { "term": { "speaker.keyword": "HAMLET" }},
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

---

# 🏦 Bank Index — CRUD + Search + Bulk + Tasks

## Get Document
```json
GET bank/_doc/100
```

## Insert Document
```json
PUT bank/_doc/1000
{
  "account_number": 1000,
  "balance": 65536,
  "firstname": "John",
  "lastname": "Doe",
  "age": 23,
  "gender": "M",
  "address": "45 West 27th Street",
  "employer": "Elastic",
  "email": "john@elastic.com",
  "city": "New York",
  "state": "NY"
}
```

## Update Document
```json
POST bank/_update/100/
{
  "doc": {
    "address": "1600 Pennsylvania Ave NW",
    "city": "Washington",
    "state": "DC"
  }
}
```

## Delete Document
```json
DELETE bank/_doc/1
```

## Bulk Insert
```json
POST bank/_bulk
{ "index": { "_id": "1003" } }
{ "account_number": 1003, "balance": 42000, "firstname": "Carol", "lastname": "Williams", "age": 42, "gender": "F", "address": "789 Pine Road", "employer": "Health Systems", "email": "carol@health.com", "city": "Seattle", "state": "WA" }
{ "index": { "_id": "1004" } }
{ "account_number": 1004, "balance": 15000, "firstname": "David", "lastname": "Brown", "age": 31, "gender": "M", "address": "321 Elm Street", "employer": "Retail Co", "email": "david@retail.com", "city": "Denver", "state": "CO" }
{ "index": { "_id": "1005" } }
{ "account_number": 1005, "balance": 75000, "firstname": "Eva", "lastname": "Davis", "age": 45, "gender": "F", "address": "654 Maple Drive", "employer": "Consulting Partners", "email": "eva@consulting.com", "city": "Atlanta", "state": "GA" }
```

## Multi-get
```json
GET bank/_mget
{
  "docs": [
    { "_id": "1001" },
    { "_id": "1003" },
    { "_id": "1005" }
  ]
}
```

## Delete by query — low balance
```json
POST bank/_delete_by_query
{
  "query": {
    "range": { "balance": { "lt": 20000 } }
  }
}
```

## Delete by query — multiple conditions
```json
POST bank/_delete_by_query
{
  "query": {
    "bool": {
      "must": [
        { "term": { "state": "NY" }},
        { "range": { "age": { "gt": 20 }}}
      ]
    }
  }
}
```

---

# 🧪 Practice Scenario — Bank System

## Create 5 accounts
(kept exactly as provided)
```json
POST bank/_bulk
{ "index": { "_id": "2001" } }
{ "account_number": 2001, "balance": 35000, "firstname": "Grace", "lastname": "Wilson", "age": 38, "gender": "F", "address": "111 Tech Park", "employer": "Software Inc", "email": "grace@software.com", "city": "San Francisco", "state": "CA", "account_type": "business" }
{ "index": { "_id": "2002" } }
{ "account_number": 2002, "balance": 12000, "firstname": "Henry", "lastname": "Taylor", "age": 25, "gender": "M", "address": "222 Startup Ave", "employer": "Innovation Labs", "email": "henry@innovation.com", "city": "Portland", "state": "OR", "account_type": "student" }
{ "index": { "_id": "2003" } }
{ "account_number": 2003, "balance": 85000, "firstname": "Ivy", "lastname": "Anderson", "age": 52, "gender": "F", "address": "333 Executive Blvd", "employer": "Corporate Solutions", "email": "ivy@corporate.com", "city": "New York", "state": "NY", "account_type": "premium" }
{ "index": { "_id": "2004" } }
{ "account_number": 2004, "balance": 5000, "firstname": "Jack", "lastname": "Thomas", "age": 22, "gender": "M", "address": "444 College Street", "employer": "University", "email": "jack@university.edu", "city": "Madison", "state": "WI", "account_type": "student" }
{ "index": { "_id": "2005" } }
{ "account_number": 2005, "balance": 45000, "firstname": "Karen", "lastname": "Jackson", "age": 41, "gender": "F", "address": "555 Professional Drive", "employer": "Legal Associates", "email": "karen@legal.com", "city": "Washington", "state": "DC", "account_type": "business" }
```

## Add $100 to student accounts
```json
POST bank/_update_by_query
{
  "query": { "term": { "account_type": "student" }},
  "script": { "source": "ctx._source.balance += 100", "lang": "painless" }
}
```

## Premium accounts in NY
```json
GET bank/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "account_type": "premium" }},
        { "term": { "state": "NY" }}
      ]
    }
  }
}
```

## Delete accounts balance < 10,000
```json
POST bank/_delete_by_query
{
  "query": {
    "range": { "balance": { "lt": 10000 } }
  }
}
```

---

# 👔 Employee Index — CRUD + Bulk + Search + Update

## Insert Employee
```json
PUT employees/_doc/1
{
  "employee_id": "EMP001",
  "first_name": "Sarah",
  "last_name": "Chen",
  "department": "Engineering",
  "position": "Software Engineer",
  "salary": 95000,
  "hire_date": "2022-03-15",
  "skills": ["Java", "Python", "Elasticsearch"],
  "active": true,
  "manager_id": "MGR001"
}
```

## Bulk Insert Employees
```json
POST employees/_bulk
{ "index": { "_id": "2" }}
{ "employee_id": "EMP002", "first_name": "Mike", "last_name": "Rodriguez", "department": "Sales", "position": "Sales Manager", "salary": 85000, "hire_date": "2021-07-22", "skills": ["Negotiation", "CRM", "Presentation"], "active": true, "manager_id": "MGR002" }
{ "index": { "_id": "3" }}
{ "employee_id": "EMP003", "first_name": "Lisa", "last_name": "Wang", "department": "Engineering", "position": "DevOps Engineer", "salary": 110000, "hire_date": "2020-11-05", "skills": ["Docker", "Kubernetes", "AWS"], "active": true, "manager_id": "MGR001" }
{ "index": { "_id": "4" }}
{ "employee_id": "EMP004", "first_name": "James", "last_name": "Wilson", "department": "Marketing", "position": "Content Strategist", "salary": 75000, "hire_date": "2023-01-10", "skills": ["SEO", "Content Writing", "Social Media"], "active": true, "manager_id": "MGR003" }
{ "index": { "_id": "5" }}
{ "employee_id": "EMP005", "first_name": "Emily", "last_name": "Davis", "department": "Engineering", "position": "Frontend Developer", "salary": 90000, "hire_date": "2022-09-18", "skills": ["JavaScript", "React", "CSS"], "active": true, "manager_id": "MGR001" }
```

## Update by Query — 10% Raise for Engineers
```json
POST employees/_update_by_query
{
  "query": { "term": { "department": "Engineering" }},
  "script": { "source": "ctx._source.salary *= 1.10", "lang": "painless" }
}
```

## Add New Skill
```json
POST employees/_update/3
{
  "doc": {
    "skills": ["Docker", "Kubernetes", "AWS", "Terraform"]
  }
}
```

## Change Department & Position
```json
POST employees/_update/2
{
  "doc": {
    "department": "Business Development",
    "position": "Business Development Manager",
    "salary": 95000
  }
}
```

## Find Engineers With Salary > 100000
```json
GET employees/_search
{
  "query": {
    "bool": {
      "must": [
        { "term": { "department": "Engineering" }},
        { "range": { "salary": { "gt": 100000 }}}
      ]
    }
  }
}
```

## Search Employees by Skill
```json
GET employees/_search
{
  "query": { "match": { "skills": "AWS" }}
}
```

## Multi-field Search for Management Positions
```json
GET employees/_search
{
  "query": {
    "multi_match": {
      "query": "manager",
      "fields": ["position", "department"]
    }
  }
}
```

---

# ✅ End of Document  
You now have a **complete Elasticsearch cookbook** covering CRUD, search, aggregation, updates, bulk operations, and real-world scenarios.

# Reference:

- Search Data in Elasticsearch - PluralSight
- Execute CRUD Operations in Elasticsearch - PluralSight


