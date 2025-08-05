#!/usr/bin/env python3
"""
Auto-Tagging Script for Markdown Documents
Scans markdown files for data engineering keywords and generates tags.
Creates both tag.md file and SQLite database for storage.
"""

import os
import re
import sqlite3
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AutoTagger:
    """Auto-tagging system for markdown documents"""
    
    def __init__(self, scan_path: str, db_path: str = "tags.db"):
        self.scan_path = Path(scan_path)
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        
        # Data Engineering specific keywords and tags
        self.tag_keywords = {
            "#data-warehouse": [
                "data warehouse", "datawarehouse", "snowflake", "bigquery", "redshift", 
                "databricks", "synapse", "warehouse", "dimensional modeling", "star schema",
                "fact table", "dimension table", "etl", "elt", "data vault"
            ],
            "#data-pipeline": [
                "data pipeline", "pipeline", "airflow", "dag", "workflow", "orchestration",
                "scheduler", "cron", "batch processing", "stream processing", "dataflow",
                "glue", "step functions", "prefect", "dagster"
            ],
            "#big-data": [
                "big data", "hadoop", "spark", "mapreduce", "hdfs", "yarn", "kafka",
                "distributed computing", "cluster", "scalability", "parallel processing",
                "flink", "storm", "beam"
            ],
            "#cloud-platform": [
                "aws", "gcp", "azure", "cloud", "s3", "gcs", "blob storage", "lambda",
                "cloud functions", "emr", "dataproc", "data factory", "kinesis", "pub/sub"
            ],
            "#database": [
                "database", "sql", "nosql", "postgresql", "mysql", "mongodb", "cassandra",
                "dynamodb", "redis", "elasticsearch", "rdbms", "oltp", "olap"
            ],
            "#analytics": [
                "analytics", "bi", "business intelligence", "dashboard", "reporting",
                "tableau", "power bi", "looker", "superset", "metrics", "kpi",
                "data visualization", "charts"
            ],
            "#ml-ai": [
                "machine learning", "ml", "artificial intelligence", "ai", "model",
                "training", "inference", "tensorflow", "pytorch", "scikit-learn",
                "feature engineering", "mlops", "sagemaker"
            ],
            "#data-quality": [
                "data quality", "data governance", "validation", "testing", "monitoring",
                "anomaly detection", "data lineage", "catalog", "metadata", "profiling",
                "great expectations", "monte carlo"
            ],
            "#streaming": [
                "streaming", "real-time", "kafka", "kinesis", "pubsub", "event streaming",
                "stream processing", "flink", "spark streaming", "windowing", "watermark"
            ],
            "#infrastructure": [
                "infrastructure", "terraform", "docker", "kubernetes", "container",
                "devops", "ci/cd", "deployment", "monitoring", "observability",
                "infrastructure as code", "iac"
            ],
            "#data-engineering-fundamentals": [
                "data engineering", "data engineer", "data architecture", "data modeling",
                "data integration", "data ingestion", "data processing", "data storage",
                "data lifecycle", "data strategy"
            ]
        }
        
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with required tables"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # Create tables
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    title TEXT,
                    word_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS document_tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER,
                    tag_id INTEGER,
                    relevance_score REAL DEFAULT 1.0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (document_id) REFERENCES documents (id),
                    FOREIGN KEY (tag_id) REFERENCES tags (id),
                    UNIQUE(document_id, tag_id)
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag_id INTEGER,
                    keyword TEXT NOT NULL,
                    weight REAL DEFAULT 1.0,
                    FOREIGN KEY (tag_id) REFERENCES tags (id)
                )
            ''')
            
            # Insert predefined tags and keywords
            self.insert_predefined_tags()
            
            self.conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
            
        except sqlite3.Error as e:
            logger.error(f"Database initialization error: {e}")
    
    def insert_predefined_tags(self):
        """Insert predefined tags and keywords into database"""
        for tag_name, keywords in self.tag_keywords.items():
            # Insert tag
            self.cursor.execute(
                "INSERT OR IGNORE INTO tags (name, description) VALUES (?, ?)",
                (tag_name, f"Auto-generated tag for {tag_name}")
            )
            
            # Get tag ID
            tag_id = self.cursor.execute(
                "SELECT id FROM tags WHERE name = ?", (tag_name,)
            ).fetchone()[0]
            
            # Insert keywords
            for keyword in keywords:
                self.cursor.execute(
                    "INSERT OR IGNORE INTO keywords (tag_id, keyword, weight) VALUES (?, ?, ?)",
                    (tag_id, keyword.lower(), 1.0)
                )
    
    def scan_markdown_files(self) -> List[Path]:
        """Scan for markdown files in the specified path"""
        markdown_files = list(self.scan_path.rglob("*.md"))
        logger.info(f"Found {len(markdown_files)} markdown files")
        return markdown_files
    
    def extract_title(self, content: str) -> str:
        """Extract title from markdown content"""
        # Look for first h1 heading
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # Fallback to filename
        return "Untitled"
    
    def analyze_content(self, content: str, file_path: str) -> Dict[str, float]:
        """Analyze content and return tags with relevance scores"""
        content_lower = content.lower()
        tags_found = {}
        
        # Get all tags and their keywords from database
        self.cursor.execute('''
            SELECT t.name, k.keyword, k.weight 
            FROM tags t 
            JOIN keywords k ON t.id = k.tag_id
        ''')
        
        tag_keywords = {}
        for tag_name, keyword, weight in self.cursor.fetchall():
            if tag_name not in tag_keywords:
                tag_keywords[tag_name] = []
            tag_keywords[tag_name].append((keyword, weight))
        
        # Calculate relevance scores
        for tag_name, keywords in tag_keywords.items():
            score = 0.0
            matches = 0
            
            for keyword, weight in keywords:
                keyword_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', content_lower))
                if keyword_count > 0:
                    score += keyword_count * weight
                    matches += keyword_count
            
            if matches > 0:
                # Normalize score based on document length
                doc_length = len(content.split())
                normalized_score = min(score / (doc_length / 100), 1.0)
                tags_found[tag_name] = normalized_score
        
        return tags_found
    
    def process_file(self, file_path: Path) -> Dict:
        """Process a single markdown file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            title = self.extract_title(content)
            word_count = len(content.split())
            tags = self.analyze_content(content, str(file_path))
            
            # Store in database
            self.store_document(file_path, title, word_count, tags)
            
            return {
                'file_path': str(file_path),
                'title': title,
                'word_count': word_count,
                'tags': tags
            }
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None
    
    def store_document(self, file_path: Path, title: str, word_count: int, tags: Dict[str, float]):
        """Store document and its tags in database"""
        try:
            # Insert document
            self.cursor.execute('''
                INSERT OR REPLACE INTO documents (file_path, title, word_count)
                VALUES (?, ?, ?)
            ''', (str(file_path), title, word_count))
            
            document_id = self.cursor.execute(
                "SELECT id FROM documents WHERE file_path = ?", (str(file_path),)
            ).fetchone()[0]
            
            # Insert document tags
            for tag_name, score in tags.items():
                tag_id = self.cursor.execute(
                    "SELECT id FROM tags WHERE name = ?", (tag_name,)
                ).fetchone()[0]
                
                self.cursor.execute('''
                    INSERT OR REPLACE INTO document_tags (document_id, tag_id, relevance_score)
                    VALUES (?, ?, ?)
                ''', (document_id, tag_id, score))
            
            self.conn.commit()
            
        except sqlite3.Error as e:
            logger.error(f"Database storage error: {e}")
    
    def generate_tag_md(self, output_path: str = "tags.md"):
        """Generate tags.md file with document listings"""
        try:
            # Get all tags with their documents
            self.cursor.execute('''
                SELECT t.name, d.file_path, d.title, dt.relevance_score
                FROM tags t
                JOIN document_tags dt ON t.id = dt.tag_id
                JOIN documents d ON dt.document_id = d.id
                ORDER BY t.name, dt.relevance_score DESC
            ''')
            
            tag_documents = {}
            for tag_name, file_path, title, score in self.cursor.fetchall():
                if tag_name not in tag_documents:
                    tag_documents[tag_name] = []
                tag_documents[tag_name].append((file_path, title, score))
            
            # Generate markdown content
            md_content = ["# Document Tags\n"]
            md_content.append("Auto-generated tags for data engineering documents.\n")
            
            for tag_name in sorted(tag_documents.keys()):
                documents = tag_documents[tag_name]
                md_content.append(f"## {tag_name}")
                md_content.append(f"Found in {len(documents)} documents\n")
                
                for file_path, title, score in documents:
                    # Convert absolute path to relative path
                    rel_path = os.path.relpath(file_path, self.scan_path)
                    md_content.append(f"- [{title}]({rel_path}) (relevance: {score:.2f})")
                
                md_content.append("")
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(md_content))
            
            logger.info(f"Generated {output_path}")
            
        except Exception as e:
            logger.error(f"Error generating tags.md: {e}")
    
    def run(self):
        """Run the complete auto-tagging process"""
        logger.info("Starting auto-tagging process...")
        
        # Scan markdown files
        markdown_files = self.scan_markdown_files()
        
        # Process each file
        processed_count = 0
        for file_path in markdown_files:
            result = self.process_file(file_path)
            if result:
                processed_count += 1
                logger.info(f"Processed: {file_path.name} - Tags: {list(result['tags'].keys())}")
        
        # Generate tags.md
        self.generate_tag_md()
        
        # Generate summary
        self.cursor.execute('SELECT COUNT(*) FROM documents')
        total_docs = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM tags')
        total_tags = self.cursor.fetchone()[0]
        
        self.cursor.execute('SELECT COUNT(*) FROM document_tags')
        total_taggings = self.cursor.fetchone()[0]
        
        logger.info(f"Completed! Processed {processed_count} files")
        logger.info(f"Total documents: {total_docs}")
        logger.info(f"Total tags: {total_tags}")
        logger.info(f"Total tag assignments: {total_taggings}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(description="Auto-tag markdown documents for data engineering")
    parser.add_argument("path", help="Path to scan for markdown files")
    parser.add_argument("--db", default="tags.db", help="SQLite database path (default: tags.db)")
    parser.add_argument("--output", default="tags.md", help="Output markdown file (default: tags.md)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        logger.error(f"Path does not exist: {args.path}")
        return
    
    tagger = AutoTagger(args.path, args.db)
    try:
        tagger.run()
    finally:
        tagger.close()


if __name__ == "__main__":
    main()