export default function NotFound() {
  return (
    <main className="landing-shell landing-shell--features">
      <section className="features-hero card-3d">
        <div className="features-hero__copy">
          <p className="eyebrow">Lexora</p>
          <h1>Page not found.</h1>
          <p>The route you requested does not exist. Return to the landing page and continue from there.</p>
        </div>

        <a className="button button--secondary features-hero__back" href="/">
          Back home
        </a>
      </section>
    </main>
  );
}
