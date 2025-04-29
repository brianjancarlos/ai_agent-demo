# Incident Response Runbook

<think>
Okay, the user wants me to create a runbook based on the incident analysis they provided. Let me start by recalling the key points from the analysis. The main issue is an OutOfMemoryError due to a memory leak in the XYZ caching system. The root cause is that the cache isned properly managing memory, leading to heap exhaustion.

First, I need to structure the runbook into sections. The user specified that each planning step must be on a new line, so I should make sure that each part of the runbook is clearly separated. The sections required are Incident Summary, Root Cause, Immediate Actions, Long-term Actions, and Lessons Learned. 

Starting with the Incident Summary, I need to summarize the problem concisely. Then, the Root Cause section should explain why the error occurred, which is the memory leak in the caching system. For Immediate Actions, the user mentioned increasing heap size, monitoring, evicting data, and checking static references. Long-term actions include fixing the cache configuration, refactoring, adding monitoring, and code reviews. Lessons Learned should focus on proactive monitoring and cache management.

I should also ensure that each section is well-organized and uses clear, actionable steps. The user might be a technical team lead or a system administrator who needs a clear, step-by-step guide to resolve and prevent such issues. They might also want to ensure that the runbook is comprehensive enough to be used by others on the team, so clarity and detail are important.

I need to make sure that the runbook is in Markdown format, with proper headings and bullet points. Also, the user emphasized that each planning step must be on a new line, so I should avoid using markdown for the planning steps but present them as separate lines in the response. However, since the final answer is in Markdown, I'll format it accordingly.

Wait, the user said "each planning step must be on a new line" but in the context of the runbook, which is already structured. Maybe the user is referring to the thought process, but in the final answer, the sections are separate. I need to make sure that the runbook is well-structured with clear sections and that each part is properly labeled. Also, check that the immediate and long-term actions are actionable and specific, not vague. For example, instead of just "monitor cache usage," specify using tools like jstat or heap dumps.

I should also ensure that the lessons learned section ties back to the incident, emphasizing the importance of monitoring and proper cache management. The user might be looking for a runbook that can be followed by other team members to resolve similar issues, so clarity and actionable steps are crucial. Alright, I think that's covered. Now, time to structure the runbook accordingly.
</think>

```markdown
# Incident Response Runbook: OutOfMemoryError (Java Heap Space) in XYZ Caching System

## Incident Summary
A Java application encountered an `OutOfMemoryError: Java heap space` during request processing. The error originated in the `Service.processRequest` method, linked to a memory leak in the XYZ caching system. Heap usage increased over time, leading to failure.

---

## Root Cause
- **Memory Leak in XYZ Caching System:** The cache retains objects indefinitely, preventing garbage collection.  
- **Unbounded Cache Size:** No eviction policy or size limits are enforced, allowing memory to grow uncontrolled.  
- **Heap Size Inadequacy:** The allocated heap size may not suffice for the workload, compounded by the leak.  

---

## Immediate Actions
1. **Increase Heap Size Temporarily**  
   - Modify JVM arguments (e.g., `-Xmx4g`) to allocate more memory.  
   - Monitor system resources to ensure the increase resolves the OOM without causing other issues.  

2. **Monitor Cache Usage**  
   - Use `jstat` or heap dumps to track memory consumption and identify problematic cache entries.  
   - Check for stagnant or large objects in the cache.  

3. **Evict Stale Data**  
   - Manually clear the cache during maintenance windows or implement a scheduled cleanup.  
   - Ensure cache entries have a TTL (Time-to-Live) to expire after a set period.  

4. **Review Static References**  
   - Audit code for static fields or global variables holding references to the cache.  
   - Remove or nullify such references to allow garbage collection.  

---

## Long-term Actions
1. **Fix Cache Configuration**  
   - Configure XYZ with a bounded size, eviction policy (e.g., LRU), and TTL for entries.  
   - Replace XYZ with a managed caching solution (e.g., Caffeine, Redis) if XYZ is not supported.  

2. **Refactor Cache Usage**  
   - Avoid holding references to cached objects in long-lived contexts (e.g., static variables, thread-local storage).  
   - Use weak references or soft references for non-critical data.  

3. **Add Monitoring and Alerts**  
   - Deploy tools like Prometheus + Grafana to track memory usage and trigger alerts when thresholds are exceeded.  
   - Integrate with logging to capture heap dumps during OOM events.  

4. **Code Review and Testing**  
   - Conduct a code review to identify and fix all instances of improper cache usage.  
   - Test the application under load to ensure the cache does not cause memory leaks.  

5. **Documentation and Training**  
   - Document cache management best practices for future development.  
   - Train the team on monitoring tools and memory optimization techniques.  

---

## Lessons Learned
- **Proactive Monitoring:** Implement continuous monitoring for memory usage to detect leaks early.  
- **Cache Design Principles:** Use bounded caches with eviction policies to prevent uncontrolled growth.  
- **Heap Size Tuning:** Balance heap size with application demands and avoid over-reliance on temporary increases.  
- **Code Discipline:** Avoid static references to objects that may cause memory leaks.  
```