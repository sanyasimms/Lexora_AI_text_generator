export default function HomePage() {
  return (
    <main className="landing-shell">
      <section className="hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">Lexora</p>
          <h1>Design subtitles that feel cinematic, not generic.</h1>
          <p className="hero-copy__text">
            Lexora is a clean caption workflow for uploading video, generating subtitles, styling them live, and
            exporting a finished burn-in video. It is built for fast iteration and a polished presentation.
          </p>

          <div className="hero-actions">
            <a className="button" href="/features">
              View features
            </a>
            <a className="button button--secondary" href="#preview-card">
              See the 3D preview
            </a>
          </div>

          <div className="status-row">
            <span className="status-chip">Video upload</span>
            <span className="status-chip">Live subtitle styling</span>
            <span className="status-chip status-chip--accent">Export ready</span>
          </div>
        </div>

        <div className="hero-visual card-3d" id="preview-card" aria-hidden="true">
          <div className="card-3d__glow card-3d__glow--one" />
          <div className="card-3d__glow card-3d__glow--two" />
          <div className="hero-visual__frame">
            <div className="hero-visual__topbar">
              <span />
              <span />
              <span />
            </div>
            <div className="hero-visual__screen">
              <div className="hero-visual__title">Lexora preview</div>
              <div className="hero-visual__subtitle">3D caption surfaces, motion depth, and clean export flow.</div>
              <div className="hero-visual__panel hero-visual__panel--front">Upload</div>
              <div className="hero-visual__panel hero-visual__panel--left">Style</div>
              <div className="hero-visual__panel hero-visual__panel--right">Export</div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}