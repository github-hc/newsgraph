from graph import graph

result = graph.invoke(
    {
        "topic": "Indian Startup Ecosystem",
        "description": "Recent developments and trends in Indian startup ecosystem",
        "urls": [
            "http://en.wikipedia.org/wiki/Shark_Tank_India",
            "https://en.wikipedia.org/wiki/Startup_India",
            "https://en.wikipedia.org/wiki/List_of_Indian_entrepreneurs",
        ],
    }
)

print("=" * 60)
print("RESEARCH SUMMARY")
print("=" * 60)
print(result["research"])
print()
print("=" * 60)
print("NEWSLETTER")
print("=" * 60)
print(result["newsletter"])