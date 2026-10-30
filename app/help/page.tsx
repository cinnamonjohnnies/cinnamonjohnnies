import Header from "@/components/Header";
import Disclaimer from "@/components/Disclaimer";
import Link from "next/link";
import { PLAN, FEEDBACK_URL } from "@/lib/env";

export const metadata = { title: "User Guide", description: "The complete guide to Talk Gooder: writing, importing, timing, AI help, dictation, rehearsing, printing, backups, plans and billing." };

const toc: [string, string][] = [
  ["start", "Quick start"],
  ["library", "Your speeches"],
  ["templates", "Starting outlines"],
  ["import", "Bringing in a speech"],
  ["sections", "Sections and tabs"],
  ["lines", "Working with lines"],
  ["move", "Selecting and moving lines"],
  ["dictate", "Speaking instead of typing"],
  ["timing", "Timing and pace"],
  ["ai", "AI help (paid)"],
  ["punch", "Punch up"],
  ["rehearse", "Rehearsing and printing"],
  ["backup", "Backing up and restoring"],
  ["plans", "Plans and billing"],
  ["faq", "Questions"],
];

export default function Help() {
  return (
    <>
      <Header />
      <main className="wrap help-page">
        <section className="help-hero">
          <span className="eyebrow">User guide</span>
          <h1>Everything you need to <em>speak gooder</em></h1>
          <p className="lede">Write, time, polish and rehearse a speech. Skim the quick start, then jump to whatever you need.</p>
        </section>

        <div className="quick">
          <div><span className="num">1</span><h3>Start a speech</h3><p>Choose <strong>Start New</strong>, <strong>Upload Speech</strong>, or try the <strong>sample speech</strong> to look around first.</p></div>
          <div><span className="num">2</span><h3>Shape and time it</h3><p>Move lines and sections around and watch the clock against your target time.</p></div>
          <div><span className="num">3</span><h3>Polish and rehearse</h3><p>Flag weak spots, get ideas, then practice in Stage view.</p></div>
        </div>

        <div className="help-layout">
          <aside className="toc" aria-label="On this page">
            <strong>On this page</strong>
            {toc.map(([id, label]) => <a key={id} href={`#${id}`}>{label}</a>)}
          </aside>

          <div className="help-body">
            <section id="start" className="topic">
              <h2>Quick start</h2>
              <ol>
                <li>Create a free account and open <Link href="/app">My Speeches</Link>.</li>
                <li>New here? Press <strong>Try a sample speech</strong>. It is a short speech with a few lines already flagged, so you can click around without risk. It does not count toward your free speeches, and you can delete it any time.</li>
                <li>When you are ready, choose <strong>Start New</strong> to write from scratch, or <strong>Upload Speech</strong> to bring in a script you already have.</li>
                <li>Type or paste your lines. Each line is one thing you say. Everything saves automatically.</li>
                <li>Set your target time. The big clock at the top shows how long your speech runs and whether you are short, in range or over.</li>
              </ol>
              <div className="tip"><strong>Tip:</strong> the same menu is at the top of every page. <em>My Speeches</em> lists your recent speeches, <em>Start New</em>, <em>Upload Speech</em>, <em>Load Sample Speech</em> and <em>Back Up and Restore</em>.</div>
            </section>

            <section id="library" className="topic">
              <h2>Your speeches</h2>
              <p>The My Speeches page shows a card for each speech with its length and whether it is short, in range or over its target. Click a card title to open it. <em>Duplicate</em> makes a copy, which is a good way to try a shorter version. <em>Delete</em> asks you to tap twice so you do not remove one by accident.</p>
              <p>The free plan holds {PLAN.freeSpeechLimit} speeches. The sample speech does not count.</p>
            </section>

            <section id="templates" className="topic">
              <h2>Starting outlines</h2>
              <p>When you choose <strong>Start New</strong>, pick an outline that fits what you are writing:</p>
              <ul>
                <li><strong>Open, body, close</strong>: the classic structure.</li>
                <li><strong>Story</strong>: hook, story, turn, lesson and close.</li>
                <li><strong>Humor piece</strong>: an opening, three bits and a close that calls back to the start.</li>
                <li><strong>Jokemaster</strong>: a setup, a run of jokes and a close.</li>
                <li><strong>Elevator pitch</strong>: 30 to 60 seconds. Answer a few short questions and, on a paid plan, the AI blends them into one tight pitch plus a shorter version. On the free plan your answers fill the outline and you write it yourself.</li>
                <li><strong>Presentation notes</strong>: an opener, a tab for each of nine slides, and a closer, for speaker notes.</li>
              </ul>
              <p>The short grey prompts under each section title guide you. They are not counted in your time.</p>
            </section>

            <section id="import" className="topic">
              <h2>Bringing in a speech you already have</h2>
              <p>Choose <strong>Upload Speech</strong>. You can upload a <strong>.txt, .md, .docx or .pdf</strong> file, or paste the text. Everything is read in your browser, so the file itself is never sent anywhere.</p>
              <h3>Two ways to import</h3>
              <ul>
                <li><strong>Mark sections</strong> shows your text. Highlight a passage and tell Talk Gooder whether it is the opening, a body part or the close. It suggests a first pass, and you can reassign any passage or skip parts you do not want. Best for control.</li>
                <li><strong>Quick import</strong> guesses the sections from the blank lines in your text. Best for speed.</li>
              </ul>
              <h3>What it does for you</h3>
              <ul>
                <li><strong>Numbered speeches.</strong> If your speech has numbered points (1, 2, 3 and so on), each number becomes its own section, with everything before the first number as the Opening and everything after the last point as the Close.</li>
                <li><strong>Tidy the lines.</strong> Text copied from PDFs and emails often breaks mid-sentence at the edge of the page. With <em>Tidy the lines</em> checked, those pieces are joined back together and every sentence goes on its own line, which makes lines easy to move and edit. Uncheck it to keep your lines exactly as written.</li>
                <li><strong>Pauses and stage directions.</strong> A line in square brackets, like [Pause, 3s] or [Walk to the left of the stage, 4s], becomes a timed direction.</li>
              </ul>
              <div className="tip"><strong>PDF notes:</strong> a PDF needs real text in it. A scan or a photo of a page has none, and you will see a message saying so. Paste the text or save the file as a Word document instead. PDFs with columns or tables can come in out of order, so check them.</div>
              <p>Placed something in the wrong section? See <a href="#move">Selecting and moving lines</a>.</p>
            </section>

            <section id="sections" className="topic">
              <h2>Sections and tabs</h2>
              <ul>
                <li>Each section has its own tab. Click a tab to work on just that part.</li>
                <li><strong>Show all together</strong> displays the whole speech in order.</li>
                <li>Drag a tab to reorder sections. <em>Move earlier</em> and <em>Move later</em> do the same and work on phones.</li>
                <li><strong>Add section</strong> makes a new part, <strong>Merge next</strong> combines two, <strong>Remove section</strong> deletes one, and <strong>Color</strong> changes a section&apos;s color.</li>
                <li><strong>Skip in timer</strong> keeps a section in your speech but leaves it out of the time. It is handy for notes, alternate endings or a shorter version. Use <em>Count in timer</em> to turn it back on.</li>
                <li>Each section shows where it starts, its word count and its length.</li>
                <li><em>Introduction for the Toastmaster</em> is a box for the introduction someone reads before you begin. It is not timed and it prints at the top of your PDF.</li>
              </ul>
            </section>

            <section id="lines" className="topic">
              <h2>Working with lines</h2>
              <ul>
                <li>Click a line to edit it. Press <strong>Enter</strong> for a new line, <strong>Shift+Enter</strong> for a line break inside a line, and <strong>Backspace</strong> on an empty line to remove it.</li>
                <li>Drag the grip (⋮⋮) at the left of a line to move it within its section, or use <em>Up</em> and <em>Down</em> to move it one step.</li>
                <li><strong>Cut</strong> strikes a line out without deleting it, so you can see your time without it. Cut lines are skipped when you copy, print or rehearse.</li>
                <li><strong>Cue</strong> turns a line into a stage direction, such as a pause, a gesture or a walk across the stage. A stage direction is not spoken and does not print in your script, but the seconds you give it count toward your time. <em>Add pause</em> and <em>Add stage direction</em> at the bottom of a section make them for you.</li>
                <li><strong>Split here</strong> starts a new section at that line.</li>
                <li><strong>Undo</strong> and <strong>Redo</strong> are at the top, and Ctrl or Cmd + Z works too. They cover almost everything, including moves and AI changes.</li>
              </ul>
            </section>

            <section id="move" className="topic">
              <h2>Selecting and moving lines</h2>
              <p>Use this when something landed in the wrong section, for example part of your close ended up at the end of the last body section.</p>
              <ol>
                <li>Press <strong>Select lines</strong> above your speech.</li>
                <li>Click any line to pick it. Click anywhere on the line, not just the box. <strong>Shift-click</strong> a second line to pick everything between the two.</li>
                <li>Shortcuts: <em>Select down to the end of the section</em> picks the line you just clicked and everything below it. <em>Select a whole section</em> picks all of a section.</li>
                <li>Choose <strong>Move to</strong> a section and press <strong>Move</strong>. Moving text down into a later section puts it at the start of that section, which is usually what you want. Change <em>at the start</em> or <em>at the end</em> if it is not.</li>
                <li>Press <strong>Done, back to editing</strong> when you finish. Undo reverses a move.</li>
              </ol>
              <p>The same selection is used for flagging lines for punch up and for <a href="#ai">Condense</a>.</p>
            </section>

            <section id="dictate" className="topic">
              <h2>Speaking instead of typing</h2>
              <p>Press <strong>Dictate</strong> at the bottom of any section, then say your speech out loud. Your words appear as you speak, and every natural pause becomes a new line. Press <strong>Done</strong> when you finish.</p>
              <ul>
                <li>It works in Chrome, Edge and Safari. Your browser will ask for permission to use the microphone the first time. If you said no by accident, click the lock icon next to the web address to allow it.</li>
                <li>Each line gets a period at the end, and the first letter is capitalized. Fix commas and question marks afterwards.</li>
                <li>Your browser does the listening. Depending on the browser, the audio is processed by Google or Apple. Talk Gooder does not record or keep your audio.</li>
                <li>It is free on every plan.</li>
              </ul>
            </section>

            <section id="timing" className="topic">
              <h2>Timing and pace</h2>
              <p>The clock at the top estimates your running time from your word count, your speaking pace, the pause after each line, and any stage directions. The bar shows your target range, and the label says whether you are short, in range or over.</p>
              <p>Open <em>Timing, room and editing tips</em> to change:</p>
              <ul>
                <li><strong>Pace</strong>, in words per minute. Most people speak between 120 and 160. This number drives the whole clock, so it is worth getting right (see below).</li>
                <li><strong>Laugh pad</strong>, the seconds added after each line for laughs, breaths and pauses.</li>
                <li><strong>Target</strong>, the shortest and longest length you are aiming for, in minutes. A club speech might be 5 to 7.</li>
              </ul>
              <h3>Find your real pace</h3>
              <p>Most people do not know how fast they actually talk. Press <strong>Find my pace</strong> next to the Pace box, read the sample passage (or your own speech) out loud, and press <em>Done</em>. You get a words-per-minute number. Read it two or three times for a steadier result, then press the button that says <strong>Use (your number) as my pace</strong>. Your pace is remembered for new speeches too.</p>
              <div className="tip"><strong>Good to know:</strong> reading from a page is usually a little faster than speaking from memory. If you will tell the speech naturally, go 5 to 10 words per minute lower than your result.</div>
            </section>

            <section id="ai" className="topic">
              <h2>AI help (paid plan)</h2>
              <p>On a paid plan, Talk Gooder uses AI to help you improve your own words. It never writes a speech for you without your material, and it is told not to invent facts. When a real number, name or detail is needed, it leaves a [bracketed placeholder] for you to fill in. Always read what it gives you and keep what sounds like you.</p>
              <h3>Rewrite suggestions</h3>
              <p>Flag a line (see <a href="#punch">Punch up</a>), choose what it needs, and press <strong>Suggest rewrites</strong>. You get three different options. <em>Replace line</em> swaps one in. <em>Add after</em> keeps your line and adds the new one below it. A spinning circle shows while it works, usually about ten seconds.</p>
              <h3>Condense</h3>
              <p>For a long speech that must fit a shorter slot: press <strong>Select lines</strong>, pick the lines to shorten (they can be anywhere), choose <em>Half the length</em>, <em>A bit tighter</em> or <em>One short line</em>, and press <strong>Condense with AI</strong>. You get three versions with the word count and the seconds each saves. <em>Use this</em> replaces your selected lines with that one line, and Undo reverses it.</p>
              <h3>Room and tone</h3>
              <p>Open <em>Timing, room and editing tips</em> and choose a <strong>Room</strong>, such as club speech, conference, keynote, toast, ceremony, tribute, roast or stand-up. Add a <strong>Tone note</strong> in your own words, like &quot;warm, a little self-deprecating&quot;. The rewrite suggestions and Condense then fit the room, so the same line comes out differently for a eulogy than for a roast.</p>
              <h3>Elevator pitch builder</h3>
              <p>Start New, choose <em>Elevator pitch</em>, answer the short questions, and press <strong>Write my pitch</strong>. The AI blends your answers into one pitch that fits your time, plus a shorter version, and keeps your answers on a tab for reference.</p>
              <div className="tip"><strong>Limits:</strong> AI features share a daily allowance per account. If you reach it, it resets the next day. Free accounts see an upgrade prompt when they try an AI feature.</div>
            </section>

            <section id="punch" className="topic">
              <h2>Punch up</h2>
              <p>Flag any line, or a whole section, that needs more. Choose what it needs (humor, a stat or fact, context, a story or example, tightening, or any improvement) and add a note to yourself. This part is free on every plan.</p>
              <ul>
                <li><strong>Need an idea?</strong> on a flagged line gives a prompt, such as the rule of three or a callback. Tap again for another.</li>
                <li>The <em>Punch-up list</em> shows every flag in one place so you can work through them one by one.</li>
                <li>On a paid plan, <strong>Suggest rewrites</strong> writes options for you, and you can copy all your flags as a punch-up brief to share with a coach or evaluator.</li>
                <li>To flag many lines at once, use <strong>Select lines</strong>, pick them, choose a type and press <em>Flag for punch up</em>.</li>
              </ul>
            </section>

            <section id="rehearse" className="topic">
              <h2>Rehearsing and printing</h2>
              <ul>
                <li><strong>Stopwatch.</strong> Press <em>Start</em> at the top right and speak. The section you are in follows along, so you can see where you run long. <em>Reset</em> clears it.</li>
                <li><strong>Stage view</strong> hides the controls and shows large, easy-to-read text for practicing. Cut lines are hidden.</li>
                <li><strong>Copy script</strong> puts the text of your speech on your clipboard.</li>
                <li><strong>Export PDF</strong> makes a clean printable script (paid plan), with your Toastmaster introduction at the top.</li>
              </ul>
            </section>

            <section id="backup" className="topic">
              <h2>Backing up and restoring</h2>
              <p>Your speeches are saved to your account automatically. A backup is an extra copy you keep yourself, which is good practice before big changes.</p>
              <h3>Back up</h3>
              <ol>
                <li>Open <strong>My Speeches</strong> at the top of the page and choose <strong>Back Up and Restore</strong>, or scroll to the bottom of your speech list.</li>
                <li>Click <strong>Back up all speeches</strong>. A file ending in <em>.json</em> (named talk-gooder-backup and the date) downloads to your device.</li>
                <li>Keep the file somewhere safe, such as a cloud drive or an email to yourself.</li>
              </ol>
              <h3>Restore</h3>
              <ol>
                <li>Go to the same spot and click <strong>Restore a backup</strong>.</li>
                <li>Choose your backup file. The speeches inside it are added back to your list.</li>
              </ol>
              <div className="tip"><strong>Good to know:</strong> restoring never overwrites a speech. If a speech is identical to one you already have, it is skipped. If it has the same name but different content, it comes back as a copy marked &quot;(restored)&quot;. On the free plan, the {PLAN.freeSpeechLimit} speech limit still applies.</div>
            </section>

            <section id="plans" className="topic">
              <h2>Plans and billing</h2>
              <p><strong>Free</strong> includes {PLAN.freeSpeechLimit} speeches, the editor, timing, the pace finder, dictation, punch-up flags and ideas, Stage view and backups.</p>
              <p><strong>Paid</strong> adds unlimited speeches, PDF export, the punch-up brief, and the AI features: rewrite suggestions, Condense, room and tone, and the pitch builder. It starts with a {PLAN.trialDays} day free trial. Manage or cancel any time on your <Link href="/account">Account</Link> page. See <Link href="/pricing">Pricing</Link>.</p>
            </section>

            <section id="faq" className="topic">
              <h2>Questions</h2>
              <details><summary>I forgot my password.</summary><p>Choose <em>Forgot your password?</em> on the sign-in page and follow the link in the email. You can change it any time from the Account page. Use the <em>Show</em> button in any password box to check what you typed.</p></details>
              <details><summary>The confirmation email did not arrive.</summary><p>Check your spam or promotions folder, then look for a message from hello@talkgooder.app. Open the link in the same browser where you signed up. If it still does not arrive, email us.</p></details>
              <details><summary>Can other people see my speeches?</summary><p>No. Your speeches are private to your account. We do not read them or use them to train AI.</p></details>
              <details><summary>Why did I hit a limit on the free plan?</summary><p>The free plan holds {PLAN.freeSpeechLimit} speeches. Delete one you no longer need, or upgrade for unlimited speeches.</p></details>
              <details><summary>My upload came in with sentences cut in half.</summary><p>Make sure <em>Tidy the lines</em> is checked on the upload screen. It joins text that wrapped at the edge of the page and puts each sentence on its own line.</p></details>
              <details><summary>The time looks wrong.</summary><p>The clock depends on your pace. Use <em>Find my pace</em> to measure your real words per minute, and check your laugh pad. Stage directions and pauses also add seconds.</p></details>
              <details><summary>Dictate does not show up or does not hear me.</summary><p>Use Chrome, Edge or Safari, and allow the microphone when asked. The button does not appear in Firefox.</p></details>
              <details><summary>I deleted something by mistake.</summary><p>Press <em>Undo</em> at the top, or Ctrl or Cmd + Z. If you deleted a whole speech, restore it from a backup.</p></details>
              <details><summary>How do I cancel?</summary><p>Open <Link href="/account">Account</Link> and choose manage billing. You keep access until the end of the period you paid for.</p></details>
              <div className="contact">Still stuck? Email <a href="mailto:hello@talkgooder.app">hello@talkgooder.app</a> and we will help. Ideas and complaints are welcome too: <a href={FEEDBACK_URL} target="_blank" rel="noopener noreferrer">send feedback</a>.</div>
            </section>
          </div>
        </div>
      </main>
      <Disclaimer />
    </>
  );
}
