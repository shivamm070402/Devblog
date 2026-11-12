"""
Management command to seed the database with sample blog data.
Usage:  python manage.py seed_data
        python manage.py seed_data --reset   (clears and re-seeds)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Post

# ─────────────────────────────────────────────────────────────
#  System Design posts  (rich content with inline diagrams)
# ─────────────────────────────────────────────────────────────
SD_POSTS = [
    {
        "title": "Load Balancing – Distributing Traffic at Scale",
        "slug": "load-balancing-distributed-traffic",
        "category": "System Design",
        "body": """Load balancing is one of the most fundamental techniques in distributed systems design. It distributes incoming network traffic across multiple servers to ensure no single server becomes a bottleneck.

WHY LOAD BALANCING?

Without a load balancer, a single application server handles every request. As traffic grows, the server becomes overwhelmed. Load balancers solve this by acting as a reverse proxy that sits in front of a pool of servers.

KEY LOAD BALANCING ALGORITHMS

1. Round Robin – requests distributed sequentially to each server in turn. Simple and effective when servers have equal capacity.

2. Least Connections – routes each new request to the server with the fewest active connections. Best when requests vary significantly in processing time.

3. IP Hash – uses the client IP address to determine which server handles the request. Ensures the same client always reaches the same server (session persistence).

4. Weighted Round Robin – servers are assigned weights based on capacity. A server with weight 3 receives 3× more traffic than one with weight 1.

ARCHITECTURE DIAGRAM

┌─────────────────────────────────────────────────────────────┐
│                    CLIENT REQUESTS                           │
│                    ┌──────────┐                              │
│                    │  Client  │                              │
│                    └────┬─────┘                              │
│                         │  HTTP/HTTPS                        │
│                    ┌────▼─────┐                              │
│                    │  Load    │  ← DNS routes to VIP         │
│                    │ Balancer │                               │
│                    └─┬──┬──┬──┘                              │
│            ┌─────────┘  │  └─────────┐                      │
│       ┌────▼────┐  ┌────▼────┐  ┌────▼────┐                 │
│       │Server 1 │  │Server 2 │  │Server 3 │                 │
│       │ (App)   │  │ (App)   │  │ (App)   │                 │
│       └────┬────┘  └────┬────┘  └────┬────┘                 │
│            └────────────┴────────────┘                       │
│                         │                                    │
│                   ┌─────▼──────┐                             │
│                   │  Database  │                             │
│                   └────────────┘                             │
└─────────────────────────────────────────────────────────────┘

TYPES OF LOAD BALANCERS

Layer 4 (Transport Layer) – operates on TCP/UDP packets. Faster but less flexible. Routes based on IP address and port number only.

Layer 7 (Application Layer) – understands HTTP. Can route based on URL path, headers, cookies, or request content. More powerful for microservices.

HEALTH CHECKS

Load balancers continuously probe backend servers. If a server fails to respond within a timeout threshold, the balancer removes it from the rotation automatically. This provides high availability — the system keeps serving traffic even when individual servers fail.

HIGH AVAILABILITY OF THE LOAD BALANCER ITSELF

A single load balancer is a single point of failure. Production systems use:
- Active-Passive: a standby LB takes over via virtual IP (VIP) failover
- Active-Active: multiple LBs share traffic using anycast routing or DNS-based load balancing

Popular tools: Nginx, HAProxy, AWS ELB/ALB, GCP Load Balancer, Cloudflare.

KEY TAKEAWAY

Load balancing is not just about performance. It's about availability, fault tolerance, and the ability to scale horizontally without downtime."""
    },
    {
        "title": "Caching Strategies – Speed Up Every Layer",
        "slug": "caching-strategies-every-layer",
        "category": "System Design",
        "body": """Caching is the practice of storing copies of data in a faster storage layer so future requests for that data can be served more quickly. It is one of the highest-leverage optimizations in system design.

THE CACHING HIERARCHY

Modern systems have multiple cache layers. From fastest to slowest:

L1 CPU Cache (nanoseconds) → L2/L3 Cache → RAM → SSD → HDD → Network

Each layer is 10–1000× slower than the one above it. The goal of application-level caching is to serve as many requests as possible from RAM.

WHERE TO CACHE

1. Client-side caching – browser caches HTML, CSS, JS, and images using HTTP Cache-Control headers. Zero server cost per cached hit.

2. CDN (Content Delivery Network) – geographically distributed edge servers cache static and sometimes dynamic content close to the user. Reduces latency and origin server load.

3. Application-level cache – in-process memory cache (e.g., Python's functools.lru_cache) or a distributed cache like Redis or Memcached.

4. Database query cache – the database itself caches frequent query results. PostgreSQL uses a shared buffer pool.

CACHING STRATEGIES

Cache-Aside (Lazy Loading)
The application checks the cache first. On a miss, it fetches from the database, writes the result to the cache, then returns it. Simple and widely used.

  read(key):
    value = cache.get(key)
    if value is None:
        value = db.query(key)
        cache.set(key, value, ttl=300)
    return value

Write-Through
Every database write is also written to the cache synchronously. Cache is always consistent with the database. Slightly slower writes but reads are always fast.

Write-Behind (Write-Back)
Writes go to the cache immediately and are asynchronously flushed to the database. Faster writes, but risk of data loss if the cache crashes before flushing.

Read-Through
The cache sits in front of the database. The application only talks to the cache. On a miss, the cache fetches from the database itself.

EVICTION POLICIES

When a cache is full, it must evict entries. Common policies:
- LRU (Least Recently Used) – evicts the entry not used for the longest time
- LFU (Least Frequently Used) – evicts the entry accessed least often
- TTL (Time-To-Live) – entries expire after a fixed duration regardless of access

CACHE INVALIDATION

"There are only two hard things in CS: cache invalidation and naming things." – Phil Karlton

Strategies:
1. TTL expiry – let entries expire naturally
2. Event-driven invalidation – when data changes, explicitly delete the cache key
3. Cache versioning – embed a version in the cache key; changing the version effectively invalidates everything

THE THUNDERING HERD PROBLEM

When a cache entry expires, many simultaneous requests hit the database at once. Solutions:
- Request coalescing / mutex lock on cache miss
- Probabilistic early expiration (refresh slightly before TTL expires)
- Background refresh threads

KEY TAKEAWAY

Cache aggressively, but measure first. Use cache-aside for most cases, Redis for distributed systems, and always plan for invalidation from day one."""
    },
    {
        "title": "CAP Theorem – Consistency, Availability, Partition Tolerance",
        "slug": "cap-theorem-consistency-availability-partition",
        "category": "System Design",
        "body": """The CAP Theorem, proven by Eric Brewer in 2000, states that a distributed data store can only guarantee two out of three properties simultaneously: Consistency, Availability, and Partition Tolerance.

THE THREE PROPERTIES

Consistency (C) – Every read receives the most recent write or an error. All nodes see the same data at the same time. This is a strong guarantee.

Availability (A) – Every request receives a non-error response, but it is not guaranteed to contain the most recent data. The system is always up and responsive.

Partition Tolerance (P) – The system continues to operate even when network partitions (message delays or drops between nodes) occur.

WHY YOU MUST CHOOSE P

In any real distributed system, network partitions are unavoidable. Servers crash. Network cables are cut. Cloud regions become temporarily unreachable. This means Partition Tolerance is not optional — it is a given in distributed systems.

The real choice is therefore: when a partition occurs, do you sacrifice Consistency or Availability?

CP SYSTEMS (Consistent + Partition Tolerant)
When a partition happens, the system refuses to respond rather than return potentially stale data. It prioritizes correctness over availability.

Examples: HBase, Zookeeper, MongoDB (with majority write concern), etcd.
Use case: Financial transactions, inventory systems — where stale data causes real harm.

AP SYSTEMS (Available + Partition Tolerant)
When a partition happens, the system returns the best answer it has, even if it may be stale. It prioritizes uptime over consistency.

Examples: Cassandra, DynamoDB (eventual consistency), CouchDB.
Use case: Social feeds, DNS, shopping carts — where temporary inconsistency is acceptable.

BEYOND CAP: THE PACELC MODEL

PACELC extends CAP: even when there is no partition (E = else), there is a tradeoff between Latency (L) and Consistency (C).

- DynamoDB: PA/EL (available during partitions, low latency otherwise)
- PostgreSQL: PC/EC (consistent always, may have higher latency)

EVENTUAL CONSISTENCY IN PRACTICE

AP systems often use eventual consistency — given enough time without new writes, all replicas converge to the same value. Amazon's shopping cart is a classic example: two devices may briefly show different cart contents, but they converge when synced.

Conflict resolution strategies:
- Last-Write-Wins (LWW) – timestamp determines the winner
- Vector clocks – track causal history of updates
- CRDTs (Conflict-free Replicated Data Types) – data structures that merge without conflicts

REAL-WORLD SYSTEM CLASSIFICATIONS

System          | Type | Reason
----------------|------|---------------------------
PostgreSQL      | CP   | ACID transactions, strong consistency
MongoDB         | CP   | Majority write/read concern
Cassandra       | AP   | Leaderless, tunable consistency
DynamoDB        | AP   | Eventually consistent by default
Redis (single)  | CP   | Single-node is always consistent
Redis Cluster   | AP   | Can return stale data during partition
Zookeeper       | CP   | Used for leader election, requires quorum

KEY TAKEAWAY

CAP is a framework for thinking, not a strict prescription. Modern systems like Google Spanner use Paxos consensus to achieve strong consistency with high availability by minimizing partition probability through redundant global network infrastructure."""
    },
    {
        "title": "Database Sharding – Horizontal Scaling Explained",
        "slug": "database-sharding-horizontal-scaling",
        "category": "System Design",
        "body": """Database sharding is a horizontal scaling technique that partitions data across multiple database instances, called shards. Each shard holds a subset of the total data, allowing the system to scale beyond the limits of a single machine.

WHY SHARDING?

A single PostgreSQL instance can typically handle millions of rows and thousands of queries per second. But as data grows to billions of rows and traffic spikes to tens of thousands of QPS, vertical scaling (bigger machine) hits a ceiling. Sharding allows you to distribute both data and query load horizontally.

SHARDING STRATEGIES

1. Range-Based Sharding
Data is partitioned by a continuous range of a shard key. For example, users with IDs 1–1,000,000 go to shard 1; 1,000,001–2,000,000 to shard 2.

  Pros: Simple range queries, natural data locality
  Cons: Hotspots — if most activity is on recent data (like user IDs), one shard gets all the load

2. Hash-Based Sharding
A hash function is applied to the shard key to determine the shard. shard = hash(user_id) % num_shards

  Pros: Even data distribution, eliminates hotspots
  Cons: Range queries require hitting all shards; re-sharding is expensive

3. Directory-Based Sharding
A lookup service (directory) maps each key to its shard. Flexible but the directory itself can become a bottleneck.

4. Geographic Sharding
Data is partitioned by region (US, EU, APAC). Reduces latency for users and helps with data residency compliance (GDPR).

CONSISTENT HASHING

Standard hash sharding breaks when you add or remove shards — all data must be remapped. Consistent hashing places shards on a ring. When a shard is added, only a fraction of keys need to move. Used by DynamoDB, Cassandra, and distributed caches like Memcached.

CHALLENGES OF SHARDING

Cross-shard joins – queries that span multiple shards require application-level join logic or a scatter-gather pattern. Expensive and complex.

Distributed transactions – maintaining ACID properties across shards requires 2-Phase Commit (2PC) or Sagas, both of which add latency and complexity.

Rebalancing – when a shard becomes too large, splitting it means moving large volumes of data with no downtime.

Schema changes – running DDL (ALTER TABLE) across all shards simultaneously is risky and slow.

SHARDING VS PARTITIONING VS REPLICATION

Concept         | What it does                    | Purpose
----------------|----------------------------------|---------------------
Partitioning    | Splits one DB into logical parts | Query performance
Sharding        | Spreads across multiple DB hosts | Horizontal scale
Replication     | Copies data to replica servers   | Availability & reads

WHEN NOT TO SHARD

Sharding adds enormous operational complexity. Before sharding, exhaust these options:
1. Add read replicas for read-heavy workloads
2. Add caching (Redis) to reduce DB load
3. Optimize queries and add proper indexes
4. Upgrade to a larger instance (vertical scaling)
5. Use connection pooling (PgBouncer)

POPULAR TOOLS

- Vitess: horizontal sharding for MySQL (used by YouTube, Slack)
- Citus: sharding extension for PostgreSQL
- PlanetScale: serverless MySQL with Vitess under the hood
- Amazon Aurora: auto-scaling storage, partial sharding built in

KEY TAKEAWAY

Shard only when you have truly exhausted other options. The complexity cost is high. When you do shard, choose your shard key carefully — it determines data distribution and query patterns for the lifetime of the system."""
    },
    {
        "title": "Message Queues & Event-Driven Architecture",
        "slug": "message-queues-event-driven-architecture",
        "category": "System Design",
        "body": """Message queues decouple the components of a distributed system, allowing them to communicate asynchronously. Rather than Service A calling Service B directly (synchronous, tight coupling), A publishes a message to a queue; B reads from the queue at its own pace.

THE CORE PROBLEM: SYNCHRONOUS COUPLING

In a synchronous architecture:
- If Service B is slow, Service A is blocked waiting
- If Service B is down, Service A gets an error
- If Service A produces 10,000 events/second but B processes 1,000/second, messages are lost

Message queues solve all three problems.

KEY CONCEPTS

Producer – the service that sends messages (also called Publisher).
Consumer – the service that receives and processes messages (also called Subscriber).
Queue / Topic – the message buffer that decouples producer from consumer.
Broker – the server that manages queues and routes messages (Kafka, RabbitMQ, SQS).

QUEUE vs TOPIC

Queue (Point-to-Point):
- Each message is consumed by exactly one consumer
- Used for task distribution (work queues)
- Example: order processing, email sending

Topic (Publish-Subscribe):
- Each message is delivered to all subscribers
- Used for event broadcasting
- Example: user signup event consumed by email, analytics, and CRM services simultaneously

DELIVERY GUARANTEES

At-most-once – messages may be lost but never duplicated. Fastest, used for metrics/logs where loss is acceptable.

At-least-once – messages are never lost but may be delivered multiple times. Requires idempotent consumers. Most common in practice.

Exactly-once – messages delivered exactly once. Hardest to achieve. Requires transactions or deduplication IDs. Kafka supports this with idempotent producers.

BACKPRESSURE

If consumers fall behind, the queue grows. Systems handle this by:
- Scaling consumers horizontally (spin up more workers)
- Rate limiting producers
- Using dead-letter queues (DLQ) for failed messages after N retries

EVENT-DRIVEN ARCHITECTURE (EDA)

EDA takes message queues further. The entire system is modeled as a stream of events. Services react to events rather than calling each other.

User signs up → "UserCreated" event published
  → Email Service: send welcome email
  → Analytics Service: record new user metric
  → CRM Service: create contact record
  → Recommendation Service: seed initial recommendations

Benefits: loose coupling, independent scaling, full audit trail (event log).
Challenges: eventual consistency, complex debugging, event schema versioning.

EVENT SOURCING

Instead of storing the current state, store the history of events. The current state is derived by replaying events. Provides complete audit trail and time-travel debugging.

POPULAR MESSAGE BROKERS

Tool         | Best For                              | Key Feature
-------------|---------------------------------------|---------------------------
Apache Kafka | High-throughput event streaming       | Distributed log, replay
RabbitMQ     | Task queues, flexible routing         | AMQP protocol, plugins
AWS SQS      | Managed queue, simple use cases       | Serverless, integrates with Lambda
AWS SNS      | Fan-out pub/sub notifications         | Push to SQS, Lambda, HTTP
Redis Streams| Lightweight streaming                 | In-memory, low latency
Google Pub/Sub | Global event streaming              | Managed, strong consistency

DJANGO + CELERY EXAMPLE

Django apps often use Celery with Redis or RabbitMQ as a broker for async task processing:

  # tasks.py
  from celery import shared_task

  @shared_task
  def send_welcome_email(user_id):
      user = User.objects.get(id=user_id)
      # send email logic here...

  # views.py — fire and forget
  def register(request):
      user = create_user(request.POST)
      send_welcome_email.delay(user.id)  # async!
      return redirect('dashboard')

KEY TAKEAWAY

Message queues transform fragile synchronous chains into resilient, decoupled pipelines. Use them whenever: tasks are slow, services have different scaling needs, or you need guaranteed delivery of events."""
    },
    {
        "title": "Consistent Hashing – Scaling Distributed Caches",
        "slug": "consistent-hashing-distributed-caches",
        "category": "System Design",
        "body": """Consistent hashing is a technique that minimizes data redistribution when nodes are added or removed from a distributed system. It is used by distributed caches (Memcached, Redis Cluster), load balancers, and distributed databases like Cassandra and DynamoDB.

THE PROBLEM WITH NAIVE HASHING

Suppose you have 3 cache servers and use modular hashing to route keys:

  server = hash(key) % 3

This works fine. But when you add a 4th server:

  server = hash(key) % 4

Almost every key maps to a different server. The entire cache is invalidated — a cache miss storm hits your database. This is catastrophic at scale.

HOW CONSISTENT HASHING WORKS

1. Arrange the hash space (0 to 2^32 - 1) as a ring (circle).
2. Hash each server node onto the ring using the same hash function: hash(server_id) → position on ring.
3. To route a key: hash(key) → position on ring, then walk clockwise to find the first server node. That server owns the key.

RING DIAGRAM

                    0
                 ┌──────┐
            330  │      │  30
           ╱─── │      │ ───╲
        Server C │  ◉  Ring  │ Server A
           ╲─── │      │ ───╱
            210  │      │  150
                 └──────┘
                   Server B

Key "user:123" hashes to position 45° → walks clockwise → hits Server A

ADDING/REMOVING NODES

Add Server D (hashes to position 90°):
- Only keys between Server A and Server D migrate from A to D.
- All other keys are unaffected.
- With N nodes, adding one node moves only 1/N of keys on average. ✓

VIRTUAL NODES (VNODES)

A single physical server maps to multiple positions on the ring. For example, Server A appears at 10 positions, Server B at 10 positions, etc.

Benefits:
- More even distribution (without vnodes, distribution depends on hash function luck)
- When a server is added, it takes keys from multiple arcs, spreading the migration load
- Servers with higher capacity can have more vnodes than weaker servers

Cassandra uses 256 vnodes per physical node by default.

REPLICATION

For fault tolerance, a key is stored on the next K servers clockwise from its primary server (K = replication factor). If the primary fails, reads and writes fall over to the next replica.

REAL-WORLD USAGE

System          | Consistent Hashing Usage
----------------|----------------------------------
Cassandra       | Data partitioning + replication
DynamoDB        | Partition key routing
Redis Cluster   | 16,384 hash slots on a ring
Memcached       | Client-side consistent hashing
Nginx           | Consistent hash upstream module

IMPLEMENTATION IN PYTHON

  import hashlib
  import bisect

  class ConsistentHashRing:
      def __init__(self, nodes=None, vnodes=100):
          self.vnodes = vnodes
          self.ring   = {}
          self.sorted_keys = []
          for node in (nodes or []):
              self.add_node(node)

      def _hash(self, key):
          return int(hashlib.md5(key.encode()).hexdigest(), 16)

      def add_node(self, node):
          for i in range(self.vnodes):
              vkey = self._hash(f"{node}:{i}")
              self.ring[vkey] = node
              bisect.insort(self.sorted_keys, vkey)

      def get_node(self, key):
          if not self.ring:
              return None
          h = self._hash(key)
          idx = bisect.bisect(self.sorted_keys, h) % len(self.sorted_keys)
          return self.ring[self.sorted_keys[idx]]

KEY TAKEAWAY

Consistent hashing is the elegant solution to the cache invalidation storm. It is a foundational concept for anyone designing distributed caches, databases, or load balancers at scale."""
    },
]

# ─────────────────────────────────────────────────────────────
#  General posts
# ─────────────────────────────────────────────────────────────
GENERAL_POSTS = [
    {
        "title": "Getting Started with Django",
        "slug": "getting-started-with-django",
        "category": "Technology",
        "body": (
            "Django is a high-level Python web framework that encourages rapid development "
            "and clean, pragmatic design. Built by experienced developers, it takes care of "
            "much of the hassle of web development, so you can focus on writing your app "
            "without needing to reinvent the wheel.\n\n"
            "To install Django run: pip install django\n"
            "Then create a new project: django-admin startproject myproject\n\n"
            "Django follows the MVT (Model-View-Template) architecture pattern and comes "
            "with a powerful ORM, an automatic admin interface, and excellent documentation.\n\n"
            "Key features include:\n"
            "- ORM for database abstraction\n"
            "- Built-in admin panel\n"
            "- URL routing\n"
            "- Form handling and validation\n"
            "- Authentication system\n"
            "- Security features (CSRF, XSS protection)\n\n"
            "Django's philosophy is 'batteries included' — everything you need is built in."
        ),
    },
    {
        "title": "PostgreSQL with Django – Best Practices",
        "slug": "postgresql-django-best-practices",
        "category": "Technology",
        "body": (
            "PostgreSQL is the recommended database for production Django applications. "
            "It supports advanced features like JSONB fields, full-text search, window "
            "functions, and more that map perfectly to Django's ORM.\n\n"
            "To connect Django to PostgreSQL, install psycopg2-binary and configure "
            "the DATABASES setting in settings.py with your host, port, name, user and "
            "password.\n\n"
            "Best practices:\n"
            "1. Always use environment variables for credentials\n"
            "2. Enable connection pooling with PgBouncer in production\n"
            "3. Use database indexes on frequently queried columns\n"
            "4. Run ANALYZE regularly to keep query planner statistics fresh\n"
            "5. Use EXPLAIN ANALYZE to debug slow queries\n\n"
            "Django's ORM translates Python code to optimized SQL, but always check "
            "the generated queries using the Django Debug Toolbar in development."
        ),
    },
    {
        "title": "The Art of Test Cricket",
        "slug": "the-art-of-test-cricket",
        "category": "Sports",
        "body": (
            "Test cricket is the longest format of the game and is widely regarded as the "
            "ultimate test of a cricketer's skill, temperament and endurance. A Test match "
            "can last up to five days, with each team batting twice.\n\n"
            "The patience required to build an innings over hours, the swing of a Duke's "
            "ball on a cloudy English morning, or a spinner turning the ball square on a "
            "dusty subcontinental track — these are the elements that make Test cricket "
            "a timeless and beautiful sport.\n\n"
            "Notable records include Sachin Tendulkar's 15,921 Test runs and Muttiah "
            "Muralitharan's 800 wickets — both considered among the greatest sporting "
            "achievements of all time.\n\n"
            "The five-day format demands physical fitness, mental resilience, and strategic "
            "thinking from both batsmen and bowlers. It truly separates the great from the good."
        ),
    },
    {
        "title": "Healthy Living in a Digital Age",
        "slug": "healthy-living-digital-age",
        "category": "Health",
        "body": (
            "In today's screen-dominated world, maintaining physical and mental health "
            "requires conscious effort. Prolonged screen time can cause eye strain, "
            "disrupted sleep cycles, and reduced physical activity.\n\n"
            "Simple habits make a big difference: follow the 20-20-20 rule for your eyes "
            "(every 20 minutes look at something 20 feet away for 20 seconds), take regular "
            "walking breaks, and set a hard cut-off for screen use an hour before bedtime.\n\n"
            "Mental health is equally important — mindfulness apps, journaling, and "
            "simply spending time in nature can dramatically improve wellbeing.\n\n"
            "For software developers specifically: invest in a good chair, an ergonomic "
            "keyboard, and a monitor at eye level. Your body will thank you in 20 years."
        ),
    },
    {
        "title": "Exploring the World on a Budget",
        "slug": "exploring-world-on-a-budget",
        "category": "Travel",
        "body": (
            "Travel doesn't have to be expensive. With careful planning you can see the "
            "world without breaking the bank. Book flights 6-8 weeks in advance, travel "
            "during shoulder seasons, and choose accommodation like hostels or Airbnb rooms "
            "over hotels.\n\n"
            "Street food is not only cheaper but often the most authentic culinary "
            "experience a destination offers. Free walking tours, national parks, and "
            "public beaches provide incredible experiences at zero cost.\n\n"
            "South-East Asia, Eastern Europe, and Central America are perennial favourites "
            "for budget travellers offering rich culture at very low daily costs.\n\n"
            "Top budget destinations in 2026: Vietnam, Georgia (Tbilisi), Colombia, "
            "Albania, and Sri Lanka — all offering exceptional value and warm hospitality."
        ),
    },
]

ALL_POSTS = SD_POSTS + GENERAL_POSTS


class Command(BaseCommand):
    help = 'Seed the database with sample blog posts'

    def add_arguments(self, parser):
        parser.add_argument('--reset', action='store_true', help='Clear all posts before seeding')

    def handle(self, *args, **options):
        if options.get('reset'):
            Post.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all posts and categories.'))

        # Create superuser
        if not User.objects.filter(is_superuser=True).exists():
            admin = User.objects.create_superuser(
                username='admin', email='admin@example.com', password='admin123',
                first_name='Admin', last_name='User',
            )
            self.stdout.write(self.style.SUCCESS('Created superuser: admin / admin123'))
        else:
            admin = User.objects.filter(is_superuser=True).first()
            self.stdout.write('Superuser already exists.')

        created_posts = 0
        for data in ALL_POSTS:
            cat_name = data['category']
            cat_slug = cat_name.lower().replace(' ', '-')
            cat, _ = Category.objects.get_or_create(
                name=cat_name,
                defaults={'slug': cat_slug},
            )
            post, created = Post.objects.get_or_create(
                slug=data['slug'],
                defaults={
                    'title':    data['title'],
                    'author':   admin,
                    'category': cat,
                    'body':     data['body'],
                    'status':   'published',
                },
            )
            if created:
                created_posts += 1

        self.stdout.write(self.style.SUCCESS(
            f'Seeding complete. {created_posts} new post(s) created.'
        ))
