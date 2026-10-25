function App() {
  return (
    <main className="page">
      <header className="header">
        <p className="eyebrow">RETRIEVAL-AUGMENTED Q&amp;A</p>
        <h1>Ask your documents</h1>
        <p className="intro">
          Add a UTF-8 text document, then ask a question grounded in its content.
        </p>
      </header>

      <section className="card" aria-labelledby="upload-heading">
        <div className="section-heading">
          <span className="step">01</span>
          <div>
            <h2 id="upload-heading">Add a document</h2>
            <p>Upload a plain-text file to the knowledge base.</p>
          </div>
        </div>
        <div className="form-row">
          <label className="file-picker">
            <span>Choose a .txt or .md file</span>
            <input
              type="file"
              accept=".txt,.md,text/plain,text/markdown"
            />
          </label>
          <button type="button">Upload</button>
        </div>
      </section>

      <section className="card" aria-labelledby="question-heading">
        <div className="section-heading">
          <span className="step">02</span>
          <div>
            <h2 id="question-heading">Ask a question</h2>
            <p>Answers include the passages used to form them.</p>
          </div>
        </div>
        <div className="form-row">
          <label className="visually-hidden" htmlFor="question">
            Your question
          </label>
          <input
            id="question"
            className="question-input"
            placeholder="What would you like to know?"
          />
          <button type="button">Ask</button>
        </div>
      </section>

      <section className="card result" aria-labelledby="answer-heading">
        <h2 id="answer-heading">Answer</h2>
        <p className="answer-text">
          Your answer and its supporting passages will appear here.
        </p>
      </section>
      <footer>RaaS · Document Q&amp;A</footer>
    </main>
  );
}

export default App;
