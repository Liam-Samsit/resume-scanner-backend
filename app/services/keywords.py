DEFAULT_KEYWORDS = {
    "programming_languages": [
        "python", "java", "c", "c++", "c#", "javascript", "typescript",
        "php", "ruby", "swift", "kotlin", "dart", "go", "rust",
        "scala", "perl", "r", "matlab", "bash", "shell scripting"
    ],

    "frameworks_libraries": [
        "react", "react native", "angular", "vue", "svelte", "jquery",
        "nodejs", "express", "fastapi", "django", "flask", "spring boot",
        "hibernate", "laravel", "symfony", "bootstrap", "tailwind css",
        "material ui", "three.js", "tensorflow", "keras", "pytorch",
        "scikit-learn", "opencv", "pandas", "numpy", "matplotlib", "seaborn"
    ],

    "databases": [
        "sql", "postgresql", "mysql", "sqlite", "mssql", "oracle",
        "mongodb", "cassandra", "redis", "elasticsearch", "dynamodb",
        "neo4j", "couchdb", "firestore", "bigquery"
    ],

    "tools_platforms": [
        "docker", "kubernetes", "jenkins", "github actions", "gitlab ci",
        "travis ci", "circleci", "terraform", "ansible", "vagrant",
        "aws", "azure", "gcp", "cloud computing", "firebase",
        "heroku", "netlify", "vercel", "render", "digitalocean",
        "linux", "unix", "windows server", "bash", "powershell",
        "jira", "trello", "slack", "notion", "figma", "adobe xd",
        "photoshop", "illustrator", "blender", "aseprite"
    ],

    "dev_concepts": [
        "object oriented programming", "functional programming",
        "design patterns", "unit testing", "integration testing",
        "test driven development", "rest api", "graphql",
        "microservices", "monolith architecture", "version control",
        "git", "agile", "scrum", "kanban", "ci/cd", "devops",
        "clean code", "refactoring", "scalability", "performance optimization"
    ],

    "data_ai": [
        "machine learning", "deep learning", "artificial intelligence",
        "data science", "data analysis", "data engineering",
        "big data", "data visualization", "natural language processing",
        "computer vision", "predictive modeling", "recommendation systems",
        "cloud ml", "business intelligence", "etl"
    ],

    "cybersecurity": [
        "penetration testing", "ethical hacking", "network security",
        "application security", "vulnerability assessment",
        "firewalls", "intrusion detection", "siem", "incident response",
        "encryption", "public key infrastructure", "security auditing"
    ],

    "soft_skills": [
        "teamwork", "communication", "leadership", "project management",
        "problem solving", "critical thinking", "time management",
        "adaptability", "creativity", "conflict resolution",
        "negotiation", "decision making", "collaboration",
        "empathy", "work ethic"
    ]
}


# Technical categories have weight 3, Soft skills weigh 1
DEFAULT_WEIGHTS = {}

for category, terms in DEFAULT_KEYWORDS.items():
    if category == "soft_skills":
        DEFAULT_WEIGHTS.update({term: 1 for term in terms})
    else:
        DEFAULT_WEIGHTS.update({term: 3 for term in terms})
