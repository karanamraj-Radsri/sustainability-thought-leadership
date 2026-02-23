import os
import re
import glob
import sys

from openai import OpenAI
from github import Github


AUTHOR = "Sreepad Karanam"
GITHUB_USER = "karanamraj-Radsri"

SYSTEM_PROMPT = (
    "You are {author}, a C-suite sustainability leader with 20+ years of expertise in "
    "polymers, materials science, petrochemicals, and circular economy. "
    "Write in a confident, first-person executive voice. Be specific, data-driven, and "
    "thought-provoking. Draw on deep materials science knowledge and strategic industry insight. "
    "Avoid generic statements. Always connect material science to business outcomes."
).format(author=AUTHOR)


def find_trending_topics_file():
    """Find the most recent trending topics markdown file in the research/ directory."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    research_dir = os.path.join(repo_root, "research")
    pattern = os.path.join(research_dir, "*.md")
    files = glob.glob(pattern)
    trending_files = [f for f in files if "trending topics" in os.path.basename(f).lower() or "trending-topics" in os.path.basename(f).lower()]
    if not trending_files:
        raise FileNotFoundError(
            f"No trending topics file found in {research_dir}. "
            "Expected a file matching 'Trending Topics - Week X' or 'trending-topics-week-X.md'."
        )
    return sorted(trending_files)[-1]


def extract_week_number(filepath):
    """Extract week number from the trending topics filename."""
    basename = os.path.basename(filepath)
    match = re.search(r"Week\s+(\d+)", basename, re.IGNORECASE)
    return match.group(1) if match else "X"


def parse_trending_topics(filepath):
    """Parse the trending topics markdown file and return a list of trend dicts."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    trend_pattern = re.compile(
        r"##\s+[^\n]*TREND\s+#(\d+)[:\s]+([^\n]+)\n(.*?)(?=##\s+[^\n]*TREND\s+#\d+|##\s+📊\s+TREND\s+COMPARISON|##\s+✅|$)",
        re.DOTALL,
    )

    trends = []
    for match in trend_pattern.finditer(content):
        number = int(match.group(1))
        name = match.group(2).strip()
        body = match.group(3)

        description = _extract_section(body, "Description")
        relevance = _extract_section(body, "Your Relevance")
        references = _extract_references(body)

        trends.append({
            "number": number,
            "name": name,
            "description": description,
            "relevance": relevance,
            "references": references,
        })

    trends.sort(key=lambda t: t["number"])
    return trends


def _extract_section(body, heading):
    """Extract a named section from a trend body."""
    pattern = re.compile(
        r"\*\*" + re.escape(heading) + r"[^*]*\*\*[:\s]*(.*?)(?=\*\*[A-Z]|\Z)",
        re.DOTALL,
    )
    match = pattern.search(body)
    if match:
        return match.group(1).strip()
    return ""


def _extract_references(body):
    """Extract numbered reference links from a trend body."""
    ref_section_match = re.search(r"\*\*Sources[^*]*\*\*(.*?)(?=---|\Z)", body, re.DOTALL)
    if not ref_section_match:
        return []
    ref_text = ref_section_match.group(1)
    refs = re.findall(r"\d+\.\s+\[([^\]]+)\]\((https?://[^\)]+)\)", ref_text)
    return [{"title": title, "url": url} for title, url in refs]


def format_references_for_prompt(references):
    """Format references as a bulleted list for inclusion in prompts."""
    if not references:
        return ""
    lines = [f"- {ref['title']}: {ref['url']}" for ref in references]
    return "\n".join(lines)


def format_references_for_issue(references):
    """Format references as a markdown numbered list for a GitHub Issue."""
    if not references:
        return "_No references available._"
    lines = [f"{i+1}. [{ref['title']}]({ref['url']})" for i, ref in enumerate(references)]
    return "\n".join(lines)


def generate_short_post(client, trend):
    """Generate a 400-500 word LinkedIn short-form post for the given trend."""
    refs_text = format_references_for_prompt(trend["references"])
    prompt = (
        f"Write a LinkedIn post (400-500 words) in my first-person C-suite voice about the following trend:\n\n"
        f"**Trend:** {trend['name']}\n\n"
        f"**Description:** {trend['description']}\n\n"
        f"**Why this matters to me as a materials/polymers expert:**\n{trend['relevance']}\n\n"
        f"The post should:\n"
        f"- Start with a compelling hook\n"
        f"- Share a specific expert insight or contrarian perspective from my 20+ years in polymers/materials\n"
        f"- Connect materials science to business strategy and circular economy outcomes\n"
        f"- End with a thought-provoking question to drive engagement\n"
        f"- Be 400-500 words\n\n"
    )
    if refs_text:
        prompt += f"Reference sources for accuracy (do not list them in the post):\n{refs_text}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def generate_long_post(client, trend):
    """Generate a 500-800 word LinkedIn long-form post for the given trend."""
    refs_text = format_references_for_prompt(trend["references"])
    prompt = (
        f"Write a long-form LinkedIn post (500-800 words) in my first-person C-suite voice about the following trend:\n\n"
        f"**Trend:** {trend['name']}\n\n"
        f"**Description:** {trend['description']}\n\n"
        f"**Why this matters to me as a materials/polymers expert:**\n{trend['relevance']}\n\n"
        f"The post should:\n"
        f"- Open with a strong executive hook\n"
        f"- Provide a detailed analysis drawing on materials science expertise\n"
        f"- Include 2-3 specific strategic recommendations for business leaders\n"
        f"- Address challenges and opportunities from a polymers/materials perspective\n"
        f"- Close with a call-to-action and engagement question\n"
        f"- Be 500-800 words\n\n"
    )
    if refs_text:
        prompt += f"Reference sources for accuracy (do not list them in the post):\n{refs_text}\n"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def create_github_issue(short_post, long_post, trend, week_number):
    """Create a GitHub Issue with the content drafts and references."""
    github_token = os.getenv("GITHUB_TOKEN")
    github_repo = os.getenv("GITHUB_REPOSITORY", f"{GITHUB_USER}/sustainability-thought-leadership")

    if not github_token:
        print("\n⚠️  GITHUB_TOKEN not set. Skipping GitHub Issue creation.")
        print("Set GITHUB_TOKEN environment variable to enable automatic issue creation.")
        return None

    g = Github(github_token)
    repo = g.get_repo(github_repo)

    refs_md = format_references_for_issue(trend["references"])
    issue_title = f"Week {week_number} Content Draft: {trend['name']}"
    issue_body = (
        f"## 📝 Short-Form Post (400-500 words)\n\n"
        f"{short_post}\n\n"
        f"---\n\n"
        f"## 📄 Long-Form Post (500-800 words)\n\n"
        f"{long_post}\n\n"
        f"---\n\n"
        f"## 📚 References\n\n"
        f"{refs_md}\n\n"
        f"---\n\n"
        f"_Generated by content_generator.py — Review, edit, and approve before posting to LinkedIn._"
    )

    from github import UnknownObjectException
    # Attempt to apply the 'content-draft' label (create it if it doesn't exist)
    try:
        repo.get_label("content-draft")
    except UnknownObjectException:
        repo.create_label("content-draft", "0075ca")

    issue = repo.create_issue(
        title=issue_title,
        body=issue_body,
        assignees=[GITHUB_USER],
        labels=["content-draft"],
    )
    return issue


def select_trend(trends):
    """Display trend names and prompt user to select one (1-3)."""
    print("\nAvailable trends:")
    for trend in trends:
        print(f"  ({trend['number']}) {trend['name']}")
    print()

    while True:
        choice = input("Which trend do you want to draft content for? (1/2/3): ").strip()
        if choice in ("1", "2", "3"):
            chosen = next((t for t in trends if t["number"] == int(choice)), None)
            if chosen:
                return chosen
        print("Invalid selection. Please enter 1, 2, or 3.")


def main():
    # Validate OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Set it with: export OPENAI_API_KEY='your-api-key'")
        sys.exit(1)

    # Find and parse trending topics file
    print("🔍 Looking for trending topics file...")
    try:
        topics_file = find_trending_topics_file()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"📄 Found: {os.path.basename(topics_file)}")
    week_number = extract_week_number(topics_file)
    trends = parse_trending_topics(topics_file)

    if not trends:
        print("Error: No trends found in the trending topics file.")
        sys.exit(1)

    # Prompt user for trend selection
    selected_trend = select_trend(trends)
    print(f"\n✅ Selected: Trend #{selected_trend['number']} — {selected_trend['name']}\n")

    # Generate content
    client = OpenAI(api_key=api_key)

    print("✍️  Generating short-form post (400-500 words)...")
    short_post = generate_short_post(client, selected_trend)

    print("✍️  Generating long-form post (500-800 words)...")
    long_post = generate_long_post(client, selected_trend)

    print("\n--- SHORT-FORM POST ---\n")
    print(short_post)
    print("\n--- LONG-FORM POST ---\n")
    print(long_post)

    # Create GitHub Issue
    print("\n🐙 Creating GitHub Issue...")
    issue = create_github_issue(short_post, long_post, selected_trend, week_number)
    if issue:
        print(f"✅ GitHub Issue created: {issue.html_url}")
    else:
        print("ℹ️  Drafts printed above. Create GitHub Issue manually or set GITHUB_TOKEN.")


if __name__ == "__main__":
    main()
