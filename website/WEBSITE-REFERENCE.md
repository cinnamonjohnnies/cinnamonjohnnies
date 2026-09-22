# Checkpoint Planning Website: Content, Design Guidelines, and Updates

Single reference for the live site (`website/`), what it says, what it
looks like, and what's changed or still pending. Content below is
extracted directly from the current HTML, if this file and the live
pages ever disagree, the HTML is the source of truth and this needs
regenerating.

---

## 1. Design guidelines

### Colors

Defined as CSS custom properties in `website/styles.css`:

| Token | Hex | Use |
|---|---|---|
| `--navy-900` | `#1b2027` | Darkest background (footer, dark sections) |
| `--navy-800` | `#252b33` | Header background |
| `--navy-700` | `#394452` | Secondary dark text/backgrounds |
| `--teal-700` | `#285d88` | Primary brand blue (despite the variable name, this is blue not teal, left over from an earlier palette) |
| `--teal-600` | `#33719f` | Blue, links/accents |
| `--teal-500` | `#4c8cbe` | Lighter blue |
| `--teal-300` | `#9cc4e2` | Light blue, text on dark backgrounds |
| `--teal-100` | `#e7eff6` | Palest blue, section backgrounds |
| `--gold-500` | `#c8963e` | CTA accent, primary button color |
| `--gold-600` | `#b07f2c` | Gold hover state |
| `--ink` | `#232a30` | Body text |
| `--ink-soft` | `#57626c` | Secondary/muted text |
| `--paper` | `#ffffff` | White |
| `--paper-alt` | `#f5f7f9` | Off-white section background |
| `--border` | `#dde3e9` | Hairline borders |

Palette was deliberately built with no green, an earlier version used
green/teal and was recolored to this navy/blue/gold system to match
Scott's real branding. Gold is used sparingly, CTA buttons and small
accent rules only, never as a large fill.

### Typography

- **Headings and body copy**: Georgia / Iowan Old Style (serif), set on
  `body`. This is the site's primary reading typeface.
- **UI chrome**: Helvetica Neue / Arial (sans), used for navigation,
  buttons, labels, eyebrows, form fields, and anything functional
  rather than editorial.
- This serif/sans split is a deliberate pairing (editorial warmth for
  content, clean functional sans for interface), keep it if redesigning
  rather than moving everything to one typeface.

### Logo and imagery

- `website/assets/checkpoint-logo-full.png`, full lockup (mark +
  wordmark).
- `website/assets/checkpoint-logo-mark.png`, mark only. Used inverted
  (white) on dark backgrounds throughout.
- `website/assets/crpc-badge.png`, CRPC™ credential badge, used on About.
- `website/assets/scott-marcoe.jpg`, current headshot, the only
  photography asset on the site currently.
- No stock photography anywhere on the site by design, every image is
  either the logo, the badge, or an actual photo of Scott.

### UI components (from `website/styles.css`)

- **Buttons** (`.btn`): pill-shaped (`border-radius: 999px`), three
  variants: `.btn-primary` (gold fill, main CTA), `.btn-outline`
  (transparent, for use on dark backgrounds), `.btn-teal` (blue fill,
  secondary CTA). Hover state lifts slightly (`translateY(-1px)`).
- **Header** (`.site-header`): logo left, nav center, phone number +
  primary CTA button right. Includes a hover/focus dropdown
  (`.nav-crs`) for the two Form CRS links (AIC and AAS).
- **Hero** (`.hero`): large serif headline + lede paragraph on one
  side, a `.lead-card` (white card, rounded corners, drop shadow)
  containing the lead-capture form on the other. This pattern repeats
  on all 4 transition landing pages and the homepage.
- **5-phase process strip**: used on the homepage, process page, and
  all 4 landing pages, five steps (Where We Begin™, Identify &
  Protect™, Plot Checkpoints™, Implement™, Track & Reset™),
  numbered, consistent across every instance. Treat this as a locked
  component, the five phase names and order are core to the brand
  ("The Checkpoint Strategy") and used verbatim everywhere.
- **Pricing tiers**: three cards (Clarity Session, Full Picture, Legacy
  Blueprint), each listing what's included, each tier includes
  everything from the tier before it.
- **FAQ pattern**: question as a heading, answer as a paragraph
  directly below, no accordion/collapse behavior currently, all
  answers are always visible.
- **Footer**: dark navy background, four columns (firm info/address,
  Life Transitions links, Explore/page links, disclosure text), see
  Global Elements below for exact content.

### Voice and tone

- Direct, calm, plain language, no jargon without explanation.
- No urgency or pressure language anywhere ("act now," "limited time,"
  etc.), the brand promise is the opposite of that.
- **No em dashes anywhere**, standing rule for all site copy (see
  `docs/CONTENT-STYLE.md`).
- First-person from Scott on About, third-person ("Scott helps...")
  elsewhere, this mix is intentional, keep it.
- "One checkpoint at a time" is the recurring closing line/tagline,
  used at the bottom of nearly every page, treat it as the brand's
  signature phrase.

### Compliance constraints that affect design

- **FINRA disclosure block is required on every page footer** (exact
  text in Global Elements below), do not shorten, paraphrase, or move
  it behind a click.
- **Form CRS links** (AIC and AAS) must stay in both the header
  dropdown and the footer on every page.
- **No client testimonials, no performance claims, no named outside
  professionals** on the Extended Team / Coordinated Support section
  (About page), this was specifically rejected by compliance once
  already, current copy uses unnamed service areas instead (Trusts &
  Wills, Estate Planning, Charitable Giving, Business Planning & Exit
  Strategy, Tax Planning, Life Insurance).

---

## 2. Global elements

These repeat, identically or near-identically, on all 10 pages.

### Header

Logo (links home) + nav (Home, About, Services, Our Process, Fees,
Contact, varies slightly per page since the current page is usually
omitted from its own nav) + Form CRS dropdown + phone number
`(949) 702-0139` + primary CTA button.

### Firm info block (footer, column 1)

> **Checkpoint Planning**
> 3333 Michelson Drive
> Irvine, CA 92612
> (949) 702-0139
> scott@checkpointplanning.com

### Life Transitions links (footer, column 2)

Job Loss & Layoff, Early Retirement, Divorce, Inheritance (each links
to its landing page).

### Explore links (footer, column 3)

Varies slightly by page (the current page is typically dropped from its
own footer nav), generally: Home, About, Services, Our Process, Fees,
Contact, plus the page's own lead magnet link ("Get the Free Guide" /
"Get the Free Workbook") on the 4 transition pages.

### Disclosure (footer, column 4, every page)

> Scott Marcoe offers products and services using the following
> business names: Checkpoint Planning, Capstone Financial Group,
> insurance and financial services. Ameritas Investment Company, LLC
> (AIC), Member FINRA/SIPC, securities and investments. Ameritas
> Advisory Services, LLC (AAS), investment advisory services. AIC and
> AAS are not affiliated with Capstone Financial Group. For educational
> purposes only. Not investment advice.
>
> Form CRS: Ameritas Investment Company, LLC (AIC) | Ameritas Advisory
> Services, LLC (AAS)
>
> © Checkpoint Planning. All rights reserved.

(Some pages add: "The opinions voiced in this material are for general
information only and are not intended to provide specific advice or
recommendations for any individual.")

---

## 3. Page-by-page content

### Home (`index.html`)

**Hero**
# A structured plan for the moment your life just changed.
Job loss. Divorce. Early retirement. Inheritance. When something major
shifts, financial decisions get harder and more consequential.
Checkpoint Planning brings a fiduciary advocate and a proven five-phase
process to help you move forward with clarity, not guesswork.

Lead card: **Where We Begin™ Session**, a complimentary, no-obligation
45-minute conversation. No forms, no pressure, just clarity on your next
step. Your information is confidential and never sold. No obligation.

**You are in the middle of something significant.**
Most people know they need a plan. Few have one that actually keeps up
with life. Here's where we focus.

- **Job Loss & Layoff**: Severance decisions, COBRA vs. marketplace
  coverage, unemployment, and a financial runway plan for what's next.
- **Early Retirement**: Retirement readiness, Social Security timing,
  pension elections, and building income that lasts longer than you
  planned for.
- **Divorce**: Settlement analysis, QDROs, tax impact, and rebuilding a
  financial plan that's entirely your own.
- **Inheritance & Unexpected Wealth**: Thoughtful, unhurried decisions
  about a windfall: taxes, investing, and honoring what it represents.
- **Loss of a Spouse**: Benefit claims, beneficiary transfers, and
  stabilizing finances during an emotionally difficult time.
- **Career Reinvention**: Sabbaticals, career pivots, and equity
  compensation decisions when you're building something new.

**Your unique transition. Our systematic process.**
A structured, five-phase planning process designed to bring clarity and
confidence to life's most important financial transitions.

1. **Where We Begin™**, a complimentary 45-minute clarity session. No
   cost, no obligation.
2. **Identify & Protect™**, stabilize cash flow, review benefits and
   insurance, protect what matters most.
3. **Plot Checkpoints™**, build your plan with clear 30-, 90-, and
   180-day milestones.
4. **Implement™**, execute the plan: rollovers, portfolio changes,
   documents, referrals.
5. **Track & Reset™**, ongoing reviews and recalibration as your life
   evolves.

**Meet Scott Marcoe, CRPC™**
Scott is a financial planner and CRPC™ professional who helps people
find clarity and direction during major life and career transitions. As
founder of Checkpoint Planning and creator of The Checkpoint Strategy,
he brings structure and calm to moments that often feel chaotic.

His planning philosophy was forged on the race course. As a State
Champion mountain bike racer and National Champion in 24-hour endurance
racing, Scott learned that winning required breaking a massive
challenge into manageable checkpoints and adjusting to real conditions
along the way. Financial transitions work the same way.

"One checkpoint at a time."

Based in Orange County, California, serving clients across the United
States, primarily via video conference and the Checkpoint Planning
Client Portal.

*Read Scott's full story and meet the extended planning team →*

**What you can always expect from Checkpoint Planning.**
These are not aspirational statements. They are structural commitments
built into how this practice operates.

- **Fiduciary Standard**: We are legally required to act in your best
  interest at all times, not the firm's, not a product manufacturer's,
  and not our own.
- **Full Fee Transparency**: Every fee is disclosed before work begins.
  Planning fees are flat. Investment management fees are AUM-based and
  billed monthly.
- **No Long-Term Contracts**: Planning engagements are flat-fee
  agreements. Investment management relationships can be terminated at
  any time.
- **Direct Access to Your Planner**: You work directly with Scott in
  every meeting, every review, every planning conversation. Never
  handed off to a junior associate.
- **Commission Disclosure**: Some insurance and annuity products carry
  commissions. When that's the case, it's disclosed to you in writing
  before any recommendation.
- **Coordinated Planning**: We work with your existing CPA, estate
  attorney, and other advisors so your decisions are never made in
  silos.

**Transparent, flat-fee planning.**
Pick the package that fits your situation. All planning packages
include access to the Checkpoint Planning Client Portal. *See the full
fee schedule →*

- **Clarity Session**: Investment management review, retirement account
  guidance, employee benefits review, cash flow management, insurance &
  beneficiary review, one follow-up session.
- **Full Picture**: Everything in Clarity Session, plus: full financial
  plan (Client Portal), "what if" scenario projections, tax strategy
  coordination, Social Security & Medicare review, quarterly reviews
  (year one).
- **Legacy Blueprint**: Everything in Full Picture, plus: estate & trust
  planning review, wealth transfer scenarios, advanced tax planning,
  CPA & attorney coordination, annual plan reviews, ongoing.

**Questions we hear most often.**
- *What does the first meeting look like?* The "Where We Begin" session
  is a 45-minute clarity conversation. We ask about your situation, your
  goals, and what feels most uncertain. No preparation needed.
- *How are you different from an advisor at a bank?* We are an
  independent, fee-based practice. We do not sell proprietary products,
  meet sales quotas, or earn commissions on managed assets. Our only
  financial incentive is the fee you pay us.
- *Do you only work with clients in California?* No. While we are based
  in Irvine, we serve clients across the United States. Most planning
  work is done via video conference and our online client portal.
- *What does investment management cost?* Fees are charged as a
  percentage of assets under management, billed monthly. Rates range
  from 0.65% to 1.25% depending on portfolio size, stepping down as
  assets grow.
- *Do I have to use your investment management service?* No. Planning
  and investment management are separate services. Some clients engage
  us for planning only. We discuss what makes sense in the Where We
  Begin session.
- *Who is a good fit for Checkpoint Planning?* Someone navigating a
  major life transition who needs a structured process and a fiduciary
  advocate. If that describes you, you are likely a strong fit.

*See more frequently asked questions →*

**Closing**: One checkpoint at a time. The best next step is a
conversation. The Where We Begin session is complimentary, carries no
obligation, and takes 45 minutes. It is designed to give you clarity,
not sell you something.

---

### About (`about.html`)

**Hero**
# Financial planner. CRPC™ professional. Endurance athlete.
Scott Marcoe helps people find clarity and confidence during major life
and career transitions, such as job loss, career change, divorce, early
retirement, and inheritance.

**The planner behind the practice.**
Scott Marcoe is a financial planner and CRPC™ professional who helps
people find clarity and direction during major life and career
transitions. As the founder of Checkpoint Planning and creator of The
Checkpoint Strategy, he brings structure and calm to moments that often
feel chaotic.

Scott's approach to planning is shaped by his background as a
competitive endurance athlete. He is a State Champion mountain bike
racer and a National Champion in 24-hour mountain bike racing. The long
training hours, constantly changing terrain, and mental discipline
required for endurance success influenced the philosophy behind The
Checkpoint Strategy. Training to win meant having a clear goal, breaking
the work into smaller checkpoints, and adjusting to real conditions
along the way. Financial transitions follow the same pattern. Progress
happens through checkpoints, pacing, and smart decisions made under
real circumstances.

Scott's planning process breaks big financial questions into clear,
manageable steps so clients can stabilize quickly, build confidence,
and move forward at a pace that feels right. His work is grounded in
empathy, experience, and the belief that clarity creates confidence.

"One checkpoint at a time." That is the philosophy Scott learned from
endurance racing, and the foundation of how he helps people navigate
financial transitions.

Scott lives in Orange County, California and supports clients across
the United States.

**Licensed, registered, and independently held accountable.**
- **CRPC™**: Chartered Retirement Planning Counselor, College for
  Financial Planning.
- **FINRA/SIPC**: Registered through Ameritas Investment Company, LLC,
  Member FINRA/SIPC.
- **Life & Health**: Licensed Life and Health Agent. Insurance License
  #0E59309. Board Member, AISS (Achievement Institute for STEM
  Scholars); Chairman, Marketing Committee.

**One point of contact. A coordinated team behind you.**
You work directly with Scott in every meeting, every review, and every
planning conversation. Your relationship is never handed off to someone
else. When your situation calls for specialized expertise, Scott
coordinates that work on your behalf, covering areas such as:

- **Trusts & Wills**: Reviewing or establishing trusts and wills as
  part of your broader estate plan.
- **Estate Planning**: Legacy, gifting, and asset protection guidance
  when your plan involves wealth transfer.
- **Charitable Giving**: Structuring charitable contributions and
  giving strategies that align with your goals.
- **Business Planning & Exit Strategy**: Succession planning and the
  financial decisions that come with selling or transitioning a
  business.
- **Tax Planning**: Coordinating on income strategy, estimated
  payments, Roth conversions, and filing implications.
- **Life Insurance**: Coverage analysis and protection strategies
  tailored to your transition.

*Note: this section deliberately names service areas, not outside
professionals, compliance rejected an earlier version naming specific
non-Ameritas-affiliated people.*

**Closing**: One checkpoint at a time. The best next step is a
conversation. The Where We Begin session is complimentary, carries no
obligation, and takes 45 minutes.

---

### Services (`services.html`)

**Hero**
# You are in the middle of something significant.
Most people know they need a plan. Few have one that actually keeps up
with their life. Checkpoint Planning brings structure, clarity, and a
fiduciary advocate to wherever you are.

- **Life Transitions**: Job loss, divorce, early retirement,
  inheritance. The moments when financial decisions are most
  consequential and most often made without a plan. This is where
  Checkpoint Planning was built to work.
- **Investment & Retirement Planning**: Building a portfolio aligned
  with your goals, timeline, and risk tolerance. Social Security
  timing, retirement income strategy, and ongoing investment
  management.
- **Financial Planning & Organization**: Cash flow, debt, insurance,
  estate documents, tax coordination. A comprehensive plan that
  connects every piece of your financial picture and keeps it current.

We also work with clients navigating inheritance and unexpected wealth,
loss of a spouse, and career reinvention or sabbaticals.

**Dedicated planning for your specific situation.**
(Same 6 transition cards as the homepage: Job Loss & Layoff, Early
Retirement, Divorce, Inheritance & Unexpected Wealth, Loss of a Spouse,
Career Reinvention, see Home section above for exact text.)

**Starting the journey toward your goals.**
We start by helping you prioritize what's most important to you today
and in the future. Together we review the following areas of your
financial life.

- **Life Transitions**: Recently moved or considering a relocation; job
  loss, layoff, or career change; getting married or divorced; recently
  retired or planning to retire; loss of a spouse or loved one;
  receiving a gift or inheritance; adding to family through birth or
  adoption.
- **Cash Flow and Debt**: Monthly budget feels unmanageable; building or
  rebuilding an emergency fund; debt payoff or reduction strategy;
  managing severance or lump-sum income; understanding my financial
  runway; planning for a major purchase or expense.
- **Tax Planning**: Income tax strategies; tax impact of severance or
  settlement; estimated quarterly tax payments; capital gain/loss
  strategies; Roth conversion analysis; coordinating with my CPA.
- **Insurance and Risk Management**: Health coverage after leaving
  employer; reviewing life and disability income insurance; long-term
  care planning; reviewing beneficiary designations; umbrella or
  liability coverage; Medicare planning.
- **Investments and Retirement**: 401(k) or IRA rollover decision;
  retirement readiness projection; Social Security timing strategy;
  pension election analysis; required minimum distributions; portfolio
  review and asset allocation; Roth conversion and tax planning.
- **Estate and Legacy**: Reviewing or creating a will or trust; updating
  beneficiary designations; powers of attorney and healthcare
  directives; wealth transfer and gifting strategy; charitable giving
  planning; divorce financial planning (QDRO, settlement); coordinating
  with an estate attorney.

**Closing**: One checkpoint at a time. Not sure where your situation
fits? The Where We Begin session is the easiest way to find out,
complimentary, no obligation, 45 minutes.

---

### Our Process (`process.html`)

**Hero**
# Your unique transition. Our systematic process.
A structured, five-phase planning process designed to bring clarity and
confidence to life's most important financial transitions. Every
engagement follows the same path.

(5-phase strip, same as Home, with slightly different descriptive text
here):
1. **Where We Begin™**: Understand what is changing, define
   priorities, and establish a clear starting point.
2. **Identify & Protect™**: Stabilize cash flow, review benefits and
   insurance, and protect what matters most.
3. **Plot Checkpoints™**: Set 30-, 90-, and 180-day milestones with a
   plan built around your situation.
4. **Implement™**: Execute the plan with focus, coordination, and
   support at every step.
5. **Track & Reset™**: Review progress, adjust as life evolves, and
   stay aligned with your goals.

The "Where We Begin" session is complimentary and carries no
obligation. It is a 45-minute clarity conversation to understand where
you are, what is changing, and whether working together makes sense.

**From your first call to your ongoing relationship.**
Here's what a typical client engagement looks like from first contact
through the first year. Every engagement is customized to your
situation, but the structure remains consistent.

1. **Where We Begin Session**: A complimentary 45-minute clarity
   conversation. We discuss your situation, your goals, and whether
   Checkpoint Planning is the right fit. No cost, no obligation.
2. **Engagement and Data Gathering**: You complete our financial intake
   and we gather the documents we need: account statements, tax
   returns, benefit summaries, estate documents, and anything else
   relevant.
3. **Plan Development**: We build your personalized financial plan in
   the Checkpoint Planning Client Portal, including cash flow analysis,
   retirement projections, scenario modeling, and a prioritized action
   list.
4. **Plan Presentation**: We walk through your plan together, explain
   every recommendation, and confirm your priorities. You leave with a
   clear 30-, 90-, and 180-day roadmap.
5. **Implementation**: We execute the plan. Account rollovers, portfolio
   construction, insurance applications, beneficiary updates, and
   referrals to attorneys or CPAs where needed.
6. **Track and Reset**: Regular check-ins and plan reviews keep you on
   track as life evolves. Frequency is based on your needs and your
   planning engagement.

**What you can always expect from Checkpoint Planning.**
(Same structural commitments as Home, with a couple of expanded lines):
- **Fiduciary Standard**: We are legally required to act in your best
  interest at all times, not the firm's interest, not a product
  manufacturer's, and not our own financial interest. Yours.
- **Full Fee Transparency**: Every fee is disclosed before work begins.
  Planning fees are flat. Investment management fees are AUM-based and
  billed monthly. No hidden costs. No surprises.
- **Commission Disclosure**: Some insurance and annuity products carry
  commissions. When that is the case, it is disclosed to you in writing
  before any recommendation is made.
- **No Long-Term Contracts**: Planning engagements are flat-fee
  agreements. Investment management relationships can be terminated at
  any time. We earn your business by delivering value, not by locking
  you in.
- **Direct Access to Your Planner**: You work directly with Scott in
  every meeting, every review, and every planning conversation. Your
  relationship is never handed off to a junior associate.
- **Coordinated Planning**: We work with your existing CPA, estate
  attorney, and other advisors so your financial decisions are never
  made in silos.

**Closing**: One checkpoint at a time. The best next step is a
conversation. The Where We Begin session is complimentary, carries no
obligation, and takes 45 minutes.

---

### Fees (`fees.html`)

**Hero**
# Transparent, flat-fee planning.
We are committed to providing proactive, transparent financial planning
to every client. Pick the package that best suits your needs and
current situation. All planning packages include access to the
Checkpoint Planning Client Portal.

**Clarity Session**
All services include: Investment Management Review, Retirement Account
Guidance, Employee Benefits Review, Cash Flow Management, Goals and
Priorities Review, Insurance and Beneficiary Review, Debt Reduction
Planning, One Follow-Up Session.

**Full Picture**
All previous services, plus: Full Financial Plan (Client Portal), "What
If" Scenario Projections, Tax Strategy Coordination, Held-Away Account
Advice, Multiple Goal Analysis, Education Savings Planning, Social
Security and Medicare Review, Quarterly Reviews (Year One).

**Legacy Blueprint**
All previous services, plus: Estate and Trust Planning Review, Wealth
Transfer Scenarios, Stock Option Analysis, Charitable Giving
Strategies, Advanced Tax Planning, Roth Conversion Review, CPA and
Attorney Coordination, Annual Plan Reviews (Ongoing).

All payments are processed via secure ACH. Ongoing planning and plan
maintenance fees are discussed individually based on the scope of your
engagement. We welcome any questions, at any time, regarding our
pricing philosophy.

**Straightforward, tiered pricing.**
Checkpoint Planning directs and supervises the investment management of
your assets, maintaining an appropriate portfolio allocation year after
year. The rate is determined by your total portfolio value. Whichever
tier your portfolio falls into, that single rate applies to the entire
account balance. No cost for the purchase and sale of securities within
the managed account.

*Industry average fees based on Cerulli, US Advisor Metrics 2023.

**The fee schedule includes:**
- Investment Management Account billing, Portfolio Performance
  Reporting, and Consolidated Online Account Access
- Record keeping of original cost basis
- Custom Analysis of Investment Risk Tolerance
- Asset Allocation and Portfolio Management Review

**A note on strategy**
We aim to address a variety of complex financial situations with plans
and solutions tailored to meet your specific needs. In order to do
this, we utilize a variety of investment strategies and methods. Please
note that additional corresponding platform or investment strategist
fees may be applied to the Advisor Fee and will vary depending on the
specific platform or strategist.

**Closing**: Questions about pricing? We welcome them, at any time. The
Where We Begin session is a great place to start, complimentary and no
obligation.

---

### Contact (`contact.html`)

**Hero**
# One checkpoint at a time.
The best next step is a conversation. The Where We Begin session is
complimentary, carries no obligation, and takes 45 minutes. It is
designed to give you clarity, not sell you something.

Checkpoint Planning, 3333 Michelson Drive, Irvine, CA 92612, (949)
702-0139, scott@checkpointplanning.com

**Where We Begin™ Session**
A complimentary, no-obligation 45-minute conversation. No forms, no
pressure, just clarity on your next step. Your information is
confidential and never sold. No obligation.

**In your Where We Begin session:**
- **You talk, we listen.** Tell us where you are, what just happened,
  and what feels most uncertain. No agenda, no forms.
- **We ask the right questions.** We help you see the financial
  decisions in front of you clearly, including ones you may not have
  considered.
- **We are honest about fit.** If Checkpoint Planning is the right
  choice for you, we explain how. If it is not, we tell you that too.

**Questions we hear most often.**
(Same FAQ as Home, plus two additional questions specific to Contact:)
- *What does investment management cost?* Fees are charged as a
  percentage of assets under management, billed monthly. Rates range
  from 0.65% to 1.25% depending on portfolio size, stepping down as
  assets grow. See the full fee schedule.
- *How long does the planning process take?* The initial engagement
  typically runs four to six weeks from intake to plan presentation.
  Implementation follows and can take an additional two to four weeks.
- *Do I have to use your investment management service?* No. Planning
  and investment management are separate services. Some clients engage
  us for planning only. We discuss what makes sense in the Where We
  Begin session.
- *Who is a good fit for Checkpoint Planning?* Someone navigating a
  major life transition who needs a structured process and a fiduciary
  advocate. If that describes you, you are likely a strong fit.
- *What happens after the plan is delivered?* Implementation, then
  ongoing support. We execute the plan together, then review it
  regularly through the Track and Reset phase.

**Closing**: Based in Irvine, serving clients nationwide.

---

### Job Loss & Layoff (`job-loss.html`)

**Hero**
# Just lost your job? Get a clear 90-day plan before you make any big decisions.
A layoff puts a dozen financial decisions in front of you at once,
including severance, COBRA, unemployment, and your 401(k), usually the
week you can least afford to rush them. Checkpoint Planning helps you
slow down, stabilize, and know what to do first.

Lead magnet: **Get Your Free Workbook**, "Your Next Checkpoint": a
90-day workbook to organize your income, expenses, runway, and
priorities after a layoff. Plus an invitation to a free Where We Begin
session.

**You don't need to figure this out alone, or all at once.**
These are the decisions that show up in the first 30 days. Most don't
need to be solved today.

- **Severance & Unemployment**: Understanding severance structure, tax
  withholding, and when to file for unemployment.
- **Health Coverage**: COBRA vs. marketplace vs. a spouse's plan,
  comparing real costs and deadlines before coverage lapses.
- **Your 401(k)**: Rollover, leave it, or something else, a decision
  that's easy to get wrong under time pressure.
- **Your Financial Runway**: How long your savings and severance
  actually cover essential expenses, so you know your real timeline.
- **Spending & Debt Priorities**: What to keep, reduce, or pause, and
  which debts genuinely need to stay current right now.
- **What Can Wait**: Not every decision needs to happen this month.
  Knowing what to defer reduces stress and prevents mistakes.

Lead magnet detail: **Your Next Checkpoint: Financial Clarity During
Career Transition**, a companion workbook for navigating job loss,
career change, or employment transitions. Organize your income,
expenses, runway, and a 30/60/90-day plan, at your own pace.

**A structured process for an unstructured moment.**
1. Where We Begin™: Free 45-minute clarity session. No cost, no
   obligation.
2. Identify & Protect™: Stabilize cash flow, benefits, and insurance
   gaps.
3. Plot Checkpoints™: 30-, 90-, and 180-day milestones built around
   your runway.
4. Implement™: Rollovers, benefits decisions, and next steps, all
   executed.
5. Track & Reset™: Ongoing support as your next chapter takes shape.

**Meet Scott Marcoe, CRPC™**
Scott helps people find clarity and direction during major life and
career transitions, including job loss and layoffs. As a fiduciary, he
is legally required to act in your best interest, not to sell you a
product. "One checkpoint at a time." Based in Orange County,
California, serving clients across the United States via video
conference and the Checkpoint Planning Client Portal.

**Questions people ask after a layoff.**
- *I just got laid off. What should I do first?* Start with the free
  workbook. It walks through severance, benefits deadlines, and your
  financial runway. Then schedule a free Where We Begin session to talk
  through your specific situation.
- *Does the free session cost anything?* No. The Where We Begin session
  is a complimentary, 45-minute clarity conversation with no
  obligation.
- *Do you help with severance and 401(k) decisions specifically?* Yes,
  this is core to what we do. We help you understand severance tax
  treatment, COBRA vs. marketplace options, and whether to roll over,
  leave, or otherwise handle your 401(k).
- *What if I haven't found a new job yet?* That's exactly who this is
  for. We help you build a plan around uncertainty, not around a
  guaranteed next paycheck.

**Closing**: One checkpoint at a time. Get the free workbook, then
schedule your complimentary Where We Begin session whenever you're
ready to talk it through.

---

### Early Retirement (`early-retirement.html`)

**Hero**
# Retiring earlier than planned? Make sure your money can retire too.
Whether it's your choice or the decision was made for you, early
retirement changes the math: Social Security timing, healthcare before
Medicare, pension elections, and how long your portfolio needs to last.
Checkpoint Planning helps you pressure-test the plan before you commit.

Lead magnet: **Get Your Free Guide**, the Early Retirement Checkpoint
Guide: key decisions on income, healthcare, and timing before you
retire. Plus an invitation to a free Where We Begin session.

**The decisions that don't wait until 65.**
Retiring before traditional retirement age means solving problems the
standard playbook doesn't cover.

- **Healthcare Before Medicare**: COBRA, marketplace coverage, or a
  spouse's plan, bridging the gap until Medicare eligibility at 65.
- **Social Security Timing**: When to claim, and how retiring early
  changes the tradeoffs between claiming early, at full retirement age,
  or later.
- **Pension Elections**: Lump sum vs. annuity, survivor benefit
  options: decisions that are usually permanent once made.
- **Portfolio Longevity**: A "what if" retirement readiness projection
  that accounts for a longer retirement than you originally planned
  for.
- **Required Minimum Distributions**: Sequencing withdrawals and Roth
  conversions in the years before RMDs begin.
- **401(k) & IRA Rollover Decisions**: Whether to consolidate, roll
  over, or leave accounts where they are, and the tax impact of each
  choice.

Lead magnet detail: **The Early Retirement Checkpoint Guide**, a short,
practical guide to the healthcare, Social Security, pension, and
portfolio decisions that come with retiring earlier than the standard
timeline.

**A structured process for a permanent decision.**
1. Where We Begin™: Free 45-minute clarity session. No cost, no
   obligation.
2. Identify & Protect™: Stabilize health coverage, benefits, and
   income sources.
3. Plot Checkpoints™: Retirement income projections and 30-, 90-,
   180-day milestones.
4. Implement™: Pension elections, Social Security filing, portfolio
   restructuring.
5. Track & Reset™: Annual reviews as markets and your life evolve.

**Meet Scott Marcoe, CRPC™**
Scott is a CRPC™, Chartered Retirement Planning Counselor, who
specializes in helping people navigate the financial decisions of early
retirement. As a fiduciary, he's legally required to act in your best
interest. "One checkpoint at a time." Based in Orange County,
California, serving clients across the United States via video
conference and the Checkpoint Planning Client Portal.

**Questions people ask about early retirement.**
- *Is it too early to plan if I haven't set a retirement date yet?* No,
  the earlier we run the numbers, the more options you have. The free
  guide and a Where We Begin session can help you pressure-test a
  timeline before you commit to it.
- *Can you help with Social Security timing specifically?* Yes. Social
  Security timing strategy is part of every retirement engagement,
  alongside pension elections and RMD planning.
- *What if my retirement wasn't entirely voluntary?* Many clients
  arrive here after a layoff or buyout accelerated a retirement they
  hadn't fully planned for. We build the plan around your real
  timeline, not the one you expected.
- *Do you help figure out health coverage before Medicare?* Yes,
  comparing COBRA, marketplace plans, and other options is part of the
  Identify & Protect phase.

**Closing**: One checkpoint at a time. Get the free guide, then
schedule your complimentary Where We Begin session whenever you're
ready to talk it through.

---

### Divorce (`divorce.html`)

**Hero**
# Divorce changes everything financially. Build a plan that's entirely your own.
Settlement analysis, QDROs, tax filing status, splitting retirement
accounts, and rebuilding a budget on your own: divorce brings a wave of
financial decisions on top of an already difficult time. Checkpoint
Planning helps you see the full picture clearly, and independently of
the emotion of the moment.

Lead magnet: **Get Your Free Guide**, the Divorce Financial Checkpoint
Guide: what to understand before you sign a settlement. Plus an
invitation to a free, confidential Where We Begin session. Every
conversation is confidential. Your information is never sold. No
obligation.

**The financial decisions behind the legal ones.**
Your attorney handles the legal process. Checkpoint Planning helps you
understand what the numbers actually mean for your life afterward.

- **Settlement Analysis**: Understanding the real, after-tax value of a
  proposed settlement, not just the headline number.
- **QDROs & Retirement Accounts**: How 401(k)s, pensions, and IRAs are
  divided, and the tax rules that apply to each.
- **Tax Impact**: Filing status changes, support payment tax treatment,
  and capital gains on any assets that are sold or transferred.
- **A New Household Budget**: Rebuilding a realistic cash flow plan for
  a single household, often on a single income.
- **Insurance & Beneficiaries**: Updating life insurance, health
  coverage, and beneficiary designations that often get missed after a
  divorce is final.
- **Coordinating With Your Attorney**: Working alongside your divorce
  attorney so financial and legal decisions are aligned, not made in
  isolation.

Lead magnet detail: **The Divorce Financial Checkpoint Guide**, a
clear-eyed guide to the financial questions worth asking before you
finalize a settlement, and the ones to revisit in the year after.

**A steady process for an unsteady time.**
1. Where We Begin™: Free, confidential 45-minute clarity session.
2. Identify & Protect™: Stabilize cash flow, insurance, and
   beneficiary designations.
3. Plot Checkpoints™: A plan built around your settlement and new
   household budget.
4. Implement™: QDRO execution, account splits, and document updates.
5. Track & Reset™: Ongoing reviews as your new chapter takes shape.

**Meet Scott Marcoe, CRPC™**
Scott helps people rebuild a clear, independent financial plan during
and after divorce. As a fiduciary, he works only for you, never for an
attorney, a bank, or a product manufacturer. "One checkpoint at a
time." Based in Orange County, California, serving clients across the
United States via video conference and the Checkpoint Planning Client
Portal.

**Questions people ask during divorce.**
- *Is this a replacement for my divorce attorney?* No. We work
  alongside your attorney, focused on the financial implications of
  your settlement, not the legal process itself.
- *Can you review a settlement before I sign it?* Yes. Understanding
  the real financial impact of a proposed settlement is one of the most
  common reasons clients reach out before finalizing.
- *Is our conversation confidential?* Yes. Everything discussed in a
  Where We Begin session and any engagement afterward is confidential.
- *What if I've never managed the finances before?* That's a common
  starting point. We build the plan from the ground up, in plain
  language, at a pace that works for you.

**Closing**: One checkpoint at a time. Get the free guide, then
schedule your complimentary, confidential Where We Begin session
whenever you're ready.

---

### Inheritance & Unexpected Wealth (`inheritance.html`)

**Hero**
# Received an inheritance? Slow down before you decide anything.
An inheritance brings relief, grief, opportunity, and pressure all at
once, plus real decisions about taxes, investing, and what the money
represents. There is rarely a need to decide anything quickly.
Checkpoint Planning helps you take the time to get it right.

Lead magnet: **Get Your Free Guide**, the Inheritance Checkpoint Guide:
first steps, tax basics, and questions to ask before you invest or
spend. Plus an invitation to a free Where We Begin session.

**Decisions worth making carefully, not quickly.**
Most inheritance mistakes come from moving too fast. Here's what's
actually worth thinking through.

- **Inherited IRA Rules**: Required distribution timelines and tax
  treatment differ significantly depending on your relationship to the
  deceased.
- **Tax Basics**: Understanding step-up in cost basis, potential
  capital gains, and estate versus income tax exposure.
- **Real Estate & Property**: Keep, rent, or sell, weighing the
  financial and emotional considerations of an inherited home.
- **Investing the Proceeds**: Building a portfolio and asset allocation
  that fits your goals and risk tolerance, not just what was inherited.
- **Debt & Goals**: Deciding whether to pay down debt, fund goals, or
  invest, often all three, in the right proportion.
- **What It Represents**: Space to think through what this money means
  to you, and how you want to honor it, before deciding what to do with
  it.

Lead magnet detail: **The Inheritance Checkpoint Guide**, a calm,
practical first look at inherited IRA rules, tax basics, and the
questions worth asking before you invest, spend, or sell.

**No need to decide everything at once.**
1. Where We Begin™: Free 45-minute clarity session. No cost, no
   obligation.
2. Identify & Protect™: Understand tax deadlines and protect the
   assets while you decide.
3. Plot Checkpoints™: A plan for investing, spending, and goals, all
   on your timeline.
4. Implement™: Account transfers, investment allocation, and
   document updates.
5. Track & Reset™: Ongoing reviews as the plan and your goals
   evolve.

**Meet Scott Marcoe, CRPC™**
Scott helps people navigate inheritance and unexpected wealth
thoughtfully, with no pressure to decide quickly. As a fiduciary, he's
legally required to act in your best interest, not to rush you into an
investment. "One checkpoint at a time." Based in Orange County,
California, serving clients across the United States via video
conference and the Checkpoint Planning Client Portal.

**Questions people ask after an inheritance.**
- *Do I need to decide what to do with the money right away?* Almost
  never. Aside from a few tax deadlines worth knowing about, most
  decisions can, and should, wait until you've had time to think
  clearly.
- *I inherited a retirement account. What are the rules?* Inherited IRA
  distribution rules vary based on your relationship to the original
  owner and when they passed. This is one of the most common questions
  we help clients work through.
- *Can you help me decide what to do with an inherited house?* Yes, we
  help weigh the financial tradeoffs of keeping, renting, or selling
  inherited property alongside your broader plan.
- *I feel guilty about the money. Is that normal?* Very common. The
  Where We Begin session gives you space to think through what the
  inheritance represents, not just what to do with it financially.

**Closing**: One checkpoint at a time. Get the free guide, then
schedule your complimentary Where We Begin session whenever you're
ready to talk it through.

---

## 4. Updates

Running log. Add a dated entry under Completed when something ships,
keep Planned / Open trimmed to what's actually still outstanding.

### Completed

- **2026-09-21**: Initial lead-generation system built, homepage,
  4 transition landing pages, lead magnets, email sequences (draft),
  prospecting plan, Google Sheet backend.
- **2026-09-21**: Self-deploy guide added for `start.checkpointplanning.com`.
- **2026-09-21**: Expanded to full base site, About, Services, Process,
  Fees, Contact, matching real branding (logo, icon mark, CRPC badge).
- **2026-09-21**: Palette recolored to remove all green, Form CRS links
  added to nav and footer across all 10 pages, first compliance review
  PDF built.
- **2026-09-21**: Extended Team section on About reworked, named
  non-Ameritas professionals removed per compliance feedback, replaced
  with unnamed coordinated service areas.
- **2026-09-21 to 2026-09-22**: LinkedIn/Facebook campaign built
  (targeting, ad copy, budget plan, launch checklist), UTM tracking
  extended to ad-level (`utm_medium`, `utm_content`), LinkedIn Insight
  Tag and custom conversion event added site-wide.

### Planned / open

- **Root domain migration**: site currently lives at
  `start.checkpointplanning.com`. Decision to swap DNS so it becomes
  the primary `checkpointplanning.com` is intentionally deferred, see
  `docs/DEPLOY.md`.
- **LinkedIn Page link in footer**: offered but not yet added, would
  go alongside the existing contact links in the footer's firm-info
  column, across all 10 pages.
- **Email nurture sequences**: drafted but on hold, follow-up is
  handled manually for now by design, automation is a later phase.
- **Compliance sign-off**: site content submitted for Ameritas
  compliance review, confirm final approval status before any paid
  traffic points at it (see `docs/DEPLOY.md` Step 4/5 checklist).
- **New creative direction**: LinkedIn campaign visual design (ads,
  carousel posts) has moved to a separate design project, see
  `campaign/10-creative-brief-handoff.md`. If that project produces a
  refreshed visual system, evaluate whether it should extend back to
  the website (currently no photography beyond one headshot, and the
  site's HTML/CSS design predates that creative brief).
