"""Debug test to see what's happening."""
from src.core.csdiff_web import CSDiffWeb

csdiff = CSDiffWeb(".ts", skip_filter=True)

base = "function foo() { return 1; }"
left = "function foo() { return 2; }"
right = "function foo() { return 2; }"

result, has_conflict, num_conflicts = csdiff.merge(base, left, right)

print("=== RESULT ===")
print(result)
print("\n=== METADATA ===")
print(f"has_conflict: {has_conflict}")
print(f"num_conflicts: {num_conflicts}")

# Test stats
stats = csdiff.get_statistics(base, left, right)
print("\n=== STATS ===")
for key, value in stats.items():
    print(f"{key}: {value}")
