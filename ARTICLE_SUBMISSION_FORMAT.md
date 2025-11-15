# How to Submit Malta Law Articles - Format Guide

## 🎯 Quick Template

Copy this template for each article or article group you submit:

```
---
ACT: [Act name and chapter number]
CITATION: [Full citation for metadata]
ARTICLES: [Article number(s)]
TOPIC: [What this article is about]
---

[Paste exact text from legislation.mt here, including article numbers and sub-articles]

---
```

## ✅ Example Submission (Correct Format)

```
---
ACT: Civil Code
CITATION: Civil Code Cap. 16, Article 320-322
ARTICLES: 320-322
TOPIC: Ownership
---

320. Ownership is the right of enjoying and disposing of things in the most absolute manner, provided no use thereof is made which is prohibited by law.

321. No person can be compelled to give up his property or to permit any other person to make use of it, except for a public purpose, and upon payment of a fair compensation.

322. (1) Save as otherwise provided by law, the owner of a thing has the right to recover it from any possessor.

(2) A possessor who, after being notified of the judicial demand for the recovery of the thing ceases of his own act, to possess such thing, is bound, at his own expense, to regain possession of the thing for the plaintiff, or, if unable to do so, to make good its value, unless the plaintiff elects to proceed against the actual possessor.

---
```

## ✅ Another Example (Single Article)

```
---
ACT: Income Tax Act
CITATION: Income Tax Act Cap. 123, Article 56(13)
ARTICLES: 56(13)
TOPIC: Contractor Tax Rate
---

56.(13) (a) The tax upon the chargeable income of any person referred to as a Contractor in article 23 shall be levied at the rate of 35 cents (€0.35) on every euro of the chargeable income.

(b) The provisions of this subarticle shall apply to tax years commencing on or after 1st January 2020.

---
```

## 📏 Formatting Rules

### ✅ DO:
- Include the `---` separators
- Include all metadata (ACT, CITATION, ARTICLES, TOPIC)
- Copy **exact text** from legislation.mt (word-for-word)
- Include **all sub-articles** with their parent
- Keep article numbers as they appear (bold not needed - just the number)
- Preserve all punctuation and formatting
- Use the full article number format (e.g., `56.(13)` not just `13`)

### ❌ DON'T:
- Don't paraphrase or rewrite
- Don't add your own commentary
- Don't skip sub-articles
- Don't mix articles from different Acts
- Don't include headers like "CAP.540.]" (just the article text)

## 📊 How to Group Articles

### Group Together IF:
- Sequential numbers (320, 321, 322)
- Same topic (all about ownership)
- Combined size: 150-400 tokens
- They reference each other

### Separate IF:
- Different topics
- Large standalone articles (200+ tokens)
- Different chapters/sections

## 🤖 LLM Helper Prompt

Copy this prompt and paste it to ChatGPT, Claude, or any LLM along with text from legislation.mt:

```
You are helping extract Malta law articles from legislation.mt for a legal RAG system.

TASK: Identify and format articles from the provided legal text.

RULES FOR IDENTIFYING ARTICLES:
1. ARTICLE = A number followed by a period (e.g., "15.", "320.", "1234.")
   - The number is usually in BOLD in the source
   - Must be just a number + period (not "CAP.540" or other prefixes)
   - Example: "15." is an article, "CAP.540.]" is NOT

2. SUB-ARTICLE = A number in parentheses (e.g., "(1)", "(2)", "(a)", "(b)")
   - Always belongs to the preceding article
   - Can be nested: "(1)" can contain "(a)", "(b)", etc.
   - Example: "15.(1)" means Article 15, sub-article 1

3. ARTICLE vs SUB-ARTICLE:
   - "15." ← ARTICLE (number + period)
   - "(1)" ← SUB-ARTICLE (number in parentheses)
   - "15.(1)" ← Article 15, sub-article 1
   - "(a)" ← SUB-ARTICLE under a numbered sub-article

OUTPUT FORMAT:
For each article or related group of articles, output:

---
ACT: [Name of the Act]
CITATION: [Act Name Cap. X, Article Y-Z]
ARTICLES: [Article number(s)]
TOPIC: [Brief description of what this covers]
---

[Full text of article(s) exactly as written, including all sub-articles]

---

EXAMPLES:

Input text:
"320. Ownership is the right of enjoying and disposing of things..."

Output:
---
ACT: Civil Code
CITATION: Civil Code Cap. 16, Article 320
ARTICLES: 320
TOPIC: Definition of Ownership
---

320. Ownership is the right of enjoying and disposing of things in the most absolute manner, provided no use thereof is made which is prohibited by law.

---

Input text:
"15.(1) All persons seeking psychosocial counselling...
15.(2) The pathologisation of any form...
16.(1) The Minister, after consulting..."

Output:
---
ACT: Gender Identity, Gender Expression and Sex Characteristics Act
CITATION: GIGESC Cap. 540, Article 15
ARTICLES: 15
TOPIC: Psychosocial Counselling and Support
---

15.(1) All persons seeking psychosocial counselling, support and medical interventions relating to sex or gender should be given expert sensitive and individually tailored support by psychologists and medical practitioners or peer counselling. Such support should extend from the date of diagnosis or self-referral for as long as necessary.

(2) The pathologisation of any form of sexual orientation, gender identity and, or gender expression as may be classified under the International Classification of Diseases or any other similar internationally recognised classification, shall be null and void in Malta. The nullity of such classification shall not impact negatively the provision of any healthcare service related to sex and, or gender.

---

---
ACT: Gender Identity, Gender Expression and Sex Characteristics Act
CITATION: GIGESC Cap. 540, Article 16
ARTICLES: 16
TOPIC: Treatment Protocol Working Group
---

16.(1) The Minister, after consulting the Minister responsible for health, shall appoint a working group.

(2) The working group shall consist of a Chairperson and nine members.

(3) The Chairperson shall be a medical doctor with at least twelve years experience.

(4) The members shall be three experts in human rights issues, three psychosocial professionals and three medical experts.

(5) The Minister shall appoint the working group within three months of the entry into force of this Act.

(6) The members of the working group shall review the current medical treatment protocols in line with current medical best practices and human rights standards and shall, within one year from the date of their appointment, issue a report with recommendations for revision of the current medical treatment protocols.

---

GROUPING RULES:
- Group 2-4 sequential articles together IF they share the same topic
- Separate articles that cover different topics
- Each article must include ALL its sub-articles
- NO TOKEN LIMITS - include complete articles regardless of length

Now process the following legal text:

[PASTE YOUR TEXT FROM LEGISLATION.MT HERE]
```

## 🎓 Understanding Article Structure

### Visual Guide

```
15. ← ARTICLE 15 (number + period)
    (1) ← SUB-ARTICLE 1 (number in parentheses)
        Text of sub-article 1...

    (2) ← SUB-ARTICLE 2
        Text of sub-article 2...

16. ← ARTICLE 16 (new article)
    (1) ← SUB-ARTICLE 1
        Text...

    (2) ← SUB-ARTICLE 2
        Text...

        (a) ← NESTED SUB-ARTICLE (under 16.(2))
            Text...

        (b) ← NESTED SUB-ARTICLE
            Text...

    (3) ← SUB-ARTICLE 3
        Text...
```

### Common Patterns

**Pattern 1: Simple Article (No Sub-articles)**
```
17. The Minister may make regulations to give better effect to any of the provisions of this Act.
```

**Pattern 2: Article with Sub-articles**
```
15.(1) All persons seeking psychosocial counselling...
(2) The pathologisation of any form...
```

**Pattern 3: Article with Nested Sub-articles**
```
56.(13) (a) The tax upon the chargeable income...
(b) The provisions of this subarticle...
```

## 🔍 Quality Checklist

Before submitting, verify:
- [ ] Copied exact text from legislation.mt (no paraphrasing)
- [ ] Included all metadata (ACT, CITATION, ARTICLES, TOPIC)
- [ ] All sub-articles included with parent article
- [ ] Article numbers are correct
- [ ] No CAP.XXX] headers included in article text
- [ ] Used `---` separators
- [ ] Related articles grouped appropriately

## 📤 How to Submit to Me

### Option A: Single Submission
Post one or more articles in a single message:
```
Here are 5 articles about property law:

---
ACT: Civil Code
CITATION: Civil Code Cap. 16, Article 323
...
---

---
ACT: Civil Code
CITATION: Civil Code Cap. 16, Article 324
...
---
```

### Option B: Batch Submission
```
I have 50 articles ready from the Civil Code about property law.
Here's the first 10:

[articles in format above]

Let me know when you're ready for the next batch.
```

### Option C: Topic Request
```
I want to add articles about:
- Marriage requirements (10 articles)
- Company registration (15 articles)
- Tax penalties (8 articles)

I'll extract and format them using the LLM prompt you provided.
```

## 💡 Pro Tips

1. **Use the LLM prompt** - It will handle the formatting for you
2. **Verify article numbers** - Double-check they match legislation.mt
3. **Group by topic** - Helps with retrieval accuracy
4. **Start small** - Submit 5-10 articles first, then expand
5. **Note any uncertainties** - If unsure about grouping, ask me

## ❓ When in Doubt

**Just paste the raw text from legislation.mt and tell me:**
- What Act it's from
- What topic it covers
- Any special notes

I'll format it correctly!

## 🎯 Example: What to Send Me

Perfect submission:
```
I have articles about marriage requirements:

---
ACT: Civil Code
CITATION: Civil Code Cap. 16, Article 18-20
ARTICLES: 18-20
TOPIC: Marriage Requirements and Capacity
---

18. Marriage is the lawful union of two persons of full age in accordance with law.

19. (1) No marriage shall be contracted by any person who has not attained the age of eighteen years.

(2) Any marriage contracted in contravention of this article shall be null.

20. Marriage shall be based on the equality of rights and duties of the spouses and on mutual respect and understanding.

---
```

Then I'll respond:
```
✅ Added: Civil Code Articles 18-20 (Marriage Requirements)
✅ Format: Perfect
✅ Token count: 95 tokens
✅ Chunking: Optimal (related articles grouped)
✅ Ready for testing

Current database: 9 articles across 6 documents
```

---

**Ready to start! Send me articles in the format above.** 🚀
